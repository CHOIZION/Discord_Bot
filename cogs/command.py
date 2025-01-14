import discord
from discord.ext import commands

class CommandList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='command')
    async def show_commands(self, ctx):
        """모든 명령어를 정리하여 출력합니다."""
        embed = discord.Embed(title="📜 명령어 목록", color=0x3498db)
        embed.set_footer(text="디스코드 봇 도움말")

        for cog_name, cog in self.bot.cogs.items():
            if cog.get_commands():
                command_list = [f"`!{command.name}`: {command.help}" for command in cog.get_commands()]
                embed.add_field(name=f"**{cog_name}**", value="\n".join(command_list), inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandList(bot))
