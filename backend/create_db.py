import asyncio
import asyncpg
from sqlalchemy.engine.url import make_url

url = make_url("postgresql+asyncpg://postgres:Lavish%402003@localhost:5432/postgres")

async def create_db():
    conn = await asyncpg.connect(
        user=url.username,
        password=url.password,
        host=url.host,
        port=url.port,
        database='postgres'
    )
    # Check if database exists
    exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = 'hcp_crm'")
    if not exists:
        print("Creating database hcp_crm...")
        await conn.execute('CREATE DATABASE hcp_crm')
    else:
        print("Database hcp_crm already exists.")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(create_db())
