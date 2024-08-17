import ast
import os

# Specify the folder containing the Python files
file_path = r'C:\genai\project'

# List all files in the specified directory
list_of_files = os.listdir(file_path)

def extract_functions_from_file(file_path):
    # Read the Python file
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())

    # Extract function definitions
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            function_code = ast.get_source_segment(open(file_path).read(), node)
            functions.append({"name": function_name, "code": function_code})
    
    return functions

def save_functions_to_files(functions, output_dir, base_file_name):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, function in enumerate(functions, start=1):
        # Create a unique filename for each function
        file_name = f"{base_file_name}_function_{i}.py"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w") as file:
            file.write(function['code'])
        print(f"Saved {function['name']} to {file_name}")

def main():
    output_dir = "extracted_functions"  # Directory to save extracted functions

    for file_name in list_of_files:
        if file_name.endswith(".py"):
            full_file_path = os.path.join(file_path, file_name)
            print(f"Processing file: {file_name}")
            
            functions = extract_functions_from_file(full_file_path)
            
            if functions:
                save_functions_to_files(functions, output_dir, os.path.splitext(file_name)[0])
                print(f"Extracted {len(functions)} functions from '{file_name}' and saved them to '{output_dir}'")
            else:
                print(f"No functions found in '{file_name}'")

if __name__ == "__main__":
    main()
