import os
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st
import inspect
from main import Sum

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"]

# Create an OpenAI LLM with a specified temperature
llm = OpenAI(temperature=0.3)

# Streamlit interface
st.title("Pytest Code Generator")

file_path = r'C:\genai\project'

list_of_files = os.listdir(file_path)

for file_name in list_of_files:
    # python_files = []
    if file_name.endswith(".py"):
        st.success(file_name)


# Text input for the user
text = inspect.getsource(Sum)

st.success(text)
# Submit button
submit = st.button("Generate Code")

# Generate and display the response when the button is pressed
if submit and text:
    # Create a prompt template
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="Write a pytest code for: {text}"
    )

    # Create a chain with the LLM and prompt
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    # Run the chain to generate the pytest code
    pytest_code = chain.run({"text": text})
    
    # Display the generated pytest code
    st.code(pytest_code, language='python')
