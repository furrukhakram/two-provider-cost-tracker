# Two Provider Cost Tracker

A Python tool that compares API usage, response time, and cost between two AI providers — Google Gemini and Groq — using the same prompt.

## Features

- Sends the same prompt to Gemini and Groq.
- Displays the response from each provider.
- Tracks actual input and output tokens.
- Measures API response time.
- Calculates API cost based on token usage and pricing per million tokens.
- Saves comparison results to `results.json`.
- Handles API errors and missing prompts.

## Technologies Used

- Python 3.12
- Google Gemini API (`google-genai`)
- Groq API (`groq`)
- python-dotenv
- uv

## Requirements

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- Gemini API key
- Groq API key

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/furrukhakram/two-provider-cost-tracker.git
cd two-provider-cost-tracker
```

**2. Install dependencies**

```bash
uv sync
```

**3. Create your environment file**

Create a `.env` file in the project root and add the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key

GEMINI_MODEL=gemini-3.5-flash-lite
GROQ_MODEL=openai/gpt-oss-20b
```

Replace the placeholder values with your actual API keys. Keep your `.env` file private and never commit it to GitHub.

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | API key for Google Gemini |
| `GROQ_API_KEY` | API key for Groq |
| `GEMINI_MODEL` | Gemini model to use |
| `GROQ_MODEL` | Groq model to use |

## How to Run

Run the tracker from the project root directory and provide your prompt in quotation marks:

```bash
uv run tracker.py "Explain what Python is in one sentence."
```

The program will call both providers, display their responses, token usage, response time, and calculated cost, then save the results to `results.json`.

## Sample Output

```text
Calling Gemini...

Calling Groq...

==================================================
Provider: Gemini
Model: gemini-3.5-flash-lite
Response Time: 1.87 seconds
Input Tokens: 9
Output Tokens: 30
Cost: $0.00007770
--------------------------------------------------
Reply:
Python is a high-level, interpreted programming language
known for its clear syntax and readability, making it
popular for everything from web development to artificial
intelligence.
==================================================

==================================================
Provider: Groq
Model: openai/gpt-oss-20b
Response Time: 2.58 seconds
Input Tokens: 79
Output Tokens: 103
Cost: $0.00003683
--------------------------------------------------
Reply:
Python is a high-level, interpreted, general-purpose
programming language renowned for its readability,
simplicity, and extensive standard library.
==================================================

Results saved to results.json
```

*Note: Response times, token counts, responses, and costs will vary with each run and prompt.*

## Results File

The program creates `results.json` containing the results from both providers, including:

- Provider name and model
- AI response
- Input and output token counts
- Input and output price per million tokens
- Calculated cost in USD

## What I Learned

Through this project, I learned how to integrate two AI provider APIs into a Python application and retrieve actual token usage. I practiced working with environment variables to protect API keys, handling API errors, measuring response time, calculating costs, and saving structured data into a JSON file.

I also learned how to use Python functions to organize code and how to manage a project with Git and GitHub.

---

**Author:** Farrukh Akram