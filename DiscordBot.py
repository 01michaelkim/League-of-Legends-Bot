import discord
from riotwatcher import LolWatcher, ApiError

key = 'RGAPI-23c99287-ed70-41cf-b87f-5dfef5fba2f1'
watcher = LolWatcher(key)

client = discord.Client()

def printStats(summonerName):
    summoner = watcher.summoner.by_name('na1', summonerName)
    stats = watcher.league.by_summoner('na1', summoner['id'])

    for i in range(len(stats)):
        if stats[i]['queueType'] == 'RANKED_FLEX_SR':
            del stats[i]
            break

    try:
        tier = stats[0]['tier']
    except IndexError as err:
        tier = 'unranked'

    try:
        rank = stats[0]['rank']
    except IndexError as err:
        rank = 'unranked'

    try:
        lp = stats[0]['leaguePoints']
    except IndexError as err:
        lp = 0

    try:
        wins = int(stats[0]['wins'])
    except IndexError as err:
        wins = 1

    try:
        losses = int(stats[0]['losses'])
    except IndexError as err:
        losses = 1

    winrate = int((wins / (wins + losses)) * 100)


    if (tier == 'unranked'):
        return (summonerName + " is currently " + str(tier) + ".")
    else:
        return (summonerName + " is currently ranked in " + str(tier) + " " + str (rank) +
            " with " + str(lp) + "LP and a " + str(winrate) + "% winrate")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    actualMessage = str(message.content.split(' ', 1)[1])
    try:
        if message.author == client.user:
            return

        if message.content.startswith('/check '):
            result = printStats(actualMessage)
            await message.channel.send(result)
    except ApiError as err:
        print("error alert!")