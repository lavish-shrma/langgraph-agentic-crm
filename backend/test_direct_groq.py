import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def test_model(model_name):
    print(f"\nTesting model: {model_name}")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hello",
                }
            ],
            model=model_name,
        )
        print(f"SUCCESS: {chat_completion.choices[0].message.content}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_model("llama-3.1-8b-instant")
    test_model("llama-3.3-70b-versatile")
    test_model("gemma2-9b-it") # The decommissioned one mentioned in docstring
