import os
import inspect
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
text = st.text_area("Paste your Python code here:")

# Submit button
submit = st.button("Generate Pytest Code")

def get_function_signatures(code):
    """
    Extracts function signatures from the given Python code.
    """
    functions = []
    # Use exec to load the code in a temporary dictionary
    local_namespace = {}
    exec(code, {}, local_namespace)
    
    for name, obj in local_namespace.items():
        if inspect.isfunction(obj):
            signature = inspect.signature(obj)
            functions.append((name, signature))
    
    return functions

def generate_pytest_code(functions):
    """
    Generates pytest code based on extracted function signatures.
    """
    pytest_code = ""
    for func_name, signature in functions:
        params = ", ".join(str(param) for param in signature.parameters.values())
        pytest_code += f"\n\ndef test_{func_name}():\n"
        pytest_code += f"    # TODO: replace with actual test case\n"
        pytest_code += f"    result = {func_name}({params})\n"
        pytest_code += f"    assert result == expected_output  # replace expected_output with actual expected value\n"
    
    return pytest_code

# Generate and display the response when the button is pressed
if submit and text:
    # Get the function signatures
    functions = get_function_signatures(text)
    
    # Generate pytest code
    pytest_code = generate_pytest_code(functions)
    
    # Display the generated pytest code
    st.code(pytest_code, language='python')
