#This bot is intended for use in the general channel of your guild(aka server)
import os
import seaborn as sns
import nest_asyncio #only use these two lines
nest_asyncio.apply() #if you're running the code in a jupyter notebook
                     #or if you get error: cannot close a running event loop
import discord
from datetime import datetime

TOKEN = {your token here}
GUILD = {your guild here}
import pandas as pd
curse_df = pd.read_csv('curse_words.txt', '\n')
curse_list = curse_df['Words'].values.tolist()
curse_set = set(curse_list)
import matplotlib.pyplot as plt
client = discord.Client()

class ExtraMemberData: #class to hold more data about a guild member
    
    #this data is only collected for messages sent while the bot is running
    def __init__(self):
        self.num_mentions = 0 #number of times a member has been mentioned - TRACKED
        self.curse_freq = 0 #fraction of words in a member's messages that are curse words - CALCULATED
        self.num_curses = 0 #number of times the member has said a curse word - TRACKED
        self.num_msgs = 0 #number of messages a member has sent - TRACKED
        self.num_words = 0 #number of words a member has sent - TRACKED
        self.num_chars = 0 #number of chars a member has sent - TRACKED
        #note: spaces are not included
        self.avg_word_length = 0 #average length of a word in a member's messages - CALCULATED
        self.punc_marks = 0 #number of non-alphanumeric chars a member has sent - TRACKED
        self.punc_freq = 0 #fraction of chars a member has sent that are not alphanumeric - CALCULATED
        self.avg_msg_length = 0 #average message length for a member (in chars) - CALCULATED
        self.attachments = 0 #number of attachments a member has sent - TRACKED

extraStuff = {} #{Member object: ExtraMemberData object}
memberList = [] #We need a list that is guaranteed to stay in the same order

async def send_info(member):
    calc_stats1(member)
    str0 = member.display_name + ':\n'
    str1 = 'has been mentioned ' + str(extraStuff[member].num_mentions) + ' times\n'
    str2 = 'has cursed ' + str(extraStuff[member].num_curses) + ' times\n'
    str3 = 'has sent ' + str(extraStuff[member].num_msgs) + ' messages\n'
    str4 = 'has sent ' + str(extraStuff[member].num_words) + ' words\n'
    str5 = 'has sent ' + str(extraStuff[member].num_chars) + ' chars\n'
    str6 = 'has sent ' + str(extraStuff[member].punc_marks) + ' punctuation marks\n'
    str7 = 'has sent ' + str(extraStuff[member].attachments) + ' attachments\n'
    str8 = 'has a curse frequency of ' + str(round(extraStuff[member].curse_freq, 4)) + '\n'
    str9 = 'has an avg msg length of ' + str(round(extraStuff[member].avg_msg_length, 4)) + ' chars\n'
    str10 = 'has an avg word length of ' + str(round(extraStuff[member].avg_word_length, 4)) + ' chars\n'
    str11 = 'has a punctuation frequency of ' + str(round(extraStuff[member].punc_freq, 4)) + '\n'
    info = str0 + str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9 + str10 + str11
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    for channel in guild.channels:
        if str(channel) == "general":
            await channel.send(info)

async def show_leaderboard(stat):
    calc_stats()
    leaderboard_str = ''
    if stat == 'mentions':
        leaderboard_str += 'Most Mentioned People:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_mentions, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_mentions) + '\n')
            i += 1
    elif stat == 'curses':
        leaderboard_str += 'Most Curse Words:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_curses, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_curses) + '\n')
            i += 1
    elif stat == 'messages':
        leaderboard_str += 'Most Messages:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_messages, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_messages) + '\n')
            i += 1
    elif stat == 'words':
        leaderboard_str += 'Most Words:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_words, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_words) + '\n')
            i += 1
    elif stat == 'chars':
        leaderboard_str += 'Most Chars:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_chars, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_chars) + '\n')
            i += 1
    elif stat == 'punctuation':
        leaderboard_str += 'Most Punctuation Marks:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].punc_marks, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].punc_marks) + '\n')
            i += 1
    elif stat == 'attachments':
        leaderboard_str += 'Most Attachments:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_attachments, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_attachments) + '\n')
            i += 1
    elif stat == 'curse frequency':
        leaderboard_str += 'Highest Curse Frequency:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].curse_freq, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(round(item[1].curse_freq, 3)) + '\n')
            i += 1
    elif stat == 'average message length':
        leaderboard_str += 'Longest Average Message Length (in chars):\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].avg_msg_length, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(round(item[1].avg_msg_length, 2)) + '\n')
            i += 1
    elif stat == 'average word length':
        leaderboard_str += 'Longest Average Word Length (in chars):\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].avg_word_length, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(round(item[1].avg_word_length, 2)) + '\n')
            i += 1
    elif stat == 'punctuation frequency':
        leaderboard_str += 'Highest Punctuation Frequency:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].punc_freq, reverse = True)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(round(item[1].punc_freq, 3)) + '\n')
            i += 1
    else:
        leaderboard_str += "Sorry, that wasn't a recognized statistic. Please review the readme for this bot"
    
    
    #send the leaderboard
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    for channel in guild.channels:
        if str(channel) == "general":
            await channel.send(leaderboard_str)
        
