import logging

import discord


class RaffleJoinModal(discord.ui.Modal, title="Join the raffle!"):
    def __init__(self, raffle_system, unique_id):
        super().__init__()
        self.raffleSystem = raffle_system
        self.id = unique_id

    vod = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Please submit a link to a VOD to review",
        required=True,
        placeholder="vod link"
    )

    notes = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Noted",
        required=False,
        placeholder=""
    )


    async def on_submit(self, interaction: discord.Interaction):

        # send the embed containing description and raffle end time as a response to the start command
        await interaction.response.send_message(f"You have joined the raffle, {interaction.user.mention}!",
                                                ephemeral=True)

        self.raffleSystem.enter_raffle(self.id, interaction.user, self.vod)

    async def on_error(self, interaction: discord.Interaction, error):
        logging.error("Modal Error")