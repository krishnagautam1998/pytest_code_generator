import os
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "sk-proj-nbjFETtFADFhR7LN7KxsT3BlbkFJNCWFICekHCYtknS8xqFe"

# Create an OpenAI LLM with a specified temperature
llm = OpenAI(temperature=0.3)

# Streamlit interface
st.title("Pytest Code Generator")

# Text input for the user
text = st.text_input("Ask for any pytest code:")

# Submit button
submit = st.button("Generate Code")

# Generate and display the response when the button is pressed
if submit and text:
    prompt_template = PromptTemplate(input_variables=["text"], template="Write a pytest code for: {text}")
    chain = LLMChain(prompt_template=prompt_template, llm=llm)
    
    # Run the chain to generate the pytest code
    pytest_code = chain.run({"text": text})
    
    # Display the generated pytest code
    st.code(pytest_code, language='python')
