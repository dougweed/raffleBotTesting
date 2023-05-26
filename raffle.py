import random

import discord


class Raffle:
    def __init__(self, system, end_time, interaction: discord.Interaction):
        # a raffle will be a dictionary, with unique users as the key, and number of tickets as the value
        self.raffle = {}
        # a pointer to the owner of this raffle (the RaffleSystem
        self.raffleSystem = system
        self.end_time = end_time
        # ties user's unique id to a user object
        self.users = {}
        self.vods = {}
        self.notes = {}
        self.interaction = interaction

    def add_user(self, user):
        user_id = user.id
        self.users[user_id] = user
        tickets = 1
        for role in user.roles:
            if role.id in self.raffleSystem.role_ticket_weights:
                tickets = max(tickets, self.raffleSystem.role_ticket_weights[role.id])
        self.raffle[user_id] = tickets

    def add_vod(self, user, link: str):
        self.vods[user.id] = link

    def add_notes(self, user, notes):
        self.notes[user.id] = notes

    def get_vod(self, user_id):
        return self.vods[user_id]

    def get_notes(self, user_id):
        return self.notes[user_id]

    # returns winner as discord member object
    def pick_winner(self):
        # no one entered our raffle :(
        if not self.raffle.keys():
            return None
        raffle_list = []
        for user, tickets in self.raffle.items():
            user_entries = [user] * tickets
            raffle_list.extend(user_entries)
        winner_id = random.choice(raffle_list)
        winner = self.users[winner_id]
        return winner
