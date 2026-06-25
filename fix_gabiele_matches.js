import 'dotenv/config';
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL);

async function main() {
    const tables = ['matches', 'tournaments'];
    for (const t of tables) {
        console.log(`Checking ${t}...`);
        try {
            // Find columns of type text or varchar or json
            const cols = await sql`SELECT column_name FROM information_schema.columns WHERE table_name = ${t} AND data_type IN ('text', 'character varying', 'json', 'jsonb')`;
            for (const col of cols) {
                const query = `SELECT id, ${col.column_name} FROM ${t} WHERE ${col.column_name}::text LIKE '%Gabiele%'`;
                // we have to use string builder since dynamic column names in neon sql template literal are tricky
                const res = await sql(query);
                if (res.length > 0) {
                    console.log(`Found Gabiele in ${t}.${col.column_name}:`, res);
                    // For json/jsonb columns, we can do a replace
                    if (t === 'tournaments' && col.column_name === 'teams') {
                       // it's a json column
                       for (const row of res) {
                          const str = JSON.stringify(row[col.column_name]).replace(/Gabiele/g, 'Gabriele');
                          await sql`UPDATE tournaments SET teams = ${str}::jsonb WHERE id = ${row.id}`;
                          console.log(`Updated tournament ${row.id}`);
                       }
                    } else if (col.column_name === 'guest_player1_name' || col.column_name === 'guest_player2_name' || col.column_name === 'guest_player3_name' || col.column_name === 'guest_player4_name') {
                       const queryUpdate = `UPDATE ${t} SET ${col.column_name} = REPLACE(${col.column_name}, 'Gabiele', 'Gabriele') WHERE ${col.column_name} LIKE '%Gabiele%'`;
                       await sql(queryUpdate);
                       console.log(`Updated ${t}.${col.column_name}`);
                    }
                }
            }
        } catch (e) { console.error(e) }
    }
}

main().catch(console.error);
