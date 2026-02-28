import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

st.set_page_config(page_title="Pivot Chatbot")
st.title("🤖 Chat with your Pivot Table")

# 1. User uploads their own file
uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if "xlsx" in uploaded_file.name else pd.read_csv(uploaded_file)
    st.write("Data Preview:", df.head(3)) # Shows the user the bot sees the data

    # 2. Connect to the LLM (using Secrets for safety)
    llm = ChatOpenAI(model="arcee-ai/trinity-large-preview:free", api_key=st.secrets["MY_API_KEY"])
    # 3. Initialize the Agent
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

    # 4. Chat Interface
    query = st.text_input("Ask a question (e.g., 'What was the total sales in June?')")
    if query:
        with st.spinner("Thinking..."):
            response = agent.run(query)
            st.success(response)
