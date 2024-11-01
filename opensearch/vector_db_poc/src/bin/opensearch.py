class OpenSearch:
  def __init__(self, client):
    self.client = client

  def create_index(index_name:str, shards: int = 4):
    return 