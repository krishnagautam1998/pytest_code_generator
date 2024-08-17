import os
import streamlit as st
import ast
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()

# Set your Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key not found in environment variables.")
    st.stop()

# Initialize the Google Generative AI client with the API key
genai.api_key = api_key

# Streamlit interface
st.title("Pytest Code Generator")

# Specify the input folder containing Python files and the output folder for Pytest files
input_folder = st.text_input("Enter the path of the folder containing Python files:", r'C:\genai\python_file')
output_folder = st.text_input("Enter the path of the folder to save Pytest files:", r'C:\genai\pytest_tests')

# List all Python files in the specified directory
if os.path.isdir(input_folder):
    python_files = [f for f in os.listdir(input_folder) if f.endswith(".py")]
    if python_files:
        st.write(f"Python files found: {', '.join(python_files)}")
    else:
        st.warning("No Python files found in the specified directory.")
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
                # Create a prompt for each function
                prompt = f"Write a pytest code for the function:\n{function_code}\nCheck all the conditions of the Python program."

                try:
                    # Generate Pytest code using Google Generative AI
                    response = genai.generate_text(
                        model="models/my-model",  # Replace with a valid model name
                        prompt=prompt
                    )
                    pytest_code = response.generations[0].text

                except Exception as e:
                    st.error(f"Failed to generate Pytest code for {function_name}: {str(e)}")
                    continue
                
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
