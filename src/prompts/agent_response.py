from langchain.messages import HumanMessage

def response_agent(agent):
    messages = HumanMessage("""Summarize the errors from the db_service index in the last 30 minutes containing 'timeout' and provide the resolution."""
    )
    print(f"USER REQUEST: {messages}")
    print("FINAL AGENT SUMMARY:")
    for chunk in agent.stream({
                    "messages": [messages]
                }, 
                stream_mode="values"):
        # Each chunk contains the full state at that point
        latest_message = chunk["messages"][-1]
        if latest_message.content:
            print(f"Agent: {latest_message.content}")
        elif latest_message.tool_calls:
            print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")