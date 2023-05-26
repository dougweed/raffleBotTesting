import logging

import discord


class RoleSetupModal(discord.ui.Modal, title="Role Setup"):
    def __init__(self, raffle_system, roles):
        super().__init__()
        self.raffleSystem = raffle_system
        self.inputs = []
        for role in roles:
            name = role.name
            text_input = discord.ui.TextInput(
                style=discord.TextStyle.short,
                label=role.name,
                required=True,
                placeholder=role.name
            )
            self.add_item(text_input)
            self.inputs.append((role.id, text_input))

    async def on_submit(self, interaction: discord.Interaction):
        for input in self.inputs:
            self.raffleSystem.role_ticket_weights[input[0]] = int(input[1].value)
        self.raffleSystem.save_settings()
        await interaction.response.send_message("Roles were updated", ephemeral=True, delete_after=10)

    async def on_error(self, interaction: discord.Interaction, error):
        logging.error("Modal Error")
