"""
Database initialization script
Creates database and tables
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database import Base, engine
from auth_models import User
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not specific database)
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Ashu6672"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='weatherpro_db'")
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute("CREATE DATABASE weatherpro_db")
            print("✅ Database 'weatherpro_db' created successfully!")
        else:
            print("ℹ️  Database 'weatherpro_db' already exists")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        raise


def create_tables():
    """Create all tables"""
    try:
        # Create all tables defined in models
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise


if __name__ == "__main__":
    print("🔧 Initializing database...")
    print("=" * 50)
    
    # Step 1: Create database
    create_database()
    
    # Step 2: Create tables
    create_tables()
    
    print("=" * 50)
    print("🎉 Database initialization complete!")
    print("\nDatabase: weatherpro_db")
    print("Tables: users")
