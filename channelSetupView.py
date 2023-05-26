import discord

from raffleSystem import RaffleSystem


class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self):
        placeholder = "Choose category to use for raffles"
        super().__init__(placeholder=placeholder, channel_types=[discord.ChannelType.category])

    async def callback(self, interaction: discord.Interaction):
        await self.view.handle_channels(interaction, self.values)


class ChannelSetupView(discord.ui.View):
    def __init__(self, raffle_system: RaffleSystem):
        super().__init__()
        self.raffle_system = raffle_system
        self.add_item(ChannelSelect())

    async def handle_channels(self, interaction: discord.Interaction, selected_channel):
        if not selected_channel:
            return

        self.raffle_system.category = selected_channel[0].id
        self.raffle_system.save_settings()
        await interaction.response.send_message(f"Channel was updated to {selected_channel[0].name}!", ephemeral=True,
                                                delete_after=10)
        self.stop()
