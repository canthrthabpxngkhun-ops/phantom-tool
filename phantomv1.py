import os
import discord
from discord.ext import commands
from discord import app_commands
import requests
import datetime
import asyncio

TOKEN = "your_discord_bot_token_here"
WEATHER_API_KEY = "your_openweathermap_api_key_here"


# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


# ---------- BOT READY ----------
@bot.event
async def on_ready():
    print(f'Bot online as {bot.user}')


# ---------- คนเข้า ----------
@bot.event
async def on_member_join(member):
    text = f"Welcome to the EGL Phantom, {member.mention}!"
    
    try:
        await member.send(text)
    except discord.Forbidden:
        print(f"ส่ง DM ให้ {member} ไม่ได้ (ผู้ใช้ปิด DM)")

# ---------- คนออก ----------
@bot.event
async def on_member_remove(member):
    text = f"Goodbye, {member.mention}. We hope to see you again!"
    embed = discord.Embed(title="EGL Phantom", description="Welcome to the EGL Phantom Discord server! Please read the rules and enjoy your stay.", color=0x00ff00)
    
    
    try:
        await member.send(text)
    except discord.Forbidden:
        print(f"ส่ง DM ให้ {member} ไม่ได้ (ผู้ใช้ปิด DM)")

# ---------- ส่งข้อความ ----------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'who':
        await message.channel.send('Hi I am a robot   ' +  message.author.name)

    elif message.content == 'phantom':
        await message.channel.send(
            'sawaddeekub  ' + message.author.name
        )

    await bot.process_commands(message)


# ---------- PREFIX COMMAND ----------
@bot.command()
async def hi(ctx):
    await ctx.send(f"Hello {ctx.author.name}")
@bot.command()
async def ping(ctx, arg: str = None):
    if arg is None:
        await ctx.send("❗ ใช้แบบนี้: `!ping hello`")
    else:
        await ctx.send(arg)

    
# ---------- SLASH COMMAND ----------
@bot.tree.command(name="run", description="Run bot discord")
async def run(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🚀 Bot Status",
        description="🟢 **Bot online and fully operational**",
        color=discord.Color.green(),
    )
    
    embed.add_field(
        name="User",
        value=interaction.user.mention,
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)
    

# weather prefix command
@bot.command()
async def weather(ctx, *, city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=th"
    res = requests.get(url)

    if res.status_code != 200:
        await ctx.send("❌ ไม่พบเมืองนี้")
        return

    data = res.json()

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    desc = data["weather"][0]["description"]
    city_name = data["name"]

    embed = discord.Embed(
        title=f"🌤 สภาพอากาศ {city_name}",
        color=discord.Color.blue()
    )
    embed.add_field(name="อุณหภูมิ", value=f"{temp}°C", inline=True)
    embed.add_field(name="รู้สึกเหมือน", value=f"{feels}°C", inline=True)
    embed.add_field(name="ความชื้น", value=f"{humidity}%", inline=True)
    embed.add_field(name="สภาพอากาศ", value=desc, inline=False)

    await ctx.send(embed=embed)


# countdown to new year command
@bot.command()
async def newyear(ctx):
    import datetime, asyncio

    now = datetime.datetime.now()
    target = datetime.datetime(now.year + 1, 1, 1, 0, 0, 0)

    embed = discord.Embed(
        title="🎆 Countdown to New Year",
        color=discord.Color.gold()
    )

    msg = await ctx.send(content="@everyone 🎆 เริ่มนับถอยหลังสู่ปีใหม่แล้ว!", embed=embed)

    while True:
        now = datetime.datetime.now()
        diff = target - now
        total = int(diff.total_seconds())

        if total <= 0:
            embed.title = "🎉 HAPPY NEW YEAR!"
            embed.description = "🎊 สุขสันต์วันปีใหม่แล้ว!"
            embed.color = discord.Color.green()
            await msg.edit(content="@everyone 🎊 HAPPY NEW YEAR 2026 !!!", embed=embed)
            break

        days = total // 86400
        hours = (total % 86400) // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60

        embed.description = (
            f"🗓 {days} วัน\n"
            f"⏰ {hours} ชั่วโมง\n"
            f"🕒 {minutes} นาที\n"
            f"⏱ {seconds} วินาที"
        )

        try:
            await msg.edit(embed=embed)
        except:
            pass

        # ปรับเวลาการ refresh
        if total > 3600:
            await asyncio.sleep(60)
        elif total > 60:
            await asyncio.sleep(10)
        else:
            await asyncio.sleep(1)


# ---------- RUN ----------
bot.run(TOKEN)
