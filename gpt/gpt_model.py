from openai import AsyncOpenAI
import json

API_KEY = 'Your api key'

client = AsyncOpenAI(api_key=API_KEY)

async def create_request(prompt: str, history):
    if prompt == '':
        return ''
    history.append({"role": "user", "content": prompt})
    print(type(history))
    completion = await client.chat.completions.create(
        model="gpt-4o",
        messages=history
    )
    if completion.choices[0].message.content:
        history.append({"role": "user", "content": completion.choices[0].message.content})
    return history