async def show_leaderboard_reverse(stat):
    calc_stats()
    leaderboard_str = ''
    if stat == 'mentions':
        leaderboard_str += 'Least Mentioned People:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_mentions, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_mentions) + '\n')
            i += 1
    elif stat == 'curses':
        leaderboard_str += 'Fewest Curse Words:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_curses, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_curses) + '\n')
            i += 1
    elif stat == 'messages':
        leaderboard_str += 'Fewest Messages:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_messages, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_messages) + '\n')
            i += 1
    elif stat == 'words':
        leaderboard_str += 'Fewest Words:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_words, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_words) + '\n')
            i += 1
    elif stat == 'chars':
        leaderboard_str += 'Fewest Chars:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_chars, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_chars) + '\n')
            i += 1
    elif stat == 'punctuation':
        leaderboard_str += 'Fewest Punctuation Marks:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].punc_marks, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].punc_marks) + '\n')
            i += 1
    elif stat == 'attachments':
        leaderboard_str += 'Fewest Attachments:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].num_attachments, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(item[1].num_attachments) + '\n')
            i += 1
    elif stat == 'curse frequency':
        leaderboard_str += 'Lowest Curse Frequency:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].curse_freq, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(round(item[1].curse_freq, 3)) + '\n')
            i += 1
    elif stat == 'average message length':
        leaderboard_str += 'Shortest Average Message Length (in chars):\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].avg_msg_length, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(round(item[1].avg_msg_length, 2)) + '\n')
            i += 1
    elif stat == 'average word length':
        leaderboard_str += 'Shortest Average Word Length (in chars):\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].avg_word_length, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(round(item[1].avg_word_length, 2)) + '\n')
            i += 1
    elif stat == 'punctuation frequency':
        leaderboard_str += 'Lowest Punctuation Frequency:\n'
        mentions = sorted(extraStuff.items(), key = lambda x: x[1].punc_freq, reverse = False)
        i = 1
        for item in mentions:
            if i > 10: #only show the top 10
                break
            leaderboard_str += (item[0].display_name + ": " + str(round(item[1].punc_freq, 3)) + '\n')
            i += 1
    else:
        leaderboard_str += "Sorry, that wasn't a recognized statistic. Please review the readme for this bot"
    
    
    #send the leaderboard
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    for channel in guild.channels:
        if str(channel) == "general":
            await channel.send(leaderboard_str)           
            
    
    
def calc_stats(): #calculates the stats that aren't explicitly tracked
    for member in memberList:
        if extraStuff[member].num_words > 0:
            extraStuff[member].curse_freq = extraStuff[member].num_curses / extraStuff[member].num_words
            extraStuff[member].avg_word_length = (extraStuff[member].num_chars - extraStuff[member].punc_marks) / extraStuff[member].num_words
        else:
            extraStuff[member].curse_freq = 0
            extraStuff[member].avg_word_length = 0
        if extraStuff[member].num_chars > 0:
            extraStuff[member].punc_freq = extraStuff[member].punc_marks / extraStuff[member].num_chars
        else:
            extraStuff[member].punc_freq = 0
        if extraStuff[member].num_msgs > 0:
            extraStuff[member].avg_msg_length = extraStuff[member].num_chars / extraStuff[member].num_msgs
        else:
            extraStuff[member].avg_msg_length = 0

