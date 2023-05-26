from datetime import datetime, timezone

import discord
import json

from raffle import Raffle


class RaffleSystem:
    def __init__(self):
        # a dictionary of raffles, with unique id as key, and the Raffle class object as the value
        self.raffles = {}
        # a dictionary with user roles as the key, and the amount of tickets to be given to a user of that role as value
        self.role_ticket_weights = {}
        self.category = None
        self.client = None

    def set_client(self, client):
        self.client = client

    async def check_raffles(self):
        current_time = datetime.now(timezone.utc)
        # exit if raffles are empty
        if not self.raffles.keys():
            return

        raffles_to_end = []
        for raffle_id in self.raffles.keys():
            raffle = self.raffles[raffle_id]
            end_time = raffle.end_time
            if end_time < current_time:
                raffles_to_end.append(raffle_id)

        for raffle_id in raffles_to_end:
            await self.end_raffle(raffle_id)

    # start a raffle. schedules a call to end raffle
    def start_raffle(self, raffle_id, time, interaction: discord.Interaction):
        # the system itself gives a handle to self to the raffle
        self.raffles[raffle_id] = Raffle(self, time, interaction)

    # winner is selected, message is sent mentioning the user who won
    async def end_raffle(self, raffle_id):
        # pick a winner and send a message announcing the winner
        raffle = self.raffles[raffle_id]
        winner = raffle.pick_winner()
        vod = raffle.get_vod(winner.id)
        notes = raffle.get_notes(winner.id)
        interaction = raffle.interaction
        # winner can be returned as none if no entries, so check first
        if winner:
            await interaction.followup.send(f"Winner is {winner.mention}!")
        else:
            await interaction.followup.send("No one entered the raffle :(")
            self.raffles.pop(raffle_id)
            return
        # create a private text channel with the winner and the owners
        if self.category:
            guild = interaction.guild
            category = self.client.get_channel(self.category)
            # permissions must be overwritten after making the channel, or they will not inherit perms from category
            channel = await guild.create_text_channel(f"{winner.name}'s raffle!", category=category)
            await channel.set_permissions(winner, read_messages=True, send_messages=True)
            await channel.send(f"Congratulations {winner.mention} on winning the raffle!")
            await channel.send(f"Vod link: {vod}")
            await channel.send(f"{winner.name} has added the following notes:")

            embed = discord.Embed(
                title="Notes",
                description=notes,
                colour=discord.Colour.blurple()
            )

            await channel.send(embed=embed)

        self.raffles.pop(raffle_id)

    def enter_raffle(self, raffle_id, user, vod, notes):
        raffle = self.raffles[raffle_id]
        raffle.add_user(user)
        raffle.add_vod(user, vod)
        raffle.add_notes(user, notes)

    def save_settings(self):
        fp = open('settings.txt', 'w')
        settings = {'weights': self.role_ticket_weights, 'channel': self.category}
        fp.write(json.dumps(settings))
        fp.close()

    def load_settings(self):
        fp = open('settings.txt', 'r')
        settings = json.load(fp)
        if 'weights' in settings:
            self.role_ticket_weights = settings['weights']
        if 'channel' in settings:
            self.category = settings['channel']
        fp.close()
