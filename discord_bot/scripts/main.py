import discord
from discord.ext import commands
import requests
from discord import SyncWebhook

import com
from secret import data

intents = discord.Intents.all()
intents.messages = True

# 接続に必要なオブジェクトを生成
client = commands.Bot(command_prefix="/", intents=intents)

AuthB = "Bot " + data.TOKEN

headers = {
    "Authorization": AuthB
}  

def returnNormalUrl(channelId):
  return "https://discordapp.com/api/channels/" + str(channelId) + "/messages"

# 任意のチャンネルで挨拶する非同期関数を定義
async def start():
    channel = client.get_channel(data.bot_log_channel)
    if channel is None or not isinstance(channel, discord.TextChannel):
      return print("指定されたチャンネルが見つかりませんでした。")
    else:
      # 起動したらターミナルにログイン通知が表示される
      print("ログインしました")
      await channel.send(f'{client.user.name}が起動しました')



# 起動時に動作する処理
@client.event
async def on_ready():
    await start()
    await client.change_presence(activity=discord.Game("奴隷"))

@client.event
async def on_interaction(interaction):
    try:
      if interaction.type == discord.InteractionType.component:
        # ここでボタンの処理を実装
        custom_id = interaction.data['custom_id']
        user = interaction.user
        if custom_id[0] != "!":
          role = interaction.guild.get_role(int(custom_id))
          channel = client.get_channel(data.bot_log_channel)
          if role:
            await user.add_roles(role)
            await channel.send(str(user) + "に" + str(role.name) + "を付与しました")
            await interaction.response.send_message("")
        else:
          custom_id = custom_id.removeprefix("!")
          role = interaction.guild.get_role(int(custom_id))
          channel = client.get_channel(data.bot_log_channel)
          if role:
            await user.remove_roles(role)
            await channel.send(str(user) + "から" + str(role.name) + "を外しました")
            await interaction.response.send_message("")
    except Exception as e:
        print("ボタンが押されたよ")

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
      return
    if message.content == '/role':
      # ロールリストを取得
      role_list = message.guild.roles
      await message.channel.send(role_list)
    if message.content == '/show_role':
      await message.channel.send("付与したいロールを選択してください")
      data.role_list = []
      # ロールリストを取得
      role_list = message.guild.roles
      for role in role_list:
        role_name = role.name
        if role_name[0] == "@" or role_name[0] == "!":
          continue
        role_id = role.id
        data.role_list.append([role_name, role.id])

      role_lists = []
      role_list = []
      i = 0
      for role_info in data.role_list:
        if i == 5:
          role_lists.append(role_list)
          role_list = []
          i = 0
        role_list.append(role_info)
        i+=1
      if (len(data.role_list)+4) //5 != len(role_lists):
          role_lists.append(role_list)
      
      normal_url = returnNormalUrl(message.channel.id)

      #付与ボタンの作成
      for t in range(len(role_lists)):
        components = com.components(len(role_lists[t]), role_lists[t])
        json_payload = {
          "components": [
                {
                    "type": 1,
                    "components": components

                }
            ]
        }
        r = requests.post(normal_url, headers=headers, json=json_payload)

      await message.channel.send("外したいロールを選択してください")
      #削除ボタンの作成
      for t in range(len(role_lists)):
        components = com.del_components(len(role_lists[t]), role_lists[t])
        json_payload = {
          "components": [
                {
                    "type": 1,
                    "components": components

                }
            ]
        }
        r = requests.post(normal_url, headers=headers, json=json_payload)

    if message.content == '/test':
      await message.channel.send("付与したいロールを選択してください")

client.run(data.TOKEN)