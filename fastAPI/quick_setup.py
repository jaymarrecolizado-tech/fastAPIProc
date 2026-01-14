"""Quick setup - Create database and users using raw SQL."""
import pymysql
from app.core.security import get_password_hash

# Database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "dict_procurement"

print("=" * 60)
print("DICT Procurement System - Database Setup")
print("=" * 60)

# Step 1: Create database
print("\nStep 1: Creating database...")
try:
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=3306)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"  Database '{DB_NAME}' created successfully!")
except Exception as e:
    print(f"  Error: {e}")
    exit(1)

# Step 2: Create users table
print("\nStep 2: Creating users table...")
try:
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=3306)
    cursor = conn.cursor()
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL,
        department VARCHAR(255),
        is_active BOOLEAN DEFAULT TRUE,
        last_login_at DATETIME NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_email (email),
        INDEX idx_role (role),
        INDEX idx_is_active (is_active)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    print("  Users table created successfully!")
    
except Exception as e:
    print(f"  Error: {e}")
    exit(1)

# Step 3: Create demo users
print("\nStep 3: Creating demo users...")

demo_users = [
    {
        "name": "Administrator",
        "email": "admin@dict.gov.ph",
        "password": "AdminPass123!",
        "role": "ADMIN",
        "department": "Information Communications Technology"
    },
    {
        "name": "Procurement Officer",
        "email": "procurement@dict.gov.ph",
        "password": "ProcurePass123!",
        "role": "PROCUREMENT_OFFICER",
        "department": "Procurement Office"
    },
    {
        "name": "BAC Chairman",
        "email": "bac@dict.gov.ph",
        "password": "BacPass123!",
        "role": "BAC_CHAIR",
        "department": "Bids and Awards Committee"
    },
    {
        "name": "Juan Dela Cruz",
        "email": "user@dict.gov.ph",
        "password": "UserPass123!",
        "role": "END_USER",
        "department": "Information Technology Service"
    }
]

try:
    for user_data in demo_users:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_data["email"],))
        existing = cursor.fetchone()
        
        if existing:
            print(f"  User {user_data['email']} already exists - skipping")
            continue
        
        # Hash password
        password_hash = get_password_hash(user_data["password"])
        
        # Insert user
        insert_sql = """
        INSERT INTO users (name, email, password_hash, role, department, is_active)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (
            user_data["name"],
            user_data["email"],
            password_hash,
            user_data["role"],
            user_data["department"],
            True
        ))
        
        print(f"  Created: {user_data['name']} ({user_data['email']}) - Role: {user_data['role']}")
    
    conn.commit()
    print("\n  All demo users created successfully!")
    
except Exception as e:
    print(f"  Error: {e}")
    conn.rollback()
    exit(1)
finally:
    cursor.close()
    conn.close()

# Step 4: Verify users
print("\nStep 4: Verifying users...")
try:
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=3306)
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, role FROM users")
    users = cursor.fetchall()
    
    print(f"\n  Total users in database: {len(users)}")
    for user in users:
        print(f"    - {user[0]} ({user[1]}) - Role: {user[2]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"  Error: {e}")

print("\n" + "=" * 60)
print("Database setup complete!")
print("=" * 60)
print("\nDemo accounts:")
print("  Admin: admin@dict.gov.ph / AdminPass123!")
print("  Procurement: procurement@dict.gov.ph / ProcurePass123!")
print("  BAC: bac@dict.gov.ph / BacPass123!")
print("  User: user@dict.gov.ph / UserPass123!")
print("\nYou can now test the login at: http://localhost:3000/login.html")
print("=" * 60)
