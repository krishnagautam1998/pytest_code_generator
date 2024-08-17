from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class OperationRequest(BaseModel):
    a: float
    b: float

@app.post("/sum")
def sum_numbers(request: OperationRequest):
    a = request.a
    b = request.b
    c = a + b
    return {
        "result": c
    }

@app.post("/subtract")
def subtract_numbers(request: OperationRequest):
    a = request.a
    b = request.b
    c = a - b
    return {
        "result": c
    }

@app.post("/multiply")
def multiply_numbers(request: OperationRequest):
    a = request.a
    b = request.b
    c = a * b
    return {
        "result": c
    }

@app.post("/divide")
def divide_numbers(request: OperationRequest):
    a = request.a
    b = request.b
    if b == 0:
        return {"error": "Division by zero is not allowed"}
    c = a / b
    return {
        "result": c
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
