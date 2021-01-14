import discord
from discord.ext import commands
import random
import kdrama_scraper

client = commands.Bot(command_prefix = '/')

@client.event
async def on_ready():
    print('Hey there -Bot')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (member_name, member_discriminator) == (user.name, user.discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command(aliases=['kdrama'])
async def kbot(ctx, *, drama):
    if drama == "suggest":
        synopsis, rating, members, img, title = kdrama_scraper.getSuggest()
    else:
        synopsis, rating, members, img, title = kdrama_scraper.getstuff(drama)
    # await ctx.send(synopsis)
    # await ctx.send(rating)
    # await ctx.send(members)
    members = ", ".join(members)

    embed = discord.Embed(
        title = title,
        colour = discord.Colour.blue()
    )

    
    embed.add_field(name = 'Synopsis', value = synopsis, inline=False)
    embed.add_field(name = 'Ratings', value = rating, inline=False)
    embed.add_field(name = 'Cast', value = members, inline=False)
    embed.set_image(url = img)
    await ctx.send(embed = embed)

client.run('')
