import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ui import Modal, TextInput
import subprocess
import os
import shutil
import sys
import json
import ast
import time
import datetime
import re
import pystyle
from os import system
from datetime import datetime
from pystyle import Colors, Colorate
from PIL import Image

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='/', intents=intents)
os.system("cls||clear")

TOKEN = ""
user_data_path = "database/user.json"
user_log = "database/log"
skin_list_path = "._SkinList.json"
main_script = "main.py"
limit_skin = 15
limit_skin = limit_skin * 6
package = 2 # 1 Default 2 Accout name
modtool = 2 # 1 Killain 2 Blackz

if modtool == 1:
	tasks_folder = "Tasks" 
elif modtool == 2:
	tasks_folder = ".ลงรูปม็อด"
else:
	 exit()



guild_id = 1247202329082593401
target_channel_id = 1261970535403884617
channel_id = 1248880826482032681
channel_url = f"https://discord.com/channels/{guild_id}/{target_channel_id}"

def load_user_data():
	file_path = user_data_path
	if os.path.exists(file_path):
		with open(file_path, "r", encoding="utf-8") as f:
			return json.load(f)
	else:
		return {}

def save_user_data(data):
	file_path = user_data_path
	with open(file_path, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=4)

def update_user_usage(user_id):
	data = load_user_data()

	if str(user_id) in data:
		data[str(user_id)] = str(int(data[str(user_id)]) + 1) 
	else:
		data[str(user_id)] = "1"
	save_user_data(data)

def create_skin(skin_id: int):
	if not os.path.exists(tasks_folder):
		os.makedirs(tasks_folder)
	img = Image.new('RGB', (1, 1))
	img_path = os.path.join(tasks_folder, f"{skin_id}.jpg")
	img.save(img_path)
	return img_path

def read_skin_list(file_path: str):
    with open(file_path, 'r', encoding="utf-8") as f:
        content = f.read().strip()
        skin_ids_list = ast.literal_eval(content)  
    return skin_ids_list
    
skin_ids_list = read_skin_list(skin_list_path)


