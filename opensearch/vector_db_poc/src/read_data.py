import pandas as pd
from sentence_transformers import SentenceTransformer


class DataOperations:
    def read_data(self, path):
        file_path: str = path
        print(f"File path: {file_path}")
        columns = ["id", "original_title", "overview"]
        df_movies = pd.read_csv(file_path, usecols=columns)
        df_movies = df_movies.dropna()
        print(f"Successfully read the CSV file.")
        return df_movies

    def embedding_data(self):
        model_name = "all-MiniLM-L6-v2"
        model = SentenceTransformer(model_name)
        EMBEDDING_DIM = model.encode(["Sample sentence"])[0].shape[0]
        index_name = "movies"
        index_body = {
            "settings": {"index": {"knn": True, "knn.algo_param.ef_search": 100}},
            "mappings": {  # how do we store,
                "properties": {
                    "embedding": {
                        "type": "knn_vector",  # we are going to put
                        "dimension": EMBEDDING_DIM,
                        "method": {
                            "name": "hnsw",
                            "space_type": "l2",
                            "engine": "nmslib",
                            "parameters": {"ef_construction": 128, "m": 24},
                        },
                    }
                }
            },
        }
        return index_name, index_body
