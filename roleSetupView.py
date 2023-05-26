import discord
from discord.ui import TextInput

from roleSetupModal import RoleSetupModal


class ConfirmButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.blurple, label="Confirm")

    async def callback(self, interaction: discord.Interaction):
        await self.view.handle_roles(interaction, self.view.values)


class RoleSelect(discord.ui.RoleSelect):
    def __init__(self):
        placeholder = "Choose roles to modify tickets given"
        min_values = 0
        max_values = 25
        super().__init__(placeholder=placeholder, min_values=min_values, max_values=max_values)

    async def callback(self, interaction: discord.Interaction):
        self.view.values = self.values
        await interaction.response.defer()


class RoleSetupView(discord.ui.View):
    def __init__(self, raffle_system):
        super().__init__()
        self.raffle_system = raffle_system
        self.values = []
        self.add_item(RoleSelect())
        self.add_item(ConfirmButton())

    async def handle_roles(self, interaction: discord.Interaction, selected_roles):
        if not selected_roles:
            return

        setup_modal = RoleSetupModal(self.raffle_system, selected_roles)
        await interaction.response.send_modal(setup_modal)
        await interaction.delete_original_response()
        self.stop()
