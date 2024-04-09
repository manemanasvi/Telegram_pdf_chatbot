import openai
from config import config

openai.api_key = "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"


def generate_response(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
        ],
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extract the summary from the response
    summary = response.choices[0].message['content'].strip()

    return summary
