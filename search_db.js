import { neon } from '@neondatabase/serverless';
import dotenv from 'dotenv';
dotenv.config();

const sql = neon(process.env.DATABASE_URL);

async function main() {
    try {
        const teams = await sql`SELECT id, name, players FROM team_tournament_teams`;
        for (const team of teams) {
            let updated = false;
            let playersArray = team.players;
            if (!playersArray) continue;
            if (typeof playersArray === 'string') {
                playersArray = JSON.parse(playersArray);
            }
            
            for (const p of playersArray) {
                if (p.name === 'Gabiele' || p.name === 'Gabriele' || p.surname === 'Bettarini') {
                    console.log(`Found player: ${p.name} ${p.surname} in team ${team.name}`);
                    if (p.name === 'Gabiele') {
                        p.name = 'Gabriele';
                        updated = true;
                    }
                }
            }
            
            if (updated) {
                await sql`UPDATE team_tournament_teams SET players = ${JSON.stringify(playersArray)}::jsonb WHERE id = ${team.id}`;
                console.log("Updated team successfully!");
            }
        }
    } catch (e) {
        console.error(e);
    }
}

main();
