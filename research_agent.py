import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0) # Use 1.5 for stability
memory = MemorySaver()

def local_research_tool(query: str):
    """Search private company files in knowledge_base."""
    from mcp_server import read_local_research
    return read_local_research(query)

def web_research_tool(query: str):
    """Search the live internet for news and Bitcoin prices."""
    from mcp_server import web_research # <--- FIXED NAME HERE
    return web_research(query)

tools = [local_research_tool, web_research_tool]

system_msg = SystemMessage(content="""You are an Elite Researcher. 
When searching local files, use only the word 'investment' or 'rules'. 
When searching the web, use 'bitcoin price'. 
Always combine the information to answer the user.""")

agent = create_react_agent(llm, tools, checkpointer=memory)

if __name__ == "__main__":
    print("--- 🦖 Dinosaur Hybrid Researcher Online ---")
    config = {"configurable": {"thread_id": "teju_session_1"}}
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]: break
        inputs = {"messages": [system_msg, HumanMessage(content=user_input)]}
        for chunk in agent.stream(inputs, config=config, stream_mode="values"):
            chunk["messages"][-1].pretty_print()