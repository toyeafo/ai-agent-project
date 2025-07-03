import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_functions import available_functions
from prompts import system_prompt
from call_functions import call_function

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

    generate_content(client, messages, verbose)


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
        return f"Response: {response.text}"

    for function_call_part in response.function_calls:
        result = call_function(function_call_part, verbose)
        try:
            gen_ai_response = result.parts[0].function_response.response
            if gen_ai_response and verbose:
                print(f"-> {gen_ai_response}")
        except Exception as e:
            return f"Error: Fatal exception: {e}"
        
if __name__ == "__main__":
    main()
