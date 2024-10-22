import os
import re
import json
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Setup Google API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBjsd3_1lX3-WW3opA8O27VdkPSj55h8pg"

# Initialize Google Generative AI model
model = ChatGoogleGenerativeAI(model="gemini-pro")

# Define directories
c_file_folder = r'C:\Users\kkgau\OneDrive\testing_file\c_proj'
output_folder = r'C:\Users\kkgau\OneDrive\testing_file\test_case'
function_json_path = r'C:\Users\kkgau\OneDrive\testing_file\py_pro\c_and_header_files.json'

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load function_json_path file
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

# Extract function signatures from C files
def extract_function_signatures(c_code):
    pattern = r'\b(\w+)\s+(\w+)\s*\(([^)]*)\)\s*(?:;|\{)'  # Match function signatures
    return re.findall(pattern, c_code)

# Clean the generated C test code
def clean_generated_code(generated_code):
    cleaned_code = generated_code.replace("```", "")
    cleaned_code = re.sub(r"\bpython\b", "", cleaned_code, flags=re.IGNORECASE)
    cleaned_code = "\n".join(line.rstrip() for line in cleaned_code.splitlines() if line.strip())
    return cleaned_code

def build_prompt_for_generating_tests(function_name, parameters, dependencies):
    return (
        f"Generate C unit test code for the function '{function_name}' with parameters {parameters}. "
        "Make sure to utilize Unity's assert functions to verify correct behavior and include both normal and edge case tests. "
        f"Include any necessary functions from the following dependencies: {dependencies}.\n\n"

        "Ensure that the Unity framework is correctly linked in your test build. This includes:\n"
        "- Including the Unity source file (unity.c) in your compilation command.\n"
        "- Using the correct linking options to avoid undefined references to Unity functions like 'UnityAssertEqualNumber'.\n\n"

        "Also, ensure your program is compiled as a console application by specifying the entry point, if necessary:\n"
        "- Use the '-mconsole' flag when compiling with GCC.\n\n"

        f"C Function Signature: void {function_name}(size_t *i, size_t *n, int *t, int *x, int *y);\n"
        "Header File: #include \"my_header.h\"\n"
        "Include Unity Header: #include \"unity.h\"\n\n"

        "Generate the test cases with the following guidelines:\n"
        "1. `test_add_normal`: Implement normal addition cases with proper initialization and pointers.\n"
        "2. `test_add_edge_cases`: Test edge cases such as overflow/underflow scenarios with appropriate checks.\n\n"

        "Ensure all function calls use valid pointers and initialize variables before calling the 'add' function. "
        "Use Unity's assert functions correctly to validate the results.\n\n"

        "Provide only the C code for the test cases, including necessary headers, without additional comments or explanations."
    )

# Generate C unit test code using Gemini API
def generate_c_test_code(function_name, parameters, dependencies):
    try:
        prompt = build_prompt_for_generating_tests(function_name, parameters, dependencies)
        
        # Call Gemini API to generate C unit test code
        chain = LLMChain(llm=model, prompt=PromptTemplate(
            input_variables=["prompt"],
            template="{prompt}"
        ))
        
        test_code = chain.run({"prompt": prompt}).strip()
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

# Extract functions from dependent files
def extract_dependencies(file_path, c_and_header_data):
    dependencies = []
    if file_path in c_and_header_data:
        dep_files = c_and_header_data[file_path].get("dependencies", [])
        for dep_file in dep_files:
            dep_path = os.path.join(c_file_folder, dep_file)
            if os.path.isfile(dep_path):
                dependencies.append(dep_path)
    return dependencies

# Process the dependencies and extract function signatures from dependent files
def process_dependencies(dependencies, c_and_header_data):
    all_signatures = []
    for dep_file in dependencies:
        if os.path.isfile(dep_file):
            with open(dep_file, "r") as file:
                c_code = file.read()
                all_signatures.extend(extract_function_signatures(c_code))
        else:
            logging.warning(f"Dependent file '{dep_file}' not found in {c_and_header_data}.")
    return all_signatures

# Process C file and generate C test for each function
def process_c_file(file_path, c_and_header_data):
    with open(file_path, "r") as file:
        c_code = file.read()
        function_signatures = extract_function_signatures(c_code)
        
        # Check for dependencies in the JSON
        dependencies = extract_dependencies(file_path, c_and_header_data)
        
        # Extract functions from dependent files if any
        if dependencies:
            dep_signatures = process_dependencies(dependencies, c_and_header_data)
            function_signatures.extend(dep_signatures)
        
        # Generate C test cases for all found functions
        for _, fn_name, parameters in function_signatures:
            generate_c_test_code(fn_name, parameters, dependencies)

# Main entry point for input processing
def process_input(file_name, c_and_header_data):
    # Directly process the C file specified by the user
    file_path = os.path.join(c_file_folder, file_name)
    if os.path.isfile(file_path):
        language = detect_language(file_path)
        if language == "C":
            process_c_file(file_path, c_and_header_data)
        else:
            logging.error(f"Language '{language}' is not supported.")
    else:
        logging.error(f"No file found matching '{file_name}'.")

if __name__ == "__main__":
    # Start C test generation process
    c_and_header_data = load_function_json()
    user_input = input("Enter the C file name: ")
    process_input(user_input, c_and_header_data)
