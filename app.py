import streamlit as st
from research_agent import agent, system_msg # Importing your "Brain"
from langchain_core.messages import HumanMessage

# 1. Page Configuration
st.set_page_config(page_title="Nexus: Hybrid Intelligence Agent", page_icon="🔍")
st.title("Nexus: Hybrid Intelligence Agent")
st.markdown("Query your **Private Files** and the **Live Web** in one place.")

# 2. Session State for Chat History (Dino Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Input
if prompt := st.chat_input("Ask me about Bitcoin or Company Rules..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Agent Execution
    with st.chat_message("assistant"):
        with st.spinner("Nexus is thinking and searching..."):
            # We use the same config thread to keep memory alive
            config = {"configurable": {"thread_id": "streamlit_session"}}
            inputs = {"messages": [system_msg, HumanMessage(content=prompt)]}
            
            # Get the final response from the agent
            result = agent.invoke(inputs, config=config)
            final_answer = result["messages"][-1].content
            
            st.markdown(final_answer)
            st.session_state.messages.append({"role": "assistant", "content": final_answer})