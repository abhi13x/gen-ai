#!/usr/bin/env python3
"""Simple test script to verify PostgreSQL connection"""

import os
import sys
from psycopg2 import connect

# Set the environment variables
os.environ["DB_NAME"] = "GEN_AI_PRACTICE"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "Abhishek13"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"

# Add the mcp_server directory to path to import db_config
sys.path.append(os.path.join(os.path.dirname(__file__), 'mcp_server'))

from db_config import DatabaseConfig, DBConfigModel

print("Testing PostgreSQL connection...")

try:
    # Test database configuration
    db_config: DBConfigModel = DatabaseConfig().set_db_config()
    print(f"Database config: {db_config}")
    
    # Test connection
    conn = connect(
        user=db_config.user,
        password=db_config.password,
        host=db_config.host,
        port=db_config.port,
        database=db_config.dbname
    )
    print("✅ Connection successful!")
    
    # Test a simple query
    cur = conn.cursor()
    cur.execute("SELECT version();")
    result = cur.fetchone()
    print(f"PostgreSQL version: {result[0]}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()