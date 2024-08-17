import os
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"]

# Define a template for generating pytest code
prompt_template = PromptTemplate(
    input_variables=["function_description"],
    template="Generate pytest code for the following Python function: {function_description}"
)

# Initialize the OpenAI model with specific settings
llm = OpenAI(temperature=0.3)  # Lower temperature makes output more deterministic

# Create a chain to generate pytest code using the prompt template
pytest_chain = LLMChain(llm=llm, prompt=prompt_template)

def generate_pytest_code(function_description):
    """Generate pytest code for a given function description."""
    pytest_code = pytest_chain.run(function_description)
    return pytest_code

# Example function description
function_description = """
def add(a, b):
    \"\"\"Return the sum of a and b.\"\"\"
    return a + b
"""

# Generate pytest code
pytest_code = generate_pytest_code(function_description)

# Print the generated pytest code
print("Generated pytest code:\n")
print(pytest_code)

# Save the generated code to a file if needed
with open("test_generated.py", "w") as f:
    f.write(pytest_code)
