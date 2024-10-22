# import os
# import re
# import logging
# from difflib import get_close_matches
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

# # Setup Logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Setup
# if "GOOGLE_API_KEY" not in os.environ:
#     os.environ["GOOGLE_API_KEY"] = "AIzaSyBjsd3_1lX3-WW3opA8O27VdkPSj55h8pg"  # Replace with your API key

# model = ChatGoogleGenerativeAI(model="gemini-pro")

# # File paths and directories
# c_file_folder = r'C:\genai\c_program'
# output_folder = r'C:\genai\py_test'

# # Function to extract function signatures from C files
# def extract_function_signatures(c_code):
#     pattern = r'\b(\w+)\s+(\w+)\s*\(([^)]*)\)\s*(?:;|\{)'  # Match function signatures
#     return re.findall(pattern, c_code)

# # Function to clean the generated pytest code
# def clean_generated_code(generated_code):
#     cleaned_code = generated_code.replace("```", "")
#     cleaned_code = re.sub(r"\bpython\b", "", cleaned_code, flags=re.IGNORECASE)
#     cleaned_code = re.sub(r"\btest\b", "", cleaned_code, flags=re.IGNORECASE)
#     cleaned_code = "\n".join(line.rstrip() for line in cleaned_code.splitlines() if line.strip())
#     return cleaned_code

# # Function to build a focused prompt
# def build_prompt(function_name, parameters):
#     """
#     Builds a prompt to generate pytest functions based on the C function.
#     The prompt includes specific instructions to generate test cases that 
#     handle exceptions, edge cases, and ensure thorough validation.
#     """
#     return (
#         f"Generate a pytest function in Python to test the C function '{function_name}' with parameters {parameters}. "
#         "all the c file function define in pytest file generation in python language."
#         "i want to define all the c function in pytest file using python language."
#         "Ensure that the tests cover normal scenarios, edge cases, and potential errors. "
#         "Use assert statements to validate outputs. "
#         "Include tests to ensure that a `ZeroDivisionError` is raised when the function attempts to divide by zero. "
#         "For example, when a denominator of zero is passed as a parameter, expect a `ZeroDivisionError`. "
#         "If the C function handles division by zero differently, adjust the test accordingly. "
#         "Additionally, handle checks for `TypeError` if invalid input types are passed. "
#         "Focus on generating clean and functional pytest code without redundant code."
#         "Check the pytest program to ensure all conditions are passed before finalizing the generated pytest file."
#     )
# # Function to generate mock pytest code for a C function
# def generate_pytest_code(function_name, parameters):
#     try:
#         prompt = build_prompt(function_name, parameters)
#         prompt_template = PromptTemplate(input_variables=["name", "args"], template=prompt)
#         chain = LLMChain(llm=model, prompt=prompt_template)
#         pytest_code = chain.run({"name": function_name, "args": parameters})

#         cleaned_code = clean_generated_code(pytest_code)

#         if not os.path.exists(output_folder):
#             os.makedirs(output_folder)

#         pytest_filename = f"test_{function_name}.py"
#         filepath = os.path.join(output_folder, pytest_filename)
#         with open(filepath, "w") as file:
#             file.write(cleaned_code)
        
#         logging.info(f"Generated pytest file: {pytest_filename}")
    
#     except Exception as e:
#         logging.error(f"Failed to generate pytest for function '{function_name}': {e}")

# # Function to find closest function names
# def find_closest_function_name(user_input, c_file_folder):
#     """
#     Finds the closest matching function names to the user input from all C files in the specified folder.
#     """
#     function_names = set()
    
#     for filename in os.listdir(c_file_folder):
#         if filename.endswith(".c"):
#             with open(os.path.join(c_file_folder, filename), "r") as file:
#                 c_code = file.read()
#                 function_signatures = extract_function_signatures(c_code)
#                 for _, fn_name, _ in function_signatures:
#                     function_names.add(fn_name)

#     closest_matches = get_close_matches(user_input, function_names, n=5, cutoff=0.5)
#     return closest_matches

# # Function to process input and generate pytest files
# def process_input(user_input):
#     try:
#         file_path = os.path.join(c_file_folder, user_input)
        
#         # Check if the input is a file name
#         if os.path.isfile(file_path):
#             with open(file_path, "r") as file:
#                 c_code = file.read()
#                 function_signatures = extract_function_signatures(c_code)
#                 for return_type, fn_name, parameters in function_signatures:
#                     generate_pytest_code(fn_name, parameters)
#             logging.info(f"Generated pytest files for all functions in '{user_input}'.")
        
#         # Check if the input is a function name
#         else:
#             closest_functions = find_closest_function_name(user_input, c_file_folder)
            
