import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("Missing OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser()
parser.add_argument("user_prompt", type=str)
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()


def main():
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            tool_choice="auto",
            temperature=0,
        )

        message = response.choices[0].message

        # store assistant message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=args.verbose)

                if args.verbose:
                    print(f"-> {result_message['content']}")

                messages.append(result_message)

            continue

        # answer
        print(message.content)
        return

    print("Error: agent did not finish in 20 steps")
    exit(1)


if __name__ == "__main__":
    main()