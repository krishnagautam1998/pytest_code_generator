import ast

def extract_functions(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    return functions

# Example usage
file_path = '/path/to/your/file.py'  # Replace with the path to your Python file
functions = extract_functions(file_path)

if functions:
    print("Functions found in the file:")
    for function in functions:
        print(function)
else:
    print("No functions found in the file.")
