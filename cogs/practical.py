import discord
from discord.ext import commands, tasks
import json
import os
import asyncio

DATA_DIR = './data'
TODO_FILE = os.path.join(DATA_DIR, 'todos.json')
NOTE_FILE = os.path.join(DATA_DIR, 'notes.json')
REMINDER_FILE = os.path.join(DATA_DIR, 'reminders.json')

# 데이터 디렉토리 및 파일 초기화
for file in [TODO_FILE, NOTE_FILE, REMINDER_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f)

class Practical(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        """Cog가 로드될 때 알림 데이터를 불러옵니다."""
        await self.load_reminders()

    @commands.group()
    async def todo(self, ctx):
        """투두 리스트 관리 명령어"""
        if ctx.invoked_subcommand is None:
            await ctx.send('사용법: !todo add/list/remove [내용/번호]')

    @todo.command(name='add')
    async def todo_add(self, ctx, *, task: str):
        """투두 리스트에 할 일을 추가합니다."""
        with open(TODO_FILE, 'r') as f:
            todos = json.load(f)

        user_id = str(ctx.author.id)
        if user_id not in todos:
            todos[user_id] = []

        todos[user_id].append(task)

        with open(TODO_FILE, 'w') as f:
            json.dump(todos, f, indent=4)

        await ctx.send(f'할 일이 추가되었습니다! [{len(todos[user_id])}] {task}')

    @todo.command(name='list')
    async def todo_list(self, ctx):
        """투두 리스트를 표시합니다."""
        with open(TODO_FILE, 'r') as f:
            todos = json.load(f)

        user_id = str(ctx.author.id)
        if user_id not in todos or not todos[user_id]:
            await ctx.send('투두 리스트가 비어 있습니다.')
            return

        embed = discord.Embed(title=f"{ctx.author.name}님의 투두 리스트", color=0x00ff00)
        for idx, task in enumerate(todos[user_id], start=1):
            embed.add_field(name=f"{idx}.", value=task, inline=False)

        await ctx.send(embed=embed)

    @todo.command(name='remove')
    async def todo_remove(self, ctx, index: int):
        """투두 리스트에서 할 일을 제거합니다."""
        with open(TODO_FILE, 'r') as f:
            todos = json.load(f)

        user_id = str(ctx.author.id)
        if user_id not in todos or index < 1 or index > len(todos[user_id]):
            await ctx.send('유효한 번호를 입력해주세요.')
            return

        removed = todos[user_id].pop(index - 1)

        with open(TODO_FILE, 'w') as f:
            json.dump(todos, f, indent=4)

        await ctx.send(f'할 일이 제거되었습니다: {removed}')

    @commands.group()
    async def note(self, ctx):
        """메모 관리 명령어"""
        if ctx.invoked_subcommand is None:
            await ctx.send('사용법: !note add/list/remove [내용/번호]')

    @note.command(name='add')
    async def note_add(self, ctx, *, content: str):
        """메모를 추가합니다."""
        with open(NOTE_FILE, 'r') as f:
            notes = json.load(f)

        user_id = str(ctx.author.id)
        if user_id not in notes:
            notes[user_id] = []

        notes[user_id].append(content)

        with open(NOTE_FILE, 'w') as f:
            json.dump(notes, f, indent=4)

        await ctx.send(f'메모가 추가되었습니다! [{len(notes[user_id])}] {content}')

    @note.command(name='list')
    async def note_list(self, ctx):
        """메모 리스트를 표시합니다."""
        with open(NOTE_FILE, 'r') as f:
            notes = json.load(f)

        user_id = str(ctx.author.id)
        if user_id not in notes or not notes[user_id]:
            await ctx.send('메모가 비어 있습니다.')
            return

        embed = discord.Embed(title=f"{ctx.author.name}님의 메모", color=0x0000ff)
        for idx, note in enumerate(notes[user_id], start=1):
            embed.add_field(name=f"{idx}.", value=note, inline=False)

        await ctx.send(embed=embed)

    @note.command(name='remove')
    async def note_remove(self, ctx, index: int):
        """메모를 제거합니다."""
        with open(NOTE_FILE, 'r') as f:
            notes = json.load(f)

        user_id = str(ctx.author.id)
        if user_id not in notes or index < 1 or index > len(notes[user_id]):
            await ctx.send('유효한 번호를 입력해주세요.')
            return

        removed = notes[user_id].pop(index - 1)

        with open(NOTE_FILE, 'w') as f:
            json.dump(notes, f, indent=4)

        await ctx.send(f'메모가 제거되었습니다: {removed}')

    @commands.command(name='remind')
    async def remind(self, ctx, time: int, *, message: str):
        """지정한 시간(시간 단위)이 지난 후 알림을 보냅니다."""
        if time <= 0:
            await ctx.send('유효한 시간을 입력해주세요.')
            return

        # 알림 저장
        with open(REMINDER_FILE, 'r') as f:
            reminders = json.load(f)

        user_id = str(ctx.author.id)
        if user_id not in reminders:
            reminders[user_id] = []

        reminders[user_id].append({
            'channel_id': ctx.channel.id,
            'time_left': time * 3600,
            'message': message
        })

        with open(REMINDER_FILE, 'w') as f:
            json.dump(reminders, f, indent=4)

        await ctx.send(f'{time}시간 후에 알림을 보내드릴게요.')
        asyncio.create_task(self.send_reminder(ctx, time, message))

    async def send_reminder(self, ctx, time, message):
        await asyncio.sleep(time * 3600)
        await ctx.send(f'⏰ **알림:** {message}')

    async def load_reminders(self):
        """저장된 알림 데이터를 로드하고 예약합니다."""
        with open(REMINDER_FILE, 'r') as f:
            reminders = json.load(f)

        for user_id, user_reminders in reminders.items():
            for reminder in user_reminders:
                channel_id = reminder['channel_id']
                time_left = reminder['time_left']
                message = reminder['message']

                channel = self.bot.get_channel(channel_id)
                if channel:
                    asyncio.create_task(self.schedule_reminder(channel, time_left, message))

    async def schedule_reminder(self, channel, time_left, message):
        await asyncio.sleep(time_left)
        await channel.send(f'⏰ **알림:** {message}')

async def setup(bot):
    await bot.add_cog(Practical(bot))