def calc_stats1(mem): #calculates the stats that aren't explicitly tracked for only one member
    for member in memberList:
        if member.id == mem.id:
            if extraStuff[member].num_words > 0:
                extraStuff[member].curse_freq = extraStuff[member].num_curses / extraStuff[member].num_words
                extraStuff[member].avg_word_length = (extraStuff[member].num_chars - extraStuff[member].punc_marks) / extraStuff[member].num_words
            else:
                extraStuff[member].curse_freq = 0
                extraStuff[member].avg_word_length = 0
            if extraStuff[member].num_chars > 0:
                extraStuff[member].punc_freq = extraStuff[member].punc_marks / extraStuff[member].num_chars
            else:
                extraStuff[member].punc_freq = 0
            if extraStuff[member].num_msgs > 0:
                extraStuff[member].avg_msg_length = extraStuff[member].num_chars / extraStuff[member].num_msgs
            else:
                extraStuff[member].avg_msg_length = 0
    
async def send_heatmap():
    calc_stats()
    num_mentions = []
    curse_freq = []
    num_curses = []
    num_msgs = []
    num_words = []
    num_chars = []
    avg_word_length = []
    punc_marks = []
    punc_freq = []
    avg_msg_length = []
    attachments = []
    for member in memberList:
        if client.user.id != member.id:
            num_mentions.append(extraStuff[member].num_mentions)
            curse_freq.append(extraStuff[member].curse_freq)
            num_curses.append(extraStuff[member].num_curses)
            num_msgs.append(extraStuff[member].num_msgs)
            num_words.append(extraStuff[member].num_words)
            num_chars.append(extraStuff[member].num_chars)
            avg_word_length.append(extraStuff[member].avg_word_length)
            punc_marks.append(extraStuff[member].punc_marks)
            punc_freq.append(extraStuff[member].punc_freq)
            avg_msg_length.append(extraStuff[member].avg_msg_length)
            attachments.append(extraStuff[member].attachments)
        
    zl = list(zip(num_mentions, curse_freq, num_curses, num_msgs, num_words, num_chars, avg_word_length, punc_marks, punc_freq, avg_msg_length, attachments))
    df = pd.DataFrame(zl, columns = ['mentions', 'c_freq', 'curses', 'msgs', 'words', 'chars', 'avg WL', 'puncts', 'p_freq', 'avg ML', 'attchs'])
    s = sns.heatmap(df.corr(), vmin=-1, annot=True,)
    s.set_title('WL=word length, ML=msg length')
    figure = s.get_figure()    
    figure.savefig('heatmap.png', dpi=800)
    plt.show()
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    for channel in guild.channels:
        if str(channel) == "general":
            await channel.send(file=discord.File('heatmap.png'))

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    for member in guild.members:
        extraStuff.update({member : ExtraMemberData()})
        memberList.append(member)
            
@client.event
async def on_message(message):
    author = message.author
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    if client.user.id != author.id:
        extraStuff[author].num_msgs += 1
        extraStuff[author].attachments += len(message.attachments)
        for member in guild.members:
            if member.mentioned_in(message):
                extraStuff[member].num_mentions += 1
        word_list = message.content.split()
        for word in word_list:
            extraStuff[author].num_words += 1
            extraStuff[author].num_chars += len(word)
            if word.lower() in curse_set:
                extraStuff[author].num_curses += 1
            for char in word:
                if ((ord(char) > 32 and ord(char) < 48) or (ord(char) > 57 and ord(char) < 65)
                    or (ord(char) > 90 and ord(char) < 97) or (ord(char) > 122 and ord(char) < 127)):
                        extraStuff[author].punc_marks += 1
    if message.content.startswith('info'):
        for member in guild.members:
            if member.mentioned_in(message):
                await send_info(member)
    elif message.content == 'heatmap':   
        await send_heatmap()
    elif message.content.startswith('leaderboard '):
        stat = message.content[12:]
        await show_leaderboard(stat)
    elif message.content.startswith('reverse leaderboard '):
        stat = message.content[20:]
        await show_leaderboard_reverse(stat)


            

client.run(TOKEN)

