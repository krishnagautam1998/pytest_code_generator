import os

file_path = r'C:\genai\project'

list_of_files = os.listdir(file_path)

for file_name in list_of_files:
    # python_files = []
    if file_name.endswith(".py"):
        print(file_name)
