import os
import sys
import json
import time

from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GEMINI_MODEL = os.getenv("GEMINI_MODEL")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GEMINI_API_KEY or not GROQ_API_KEY:
    print("Error: API keys are missing. Please check your .env file.")
    sys.exit(1)

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

def ask_gemini(prompt):
    start_time = time.time()

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    elapsed_time = time.time() - start_time

    return {
        "provider": "Gemini",
        "model": GEMINI_MODEL,
        "reply": response.text,
        "input_tokens": response.usage_metadata.prompt_token_count,
        "output_tokens": response.usage_metadata.candidates_token_count,
        "response_time": round(elapsed_time, 2)
    }


def ask_groq(prompt):
    start_time = time.time()

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    elapsed_time = time.time() - start_time

    return {
        "provider": "Groq",
        "model": GROQ_MODEL,
        "reply": response.choices[0].message.content,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "response_time": round(elapsed_time, 2)
    }
def get_prompt():
    if len(sys.argv) < 2:
        print('Usage: uv run tracker.py "your prompt"')
        sys.exit(1)

    return " ".join(sys.argv[1:])


def calculate_cost(input_tokens, output_tokens, input_price, output_price):
    input_cost = (input_tokens / 1_000_000) * input_price
    output_cost = (output_tokens / 1_000_000) * output_price

    total_cost = input_cost + output_cost

    return round(total_cost, 8)

def run_comparison(prompt):
    results = []

    print("\nCalling Gemini...")
    try:
        gemini_result = ask_gemini(prompt)
        results.append(gemini_result)
    except Exception as e:
        print(f"Gemini error: {e}")

    print("\nCalling Groq...")
    try:
        groq_result = ask_groq(prompt)
        results.append(groq_result)
    except Exception as e:
        print(f"Groq error: {e}")

    return results

GEMINI_INPUT_PRICE = 0.30
GEMINI_OUTPUT_PRICE = 2.50

GROQ_INPUT_PRICE = 0.075
GROQ_OUTPUT_PRICE = 0.30


def add_costs(results):
    for result in results:
        if result["provider"] == "Gemini":
            input_price = GEMINI_INPUT_PRICE
            output_price = GEMINI_OUTPUT_PRICE
        else:
            input_price = GROQ_INPUT_PRICE
            output_price = GROQ_OUTPUT_PRICE

        result["input_price_per_m"] = input_price
        result["output_price_per_m"] = output_price

        result["cost_usd"] = calculate_cost(
            result["input_tokens"],
            result["output_tokens"],
            input_price,
            output_price
        )

    return results



def display_results(results):
    if not results:
        print("\nNo successful API responses to display.")
        return

    for result in results:
        print("\n" + "=" * 50)
        print(f"Provider: {result['provider']}")
        print(f"Model: {result['model']}")
        print(f"Response Time: {result['response_time']} seconds")
        print(f"Input Tokens: {result['input_tokens']}")
        print(f"Output Tokens: {result['output_tokens']}")
        print(f"Cost: ${result['cost_usd']:.8f}")
        print("-" * 50)
        print("Reply:")
        print(result["reply"])
        print("=" * 50)

def save_results(results):
    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print("\nResults saved to results.json")

if __name__ == "__main__":
    prompt = get_prompt()
    results = run_comparison(prompt)
    results = add_costs(results)
    display_results(results)
    save_results(results)