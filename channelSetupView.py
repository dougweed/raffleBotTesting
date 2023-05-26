import discord

from raffleSystem import RaffleSystem


class CategorySelect(discord.ui.ChannelSelect):
    def __init__(self):
        placeholder = "Choose category to use for raffles"
        super().__init__(placeholder=placeholder, channel_types=[discord.ChannelType.category])

    async def callback(self, interaction: discord.Interaction):
        await self.view.handle_category(interaction, self.values)


class ChannelSetupView(discord.ui.View):
    def __init__(self, raffle_system: RaffleSystem):
        super().__init__()
        self.raffle_system = raffle_system
        self.add_item(CategorySelect())

    async def handle_category(self, interaction: discord.Interaction, selected_category):
        if not selected_category:
            return

        self.raffle_system.category = selected_category[0].id
        self.raffle_system.save_settings()
        await interaction.response.send_message(f"Channel was updated to {selected_category[0].name}!", ephemeral=True,
                                                delete_after=10)
        self.stop()
