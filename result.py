# import subprocess

# # Define the paths to the source files using raw strings
# test_sum_path = r"C:\Users\kkgau\OneDrive\testing_file\c_proj\test_sum.c"
# add_path = r"C:\Users\kkgau\OneDrive\testing_file\c_proj\add.c"
# unity_path = r"C:\Users\kkgau\OneDrive\testing_file\c_proj\Unity\src"

# # Compile the C program by linking both test_sum.c and add.c along with Unity
# compile_process = subprocess.run([
#     "gcc", 
#     test_sum_path, 
#     add_path,
#     f"{unity_path}\\unity.c",  # Include Unity source file
#     "-o", 
#     "program.exe",  # Output executable name
#     "-I", 
#     r"C:\Users\kkgau\OneDrive\testing_file\c_proj",  
#     "-I", 
#     unity_path  # Include Unity header files
# ], capture_output=True, text=True)

# # Check for compilation errors
# if compile_process.returncode != 0:
#     print("Compilation failed with the following error:")
#     print(compile_process.stderr)  # Print the error output from GCC
# else:
#     print("Compilation succeeded. Running the program...")
#     # Run the compiled C program
#     run_process = subprocess.run(["program.exe"], capture_output=True, text=True)  # Run the program and capture output
#     if run_process.returncode != 0:
#         print("Program execution failed.")
#     else:
#         print("Program output:")
#         print(run_process.stdout)  # Print the standard output from the program
###############################################################################################

# import subprocess
# import os

# # Define the paths to the source files using raw strings
# test_sum_path = r"C:\Users\kkgau\OneDrive\testing_file\c_proj\test_sum.c"
# add_path = r"C:\Users\kkgau\OneDrive\testing_file\c_proj\add.c"
# unity_path = r"C:\Users\kkgau\OneDrive\testing_file\c_proj\Unity\src"

# # Check if the Unity source file exists
# unity_file = os.path.join(unity_path, "unity.c")
# if not os.path.isfile(unity_file):
#     print(f"Error: Unity source file not found at {unity_file}")
# else:
#     # Compile the C program by linking both test_sum.c and add.c along with Unity
#     compile_process = subprocess.run([
#         "gcc",
#         test_sum_path,
#         add_path,
#         unity_file,  # Include Unity source file
#         "-o",
#         "program.exe",  # Output executable name
#         "-I",
#         r"C:\Users\kkgau\OneDrive\testing_file\c_proj",  
#         "-I",
#         unity_path  # Include Unity header files
#     ], capture_output=True, text=True)

#     # Check for compilation errors
#     if compile_process.returncode != 0:
#         print("Compilation failed with the following error:")
#         print(compile_process.stderr)  # Print the error output from GCC
#     else:
#         print("Compilation succeeded. Running the program...")
#         # Run the compiled C program
#         run_process = subprocess.run(["program.exe"], capture_output=True, text=True)  # Run the program and capture output
        
#         # Check for runtime errors
#         if run_process.returncode != 0:
#             print("Program execution failed with the following error:")
#             print(run_process.stderr)  # Print the standard error output from the program
#         else:
#             print("Program output:")
#             print(run_process.stdout)  # Print the standard output from the program
###############################################################################
import subprocess
import os

# Define the paths to the source files using raw strings
test_sum_path = r"C:\Users\kkgau\OneDrive\testing_file\c_proj\test_sum.c"
add_path = r"C:\Users\kkgau\OneDrive\testing_file\c_proj\add.c"
unity_path = r"C:\Users\kkgau\OneDrive\testing_file\c_proj\Unity\src"

# Check if the Unity source file exists
unity_file = os.path.join(unity_path, "unity.c")
if not os.path.isfile(unity_file):
    print(f"Error: Unity source file not found at {unity_file}")
else:
    # Compile the C program by linking both test_sum.c and add.c along with Unity
    compile_process = subprocess.run([
        "gcc",
        test_sum_path,
        add_path,
        unity_file,  # Include Unity source file
        "-o",
        "program.exe",  # Output executable name
        "-I",
        r"C:\Users\kkgau\OneDrive\testing_file\c_proj",  
        "-I",
        unity_path,  # Include Unity header files
        "-mconsole"  # Ensure console subsystem is used
    ], capture_output=True, text=True)

    # Check for compilation errors
    if compile_process.returncode != 0:
        print("Compilation failed with the following error:")
        print(compile_process.stderr)  # Print the error output from GCC
    else:
        print("Compilation succeeded. Running the program...")
        # Run the compiled C program
        run_process = subprocess.run(["program.exe"], capture_output=True, text=True)  # Run the program and capture output
        
        # Check for runtime errors
        if run_process.returncode != 0:
            print("Program execution failed with the following error:")
            print(run_process.stderr)  # Print the standard error output from the program
        else:
            print("Program output:")
            print(run_process.stdout)  # Print the standard output from the program
