import discord
from discord.ext import commands
import random

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fortunes = [
            "오늘은 새로운 시작에 좋은 날입니다. 용기를 내어 도전해보세요!",
            "조심스럽게 행동하면 큰 성과를 얻을 수 있습니다.",
            "인내심을 가지고 꾸준히 노력하면 원하는 결과를 얻을 수 있습니다.",
            "오늘은 휴식이 필요할 수 있습니다. 무리하지 마세요.",
            "주변 사람들과의 소통이 중요한 날입니다.",
            "예상치 못한 기회가 찾아올 수 있으니 준비하세요.",
            "건강에 유의하고 충분한 휴식을 취하세요.",
            "창의적인 아이디어가 떠오를 수 있는 날입니다.",
            "금전운이 좋지 않을 수 있으니 신중하게 행동하세요.",
            "운동이나 취미 활동으로 스트레스를 해소해보세요."
        ]

    @commands.command(name='today')
    async def today_fortune(self, ctx):
        """오늘의 운세를 알려줍니다."""
        fortune = random.choice(self.fortunes)
        embed = discord.Embed(title="🎲 오늘의 운세 🎲", description=fortune, color=0xFFD700)
        await ctx.send(embed=embed)

async def setup(bot):
    """비동기 setup 함수"""
    await bot.add_cog(Lottery(bot))
