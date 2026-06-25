import 'dotenv/config';
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL);

async function main() {
    console.log("Checking players table...");
    const players = await sql`SELECT * FROM players WHERE name LIKE '%Gabiele%' OR surname LIKE '%Gabiele%'`;
    console.log("Players:", players);

    console.log("Checking team_tournament_teams...");
    const teams = await sql`SELECT id, name, players FROM team_tournament_teams`;
    for (const team of teams) {
        let changed = false;
        let playersJson = team.players;
        if (typeof playersJson === 'string') {
            try { playersJson = JSON.parse(playersJson); } catch(e) {}
        }
        
        if (Array.isArray(playersJson)) {
            for (const p of playersJson) {
                if (p.name && p.name.includes('Gabiele')) {
                    p.name = p.name.replace('Gabiele', 'Gabriele');
                    changed = true;
                }
            }
        }
        
        if (changed) {
            console.log(`Fixing team ${team.name} (ID: ${team.id})`);
            await sql`UPDATE team_tournament_teams SET players = ${JSON.stringify(playersJson)} WHERE id = ${team.id}`;
        }
    }
    
    // Check if matches have Gabiele in some json
    // Usually they don't, but let's check tournaments JSON configurations just in case
    console.log("Done checking teams.");
}

main().catch(console.error);
