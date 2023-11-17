from secret import data

import discord
from discord.ext import commands
from discord.ui import Button

intents = discord.Intents.all()
intents.messages = True  # 必要な権限を付与

client = commands.Bot(command_prefix="/", intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.command()
async def button(ctx):
    # ボタンの作成
    button = Button(label="Click me!", style=discord.ButtonStyle.blue)

    # ボタンがクリックされたときの処理を設定
    @button.callback
    async def on_button_click(button_ctx):
        await button_ctx.send(f"{button_ctx.author.mention} clicked the button!")

    # ボタンをメッセージに追加
    message = await ctx.send("Press the button:", components=[button])

    # ボタンが含まれたメッセージを待つ
    interaction = await client.wait_for("button_click", check=lambda i: i.component.label.startswith("Click"), timeout=30)

    # ボタンの処理が終わったらボタンを無効化
    await interaction.respond(content="Button clicked!", type=7, components=[])


client.run(data.TOKEN)
