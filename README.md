# COVID-19 Statistics Bot for Discord

This is a bot for discord that supports a variety of commands that provide statistics on the coronavirus pandemic 2020. This bot sources its data from a free-to-use API that retrieves data from Johns Hopkins CSSE.

- [COVID-19 API](https://covid19api.com/) built by Kyle Redelinghuys. Documentation can be found [here](https://documenter.getpostman.com/view/10808728/SzS8rjbc#27454960-ea1c-4b91-a0b6-0468bb4e6712).

- [COVID-19 Data Repository](https://github.com/CSSEGISandData/COVID-19) by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University; Aggregate data sources also provided via link.

## How to use

```
1. Assuming you are registered with Discord, visit the developer portal and select "New Application."
2. Give the application a name, and select "Create."
3. Navigate to the menu on the left-hand-side and select "Bot" and follow up with "Add Bot" and "Yes, do it."
4. Feel free to give your new bot a name (defaults to application name) and picture. [Optional]
5. Copy the token generated by Discord from the Build-A-Bot menu to your clipboard.
6. Paste token from clipboard into main.py of the source code on line:44.
7. Navigate to the menu on the left-hand-side and select "OAuth2."
8. Checkbox the "bot" option for SCOPES menu and copy the generated link.
9. Enter link into browser and invite to server.
   - You must have the "Manage Server" permission on the desired server in order for it to appear in the invite menu.
```

## Bot TL:DR

### Commands

- To get global COVID-19 statistics:
  - *>covid*
- To get supported countries and their country codes (generates .txt file):
  - *>countries*
- To get statistics on a specific country by name (eg. Japan):
  - *>cname japan*
- To get statistics on a specific country by country code (eg. Japan):
  - *>ccode JP*
- To get source links:
  - *>csource*
- To see all available commands:
  - *>help*
- To see help with specific command:
  - *>help <name of command>*

### Things to note

- Commands are separated into what discords calls "Cogs." Essentially just groupings of similar commands.
- If at anytime you wish to add something or modify a Cog without having to restart the bot; simply reload the specific bot (extention filename without .py).
  - For Example:
    - ">unload covidstat"
    - *make your desired changes to the code*
    - ">load covidstat"
- The commands *>cname* and *>ccode* are locked behind *>countries* upon every load to ensure the most updated list of supported countries are generated.
- I believe the API caches its data daily but could not find a consistent time in which it does so:
  - So all COVID-19 related commands generate data from the day before which is still relatively accurate.
- API generates "0" for recoveries for the United States, so the bot will output as such although wrong.

###### README date Dec. 30, 2020
###### This bot was built by [Russell Zheng](https://github.com/shoehang)

