import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int):
        """최근 메시지 삭제"""
        if amount < 1:
            await ctx.send("1개 이상의 메시지를 삭제해야 합니다!")
            return

        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"{len(deleted)}개의 메시지를 삭제했습니다.", delete_after=5)

    @commands.command(name='shutdown')
    @commands.is_owner()
    async def shutdown_bot(self, ctx):
        """봇 종료"""
        await ctx.send("봇을 종료합니다.")
        await self.bot.close()

    @commands.command(name='create_channel')
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx, *, channel_name: str):
        """새 텍스트 채널 생성"""
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if existing_channel:
            await ctx.send(f"'{channel_name}' 채널이 이미 존재합니다.")
            return

        await guild.create_text_channel(channel_name)
        await ctx.send(f"'{channel_name}' 채널을 생성했습니다.")

    @commands.command(name='delete_channel')
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(self, ctx, *, channel_name: str):
        """텍스트 채널 삭제"""
        guild = ctx.guild
        channel = discord.utils.get(guild.channels, name=channel_name)
        if not channel:
            await ctx.send(f"'{channel_name}' 채널을 찾을 수 없습니다.")
            return

        await channel.delete()
        await ctx.send(f"'{channel_name}' 채널을 삭제했습니다.")

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, member: discord.Member, *, reason=None):
        """사용자 킥"""
        await member.kick(reason=reason)
        await ctx.send(f"{member} 님을 서버에서 킥했습니다. 사유: {reason}")

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx, member: discord.Member, *, reason=None):
        """사용자 밴"""
        await member.ban(reason=reason)
        await ctx.send(f"{member} 님을 서버에서 밴했습니다. 사유: {reason}")

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban_user(self, ctx, *, user: str):
        """사용자 밴 해제"""
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            if user == str(ban_entry.user):
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(f"{ban_entry.user} 님의 밴을 해제했습니다.")
                return

        await ctx.send(f"'{user}' 사용자를 찾을 수 없습니다.")

    @commands.command(name='server_info')
    async def server_info(self, ctx):
        """서버 정보 표시"""
        guild = ctx.guild
        embed = discord.Embed(title=f"{guild.name} 서버 정보", color=0x3498db)
        embed.add_field(name="서버 이름", value=guild.name, inline=False)
        embed.add_field(name="멤버 수", value=guild.member_count, inline=False)
        embed.add_field(name="생성일", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))
