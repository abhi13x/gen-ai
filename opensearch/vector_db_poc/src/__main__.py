from opensearch import OpenSearchVectorDb
from read_data import DataOperations
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
        
        # Initiate OpenSearch Class
        opensearch = OpenSearchVectorDb(host=host, port=port)

        # Initiate Data Operation Class
        data_operations = DataOperations()

        # Data file path
        file_path = r"data\tmdb_5000_movies.csv"
        if os.path.exists(file_path):
            print("File found!")
            movies_data = data_operations.read_data(path=file_path)
        else:
            print("File not found!")
            exit(1)
        # Initialize the client with the retrieved host and port
        client = opensearch.client()
        index_name, index_body = data_operations.embedding_data()
        print(index_name, index_body)
        response = opensearch.create_index(client=client, index_name=index_name, index_body=index_body)
        
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
