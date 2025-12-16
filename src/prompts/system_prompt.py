from langchain.agents import create_agent
from langchain.messages import SystemMessage
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain import load_mcp_tools

class ResponseSchema(BaseModel):
    splunk_logs: str
    resolution_steps: str
# Define the system prompt (Crucial for ReAct and instruction following)
# # Note: The prompt explicitly guides the agent to use the tools in the correct order.

def get_system_prompt(llm, tools):
    system_message = f"""You are an expert Incident Resolution Agent. Your goal is to analyze user requests,
        FIRST use the `run_splunk_query` tool to retrieve logs,
        and THEN use the `retrieve_resolution_steps` tool based on the logs. 
        Finally, provide a consolidated summary of the error and the validated resolution steps.\n
        Use the ReAct format (Thought, Action, Action Input, Observation) for reasoning."""

    prompt_template = SystemMessage(
        "{system_message} \n\nUser Query: {input}\n\n{agent_scratchpad}"
    )
    ## Create the Agent Executor (The runtime for the agent)
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=prompt_template,
        response_format=ToolStrategy(ResponseSchema)
    )
    return agent