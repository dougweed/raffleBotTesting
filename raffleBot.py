import discord

from channelSetupView import ChannelSetupView
from raffleStartModal import RaffleStartModal
from raffleSystem import RaffleSystem
from roleSetupView import RoleSetupView
from discord import app_commands
from discord.ext import commands, tasks
import json

raffleSystem = RaffleSystem()


class RaffleBot:

    def __init__(self, token):
        self.token = token
        self.raffleSystem = raffleSystem
        self.setup_complete = False

    def run(self):
        # best way I could find to end raffles at specified time. checks once a minute
        @tasks.loop(minutes=1)
        async def check_raffles_end():
            await self.raffleSystem.check_raffles()

        intents = discord.Intents.default()
        intents.members = True
        intents.auto_moderation = False
        intents.moderation = False
        intents.invites = False
        intents.guild_typing = False
        intents.emojis_and_stickers = False
        intents.voice_states = False
        intents.message_content = True

        bot = commands.Bot(intents=intents, command_prefix="!")
        raffleSystem.set_client(bot)

        # Event handler for initial startup of bot
        @bot.event
        async def on_ready():
            # Creates a command group for subcommands under /raffle
            raffle_group = RaffleGroup(name='raffle', description='Lets raffle!')
            bot.tree.add_command(raffle_group)

            # Syncs the command tree, updating server commands
            await bot.tree.sync()
            for guild in bot.guilds:
                guild_id = discord.Object(id=int(guild.id))
                await bot.tree.sync(guild=guild_id)

            check_raffles_end.start()

            self.raffleSystem.load_settings()

        bot.run(self.token)


class RaffleGroup(app_commands.Group):

    @app_commands.command(description="Start a raffle!")
    async def start(self, interaction: discord.Interaction):
        raffle_start_modal = RaffleStartModal(raffleSystem)
        await interaction.response.send_modal(raffle_start_modal)

    @app_commands.command(description="Setup role weights")
    async def roles(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return
        setup_view = RoleSetupView(raffleSystem)
        await interaction.response.send_message(view=setup_view, ephemeral=True)
        await setup_view.wait()

    @app_commands.command(description="Setup channel for winners")
    async def channel(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return
        setup_view = ChannelSetupView(raffleSystem)
        await interaction.response.send_message(view=setup_view, ephemeral=True)
        await setup_view.wait()
        await interaction.delete_original_response()
