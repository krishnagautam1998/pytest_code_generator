import getpass
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st
import ast


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("AIzaSyBjsd3_1lX3-WW3opA8O27VdkPSj55h8pg")

from langchain_core.messages import HumanMessage, SystemMessage

model = ChatGoogleGenerativeAI(model="gemini-pro")

st.title("Pytest Code Generator")

# Specify the input folder containing Python files and the output folder for Pytest files
input_folder = st.text_input("Enter the path of the folder containing Python files:", r'C:\genai\python_file')
output_folder = st.text_input("Enter the path of the folder to save Pytest files:", r'C:\genai\pytest_tests')

# List all Python files in the specified directory
if os.path.isdir(input_folder):
    python_files = [f for f in os.listdir(input_folder) if f.endswith(".py")]
    st.write(f"Python files found: {', '.join(python_files)}")
else:
    st.error("Invalid input folder path.")

# Submit button
submit = st.button("Generate Pytest Code")

# Function to extract function nodes and their source code from a Python file
def extract_function_source(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Get the full function source code as a string
            start_lineno = node.lineno - 1  # Adjust for 0-based indexing
            end_lineno = node.end_lineno if hasattr(node, 'end_lineno') else node.body[-1].lineno
            with open(file_path, "r") as f:
                lines = f.readlines()
                function_source = "".join(lines[start_lineno:end_lineno])
                functions.append((node.name, function_source))
    return functions

# Generate and save Pytest code when the button is pressed
if submit and python_files:
    for file_name in python_files:
        full_file_path = os.path.join(input_folder, file_name)
        
        # Extract functions and their source code from the file
        functions = extract_function_source(full_file_path)
        
        if functions:
            for function_name, function_code in functions:
                # Create a prompt template for each function
                prompt_template = PromptTemplate(
                    input_variables=["text"],
                    template="Write a pytest code for the function: {text},and check all the condition and situations of python program then generate of pytest code of python file or progrmming function of python file."
                )

                # Create a chain with the LLM and prompt
                chain = LLMChain(llm=model, prompt=prompt_template)
                
                # Run the chain to generate the pytest code
                pytest_code = chain.run({"text": function_code})
                
                # Save the generated Pytest code in the specified folder
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                
                pytest_filename = f"test_{os.path.splitext(file_name)[0]}_{function_name}.py"
                pytest_filepath = os.path.join(output_folder, pytest_filename)
                
                with open(pytest_filepath, "w") as file:
                    file.write(pytest_code)
                
                # Display a success message for each generated file
                st.success(f"Generated Pytest file: {pytest_filename}")
        else:
            st.warning(f"No functions found in '{file_name}'")