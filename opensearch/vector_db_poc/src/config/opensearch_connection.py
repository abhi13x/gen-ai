from opensearchpy import OpenSearch
from opensearchpy.exceptions import ConnectionError, AuthenticationException

# Function to create and return an OpenSearch client
def client(host: str, port: int):
    try:
        # Create the OpenSearch client with specified SSL/TLS settings
        client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_compress=True,  # enables gzip compression for request bodies
            use_ssl=False,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )
        print('Connection successful')
        return client

    except ConnectionError as conn_err:
        # Handle connection-related issues, such as unreachable host or port issues
        print(f"ConnectionError: Unable to connect to OpenSearch at {host}:{port} - {conn_err}")
        raise

    except AuthenticationException as auth_err:
        # Handle authentication issues if credentials are involved
        print(f"AuthenticationError: Authentication failed - {auth_err}")
        raise

    except Exception as e:
        # Catch any other unexpected errors and log them
        print(f"An error occurred while connecting to the OpenSearch client: {e}")
        raise