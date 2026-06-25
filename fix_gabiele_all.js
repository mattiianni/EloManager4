import 'dotenv/config';
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL);

async function main() {
    console.log("Fetching all tables...");
    const tablesRes = await sql`
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
    `;
    const tables = tablesRes.map(t => t.table_name);
    
    for (const t of tables) {
        try {
            const cols = await sql`SELECT column_name FROM information_schema.columns WHERE table_name = ${t} AND data_type IN ('text', 'character varying', 'json', 'jsonb')`;
            for (const col of cols) {
                const query = `SELECT id, ${col.column_name} FROM "${t}" WHERE ${col.column_name}::text LIKE '%Gabiele%'`;
                const res = await sql(query);
                if (res.length > 0) {
                    console.log(`Found Gabiele in table ${t}, column ${col.column_name}, row IDs:`, res.map(r => r.id));
                    // I will just print them here, then we can decide how to fix them
                }
            }
        } catch (e) {
            // some tables might not have 'id' column
        }
    }
    console.log("Done.");
}

main().catch(console.error);
