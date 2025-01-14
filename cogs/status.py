import discord
from discord.ext import commands
import psutil  # 시스템 상태 확인을 위한 라이브러리
import os
import platform
import time

class SystemStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()  # 봇 가동 시작 시간 기록

    @commands.command(name='status')
    async def system_status(self, ctx):
        """현재 시스템 상태를 출력합니다."""
        # CPU, 메모리, 디스크 상태 확인
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        uptime = time.time() - self.start_time

        # 가동 시간 계산
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours}시간 {minutes}분 {seconds}초"

        # 시스템 정보
        system_info = platform.uname()
        system_name = f"{system_info.system} {system_info.release}"
        cpu_cores = psutil.cpu_count(logical=True)

        # 임베드 메시지 생성
        embed = discord.Embed(title="📊 시스템 상태", color=0x3498db)
        embed.add_field(name="🖥️ 시스템 정보", value=system_name, inline=False)
        embed.add_field(name="💻 CPU 사용량", value=f"{cpu_percent}%", inline=True)
        embed.add_field(name="🧠 메모리 사용량", value=f"{memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB", inline=True)
        embed.add_field(name="💾 디스크 사용량", value=f"{disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB", inline=True)
        embed.add_field(name="⚙️ CPU 코어 수", value=f"{cpu_cores}", inline=True)
        embed.add_field(name="⏱️ 봇 가동 시간", value=uptime_str, inline=False)
        embed.set_footer(text="디스코드 봇 시스템 상태")

        await ctx.send(embed=embed)

async def setup(bot):
    """시스템 상태 Cog 로드"""
    await bot.add_cog(SystemStatus(bot))
