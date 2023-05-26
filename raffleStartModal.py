import logging
from datetime import datetime

from raffleView import RaffleView
import discord
from discord import app_commands
from discord.ext import commands, tasks
import dateparser
import calendar


class RaffleStartModal(discord.ui.Modal, title="Start a Raffle"):
    def __init__(self, raffle_system):
        super().__init__()
        self.raffleSystem = raffle_system

    raffle_title = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Name of raffle",
        required=True,
        placeholder="Enter name of raffle"
    )

    raffle_description = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Description of raffle",
        required=True,
        placeholder="Enter description of raffle"
    )

    raffle_end_time = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Time and date of raffle end",
        required=True,
        placeholder="Enter a time and date in plain English"
    )


    async def on_submit(self, interaction: discord.Interaction):

        dateparser_settings = {'TO_TIMEZONE': 'EST', 'TIMEZONE': 'EST', 'RETURN_AS_TIMEZONE_AWARE': True}
        parsed_date = None
        formatted_time = None
        try:
            # date parser takes in user string and converts it to python datetime
            parsed_date = dateparser.parse(str(self.raffle_end_time), settings=dateparser_settings)
            dt = calendar.timegm(parsed_date.utctimetuple())

            formatted_time = f"<t:{dt}:f> ( <t:{dt}:R> )"

        # when this exception is raised, the modal calls on_error. the user can just try to resubmit a valid date
        except AttributeError as e:
            logging.error("Date parse error")

        # creates embed giving info on objective and end time of raffle
        embed = discord.Embed(
            title=self.raffle_title,
            description=self.raffle_description,
            colour=discord.Colour.blurple()
        )
        embed.add_field(name="Raffle end time: ", value=formatted_time)

        # send the embed containing description and raffle end time as a response to the start command
        await interaction.response.send_message(embed=embed)

        # use this interaction's unique id as a token for differentiating raffles
        unique_id = interaction.id

        # create the view for entering the raffle and send it under the embed created above
        raffle_view = RaffleView(unique_id, self.raffleSystem, parsed_date, interaction)
        await interaction.channel.send(view=raffle_view)

    async def on_error(self, interaction: discord.Interaction, error):
        logging.error("Modal Error")
