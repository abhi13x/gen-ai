# mcp_server.py

from mcp.server.fastmcp import FastMCP
import sys
import os
from psycopg2 import connect # Assuming you meant to import connect directly, not psycopg2

# Initialize the MCP server with a unique name
mcp = FastMCP("Postgres-Server")

# Get environment variables (defaults are used if not passed by the client)
DB_NAME=os.environ.get("DB_NAME", "GEN_AI_PRACTICE")
DB_USER=os.environ.get("DB_USER", "postgres")
DB_PASSWORD=os.environ.get("DB_PASSWORD","")
DB_HOST=os.environ.get("DB_HOST", "localhost")
DB_PORT=os.environ.get("DB_PORT", "5432")

# Optional: Print the received config to STDERR for debugging
print(f"DEBUG: Connecting to PostgreSQL at {DB_HOST}:{DB_PORT}/{DB_NAME}", file=sys.stderr)

@mcp.tool()
def query_database(sql_query: str) -> str:
    """Execute a SQL query against the PostgreSQL database and return results."""
    conn = None
    try:
        conn = connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        cur = conn.cursor()
        cur.execute(sql_query)
        
        # Check if it's a SELECT query (i.e., data is available)
        if cur.description:
            rows = cur.fetchall()
            # Get column names for better results readability
            columns = [desc[0] for desc in cur.description]
            # Simple way to format results: rows with headers
            results = [columns] + rows
            return str(results)
        else:
            # Handle non-SELECT queries (INSERT, UPDATE, DELETE)
            conn.commit()
            return f"Query executed successfully. Rows affected: {cur.rowcount}"
            
    except Exception as e:
        # Print error details to stderr for debugging
        print(f"SQL Execution Error: {e}", file=sys.stderr)
        if conn:
            conn.rollback()
        return f"Error: {str(e)}"
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    try:
        # Run the server using the stdio transport (Subprocess communication)
        print("Starting PostgreSQL database Server on stdio...", file=sys.stderr)
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error starting MCP server: {e}", file=sys.stderr)
        sys.exit(1)