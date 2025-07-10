import discord
import requests
import re

DJANGO_API_URL='http://127.0.0.1:8000/api/verify-link/'
#intialize bot
intents=discord.Intents.default()
intents.message_content=True
client=discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")
@client.event
async def on_message(message):
    if message.author==client.user:
        return
    print("Recieved message:",message.content)#debug
    if message.content.startswith('!verifylink'):
        match=re.match(r"!verifylink\s*(.*)",message.content)
        if not match or not match.group(1).strip():
            await message.channel.send("❗Usage :!verifylink <url> \nExample:!verifylink https://example.com")
            return 
        url=match.group(1).strip()
        try:
            #extracting url from command
            #parts=message.content.split('',1)
            #if len(parts)!=2 or not parts[1].strip():
            #    await message.channel.send("❗Usage :!verifylink <url> \nExample:!verifylink https://example.com")
            #    return
            #url=parts[1].strip()
            print("Verifying URL:",url)
            #send post request to our django api
            response=requests.post(DJANGO_API_URL,json={"url":url})
            if response.status_code==200:
                data=response.json()
                #formatting reply nicely
                reply=(
                  f"🔗**Original URL:**{data.get('Original_URL')}\n" 
                  f"🔗**Final URL:**{data.get('Final_URL')}\n"
                  f"🔐**Safety Verdict:**{data.get('Safety_Verdict')}\n"
                  f"📰**Title:**{data.get('Title')}\n"
                  f"📝**Description:**{data.get('Description')}\n"
                )
                await message.channel.send(reply)
            else:
                await message.channel.send("❌Failed to verify the link.Please try again.")
        except Exception as e:
            await message.channel.send(f"⚠️An error occurred:{str(e)}")
    #if message.content.startswith('!verifyimage'):
    #    FRONTEND_IMAGE_URL=""
    #   await message.channel.send(f"🖼️You can verify the image(S) here:{FRONTEND_IMAGE_URL}")
#run the bot
client.run(DISCORD_TOKEN)