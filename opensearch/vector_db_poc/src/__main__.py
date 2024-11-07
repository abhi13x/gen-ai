from config.opensearch_connection import client
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def __main__():
    try:
        # Fetch environment variables with error handling for missing variables
        host: str = os.environ["HOST"]
        print('host:', host)
        
        # Ensure the port is converted to an integer and handle errors if conversion fails
        port: int = int(os.environ["PORT"])
        print('port:', port)
        
        # Initialize the client with the retrieved host and port
        clientConn = client(host, port)
        
    except KeyError as e:
        # Handle missing environment variables specifically
        print(f"Environment variable {e} is missing.")
        exit(1)
    except ValueError:
        # Handle incorrect port format if it cannot be converted to an integer
        print("PORT environment variable must be an integer.")
        exit(1)
    except Exception as e:
        # General exception handling for other potential issues
        print(f"Error while running the file: {e}")
        exit(1)

__main__()
