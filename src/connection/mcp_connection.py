from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from . import llm_model
from config import AppConfig
from typing import Any
import sys
from langgraph.checkpoint.memory import InMemorySaver


class Connection:
    def __init__(self, config: AppConfig):
        self.mcp_server_file: str = config.MCP_SERVER_FILE
        self.llm_model: str = config.LLM_MODEL
        self.llm_temperature: float = config.LLM_MODEL_TEMPERATURE
        self.__api_key: str = config.OLLAMA_API_KEY
        self.__dbname: str = config.DB_NAME
        self.__user: str = config.DB_USER
        self.__dbpassword: str = config.DB_PASSWORD
        self.__dbhost: str = config.DB_HOST
        self.__dbport: str = config.DB_PORT
        self.__mongodb_connection_string: str = config.MONGODB_CONNECTION_STRING

    def get_mcp_client(self):
        UV_PYTHON_EXECUTABLE = sys.executable
        try:
            dbname = self.__dbname
            user = self.__user
            password = self.__dbpassword
            host = self.__dbhost
            port = self.__dbport
            server_env_vars: dict[str, str] = {
                # Pass all necessary database credentials explicitly
                "DB_NAME": dbname,
                "DB_USER": user,
                "DB_PASSWORD": password,
                "DB_HOST": host,
                "DB_PORT": port,
            }
            mcp_client_details: dict[str, Any] = {
                "MongoDB": {
                    "transport": "stdio",
                    "command": "npx",
                    "args": ["-y", "mongodb-mcp-server", "--readOnly"],
                    "env": {
                        "MDB_MCP_CONNECTION_STRING": self.__mongodb_connection_string
                    },
                }
            }
            print(mcp_client_details)
            mcp_client = MultiServerMCPClient(mcp_client_details)
            print(f"MCP Client connected to server: {self.__mongodb_connection_string}")
            return mcp_client
        except Exception as e:
            print(
                f"MCP Client connection error to server {self.__mongodb_connection_string}: {e}"
            )
            raise RuntimeError(e)

    async def get_tools(self):
        print("Connecting to MCP Server and fetching tools...")
        client = self.get_mcp_client()
        print("Getting tools from MCP Server")
        tools = await client.get_tools()
        print(f"✅ Tools loaded: {[tool.name for tool in tools]}")
        return tools

    async def agent_execution(self):
        try:
            tools = await self.get_tools()
            print("Initializing LLM Model...")
            llm = await llm_model.model_init(
                api_key=self.__api_key,
                llm_model=self.llm_model,
                llm_temperature=self.llm_temperature,
            )
            agent_executor = create_agent(llm, tools, checkpointer=InMemorySaver())
            print("LLM Model initialized and Agent created successfully.")
            return agent_executor
        except Exception as e:
            print(f"Agent execution error: {e}")
            raise RuntimeError(e)
