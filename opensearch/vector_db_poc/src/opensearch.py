from opensearchpy import AuthenticationException, OpenSearch

class OpenSearchVectorDb:
  host: str
  port: int
  def __init__(self, host: str, port: int):
     self.host = host
     self.port = port
  # Function to create and return an OpenSearch client
  def client(self):
    try:
        # Create the OpenSearch client with specified SSL/TLS settings
        CLUSTER_URL: str = f"https://{self.host}:{self.port}"
        print(f"Cluster URL: {CLUSTER_URL}")
        client = OpenSearch(
            hosts=[CLUSTER_URL],
            http_auth=("admin", "admin"),
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
        print(f"ConnectionError: Unable to connect to OpenSearch at {self.host}:{self.port} - {conn_err}")
        raise

    except AuthenticationException as auth_err:
        # Handle authentication issues if credentials are involved
        print(f"AuthenticationError: Authentication failed - {auth_err}")
        raise

    except Exception as e:
        # Catch any other unexpected errors and log them
        print(f"An error occurred while connecting to the OpenSearch client: {e}")
        raise

  def create_index(self, client, index_name, index_body):
    return client.indices.create(index=index_name, body=index_body)
  
  