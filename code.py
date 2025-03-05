import discord
import os
import requests

from dotenv import load_dotenv
load_dotenv()
print(discord.__version__)

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

def get_gemini_response(user_message):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"

    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": gemini_api_key
    }
    data = {
        "contents": [{"parts": [{"text": user_message}]}]
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    result = response.json()

  
    print("Gemini API response:", result)

    
    if 'candidates' in result and result['candidates']:
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        return "Sorry, I couldn't process that."

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    if message.author == client.user:
        return

    user_message = message.content
    response = get_gemini_response(user_message)
    await message.channel.send(response)

client.run(os.getenv('TOKEN'))
