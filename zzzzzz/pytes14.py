import getpass
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st
import ast
import requests

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("AIzaSyBjsd3_1lX3-WW3opA8O27VdkPSj55h8pg")

model = ChatGoogleGenerativeAI(model="gemini-pro")

st.title("Pytest Code Generator")

# Input the FastAPI URL to hit
fastapi_url = st.text_input("Enter the FastAPI URL to get function code:", "http://127.0.0.1:8000/")

# Submit button to hit the FastAPI URL
fetch_code = st.button("Fetch Function Code from FastAPI")

if fetch_code and fastapi_url:
    try:
        # Provide the necessary JSON payload with the POST request
        data = {
            "a": 1.0,  # Example data; modify as needed
            "b": 2.0
        }
        # Make a POST request to the FastAPI endpoint
        response = requests.post(fastapi_url, json=data)
        response.raise_for_status()  # Check if the request was successful
        
        # Print out the entire JSON response for debugging
        st.write("Full response from FastAPI:")
        st.json(response.json())

        # Try to access 'function_code' in the response
        function_code = response.json().get("function_code", None)
        
        if function_code:
            st.write("Function code fetched successfully.")
            st.code(function_code, language="python")
        else:
            st.error("The key 'function_code' was not found in the response.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching function code: {e}")

# Specify the output folder for Pytest files
output_folder = st.text_input("Enter the path of the folder to save Pytest files:", r'C:\genai\pytest_tests')

# Submit button to generate the Pytest code
submit = st.button("Generate Pytest Code")

if submit and function_code:
    # Create a prompt template
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="Write a pytest code for the function: {text}, and check all the conditions and situations of the Python program, then generate the pytest code for the Python file or programming function."
    )

    # Create a chain with the LLM and prompt
    chain = LLMChain(llm=model, prompt=prompt_template)

    # Run the chain to generate the pytest code
    pytest_code = chain.run({"text": function_code})

    # Save the generated Pytest code in the specified folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pytest_filename = "test_function.py"  # Use a suitable filename
    pytest_filepath = os.path.join(output_folder, pytest_filename)

    with open(pytest_filepath, "w") as file:
        file.write(pytest_code)

    # Display a success message
    st.success(f"Generated Pytest file: {pytest_filename}")
    st.code(pytest_code, language="python")

