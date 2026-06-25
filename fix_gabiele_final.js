import 'dotenv/config';
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL);

async function main() {
    console.log("Fixing team_tournament_matchday_matches...");
    const matches = await sql`SELECT id, team1_players FROM team_tournament_matchday_matches WHERE team1_players::text LIKE '%Gabiele%'`;
    
    for (const match of matches) {
        let playersJson = match.team1_players;
        let changed = false;
        
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
            console.log(`Fixing match ID: ${match.id}`);
            await sql`UPDATE team_tournament_matchday_matches SET team1_players = ${JSON.stringify(playersJson)}::jsonb WHERE id = ${match.id}`;
        }
    }
    console.log("Done.");
}

main().catch(console.error);
