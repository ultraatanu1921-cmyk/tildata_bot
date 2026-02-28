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
    model="arcee-ai/trinity-large-preview:free", 
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
