"""Check existing users in database."""
import asyncio
from app.core.database import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select

async def check_users():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        print(f"Total users in database: {len(users)}")
        print()
        
        if users:
            for user in users:
                print(f"  - {user.name} ({user.email})")
                print(f"    Role: {user.role}")
                print(f"    Department: {user.department}")
                print(f"    Active: {user.is_active}")
                print()
        else:
            print("  No users found in database!")
            print("  You need to create demo users to test the login.")

if __name__ == "__main__":
    asyncio.run(check_users())
