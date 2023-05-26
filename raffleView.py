import discord

from raffleJoinModal import RaffleJoinModal
from raffleSystem import RaffleSystem
from discord import app_commands
from discord.ext import commands, tasks


class RaffleView(discord.ui.View):
    def __init__(self, unique_id, raffle_system, time, interaction):
        super().__init__()
        # unique id to for this specific raffle
        self.unique_id = unique_id
        self.raffleSystem = raffle_system

        # add the raffle to raffle system on initialization
        self.raffleSystem.start_raffle(unique_id, time, interaction)

    # called when user clicks enter button under a raffle view ember
    @discord.ui.button(label="Enter", style=discord.ButtonStyle.blurple)
    async def enter(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        if not self.unique_id in self.raffleSystem.raffles:
            await interaction.response.send_message(f"This raffle has already ended.", ephemeral=True)
            return
        # check if user already entered raffle. send appropriate response and enter them if they are not already
        if user.id in self.raffleSystem.raffles[self.unique_id].users:
            await interaction.response.send_message(f"You have already joined the raffle, {interaction.user.mention}",
                                                    ephemeral=True)
        else:
            # self.raffleSystem.enter_raffle(self.unique_id, user)
            raffle_join_modal = RaffleJoinModal(self.raffleSystem, self.unique_id)
            await interaction.response.send_modal(raffle_join_modal)