#             if closest_functions:
#                 logging.info(f"Found closest matching functions: {closest_functions}")
#                 for fn_name in closest_functions:
#                     for filename in os.listdir(c_file_folder):
#                         if filename.endswith(".c"):
#                             with open(os.path.join(c_file_folder, filename), "r") as file:
#                                 c_code = file.read()
#                                 function_signatures = extract_function_signatures(c_code)
#                                 for return_type, f_name, parameters in function_signatures:
#                                     if f_name == fn_name:
#                                         generate_pytest_code(f_name, parameters)
#                                         break
#                 logging.info("Generated pytest files for closest matching functions.")
#             else:
#                 logging.info(f"No functions found matching '{user_input}'.")
    
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")

# if __name__ == "__main__":
#     user_input = input("Enter the C file name or function name: ").strip()
#     process_input(user_input)
###########################################################################################

# import os
# import re
# import json
# import logging
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

# # Setup Google API key
# if "GOOGLE_API_KEY" not in os.environ:
#     os.environ["GOOGLE_API_KEY"] = "AIzaSyBjsd3_1lX3-WW3opA8O27VdkPSj55h8pg"

# # Initialize Google Generative AI model
# model = ChatGoogleGenerativeAI(model="gemini-pro")

# # Define directories
# c_file_folder = r'C:\Users\kkgau\OneDrive\testing_file\console'
# output_folder = r'C:\Users\kkgau\OneDrive\testing_file\test_py'
# function_json_path = r'C:\Users\kkgau\OneDrive\testing_file\function.json'

# # Logging setup
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Load function.json file
# def load_function_json():
#     if os.path.exists(function_json_path):
#         with open(function_json_path, "r") as file:
#             return json.load(file)
#     else:
#         logging.error(f"function.json not found at {function_json_path}")
#         return {}

# # Search for function details in function.json
# def find_function_in_json(function_name):
#     function_data = load_function_json()
#     for entry in function_data:
#         if entry['function_name'] == function_name:
#             return entry
#     return None

# # Function to detect programming language by file extension
# def detect_language(file_path):
#     extension = os.path.splitext(file_path)[1]
#     if extension == ".c":
#         return "C"
#     elif extension == ".py":
#         return "Python"
#     elif extension == ".java":
#         return "Java"
#     return None

# # Function to extract function signatures from C files
# def extract_function_signatures(c_code):
#     pattern = r'\b(\w+)\s+(\w+)\s*\(([^)]*)\)\s*(?:;|\{)'  # Match function signatures
#     return re.findall(pattern, c_code)

# # Clean the generated pytest code
# def clean_generated_code(generated_code):
#     cleaned_code = generated_code.replace("```", "")
#     cleaned_code = re.sub(r"\bpython\b", "", cleaned_code, flags=re.IGNORECASE)
#     cleaned_code = re.sub(r"\btest\b", "", cleaned_code, flags=re.IGNORECASE)
#     cleaned_code = "\n".join(line.rstrip() for line in cleaned_code.splitlines() if line.strip())
#     return cleaned_code

# # Analyze function parameters for special conditions
# def analyze_function_conditions(parameters):
#     param_list = parameters.split(',')
#     conditions = []
#     for param in param_list:
#         if 'int' in param:
#             conditions.append("Check for edge cases like division by zero.")
#         if 'char' in param:
#             conditions.append("Check for handling of strings and char limits.")
#         if 'float' in param:
#             conditions.append("Check for floating-point precision.")
#     return conditions

# # Build the LLM prompt based on function conditions
# def build_prompt(function_name, parameters):
#     edge_case_conditions = analyze_function_conditions(parameters)
#     edge_case_info = " ".join(edge_case_conditions)

#     return (
#         f"Generate pytest code to test the function '{function_name}' with parameters {parameters}. "
#         f"Include edge case handling such as invalid inputs, null values, and boundary conditions. "
#         f"{edge_case_info} "
#         "Ensure that all assertions are clear and correctly verify the expected output. "
#         "If applicable, include mocking for any external dependencies. "
#         "Only provide the pytest code without any additional text.\n\n"
        
#         "Extract the function from this C code and convert it to Python:\n"
#         "All function definitions are followed by properly indented blocks. "
#         "The syntax for Python function signatures follows standard Python conventions (e.g., types should be expressed in Python style rather than C style, "
#         "and parameters should have valid Python syntax).\n\n"
        
#         "Fix the pytest test cases so that they properly raise TypeError for invalid inputs and IndexError for invalid indices, ensuring correct exception handling with pytest.raises().\n"
        
#         "Fix all Python syntax errors in the given files, especially focusing on correcting C-style type annotations like 'unsigned char', 'void *', and other non-Python types. "
#         "Replace them with valid Python type hints or remove them if necessary, ensuring the functions are correctly defined according to Python conventions.\n\n"
        
#         """Analyze the provided code and test cases for any function. Identify and fix all errors, including assertion errors, syntax errors, indentation issues, and exception-related errors. "
#         "Ensure the code adheres to the expected behavior and that test cases properly validate edge cases, input handling, and exception raising. 
#         Make necessary changes to both the code and the test cases to resolve all issues and ensure they pass successfully."""
#     )

