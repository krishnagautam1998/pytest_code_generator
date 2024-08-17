
# # import required modules 
# import inspect 
  
# # explicit function 
# def fun(a): 
#     return 2*a 
  
# # use isfunction() 
# print(inspect.isfunction(fun))

# import required module 
# import inspect 

# # create classes 
# class A(object): 
# 	pass

# class B(A): 
# 	pass

# class C(B): 
# 	pass

# # not nested 
# print(inspect.getmro(C)) 

# fastapi_app.py
# from fastapi import FastAPI
# from pydantic import BaseModel
# from main import Sum  # Import the Sum class from main.py

# # Initialize FastAPI app
# app = FastAPI()

# # Define a Pydantic model for input validation
# class AddInput(BaseModel):
#     a: int
#     b: int

# # Create an instance of the Sum class
# res = Sum()

# # Define the endpoint
# @app.post("/add")
# def add_numbers(input: AddInput):
#     # Use the add method from the Sum class
#     result = res.add(input.a, input.b)
#     return {"result": result}

# # This part is for running the app directly with Python
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# exa1.py
# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import inspect

app = FastAPI()

class CodeInput(BaseModel):
    code: str

def get_function_signatures(code):
    """
    Extracts function signatures from the given Python code.
    """
    functions = []
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

@app.post("/generate_pytest")
def generate_pytest(input: CodeInput):
    """
    Endpoint to generate pytest code.
    """
    try:
        functions = get_function_signatures(input.code)
        pytest_code = generate_pytest_code(functions)
        return {"pytest_code": pytest_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with:
# uvicorn api:app --reload


     