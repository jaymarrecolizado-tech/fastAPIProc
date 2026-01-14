"""Create database and demo users for testing."""
import asyncio
import pymysql
from app.core.security import get_password_hash
from app.core.config import settings
from sqlalchemy import create_engine, text
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.roles import UserRole

# Parse database URL to get connection details
db_url = settings.DATABASE_URL.replace("+aiomysql", "")
pymysql_url = db_url.replace("mysql://", "mysql+pymysql://")

# Create engine without async
engine = create_engine(pymysql_url, isolation_level="AUTOCOMMIT")

async def create_database_and_users():
    # Step 1: Create database
    print("Step 1: Creating database 'dict_procurement'...")
    try:
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS dict_procurement CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
        print("  Database created successfully!")
    except Exception as e:
        print(f"  Error creating database: {e}")
        print("\n  Trying alternative method...")
        # Try with raw MySQL connection
        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                port=3306
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS dict_procurement CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            conn.commit()
            cursor.close()
            conn.close()
            print("  Database created successfully via raw connection!")
        except Exception as e2:
            print(f"  Error with raw connection: {e2}")
            return
    
    # Step 2: Create demo users
    print("\nStep 2: Creating demo users...")
    
    demo_users = [
        {
            "name": "Administrator",
            "email": "admin@dict.gov.ph",
            "password": "AdminPass123!",
            "role": UserRole.ADMIN,
            "department": "Information Communications Technology"
        },
        {
            "name": "Procurement Officer",
            "email": "procurement@dict.gov.ph",
            "password": "ProcurePass123!",
            "role": UserRole.PROCUREMENT_OFFICER,
            "department": "Procurement Office"
        },
        {
            "name": "BAC Chairman",
            "email": "bac@dict.gov.ph",
            "password": "BacPass123!",
            "role": UserRole.BAC_CHAIR,
            "department": "Bids and Awards Committee"
        },
        {
            "name": "Juan Dela Cruz",
            "email": "user@dict.gov.ph",
            "password": "UserPass123!",
            "role": UserRole.END_USER,
            "department": "Information Technology Service"
        }
    ]
    
    try:
        async with AsyncSessionLocal() as db:
            for user_data in demo_users:
                # Check if user already exists
                from sqlalchemy import select
                result = await db.execute(
                    select(User).where(User.email == user_data["email"])
                )
                existing_user = result.scalar_one_or_none()
                
                if existing_user:
                    print(f"  User {user_data['email']} already exists - skipping")
                    continue
                
                # Create new user
                password_hash = get_password_hash(user_data["password"])
                user = User(
                    name=user_data["name"],
                    email=user_data["email"],
                    password_hash=password_hash,
                    role=user_data["role"],
                    department=user_data["department"],
                    is_active=True
                )
                db.add(user)
                print(f"  Created user: {user_data['name']} ({user_data['email']}) - Role: {user_data['role'].value}")
            
            await db.commit()
            print("\n  All demo users created successfully!")
            
    except Exception as e:
        print(f"  Error creating users: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(create_database_and_users())
    print("\nDatabase setup complete!")
    print("\nDemo accounts:")
    print("  Admin: admin@dict.gov.ph / AdminPass123!")
    print("  Procurement: procurement@dict.gov.ph / ProcurePass123!")
    print("  BAC: bac@dict.gov.ph / BacPass123!")
    print("  User: user@dict.gov.ph / UserPass123!")
