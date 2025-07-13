import aiosqlite
import asyncio

async def async_fetch_users():
    """Asynchronously fetch users from the database."""
    async with aiosqlite.connect("user.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print(f"Fetched users: {users}")
            return users
        
async def async_fetch_older_users():
    """Asynchronously fetch users older than 40."""
    async with aiosqlite.connect("user.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print(f"Fetched older users: {older_users}")
            return older_users
            
async def fetch_concurrently():
    """Fetch user data concurrently."""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
