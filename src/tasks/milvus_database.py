from langchain_core.tools import tool

# This simulates the Milvus vector search and retrieval of IT Runbooks.
@tool
def retrieve_resolution_steps(error_message: str) -> str:
    """
    Searches the Milvus Vector Database of IT Runbooks and SOPs to find validated resolution steps
    for a given error message identified in the Splunk logs.

    Args:
        error_message: The specific, key error message extracted from the log data.

    Returns:
        A string containing the relevant resolution steps from the knowledge base.
    """
    print(f"\n--- RAG Tool Executing: Milvus Search for '{error_message}' ---")

    # --- MOCK RESPONSE SIMULATING MILVUS RAG RETRIEVAL ---
    # This result would be the top K chunks retrieved from the Milvus vector store.
    if "DB_CONNECTION_POOL_EXHAUSTED" in error_message:
        return """
        Resolution Steps for DB_CONNECTION_POOL_EXHAUSTED:
        1. Check Database connection metrics for concurrent requests > 90% of pool size.
        2. Increase the 'max_pool_size' setting in the microservice configuration file (auth-config.yaml) by 25%.
        3. If issue persists, check for unclosed connections or long-running queries in the database logs.
        4. Engage DB Admin for high-level resource analysis.
        """
    return "No specific runbook found for this error. Suggest searching general troubleshooting guides."