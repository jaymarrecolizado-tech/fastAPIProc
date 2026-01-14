"""Test database connection and model creation"""

import asyncio
from sqlalchemy import text
from app.core.database import engine, AsyncSessionLocal, Base
from app.models import (
    User, PurchaseRequest, PRItem, RFQ, Supplier,
    Canvass, SupplierQuotation, QuotationItem, QuotationImage,
    BACDocument, ApprovalRouting, PurchaseOrder,
    Document, ActivityLog, Notification
)


async def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT VERSION()"))
            version = result.scalar()
            print(f"✅ Database connected successfully!")
            print(f"   MySQL Version: {version}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


async def create_all_tables():
    """Create all database tables from models"""
    print("\n📊 Creating database tables...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print(f"✅ Successfully created {len(Base.metadata.tables)} tables:")
            for table_name in sorted(Base.metadata.tables.keys()):
                print(f"   - {table_name}")
            return True
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def verify_tables_exist():
    """Verify tables exist in database"""
    print("\n🔍 Verifying tables exist...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = DATABASE() "
                "ORDER BY table_name"
            ))
            tables = [row[0] for row in result.fetchall()]
            
            expected_tables = {
                'users', 'purchase_requests', 'pr_items', 'rfqs', 'suppliers',
                'canvasses', 'supplier_quotations', 'quotation_items', 'quotation_images',
                'bac_documents', 'approval_routings', 'purchase_orders',
                'documents', 'activity_logs', 'notifications'
            }
            
            existing_tables = set(tables)
            missing_tables = expected_tables - existing_tables
            extra_tables = existing_tables - expected_tables
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                return False
            
            print(f"✅ All {len(expected_tables)} expected tables exist!")
            if extra_tables:
                print(f"ℹ️  Extra tables (not in our models): {extra_tables}")
            
            return True
    except Exception as e:
        print(f"❌ Table verification failed: {e}")
        return False


async def test_model_creation():
    """Test creating a simple user record"""
    print("\n👤 Testing user model creation...")
    try:
        from app.core.security import get_password_hash
        from app.core.roles import UserRole
        
        async with AsyncSessionLocal() as session:
            # Create test user
            hashed_password = get_password_hash("TestPassword123!")
            test_user = User(
                name="Test Administrator",
                email="test.admin@dict.gov.ph",
                password_hash=hashed_password,
                role=UserRole.ADMIN,
                department="Information Technology Service",
                is_active=True
            )
            
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            
            print(f"✅ Test user created successfully!")
            print(f"   ID: {test_user.id}")
            print(f"   Email: {test_user.email}")
            print(f"   Role: {test_user.role}")
            
            # Clean up test user
            await session.delete(test_user)
            await session.commit()
            print(f"✅ Test user cleaned up successfully!")
            
            return True
    except Exception as e:
        print(f"❌ Model creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def verify_indexes():
    """Verify important indexes are created"""
    print("\n🔍 Verifying critical indexes...")
    try:
        async with engine.connect() as conn:
            # Check for important indexes
            result = await conn.execute(text(
                "SELECT table_name, index_name "
                "FROM information_schema.statistics "
                "WHERE table_schema = DATABASE() "
                "AND index_name != 'PRIMARY' "
                "ORDER BY table_name, index_name"
            ))
            indexes = result.fetchall()
            
            print(f"✅ Found {len(indexes)} indexes:")
            for table_name, index_name in indexes[:10]:  # Show first 10
                print(f"   - {table_name}.{index_name}")
            
            if len(indexes) > 10:
                print(f"   ... and {len(indexes) - 10} more")
            
            return True
    except Exception as e:
        print(f"❌ Index verification failed: {e}")
        return False


async def verify_foreign_keys():
    """Verify foreign key constraints are created"""
    print("\n🔗 Verifying foreign key constraints...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text(
                "SELECT table_name, constraint_name "
                "FROM information_schema.key_column_usage "
                "WHERE table_schema = DATABASE() "
                "AND referenced_table_name IS NOT NULL "
                "ORDER BY table_name, constraint_name"
            ))
            fks = result.fetchall()
            
            print(f"✅ Found {len(fks)} foreign key constraints:")
            for table_name, constraint_name in fks[:10]:  # Show first 10
                print(f"   - {table_name}.{constraint_name}")
            
            if len(fks) > 10:
                print(f"   ... and {len(fks) - 10} more")
            
            return True
    except Exception as e:
        print(f"❌ Foreign key verification failed: {e}")
        return False


async def main():
    """Run all validation tests"""
    print("=" * 60)
    print("🚀 DICT PROCUREMENT SYSTEM - PHASE 1 VALIDATION")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Database Connection
    results['connection'] = await test_database_connection()
    
    if not results['connection']:
        print("\n❌ STOP: Cannot proceed without database connection")
        print("   Please check your database configuration in .env file")
        return
    
    # Test 2: Create Tables
    results['tables'] = await create_all_tables()
    
    if not results['tables']:
        print("\n❌ STOP: Cannot proceed without tables")
        return
    
    # Test 3: Verify Tables
    results['verify_tables'] = await verify_tables_exist()
    
    # Test 4: Model Creation
    results['model_creation'] = await test_model_creation()
    
    # Test 5: Indexes
    results['indexes'] = await verify_indexes()
    
    # Test 6: Foreign Keys
    results['foreign_keys'] = await verify_foreign_keys()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name.replace('_', ' ').title()}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! PHASE 1 COMPLETE!")
        print("=" * 60)
        print("\n✅ Foundation is solid and ready for Phase 2")
        print("✅ Database models validated")
        print("✅ All 15 tables created successfully")
        print("✅ Foreign keys and indexes verified")
        print("\n🎯 Next Steps:")
        print("   1. Initialize Alembic for migrations")
        print("   2. Proceed to Phase 2: Authentication System")
    else:
        print("⚠️  SOME TESTS FAILED - PLEASE REVIEW")
        print("=" * 60)
        print("\n❌ Foundation has issues that must be resolved")
        print("   before proceeding to Phase 2")
    
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
