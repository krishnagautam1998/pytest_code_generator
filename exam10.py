import os
import re
import json
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import List, Dict

# Setup Google API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBjsd3_1lX3-WW3opA8O27VdkPSj55h8pg"  # Replace with actual key

# Initialize Google Generative AI model
model = ChatGoogleGenerativeAI(model="gemini-pro")

# Define directories
c_file_folder = r'C:\Users\kkgau\OneDrive\testing_file\c_proj'
output_folder = r'C:\Users\kkgau\OneDrive\testing_file\c_proj'
function_json_path = r'C:\Users\kkgau\OneDrive\testing_file\py_pro\c_and_header_files.json'

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load function.json file
def load_function_json():
    if os.path.exists(function_json_path):
        with open(function_json_path, "r") as file:
            return json.load(file)
    else:
        logging.error(f"function.json not found at {function_json_path}")
        return {}

# Detect programming language by file extension
def detect_language(file_path):
    extension = os.path.splitext(file_path)[1]
    if extension == ".c":
        return "C"
    return None

# Extract function signatures from C files using regular expressions
# Exclude main, printf, and other standard functions
def extract_functions_from_c_file(file_content: str) -> List[Dict[str, str]]:
    functions = []
    # Regular expression to match function definitions
    function_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*[{;]')
    
    # List of functions to exclude
    excluded_functions = ['main', 'printf']
    
    for match in function_pattern.finditer(file_content):
        return_type = match.group(1)
        func_name = match.group(2)
        func_args = match.group(3)
        
        # Filter out excluded functions
        if func_name not in excluded_functions:
            functions.append({
                "function_name": func_name,
                "return_type": return_type,
                "arguments": func_args
            })
    return functions

# Extract headers from C file
def extract_headers(file_content: str) -> List[str]:
    headers = re.findall(r'#include\s+["<](.*?)[">]', file_content)
    return headers

# Clean the generated C test code
def clean_generated_code(generated_code: str) -> str:
    cleaned_code = generated_code.replace("```", "")
    cleaned_code = re.sub(r"\bpython\b", "", cleaned_code, flags=re.IGNORECASE)
    cleaned_code = "\n".join(line.rstrip() for line in cleaned_code.splitlines() if line.strip())
    return cleaned_code

# Build the LLM prompt for generating C unit tests for a specific function
def generate_unit_tests(function_name: str, return_type: str, function_args: str, user_defined_cases: List[str], headers: List[str], full_file_content: str) -> str:
    prompt = f"""
    Generate unit test cases for the C function and a test runner using the Unity framework. Below are the details:

    **Function Signature:**
    {return_type} {function_name}({function_args})

    **Specific Test Cases to Consider:**
    {', '.join(user_defined_cases)}

    **Relevant Header Files:**
    {', '.join(headers)}

    The full file content is provided for additional context. Provide only the C test code without any explanations or additional text. The code should include:

    ### Test Structure:
    1. **Test Case Descriptions**: Each test case should check specific scenarios, including:
        - Normal cases
        - Edge cases (e.g., using `INT_MAX`, `INT_MIN`, etc.)
        - User-defined cases and error scenarios

    2. **Input/Output**: Provide the correct input values for each test and expected outputs, using proper Unity macros like `TEST_ASSERT_EQUAL` for assertions.

    3. **Edge Cases**: Handle edge cases for the function being tested.

    4. **setUp and tearDown Functions**: Include both `setUp()` and `tearDown()` functions, even if they do nothing, to avoid compilation errors. Ensure proper declaration.

    5. **Test Runner Structure**:
        - Include a `main()` function to act as the test runner, calling `UNITY_BEGIN()` and `UNITY_END()` to initialize and finalize the test.
        - Use `RUN_TEST()` to execute each test function.
    
    ### Additional Compilation Considerations:
    - Ensure all declared test functions are implemented to avoid undefined references.
    - Properly include header files for the tested function and any other required files.
    - Avoid common errors like "undefined reference to `WinMain@16`" by ensuring correct linkage and function declarations.

    ### Example:
    I'm working on a C project that uses the Unity testing framework to test a `sum` function defined in `add.c`. I've created a test file `test_sum.c` with test cases. When compiling, I'm encountering errors related to undefined references for `setUp`, `tearDown`, and undefined references like "WinMain@16."

    Provide the complete C test code with:
    - Correct function declarations
    - Implementations for missing test functions
    - Proper Unity macros for assertions
    """
    return prompt


# Generate C unit test code using Gemini API
def generate_c_test_code(function_name: str, return_type: str, parameters: str, headers: List[str], full_file_content: str):
    try:
        mock_functions = []  # Add any mock functions if needed
        prompt = generate_unit_tests(function_name, return_type, parameters, mock_functions, headers, full_file_content)
        
        # Using LLMChain to generate unit test code
        chain = LLMChain(
            llm=model,
            prompt=PromptTemplate(
                input_variables=["prompt"],
                template="{prompt}"
            )
        )

        response = chain.run({"prompt": prompt})

        # Check response format
        if isinstance(response, str):
            test_code = response.strip()
        else:
            logging.error("Unexpected response format from the model.")
            return

        cleaned_code = clean_generated_code(test_code)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        test_filename = f"test_{function_name}.c"
        filepath = os.path.join(output_folder, test_filename)
        with open(filepath, "w") as file:
            file.write(cleaned_code)
        
        logging.info(f"Generated C test file: {test_filename}")

    except Exception as e:
        logging.error(f"Failed to generate C test for function '{function_name}': {e}")

# Process C file and generate C test for each function
def process_c_file(file_path: str):
    try:
        with open(file_path, "r") as file:
            c_code = file.read()
            functions = extract_functions_from_c_file(c_code)
            headers = extract_headers(c_code)

            if functions:
                for function in functions:
                    generate_c_test_code(function['function_name'], function['return_type'], function['arguments'], headers, c_code)
            else:
                logging.warning(f"No user-defined functions found in {file_path}.")
    
    except Exception as e:
        logging.error(f"Failed to process C file '{file_path}': {e}")

# Main entry point for input processing
def process_input(file_name: str):
    # Directly process the C file specified by the user
    file_path = os.path.join(c_file_folder, file_name)
    if os.path.isfile(file_path):
        language = detect_language(file_path)
        if language == "C":
            process_c_file(file_path)
        else:
            logging.error(f"Language '{language}' is not supported.")
    else:
        logging.error(f"No file found matching '{file_name}'.")

if __name__ == "__main__":
    # Start C test generation process
    user_input = input("Enter the C file name (with .c extension): ")
    process_input(user_input)
