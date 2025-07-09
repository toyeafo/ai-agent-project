import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_functions import available_functions
from prompts import system_prompt
from call_functions import call_function
from config import MAX_ITERS

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}")
        

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
        
        try:
            result = generate_content(client, messages, verbose)
            if result:
                print(result)
                break
        except Exception as e:
            return f"Error: Couldn't generate content: {e}"


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    function_responses = []
    for function_call_part in response.function_calls:
        result = call_function(function_call_part, verbose)

        if (not result.parts or not result.parts[0].function_response):
            raise Exception("No function response received or empty response.")
        
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])
    
    messages.append(types.Content(role="tool", parts=function_responses))

    if not function_responses:
        raise Exception("No function responses received.")
        
if __name__ == "__main__":
    main()
