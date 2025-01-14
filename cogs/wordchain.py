import discord
from discord.ext import commands

class WordChain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_active = False
        self.words_used = []  # 사용된 단어
        self.current_last_char = None  # 마지막 글자

    @commands.command(name='start_game')
    async def start_game(self, ctx):
        """끝말잇기를 시작합니다."""
        if self.game_active:
            await ctx.send("이미 끝말잇기 게임이 진행 중입니다!")
            return

        self.game_active = True
        self.words_used = []
        self.current_last_char = None
        await ctx.send("끝말잇기 게임을 시작합니다! 단어를 입력하세요.")

    @commands.command(name='end_game')
    async def end_game(self, ctx):
        """끝말잇기를 종료합니다."""
        if not self.game_active:
            await ctx.send("진행 중인 게임이 없습니다!")
            return

        self.game_active = False
        self.words_used = []
        self.current_last_char = None
        await ctx.send("끝말잇기 게임이 종료되었습니다.")

    @commands.command(name='word')
    async def play_word(self, ctx, *, word: str):
        """끝말잇기에 단어를 제출합니다."""
        if not self.game_active:
            await ctx.send("끝말잇기 게임이 시작되지 않았습니다. `!start_game`으로 시작하세요!")
            return

        word = word.strip().lower()

        # 단어 유효성 검사
        if word in self.words_used:
            await ctx.send(f"'{word}'는 이미 사용된 단어입니다. 다른 단어를 입력하세요.")
            return

        if self.current_last_char and not word.startswith(self.current_last_char):
            await ctx.send(f"단어는 '{self.current_last_char}'로 시작해야 합니다!")
            return

        # 단어 추가 및 다음 차례 설정
        self.words_used.append(word)
        self.current_last_char = word[-1]
        await ctx.send(f"'{word}'를 입력하셨습니다. 다음 단어는 '{self.current_last_char}'로 시작해야 합니다!")

async def setup(bot):
    await bot.add_cog(WordChain(bot))
