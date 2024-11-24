from groq import Groq

client = Groq(api_key="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")
completion = client.chat.completions.create(
    model="llama-3.2-11b-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjTA81d-wVUh3nKiMAj2BUqJeqG9_k0N30uA&s"
                    }
                }
            ]
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

print(completion.choices[0].message)
