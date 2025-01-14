import discord
from discord.ext import commands
import json
import os

DATA_DIR = './data'
JOURNEY_FILE = os.path.join(DATA_DIR, 'journey.json')

# 데이터 디렉토리 및 파일 초기화
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(JOURNEY_FILE):
    with open(JOURNEY_FILE, 'w') as f:
        json.dump({}, f)

class Journey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_journey = None  # 현재 진행 중인 기록
        self.temp_data = []  # 기록 데이터를 임시로 저장

    @commands.command(name='start')
    async def start_journey(self, ctx, *, journey_name: str):
        """기록을 시작합니다."""
        if self.current_journey:
            await ctx.send(f"이미 '{self.current_journey}' 기록이 진행 중입니다. 종료 후 다시 시작하세요.")
            return

        self.current_journey = journey_name
        self.temp_data = []
        await ctx.send(f"'{journey_name}' 기록을 시작합니다. 이제 메시지와 이미지를 저장합니다.")

    @commands.command(name='end')
    async def end_journey(self, ctx, *, journey_name: str):
        """기록을 종료하고 데이터를 저장합니다."""
        if not self.current_journey or self.current_journey != journey_name:
            await ctx.send("기록이 진행 중이 아니거나 잘못된 이름입니다.")
            return

        # 데이터 저장
        with open(JOURNEY_FILE, 'r') as f:
            data = json.load(f)

        if journey_name not in data:
            data[journey_name] = []

        data[journey_name].extend(self.temp_data)

        with open(JOURNEY_FILE, 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"'{journey_name}' 기록을 저장했습니다.")
        self.current_journey = None
        self.temp_data = []

    @commands.command(name='find')
    async def find_journey(self, ctx, *, journey_name: str):
        """특정 기록을 조회합니다."""
        with open(JOURNEY_FILE, 'r') as f:
            data = json.load(f)

        if journey_name not in data or not data[journey_name]:
            await ctx.send(f"'{journey_name}'에 대한 기록이 없습니다.")
            return

        await ctx.send(f"'{journey_name}' 기록을 조회합니다:")

        for entry in data[journey_name]:
            if 'text' in entry:
                await ctx.send(entry['text'])
            if 'image' in entry:
                await ctx.send(entry['image'])

    @commands.command(name='delete')
    async def remove_journey(self, ctx, *, journey_name: str):
        """특정 기록을 삭제합니다."""
        with open(JOURNEY_FILE, 'r') as f:
            data = json.load(f)

        if journey_name not in data:
            await ctx.send(f"'{journey_name}'에 대한 기록이 없습니다.")
            return

        del data[journey_name]

        with open(JOURNEY_FILE, 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"'{journey_name}' 기록이 삭제되었습니다.")

    @commands.Cog.listener()
    async def on_message(self, message):
        """텍스트와 이미지를 저장."""
        if not self.current_journey or message.author.bot:
            return

        # 명령어 필터링
        if message.content.startswith('!start') or message.content.startswith('!end'):
            return

        # 텍스트 저장
        if message.content:
            self.temp_data.append({'text': message.content})

        # 이미지 URL 저장
        if message.attachments:
            for attachment in message.attachments:
                if attachment.url:
                    self.temp_data.append({'image': attachment.url})

async def setup(bot):
    """비동기 setup 함수"""
    await bot.add_cog(Journey(bot))
