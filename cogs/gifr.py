from discord.ext import commands
import aiohttp
import discord
import asyncio
import os
from nltk.corpus import stopwords

GIPHY_API_KEY = "dc6zaTOxFJmzC"
DEFAULT_DIR = "./data/gifr"
DEFAULT_WORD_LIST = "wordList.csv"

STOP_WORDS = set(stopwords.words('english'))

class Gifr:
	"""General Commands"""
	def __init__(self, bot):
		self.bot = bot
		self.word_dict = {}

	@commands.command(pass_context=True)
	async def word(self, ctx):
		maxWord = await self.getMostCommonWord()

		await self.bot.send_message(ctx.message.channel, '`{0}` is the most common word, with {1} occurrences.'.format(maxWord[0], maxWord[1]))


	@commands.command(pass_context=True)
	async def saveList(self, ctx):
		await self.save_word_list()


	@commands.command(pass_context=True)
	async def clearList(self, ctx):
		fpath = os.path.join(DEFAULT_DIR, DEFAULT_WORD_LIST)
		with open(fpath, 'r+') as f:
			lines = f.readlines()
			f.seek(0)
			f.truncate()


	@commands.command(pass_context=True)
	async def gifw(self, ctx):
		maxWord = await self.getMostCommonWord()

		url = ("http://api.giphy.com/v1/gifs/random?&api_key={}&tag={}"
			   "".format(GIPHY_API_KEY, maxWord[0]))

		async with aiohttp.get(url) as r:
			result = await r.json()
			if r.status == 200:
				if result["data"]:
					await self.bot.say(result["data"]["url"])
				else:
					await self.bot.say("No results found.")
			else:
				await self.bot.say("Error contacting the API")


	async def on_message(self, message):
		"""Records all words within messages"""
		if message.author.id != self.bot.user.id and not message.content.startswith('.'):
			for word in message.content.split():
				word = word.lower()
				if word not in STOP_WORDS:
					if word in self.word_dict:
						self.word_dict[word] += 1
					else:
						self.word_dict[word] = 1

	async def getMostCommonWord(self):
		self.save_word_list()
		fpath = os.path.join(DEFAULT_DIR, DEFAULT_WORD_LIST)
		maxWord = ''
		maxNum = 0
		with open(fpath, 'r') as f:
			for line in f:
				word = line.split(',')[0]
				num = line.split(',')[1]

				if int(num) > maxNum:
					maxNum = int(num)
					maxWord = word

		return (maxWord, maxNum)

	async def save_word_list(self):
		fpath = os.path.join(DEFAULT_DIR, DEFAULT_WORD_LIST)
		with open(fpath, 'r+') as f:
			lines = f.readlines()
			f.seek(0)
			f.truncate()
			for line in lines:
				word = line.split(',')[0]
				num = line.split(',')[1]

				if word in self.word_dict:
					f.write('{0},{1}\n'.format(word, int(num) + self.word_dict[word]))
					del self.word_dict[word]
				else:
					f.write(line)

			for key in self.word_dict:
				f.write('{0},{1}\n'.format(key,self.word_dict[key]))

		self.word_dict = {}


def setup(bot):
	bot.add_cog(Gifr(bot))