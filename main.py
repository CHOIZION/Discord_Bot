import discord
from discord.ext import commands
import os

# 환경 변수 로드
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# 봇의 접두사 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user}로 로그인합니다!')

# Cog 로드 비동기 함수
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"로드된 익스텐션: {filename}")
            except Exception as e:
                print(f"로드 실패한 익스텐션 {filename}: {e}")

# 봇 실행
async def main():
    async with bot:
        await load_cogs()  # Cog 로드
        await bot.start(TOKEN)

# 이벤트 루프 실행
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
