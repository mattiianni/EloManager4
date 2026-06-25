import { neon } from '@neondatabase/serverless';
import dotenv from 'dotenv';
dotenv.config();

const sql = neon(process.env.DATABASE_URL);

async function main() {
    try {
        // Find the player
        const players = await sql`SELECT id, name, surname FROM players WHERE surname ILIKE '%Bettarini%'`;
        console.log("Found players:", players);
        
        if (players.length > 0) {
            const playerToUpdate = players.find(p => p.name === 'Gabiele' || p.name === 'Gabriele');
            if (playerToUpdate) {
                console.log("Updating player:", playerToUpdate);
                await sql`UPDATE players SET name = 'Gabriele' WHERE id = ${playerToUpdate.id}`;
                console.log("Player name updated successfully.");
            } else {
                console.log("Gabiele Bettarini not found.");
            }
        } else {
            console.log("No Bettarini found in players table.");
        }
    } catch (e) {
        console.error(e);
    }
}

main();
