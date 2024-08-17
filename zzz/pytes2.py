import os
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"]
# Define a prompt template for generating pytest code
prompt_template = PromptTemplate(
    input_variables=["function_description"],
    template=(
        "Generate pytest code for the following Python function. "
        "Include multiple test cases and edge cases: {function_description}"
    )
)

# Initialize the OpenAI model with specific settings
llm = OpenAI(temperature=0.3)  # Lower temperature for more deterministic output

# Create a chain to generate pytest code using the prompt template
pytest_chain = LLMChain(llm=llm, prompt=prompt_template)

def generate_pytest_code(function_description):
    """Generate pytest code for a given function description."""
    pytest_code = pytest_chain.run(function_description)
    return pytest_code

def main():
    print("Enter the Python function description for which you want to generate pytest code:")
    
    # Get function description from the user
    function_description = input().strip()
    
    # Generate pytest code
    pytest_code = generate_pytest_code(function_description)
    
    # Print the generated pytest code
    print("\nGenerated pytest code:\n")
    print(pytest_code)

    # Optionally save the generated code to a file
    with open("generated_test.py", "w") as f:
        f.write(pytest_code)

if __name__ == "__main__":
    main()