# # Generate pytest code using Gemini API
# def generate_pytest_code(function_name, parameters, function_path=None):
#     try:
#         prompt = build_prompt(function_name, parameters)
        
#         # Call Gemini API to generate pytest code
#         chain = LLMChain(llm=model, prompt=PromptTemplate(
#             input_variables=["prompt"],
#             template="{prompt}"
#         ))
        
#         pytest_code = chain.run({"prompt": prompt}).strip()
#         cleaned_code = clean_generated_code(pytest_code)

#         if not os.path.exists(output_folder):
#             os.makedirs(output_folder)

#         pytest_filename = f"test_{function_name}.py"
#         filepath = os.path.join(output_folder, pytest_filename)
#         with open(filepath, "w") as file:
#             file.write(cleaned_code)
        
#         logging.info(f"Generated pytest file: {pytest_filename}")
    
#     except NameError as e:
#         logging.warning(f"NameError encountered for function '{function_name}', checking function.json")
#         function_data = find_function_in_json(function_name)
#         if function_data:
#             logging.info(f"Found function '{function_data['function_name']}' in '{function_data['function_path']}'")
#             new_function_path = function_data['function_path']
#             with open(new_function_path, "r") as file:
#                 c_code = file.read()
#                 function_signatures = extract_function_signatures(c_code)
#                 for _, fn_name, parameters in function_signatures:
#                     if fn_name == function_name:
#                         generate_pytest_code(fn_name, parameters, new_function_path)
#                         return
        
#         logging.error(f"Failed to resolve NameError for function '{function_name}': {e}")
#     except Exception as e:
#         logging.error(f"Failed to generate pytest for function '{function_name}': {e}")

# # Process C file and generate pytest for each function
# def process_c_file(file_path):
#     with open(file_path, "r") as file:
#         c_code = file.read()
#         function_signatures = extract_function_signatures(c_code)
#         for _, fn_name, parameters in function_signatures:
#             generate_pytest_code(fn_name, parameters)

# # Main entry point for input processing
# def process_input(file_or_api_name):
#     if file_or_api_name.startswith("http"):
#         # If input is a FastAPI URL (not implemented here)
#         pass
#     else:
#         file_path = os.path.join(c_file_folder, file_or_api_name)
        
#         # Process C file
#         if os.path.isfile(file_path):
#             language = detect_language(file_path)
#             if language == "C":
#                 process_c_file(file_path)
#             else:
#                 logging.error(f"Language '{language}' is not supported.")
#         else:
#             logging.error(f"No file found matching '{file_or_api_name}'.")

# if __name__ == "__main__":
#     user_input = input("Enter the file name or FastAPI URL: ").strip()
#     process_input(user_input)
#######################################################################################
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

# def build_prompt(function_name, parameters, dependencies):
#     return (
#         f"Generate C unit test code for the function '{function_name}' with parameters {parameters}. "
#         "The test should use assert statements to verify correct behavior and cover normal and edge cases. "
#         f"Include any necessary functions from the following dependencies: {dependencies}.\n\n"

#         "Ensure the function's header file is correctly imported to prevent any compilation or runtime errors. "
#         "Do not include comments or explanations in the output.\n\n"

#         f"C Function: void {function_name}({', '.join(parameters)});\n"
#         "Header File: #include \"my_header.h\"\n\n"

#         "Generate the test case using ctypes or another suitable method.\n\n"

#         "Additionally, resolve the following compilation errors without comments or explanations:\n"
#         "1. Missing Header Files: Ensure that 'unity.h' is included.\n"
#         "2. Missing Type Definitions: Define 'size_t' and 'va_list' properly.\n\n"

#         "Provide necessary code to fix these issues without additional text or comments.\n\n"

#         "Lastly, generate a C test case program for the 'add' function with the following test cases:\n"
#         "1. `test_add_normal`: Test normal addition cases.\n"
#         "2. `test_add_edge_cases`: Test edge cases like integer overflow and underflow.\n\n"

#         "Ensure only the C code is provided, including necessary headers, with no extra comments or explanations."
#         "Generate a solution for the following C compilation and linking errors related to test cases:\n"
#         """Generate C test cases for the functions `subtract` and `add` defined as:
#         void subtract(size_t *i, size_t *n, int *t, int *x, int *y);
#         void add(size_t *i, size_t *n, int *t, int *x, int *y);

#         The test cases should handle normal cases, edge cases, and ensure proper pointer usage. Also, provide assertions to validate the expected outcomes.\n"""

#         "Define the function signatures and input/output expectations for the add function in your program. "
#         "In your case, the LLM will generate test cases based on the valid types and arguments."
#     )
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

        "C Function Signature: void {function_name}(size_t *i, size_t *n, int *t, int *x, int *y);\n"
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
