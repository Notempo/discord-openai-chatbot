import openai
import discord
openai.api_key = "insert openai api key here"

class MyBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
    async def on_message(self, message):
        if message.author == self.user:
            return
        elif message.content.startswith('insert character name here'):
            txt = open("log.txt", "r")
            log = txt.read()
            txt.close()
            txt = open("quota.txt", "r")
            quota = float(txt.read())
            txt.close()
            words = message.content.split()
            string = ""
            for i in range(1,len(words)):
                string += " " + words[i]
            generate = openai.Completion.create(
                model="text-davinci-003",
                prompt=log+string,
                temperature=0.5,
                max_tokens=60,
                top_p=0.3,
                frequency_penalty=0.5,
                presence_penalty=0
            )
            words2 = generate["choices"][0]["text"].split()
            string2 = ""
            for i in range(1,len(words2)):
                string2 += " " + words2[i]
            txt = open("log.txt", "w")
            txt.write(log+string+"\\"+"nCross:"+string2+"\\"+"nYou:")
            txt.close()
            txt = open("quota.txt", "w")
            txt.write(str(round(round(float(quota),3)+round(generate["usage"]["total_tokens"]/1000*2,3),3)))
            txt.close()
            await message.reply(string2, mention_author=False)
        elif message.content.startswith('!cost') or message.content.startswith('!quota') or message.content.startswith('!money'):
            txt = open("quota.txt", "r")
            quota = float(txt.read())
            txt.close()
            await message.reply("`"+str(round(quota))+"¢ / 1800¢`", mention_author=False)

bot = MyBot()
with open('token.txt') as file:
    token = file.readline()
bot.run(token)