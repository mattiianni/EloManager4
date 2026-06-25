import re

with open('server.js', 'r') as f:
    content = f.read()

# 1. Fix deleteTeamTournamentPlayoffState
old_playoff_state_func = """const deleteTeamTournamentPlayoffState = async (rootId, wsId) => {
    const playoffMatchdays = await sql`
        SELECT d.id, d.tournament_day_id
        FROM team_tournament_matchdays d
        JOIN tournaments root ON root.id = d.root_tournament_id
        WHERE d.root_tournament_id = ${rootId}
          AND root.workspace_id = ${wsId}
          AND d.phase <> 'round_robin'
    `;

    const playoffMatchdayIds = playoffMatchdays.map(r => r.id).filter(Boolean);
    const tournamentDayIds = playoffMatchdays.map(r => r.tournament_day_id).filter(Boolean);

    if (playoffMatchdayIds.length > 0) {
        await sql`
            DELETE FROM team_tournament_matchdays
            WHERE id = ANY(${playoffMatchdayIds}::uuid[])
        `;
    }

    if (tournamentDayIds.length > 0) {
        await sql`
            DELETE FROM tournaments
            WHERE id = ANY(${tournamentDayIds}::uuid[])
              AND workspace_id = ${wsId}
        `;
    }

    await sql`
        DELETE FROM team_tournament_fixtures
        WHERE root_tournament_id = ${rootId}
    `;
};"""

new_playoff_state_func = """const deleteTeamTournamentPlayoffState = async (rootId, wsId) => {
    const playoffMatchdays = await sql`
        SELECT d.id, d.tournament_day_id
        FROM team_tournament_matchdays d
        JOIN tournaments root ON root.id = d.root_tournament_id
        WHERE d.root_tournament_id = ${rootId}
          AND root.workspace_id = ${wsId}
          AND d.phase <> 'round_robin'
    `;

    const playoffMatchdayIds = playoffMatchdays.map(r => r.id).filter(Boolean);
    const tournamentDayIds = playoffMatchdays.map(r => r.tournament_day_id).filter(Boolean);

    if (playoffMatchdayIds.length > 0) {
        await sql`
            DELETE FROM team_tournament_matchdays
            WHERE id = ANY(${playoffMatchdayIds}::uuid[])
        `;
    }

    if (tournamentDayIds.length > 0) {
        // Find all matches for these playoff matchdays to delete them and revert ELO
        const matchesResult = await sql`
            SELECT id FROM matches 
            WHERE tournament_id = ANY(${tournamentDayIds}::uuid[]) 
              AND workspace_id = ${wsId}
        `;
        const matchIds = matchesResult.map(m => m.id);
        
        if (matchIds.length > 0) {
            await sql`DELETE FROM matches WHERE id = ANY(${matchIds}::uuid[])`;
        }
        
        await sql`
            DELETE FROM tournaments
            WHERE id = ANY(${tournamentDayIds}::uuid[])
              AND workspace_id = ${wsId}
        `;
    }

    // UPDATE fixtures to reset them, rather than deleting them
    await sql`
        UPDATE team_tournament_fixtures
        SET team1_number = NULL,
            team2_number = NULL,
            winner_team_number = NULL,
            loser_team_number = NULL,
            status = 'planned',
            tournament_day_id = NULL,
            matchday_id = NULL
        WHERE root_tournament_id = ${rootId}
    `;
    
    // Also revert ELO for the ROOT tournament since it's no longer completed
    const rootTournamentStatus = await sql`
        SELECT status FROM tournaments WHERE id = ${rootId} AND workspace_id = ${wsId}
    `;
    
    if (rootTournamentStatus.length > 0 && rootTournamentStatus[0].status === 'completed') {
        const eloHistoryResult = await sql`
            SELECT player_id, delta FROM elo_history
            WHERE event_id = ${rootId} AND type = 'tournament' AND workspace_id = ${wsId}
        `;

        for (const record of eloHistoryResult) {
            await sql`
                UPDATE players SET current_elo = current_elo - ${record.delta}
                WHERE id = ${record.player_id} AND workspace_id = ${wsId}
            `;
        }

        await sql`DELETE FROM elo_history WHERE event_id = ${rootId} AND type = 'tournament' AND workspace_id = ${wsId}`;
        await sql`UPDATE tournaments SET status = 'scheduled' WHERE id = ${rootId} AND workspace_id = ${wsId}`;
    }
    
    return tournamentDayIds; // Return them in case the caller needs them
};"""

content = content.replace(old_playoff_state_func, new_playoff_state_func)

# 2. Fix DELETE /api/tournaments
old_delete_handler = """            if ((matchday.phase || 'round_robin') === 'round_robin') {
                await sql`
                    DELETE FROM tournaments
                    WHERE id = ${id}
                      AND workspace_id = ${req.workspaceId}
                `;
                await deleteTeamTournamentPlayoffState(rootId, req.workspaceId);
                return res.json({ message: 'Giornata Round Robin eliminata e fase finale ripristinata con successo' });
            }

            const fixtureRows = await sql`
                SELECT id
                FROM team_tournament_fixtures
                WHERE matchday_id = ${matchday.id}
                LIMIT 1
            `;

            await sql`
                DELETE FROM tournaments
                WHERE id = ${id}
                  AND workspace_id = ${req.workspaceId}
            `;

            if (fixtureRows.length > 0) {
                await resetTeamTournamentFixtureBranch(rootId, req.workspaceId, fixtureRows[0].id);
            }

            return res.json({ message: 'Playoff matchday deleted and bracket reset successfully' });
        }"""

new_delete_handler = """            // We intentionally do NOT return here, so that the code below
            // will find the matches of THIS matchday (id) and delete them + revert ELO!
            let customMessage = '';
            
            if ((matchday.phase || 'round_robin') === 'round_robin') {
                await deleteTeamTournamentPlayoffState(rootId, req.workspaceId);
                customMessage = 'Giornata Round Robin eliminata e fase finale ripristinata con successo';
            } else {
                const fixtureRows = await sql`
                    SELECT id
                    FROM team_tournament_fixtures
                    WHERE matchday_id = ${matchday.id}
                    LIMIT 1
                `;
                if (fixtureRows.length > 0) {
                    await resetTeamTournamentFixtureBranch(rootId, req.workspaceId, fixtureRows[0].id);
                }
                customMessage = 'Playoff matchday deleted and bracket reset successfully';
            }
            
            // Now we set a flag so the rest of the endpoint knows to return customMessage
            req.customTeamTournamentMessage = customMessage;
        }"""

content = content.replace(old_delete_handler, new_delete_handler)

# 3. Handle the custom message response at the end of the endpoint
old_end_handler = """        logger.tournament("delete", id, { revertedPlayers: totalReverted, status: "completed" });
        res.json({ 
            message: 'Tournament deleted and all ELO ratings reverted successfully',
            revertedPlayers: totalReverted
        });
    } catch (error) {"""

new_end_handler = """        logger.tournament("delete", id, { revertedPlayers: totalReverted, status: "completed" });
        res.json({ 
            message: req.customTeamTournamentMessage || 'Tournament deleted and all ELO ratings reverted successfully',
            revertedPlayers: totalReverted
        });
    } catch (error) {"""

content = content.replace(old_end_handler, new_end_handler)

with open('server.js', 'w') as f:
    f.write(content)

print("server.js updated successfully")
