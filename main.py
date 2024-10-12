import os
import random
import time
import discord
import pyfiglet
from discord.ext import commands
from colorama import Fore, Style

os.system("pip install discord.py==1.7.3")
os.system("pip install pyfiglet")

class colors:
    def banner(txt):
        print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{txt}{Fore.RESET}{Style.NORMAL}")

    def error(txt):
        print(f"{Fore.RED}[{random.choice(['-', '!'])}]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

    def success(txt):
        print(f"{Fore.GREEN}[+]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

    def warning(txt):
        print(f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

# Print banner
banner = pyfiglet.figlet_format("Slinder Cloner")
colors.banner(banner)
colors.warning("\x1B[3mhttps://discord.gg/cyb\x1B[0m\n")

# Enter token
while True:
    token = input("Enter your token: ")
    if token:
        break
    else:
        colors.error("Token cannot be empty. Please try again.")

# Get guild IDs
while True:
    try:
        target_guild_id = int(input("Enter the guild ID which you want to copy: "))
        paste_guild_id = int(input("Enter the guild ID where you want to paste it: "))
        if target_guild_id == paste_guild_id:
            colors.error("Source and target guild IDs must be different. Please try again.")
        else:
            break
    except ValueError:
        colors.error("Invalid ID. Please enter valid numeric IDs.")

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents, self_bot=True)
client.remove_command('help')

@client.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')

    # Display new banner with name and link
    new_banner = pyfiglet.figlet_format("SLinder Cloner")
    colors.banner(new_banner)
    colors.warning("\x1B[3mhttps://discord.gg/cyb\x1B[0m\n")

    source_guild = client.get_guild(target_guild_id)
    if not source_guild:
        colors.error(f"Error | Source guild (ID: {target_guild_id}) not found!")
        return
    
    target_guild = client.get_guild(paste_guild_id)
    if not target_guild:
        colors.error(f"Error | Target guild (ID: {paste_guild_id}) not found!")
        return
    
    await show_options(source_guild, target_guild)

async def show_options(source_guild, target_guild):
    while True:
        # Show options for copying
        colors.warning("Choose what to copy:")
        print("\033[38;2;255;0;205m╔══════════════════════════════╗\033[0m")
        print("\033[38;2;255;0;180m║   \033[37m[1] Copy Everything   \033[38;2;255;0;180m║\033[0m")
        print("\033[38;2;255;0;155m║   \033[37m[2] Copy Roles       \033[38;2;255;0;155m║\033[0m")
        print("\033[38;2;255;0;130m║   \033[37m[3] Copy Channels    \033[38;2;255;0;130m║\033[0m")
        print("\033[38;2;255;0;105m║   \033[37m[4] Copy Emojis      \033[38;2;255;0;105m║\033[0m")
        print("\033[38;2;255;0;100m╚══════════════════════════════╝\033[0m")
        
        choice = input("Enter your choice (1/2/3/4) or 'q' to quit: ")

        if choice == '1':
            await copy_roles(source_guild, target_guild)
            await copy_channels(source_guild, target_guild)
            await copy_emojis(source_guild, target_guild)
            colors.success("Finished copying everything! (Roles, Channels, Emojis)")
            print("You can end the process by pressing 'q'.")
            break
        elif choice == '2':
            await copy_roles(source_guild, target_guild)
            colors.success("Finished copying roles!")
        elif choice == '3':
            await copy_channels(source_guild, target_guild)
            colors.success("Finished copying channels!")
        elif choice == '4':
            await copy_emojis(source_guild, target_guild)
            colors.success("Finished copying emojis!")
        elif choice.lower() == 'q':
            print("Exiting...")
            await client.logout()
            break
        else:
            colors.error("Invalid choice!")

async def copy_roles(source_guild, target_guild):
    start_time = time.time()
    
    # Deleting roles in target guild
    for role in target_guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                colors.success(f"Done | Deleted Role {role.name}")
            except Exception as e:
                colors.error(f"Couldn't delete role {role.name}: {str(e)}")

    elapsed_time = time.time() - start_time
    print(f"Finished deleting roles in: {elapsed_time:.2f} seconds\n")

    # Copying roles from source to target
    for role in source_guild.roles[::-1]:
        if role.name != "@everyone":
            try:
                new_role = await target_guild.create_role(
                    name=role.name,
                    color=role.color,
                    permissions=role.permissions,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                colors.success(f"Done | Created Role {new_role.name}")
            except Exception as e:
                colors.error(f"Couldn't create role {role.name}: {str(e)}")

async def copy_channels(source_guild, target_guild):
    start_time = time.time()
    
    # Deleting channels in target guild
    for c in target_guild.channels:
        try:
            await c.delete()
            colors.success(f"Done | Deleted Channel {c.name}")
        except Exception as e:
            colors.error(f"Couldn't delete channel {c.name}: {str(e)}")

    elapsed_time = time.time() - start_time
    print(f"Finished deleting channels in: {elapsed_time:.2f} seconds\n")

    # Copying channels from source to target
    for cate in source_guild.categories:
        x = await target_guild.create_category(cate.name)
        for chann in cate.channels:
            try:
                if isinstance(chann, discord.VoiceChannel):
                    await x.create_voice_channel(chann.name)
                elif isinstance(chann, discord.TextChannel):
                    await x.create_text_channel(
                        chann.name,
                        overwrites=chann.overwrites,
                        topic=chann.topic,
                        slowmode_delay=chann.slowmode_delay,
                        nsfw=chann.nsfw,
                        position=chann.position
                    )
                colors.success(f"Done | Created Channel {chann.name}")
            except Exception as e:
                colors.error(f"Couldn't create channel {chann.name}: {str(e)}")

async def copy_emojis(source_guild, target_guild):
    start_time = time.time()
    
    # Deleting emojis in target guild
    for emoji in target_guild.emojis:
        try:
            await emoji.delete()
            colors.success(f"Done | Deleted Emoji {emoji.name}")
        except Exception as e:
            colors.error(f"Couldn't delete emoji {emoji.name}: {str(e)}")

    elapsed_time = time.time() - start_time
    print(f"Finished deleting emojis in: {elapsed_time:.2f} seconds\n")

    # Copying emojis from source to target
    for emoji in source_guild.emojis:
        try:
            # Fetch the emoji image
            image_data = await emoji.url.read()  # Use the correct way to fetch the emoji image
            await target_guild.create_custom_emoji(name=emoji.name, image=image_data)
            colors.success(f"Done | Created Emoji {emoji.name}")
        except Exception as e:
            colors.error(f"Couldn't create emoji {emoji.name}: {str(e)}")

client.run(token, bot=False)