def kill_img(folder_path):
	if not os.path.exists(folder_path):
		return
	for filename in os.listdir(folder_path):
		file_path = os.path.join(folder_path, filename)
		try:
			if os.path.isfile(file_path):
				os.remove(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			pass
	
	pass

kill_img(tasks_folder)

def run_mod_tool():
	try:
		if modtool == 1:
			subprocess.run(["python", "AoV_Mod-Tool.py"], input="n", text=True, check=True)
		elif modtool == 2:
			subprocess.run(["python", ".Z-BLACK_MODIFY.py"], input="n", text=True, check=True)
	except subprocess.CalledProcessError as e:
		print(f"Error : {e}")

def get_filtered_keys(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        numbers = re.findall(r'(\d+):', content)

        filtered_numbers = [num for num in numbers if not num.endswith('00')]

        return filtered_numbers
    else:
        return []

@client.slash_command(name="usage", description="❤ . ดูจำนวนครั้งที่คุณใช้บอท")
async def usage(interaction: nextcord.Interaction):
    await interaction.response.defer(ephemeral=True)

    data = load_user_data()
    usage_count = int(data.get(str(interaction.user.id), 0))

    embed = nextcord.Embed(
        title="🔥 เช็คจำนวนครั้งที่ใช้บอท",
        description=f"**คุณใช้บอทไปทั้งหมด {usage_count} ครั้ง**",
        color=0x20ff00
    )

    if interaction.user.avatar:
        url = interaction.user.avatar.url
    else:
        url = ""
    embed.set_thumbnail(url=url)
    await interaction.followup.send(embed=embed, ephemeral=True)

@client.slash_command(name="mod", description="❤・Bot free Mod Skins")
async def mod(interaction: nextcord.Interaction):
	try:
		modal = SkinIDModal()
		await interaction.response.send_modal(modal)
	except:
		return

class SkinIDModal(Modal):
	def __init__(self):
		super().__init__(
			title="💖 . ทำมอดฟรี",
			timeout=None
		)
		self.add_item(
			TextInput(
				label="🌹 . ใส่สกินไอดี ไม่เกิน 15 สกิน",
				placeholder="xxxxx/xxxxx/xxxxx/...",
				max_length=limit_skin,
				min_length=5,
				required=True
			)
		)

	async def callback(self, interaction: nextcord.Interaction):
		skin_ids = self.children[0].value.strip()  
		skin_id_list = [
			int(sid.strip()) for sid in skin_ids.split('/') if sid.strip().isdigit()
		]
		
		if not skin_id_list:
			embed =  nextcord.Embed(
				title="❌ เกิดข้อผิดพลาด",
				description="Skin ID ไม่ถูกต้อง โปรดลองอีกครั้ง",
				color=0xff0000
			)
			if interaction.user.avatar:
				url = interaction.user.avatar.url
			else:
				url = ""

			embed.set_thumbnail(url=url)
			if not interaction.response.is_done():
				await interaction.response.send_message(embed=embed, ephemeral=True)
			else:
				await interaction.followup.send(embed=embed, ephemeral=True)

			kill_img(tasks_folder)
			return

		await interaction.response.defer(ephemeral=False)
		
		img_paths = []
		
		for skin_id in skin_id_list:
			if str(skin_id) in skin_ids_list:
				img_path = create_skin(skin_id)
				img_paths.append(img_path)
			else:
				embed =  nextcord.Embed(
					title="❌ เกิดข้อผิดพลาด",
					description=f"Skin ID:{skin_id} ไม่ถูกต้อง โปรดลองอีกครั้ง",
					color=0xff0000
				)
				if interaction.user.avatar:
					url = interaction.user.avatar.url
				else:
					url = ""

				embed.set_thumbnail(url=url)
				if not interaction.response.is_done():
					await interaction.response.send_message(embed=embed, ephemeral=True)
				else:
					await interaction.followup.send(embed=embed, ephemeral=True)


				kill_img(tasks_folder)
				return
				
		name_prefix_dict = {}
		for filename in os.listdir(tasks_folder):
		    if filename.lower().endswith(('.jpg')):
		        prefix = filename[:3]
		        if prefix not in name_prefix_dict:
		            name_prefix_dict[prefix] = filename
		        else:
		            filepath = os.path.join(tasks_folder, filename)
		            os.remove(filepath)
			
		count = len([f for f in os.listdir(tasks_folder)])		
		if modtool == 1:
			if count == 1:
				zip_filename = f"{skin_id_list[0]}.zip"
			elif count < 1:
				zip_filename = f"Mod_{count}_Skin(s).zip"
			else:
				return
		elif modtool == 2:
			zip_filename = f"Mod_{count}_Skin_BlackZ_1.57.1.5.zip"
			
		if package == 1:
			zip_packagename = zip_filename
		elif package == 2:
			zip_packagename = "@" + interaction.user.name + " .zip"
				
		skin_ids_str = ", ".join(map(str, skin_id_list))
		msg = nextcord.Embed(
			title="꒰PARKY MOD SKIN꒱"
		)
		
		msg.add_field(
			name="**ผู้ใช้งาน**", 
			value=f"> ||**<@{interaction.user.id}>**||", 
			inline=False
		)
		msg.add_field(
			name="**สกินไอดี**", 
			value=f"> **{skin_ids_str}**", 
			inline=False
		)
		msg.add_field(
			name="**ชื่อไฟล์**", 
			value=f"> **{zip_packagename}**", 
			inline=False
		)
		msg.add_field(
			name="**รับมอดที่ช่อง**", 
			value=f"> **{channel_url}**", 
			inline=False
		)
		
		msg.color = 0xD4EEF1
		msg.set_image(
			url="https://cdn.discordapp.com/attachments/1109158081335672934/1314545118413590578/573b76b94e8c71cec32b98a17560914a.gif?ex=6754290b&is=6752d78b&hm=6256ae444189c912cece1d1627fa850164b950ba3c395a948329ba9c38269e7b&"
		)
		if interaction.user.avatar:
			msg.set_thumbnail(
				url=interaction.user.avatar.url
			)
		else:
			msg.set_thumbnail(
				url="https://cdn.discordapp.com/attachments/1109158081335672934/1302308428433330226/0.png?ex=6727a4bd&is=6726533d&hm=21e7fbe438f797ec175e37f5ef22067e2fd6badaa6c5389364f249c813c249e6&"
			)
		msg.set_footer(
			text="© 2025 PARKY All rights reserved",
			icon_url="https://media.discordapp.net/attachments/1294936352789364827/1298282655242260531/6d2409bc093703b7c4c4291e4b84eca4.jpg?ex=6718ff71&is=6717adf1&hm=284a16f5b7a9e837b2e0f1e3783dbec9510eea0d81411293205a705320f7e67f&"
		)
		await interaction.followup.send(
			embed=msg,
			ephemeral=False
		)
	
		if zip_packagename:
			if os.path.exists(zip_packagename):
				os.remove(zip_packagename)
		else:
			pass
		await run_mod_and_send_file(interaction, skin_id_list, img_paths, zip_packagename, zip_filename)

async def run_mod_and_send_file(interaction: Interaction, skin_id_list: list, img_paths: list, zip_packagename: str, zip_default: str):
	start_time = time.time()
	run_mod_tool()
	elapsed_time = time.time() - start_time

	if package == 2:
		os.rename(zip_default, zip_packagename)

	zip_file_path = os.path.join(zip_packagename)
	if os.path.exists(zip_file_path):
		target_channel = client.get_channel(target_channel_id)
		channel = client.get_channel(channel_id)

		if target_channel:
			try:
				embed = nextcord.Embed(title="PARKY ( MOD SKIN FREE )")
				embed.add_field(name="**ผู้ใช้งาน**", value=f"> **<@{interaction.user.id}>**")
				embed.add_field(name="**ชื่อไฟล์**", value=f"> **{zip_file_path}**")
				embed.add_field(name="**เวลาที่ใช้**", value=f"> **{elapsed_time:.2f} วินาที**")
				embed.color = 0x20ff00
				embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else "https://cdn.discordapp.com/attachments/1109158081335672934/1302308428433330226/0.png")
				embed.set_footer(text="© 2025 PARKY All rights reserved")
				embed.set_image(url="https://media.discordapp.net/attachments/1109158081335672934/1312708000649052271/standard_1.gif?ex=674d7a18&is=674c2898&hm=bf9d536e2e16a54253a521b2e422f3aba6be5f2b96d2d121d7e44b782649c036&")

				await target_channel.send(embed=embed)
				await target_channel.send(file=nextcord.File(zip_file_path))

				last_message = await channel.history(limit=1).flatten()
				if last_message:
					await last_message[0].delete()

			except Exception as e:
				await interaction.followup.send(f"เกิดข้อผิดพลาด: {str(e)}", ephemeral=True)

		os.remove(zip_file_path)
		kill_img(tasks_folder)

		try:
			subprocess.run(["python", main_script], check=True)
		except subprocess.CalledProcessError as e:
			print(f"Error : {e}")

# Event เมื่อบอทพร้อม
@client.event
async def on_ready():
	await client.sync_application_commands()
	await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.streaming, url="https://www.twitch.tv/ph4rqy2x", name="Ready to Modify💖 | บอททำมอดสกินฟรี By Parky",))
	system("cls||clear")
	print(Colorate.Horizontal(Colors.red_to_blue, f'''[>] Running with python : 3.9.7
[>] Login with          : {client.user} <{client.user.name}>
[>] Version             : 1.0      

██████╗  █████╗ ██████╗ ██╗  ██╗██╗   ██╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝╚██╗ ██╔╝
██████╔╝███████║██████╔╝█████╔╝  ╚████╔╝ 
██╔═══╝ ██╔══██║██╔══██╗██╔═██╗   ╚██╔╝  
██║     ██║  ██║██║  ██║██║  ██╗   ██║   
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                         

								  [ STATUS : Bot is running smoothly!      ]

								  [ PING   : {client.latency * 1000:.2f}ms                      ]

								  [ DC     : https://discord.gg/HnFa8V7pFS ]
	'''))

@client.event
async def on_message(message):
	if message.channel.id == channel_id and not message.author.bot:
		await message.delete()

		
if __name__ == "__main__":
	client.run(TOKEN)