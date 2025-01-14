import discord
from discord.ext import commands
import json
import os
from datetime import datetime

DATA_DIR = './data'
EVENTS_FILE = os.path.join(DATA_DIR, 'events.json')

# 데이터 파일 초기화
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(EVENTS_FILE):
    with open(EVENTS_FILE, 'w') as f:
        json.dump({}, f)

class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='event_add')
    async def add_event(self, ctx, date: str, *, content: str):
        """기념일이나 이벤트를 추가합니다. 날짜 형식: YYYY-MM-DD"""
        try:
            # 날짜 유효성 확인
            event_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            await ctx.send("잘못된 날짜 형식입니다! 형식: YYYY-MM-DD")
            return

        # 이벤트 추가
        with open(EVENTS_FILE, 'r') as f:
            events = json.load(f)

        if date not in events:
            events[date] = []

        events[date].append(content)

        with open(EVENTS_FILE, 'w') as f:
            json.dump(events, f, indent=4)

        await ctx.send(f"이벤트가 추가되었습니다: {date} - {content}")

    @commands.command(name='event_list')
    async def list_events(self, ctx):
        """저장된 이벤트 목록을 표시합니다."""
        with open(EVENTS_FILE, 'r') as f:
            events = json.load(f)

        if not events:
            await ctx.send("저장된 이벤트가 없습니다.")
            return

        embed = discord.Embed(title="📅 이벤트 목록", color=0x3498db)
        for date, contents in sorted(events.items()):
            for content in contents:
                embed.add_field(name=date, value=content, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='event_remove')
    async def remove_event(self, ctx, date: str):
        """특정 날짜의 이벤트를 삭제합니다. 날짜 형식: YYYY-MM-DD"""
        with open(EVENTS_FILE, 'r') as f:
            events = json.load(f)

        if date not in events:
            await ctx.send(f"{date}에 해당하는 이벤트가 없습니다.")
            return

        del events[date]

        with open(EVENTS_FILE, 'w') as f:
            json.dump(events, f, indent=4)

        await ctx.send(f"{date}에 저장된 이벤트가 삭제되었습니다.")

async def setup(bot):
    """캘린더 Cog 로드"""
    await bot.add_cog(Calendar(bot))
