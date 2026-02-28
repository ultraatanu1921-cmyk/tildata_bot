import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

st.set_page_config(page_title="Pivot Chatbot")
st.title("🤖 Chat with your Pivot Table")

# 1. File Uploader
uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    # Load data
    df = pd.read_excel(uploaded_file) if "xlsx" in uploaded_file.name else pd.read_csv(uploaded_file)
    st.write("Data Preview:", df.head(3))

    # 2. Setup the Brain (using the NICKNAME 'MY_API_KEY')
    # Use base_url for OpenRouter/Arcee if needed
    llm = ChatOpenAI(
        model="openai/gpt-oss-120b:free", 
        api_key=st.secrets["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"],
        base_url="https://openrouter.ai/api/v1"
    )

    # 3. Create the Agent
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

    # 4. Chat Interface
    query = st.text_input("Ask a question about your data:")
    if query:
        with st.spinner("Thinking..."):
            response = agent.run(query)
            st.success(response)
