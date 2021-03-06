import requests
from datetime import date, timedelta

# discord dependencies
import discord
from discord.ext import commands

# open-source: https://api.covid19api.com/
# base uri: https://api.covid19api.com/
# functions pertaining to getting COVID-19 statistics
class CovidStatExtension(commands.Cog):
	
	# constructor
	def __init__(self, bot):
		self.bot = bot
		self.basepath = "https://api.covid19api.com/"
		self.countrycodes = {}
		self.countrystring = ''
		self.countryfile = False

	# >covid command
	# provide global covid statistics
	# params: client context
	# path uri: /summary
	@commands.command()
	async def covid(self, context):
		"""Provides global Covid-19 statistics. Updated daily according to source.\n
		Parameters: None | Example: '>covid'"""
		uri = "summary"
		response = requests.get(self.basepath + uri)
		response_json = response.json()
		summary = response_json['Global']
		rstring = 'New Confirmed Cases: {:,}\nTotal Confirmed Cases: {:,}\nNew Deaths: {:,}\nTotal Deaths: {:,}\nNew Recoveries: {:,}\nTotal Recoveries: {:,}'
		await context.send(rstring.format(summary['NewConfirmed'], summary['TotalConfirmed'], summary['NewDeaths'], summary['TotalDeaths'], summary['NewRecovered'], summary['TotalRecovered']))

	# >countries command
	# provide txt file listing countires w available covid statistics
	# params: client context
	# path uri: /countries
	@commands.command()
	async def countries(self, context):
		"""Provides a text file containing country codes and their respective names.\n
		Parameters: None | Needed for the >cname and >ccode commands."""
		# prevent lengthy api call if coutnry codes is already populated in previous command call
		if not self.countrycodes:
			uri = "countries"
			response = requests.get(self.basepath + uri)
			response_json = response.json()
			for entry in response_json:
				self.countrycodes[entry['ISO2']] = entry['Slug']
			self.countrycodes = dict(sorted(self.countrycodes.items(), key = lambda entry:entry[1]))
		# prevent lengthy string formatting if already done in previous command call
		if not self.countrystring:
			self.countrystring += '{countrycode} | {countryname}\n'
			for entry in self.countrycodes:
				self.countrystring += F'\u2022 {entry} | {self.countrycodes[entry]}\n'
		# prevent writing another file if already done in previous command call
		if not self.countryfile:
			with open('Countries.txt', 'w') as f:
				f.write(self.countrystring)
			self.countryfile = True
		with open('Countries.txt', 'rb') as f:
			await context.send('Covid-19 statistics available for the following countries:\n', file = discord.File(f, 'Countries.txt'))

	# >cname <countryname>
	# provide covid stat on specific country given its name
	# params: client context, name of country
	# status type: confirmed, deaths, or recovered
	@commands.command()
	async def cname(self, context, *, countryname):
		"""Provides Covid-19 statistics for a specific country. Country names must match results of '>countries' command.\n
		Parameters: Country Name | Examples: '>cname china' or '>cname japan'"""
		if not self.countrycodes:
			await context.send('Please run the \'>countries\' command first.')
			return
		if countryname in self.countrycodes.values():
			yesterday = date.today() - timedelta(1)
			confirmed = self.get_confirmed_cases(countryname)
			deaths = self.get_deaths(countryname)
			recovered = self.get_recovered(countryname)
			rstring = 'Covid-19 statistics for {} as of {}:\n\n{:,} Confirmed Cases\n{:,} Deaths\n{:,} Recoveries'
			await context.send(rstring.format(countryname.upper(), yesterday, confirmed, deaths, recovered))
		else:
			await context.send('Could not recognize Country Name. Refer to the list generated by \'>countries\' command.')

	# >ccode <countrycode>
	# provide covid stat on specific country given its ISO2 code
	# params: client context, country code
	# status type: confirmed, deaths, or recovered
	@commands.command()
	async def ccode(self, context, *, countrycode):
		"""Provides Covid-19 statistics for a specific country. Country names must match results of '>countries' command.\n
		Parameters: Country Name | Examples: '>ccode CN' or '>ccode JP'"""
		if not self.countrycodes:
			await context.send('Please run the \'>countries\' command first.')
			return
		if countrycode in self.countrycodes:
			countryname = self.countrycodes[countrycode]
			yesterday = date.today() - timedelta(1)
			confirmed = self.get_confirmed_cases(countryname)
			deaths = self.get_deaths(countryname)
			recovered = self.get_recovered(countryname)
			rstring = 'Covid-19 statistics for {} as of {}:\n\n{:,} Confirmed Cases\n{:,} Deaths\n{:,} Recoveries'
			await context.send(rstring.format(countryname.upper(), yesterday, confirmed, deaths, recovered))
		else:
			await context.send('Could not recognize Country Code. Refer to the list generated.')

	# >csource
	# sources cited
	# params: client context
	@commands.command()
	async def csource(self, context):
		"""Provides embedded message citing sources used to create this bot."""
		embed = discord.Embed(
			title = 'Source',
			colour = discord.Colour.dark_teal()
		)
		apisource_string = 'Bot\'s COVID-19 API is built by Kyle Redelinghuys available at:\nhttps://covid19api.com/'
		datasource_string = 'Sourced from Johns Hopkins University CSSE\nMost up-to-date statistics can be found here via desktop/mobile link:\nhttps://github.com/CSSEGISandData/COVID-19'
		embed.add_field(name = 'API', value = apisource_string, inline = False)
		embed.add_field(name = 'Data Source', value = datasource_string, inline = False)
		await context.send(embed = embed)

	# params: country name/code
	# return: string
	# path uri: total/country/<countryname>/status/confirmed?<from date>&<to date>
	def get_confirmed_cases(self, countryname):
		yesterday = date.today() - timedelta(1)
		uri = F'total/country/{countryname}/status/confirmed?from={yesterday}T00:00:00Z&to={date.today()}T00:00:00Z'
		response = requests.get(self.basepath + uri)
		response_json = response.json()
		return response_json[0]['Cases']

	# params: country name/code
	# return: string
	# path uri: total/country/<countryname>/status/deaths?<from date>&<to date>
	def get_deaths(self, countryname):
		yesterday = date.today() - timedelta(1)
		uri = F'total/country/{countryname}/status/deaths?from={yesterday}T00:00:00Z&to={date.today()}T00:00:00Z'
		response = requests.get(self.basepath + uri)
		response_json = response.json()
		return response_json[0]['Cases']

	# params: country name/code
	# return: string
	# path uri: total/country/<countryname>/status/recovered>?<from date>&<to date>
	def get_recovered(self, countryname):
		yesterday = date.today() - timedelta(1)
		uri = F'total/country/{countryname}/status/recovered?from={yesterday}T00:00:00Z&to={date.today()}T00:00:00Z'
		response = requests.get(self.basepath + uri)
		response_json = response.json()
		return response_json[0]['Cases']

# register this cog with bot when loaded
def setup(bot):
	try:
		bot.add_cog(CovidStatExtension(bot))
		print('Successfully loaded covidstat extension.')
	except Exception as e:
		sys.exit()