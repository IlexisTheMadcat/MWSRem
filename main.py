# Lib
from pickle import Unpickler
from os import getcwd
from os.path import join, exists
from random import choice

# Site
from discord import __version__
from discord.activity import Activity
from discord.enums import ActivityType, Status
from discord.permissions import Permissions
from discord.utils import oauth_url

# Local
from utils.classes import Bot

print("...\n\n#-------------------------------#")

print("Attempting to open bot_config.pkl...", end="\r")

if not exists(join(getcwd(), "Serialized", "bot_config.pkl")):
    open(join(getcwd(), "Serialized", "bot_config.pkl"), "wb").close()

with open(join(getcwd(), "Serialized", "bot_config.pkl"), "rb") as f:
    try:
        config_data = Unpickler(f).load()
    except Exception as e:
        print(f'[Using defaults] Unpickling error: {e}{" "*30}')
        debug_mode = False
        auto_pull = True
        tz = "UTC"
        prefix = "cdr:"
    else:
        try:
            debug_mode = config_data["debug_mode"]
            auto_pull = config_data["auto_pull"]
            tz = config_data["tz"]
            prefix = config_data["prefix"]
            print(f"Loaded bot_config.pkl{' '*20}")
        except KeyError:
            print(f'[Using defaults] bot_config.pkl file improperly formatted.{" "*35}')  # print excess spaces to fully overwrite the '\r' above
            debug_mode = False  # Print exceptions to stdout. Some errors will not be printed for some reason, such as NameError outside of commands.
            auto_pull = True  # Auto pulls github updates every minute and reloads all loaded cogs.
            tz = "UTC"  # Triggers python to get real UTC time for Rems's status.
            prefix = "cdr:"

print("#-------------------------------#\n")
loading_choices = [  # because why not # TODO: Change loading_choices to suit Rem rather than Ram
    "Loading Random Access Memory...",
    '"It appears nothing here will fit except women\'s clothes."',
    "Booting up the creative but stubbern mind...",
    "Waking up the older sister...",
    "Charging RAM...",
    '"I was only waiting to help Roswaal-sama put on fresh clothes."',
    '"By the way, do you have plans after this?"',
    '"I see you really are studying, sir."',
    '"No, thank you, sir."',
    '"What can you do by learning anything now?!"',
    '"I\'m not interested."',
    "Requesting the one they call Ram..."
]

print("#-------------------------------#")
print(f"{choice(loading_choices)}")
print(f"#-------------------------------#\n")

INIT_EXTENSIONS = [
    "admin",
    "background",
    "directory_management",
    "events",
    "help",
]

# Extension "repl" must be loaded manually
# as it is not automatically available
# because it is not often needed.

bot = Bot(
    description="Create a new channel system for your server.",
    owner_ids=[331551368789622784, 125435062127820800],
    activity=Activity(type=ActivityType.watching, name=f"Just woke up."),
    status=Status.idle,
    # Configurable via :>bot
    command_prefix=prefix,
    debug_mode=debug_mode,
    auto_pull=auto_pull,
    tz=tz
)

bot.remove_command("help")

print("#-------------------------------#")
print(f"Running in: {bot.cwd}")
print(f"Discord API version: {__version__}")

print("#-------------------------------#\n")


@bot.event
async def on_ready():
    app_info = await bot.application_info()
    bot.owner = bot.get_user(app_info.owner.id)

    permissions = Permissions()
    permissions.update(
        manage_channels=True,
        manage_roles=True,
        manage_messages=True,
        read_messages=True,
        send_messages=True,
        attach_files=True
    )

    print(f"\n"
          f"#-------------------------------#\n"
          f"| Loading initial cogs...\n"
          f"#-------------------------------#")

    for cog in INIT_EXTENSIONS:
        print(f"| Loading initial cog {cog}")
        try:
            bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            print(f"| Failed to load extension {cog}\n|   {type(e).__name__}: {e}", end="\n")

    print(f"#-------------------------------#\n"
          f"| Successfully logged in.\n"
          f"#-------------------------------#\n"
          f"| Usern:     {bot.user}\n"
          f"| User ID:   {bot.user.id}\n"
          f"| Owner:     {bot.owner}\n"
          f"| Guilds:    {len(bot.guilds)}\n"
          f"| Users:     {len(list(bot.get_all_members()))}\n"
          f"| OAuth URL: {oauth_url(app_info.id, permissions)}\n"
          f"# ------------------------------#")


if __name__ == "__main__":

    if not bot.auth["MWS_DBL_SUCCESS"]:
        if bot.auth["MWS_DBL_TOKEN"]:
            print("Last DBL login failed or unknown.")

    print("Logging in with token.")
    bot.run()
