from connection.mcp_connection import Connection
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from config import AppConfig
import asyncio
from typing import Any

async def agent_execution():
    try:
        config = AppConfig()
        connection = Connection(config)
        agent_executor = await connection.agent_execution()
        system_text = "Assume the role of data engineer. You are expert in NoSQL and MongoDB database."
        system_message = SystemMessage(system_text)
        print(f"\n--- System Message (NL) ---\n{system_message.content}")
        question_text = "List all collections in the connected MongoDB database."
         # 1. Create a Human Message with the user's natural language question
        question = HumanMessage(question_text)
        print(f"\n--- User Question (NL) ---\n{question.content}")
        question_text1 = "List all the shows with rating above 8"
        question1 = HumanMessage(question_text1)
        print(f"\n--- User Question (NL) ---\n{question1.content}")
        
        # 2. Invoke the agent with the Human Message
        # The agent's LLM will receive this and decide to generate SQL or use the "Postgres-Server" tool.
        result: dict[str, Any] = await agent_executor.ainvoke(
            {
                "messages": [system_message, question, question1]
                }, 
            {
                "configurable": {
                    "thread_id": "2"
                    }
                })
        print("\n--- Agent Response ---")
        # Extract structured content from tool messages
        final_answer = None
        sql_query_used = None
        for message in result["messages"]:
            if isinstance(message, AIMessage) and message.tool_calls:
                # LLM's decision to use a tool (the SQL generation step)
                print(f"🤖 LLM Tool Call: {message.tool_calls}")
                
            elif isinstance(message, ToolMessage):
                # The result returned from the tool (the database result)
                # This content is typically the raw database output (table list).
                print(f"🛠️ Tool Observation: {message.content}...") # Print first 200 chars of DB result
                
            elif isinstance(message, AIMessage) and not message.tool_calls:
                # The final, user-facing answer (the tables formatted nicely, or an error)
                final_answer = message.content 
        
        print("\n--- Final Agent Response ---")
        if final_answer:
            print(final_answer)
        else:
            print("Agent completed execution but did not generate a final human-readable answer.")
    except Exception as e:
        print(f"Execution error: {e}")

if __name__ == "__main__":
    asyncio.run(agent_execution())
