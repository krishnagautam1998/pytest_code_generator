import os
import ast
import streamlit as st
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"]

# Create an OpenAI LLM with a specified temperature
llm = OpenAI(temperature=0.3)

# Streamlit interface
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
                    template="Write a pytest code for the function: {text}, and check all the conditions of the Python program, then generate pytest code for the function."
                )

                # Create a chain with the LLM and prompt
                chain = LLMChain(llm=llm, prompt=prompt_template)
                
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
            # Generate a placeholder Pytest file when no functions are found
            prompt_template = PromptTemplate(
                input_variables=["text"],
                template="There are no functions in the file: {text}. Generate a general pytest template."
            )

            chain = LLMChain(llm=llm, prompt=prompt_template)
            pytest_code = chain.run({"text": full_file_path})

            # Save the generated Pytest code in the specified folder
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            pytest_filename = f"test_{os.path.splitext(file_name)[0]}_nofunctions.py"
            pytest_filepath = os.path.join(output_folder, pytest_filename)

            with open(pytest_filepath, "w") as file:
                file.write(pytest_code)

            st.warning(f"No functions found in '{file_name}'. Generated a general Pytest template: {pytest_filename}")
