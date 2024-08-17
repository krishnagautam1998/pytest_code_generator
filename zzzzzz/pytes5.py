import os
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"]

# Create an OpenAI LLM with a specified temperature
llm = OpenAI(temperature=0.3)

# Streamlit interface
st.title("Pytest Code Generator")

# Text input for the user
text = st.text_area("Ask for any pytest code:")

# Submit button
submit = st.button("Generate Code")

# Generate and display the response when the button is pressed
if submit and text:
    # Create a prompt template
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="Write a pytest code for: {text}. this text_area python code is given and check all the condition of python program then generate of pytest code."
    )

    # Create a chain with the LLM and prompt
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    # Run the chain to generate the pytest code
    pytest_code = chain.run({"text": text})
    
    # Display the generated pytest code
    st.code(pytest_code, language='python')
