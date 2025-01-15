import discord
from discord.ext import commands
import os
import datetime
import wikipedia
import webbrowser as wb
import os
import random
import pyjokes
import openai
from googletrans import Translator

# OpenAI API 키 설정 (환경 변수 사용 권장)
openai.api_key = os.getenv('OPENAI_API_KEY')

translator = Translator()

# 명령어 트리거 정의 (한글)
COMMANDS = {
    "time": ["시간", "몇 시", "현재 시간", "지금 몇 시야"],
    "date": ["날짜", "오늘 날짜", "오늘은 몇 월 며칠", "오늘은 무슨 날"],
    "wikipedia": ["위키피디아", "위키", "위키 검색", "백과사전 검색"],
    "play_music": ["음악 재생", "노래 틀어", "음악 틀어", "노래 재생"],
    "open_youtube": ["유튜브 열어", "유튜브 켜", "유튜브 열기", "유튜브로 이동"],
    "open_google": ["구글 열어", "구글 켜", "구글 열기", "구글로 이동"],
    "set_name": ["이름 바꿔", "너 이름 바꿔", "내 이름 설정", "너의 이름을 변경해"],
    "screenshot": ["스크린샷", "화면 캡처", "화면 찍어", "스크린 캡쳐"],
    "joke": ["농담 해", "날 웃게 해봐", "재밌는 농담 해줘", "농담 해줘", "웃겨"],
    "shutdown": ["시스템 종료", "종료", "컴퓨터 끄기", "시스템을 꺼"],
    "restart": ["재시작", "시스템 재부팅", "컴퓨터 다시 시작"],
    "offline": ["오프라인", "나가", "종료해", "서비스 중지"]
}

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.assistant_name = self.load_name()

    def load_name(self) -> str:
        """파일에서 어시스턴트의 이름을 불러오거나 기본 이름을 사용합니다."""
        try:
            with open("assistant_name.txt", "r", encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            return "Jarvis"  # 기본 이름

    def match_command(self, query: str) -> str:
        """쿼리를 분석하여 해당 명령어를 반환합니다."""
        for command, triggers in COMMANDS.items():
            for trigger in triggers:
                if trigger in query:
                    return command
        return "unknown"

    def translate_to_english(self, text: str) -> str:
        """텍스트를 영어로 번역합니다."""
        try:
            translation = translator.translate(text, src='ko', dest='en')
            return translation.text
        except Exception as e:
            print(f"Translation Error: {e}")
            return ""

    def get_gpt_response(self, prompt: str) -> str:
        """GPT-3 API를 호출하여 응답을 반환합니다."""
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # 사용하고자 하는 모델 선택
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            answer = response.choices[0].text.strip()
            return answer
        except Exception as e:
            print(f"GPT API Error: {e}")
            return "죄송합니다. 요청을 처리할 수 없습니다."

    @commands.Cog.listener()
    async def on_message(self, message):
        # 봇 자신의 메시지는 무시
        if message.author == self.bot.user:
            return

        query = message.content.lower()
        command = self.match_command(query)

        if command == "time":
            await self.time_func(message)

        elif command == "date":
            await self.date_func(message)

        elif command == "wikipedia":
            # "위키피디아" 또는 "위키" 다음에 오는 검색어 추출
            search_term = query
            for trigger in COMMANDS["wikipedia"]:
                search_term = search_term.replace(trigger, "").strip()
            await self.search_wikipedia(message, search_term)

        elif command == "play_music":
            # 음악 재생은 Discord 봇에서 직접 음악을 재생하기 위해 추가 구현 필요
            await message.channel.send("음악 재생 기능은 현재 지원되지 않습니다.")

        elif command == "open_youtube":
            # Discord에서는 링크를 직접 열 수 없으므로 URL을 공유
            await message.channel.send("https://www.youtube.com 을 여세요.")

        elif command == "open_google":
            await message.channel.send("https://www.google.com 을 여세요.")

        elif command == "set_name":
            await self.set_name(message)

        elif command == "screenshot":
            # Discord 봇에서 서버의 스크린샷을 찍는 것은 보안상 권장되지 않음
            await message.channel.send("스크린샷 기능은 현재 지원되지 않습니다.")

        elif command == "joke":
            await self.tell_joke(message)

        elif command == "shutdown":
            await message.channel.send("시스템을 종료합니다.")
            os.system("shutdown /s /f /t 1")

        elif command == "restart":
            await message.channel.send("시스템을 재시작합니다.")
            os.system("shutdown /r /f /t 1")

        elif command == "offline":
            await message.channel.send("오프라인으로 전환합니다. 안녕히 가세요!")
            await self.bot.close()

        else:
            # 일반적인 질문을 처리 (GPT 연동)
            english_query = self.translate_to_english(query)
            if not english_query:
                await message.channel.send("번역에 실패했습니다.")
                return

            gpt_response = self.get_gpt_response(english_query)
            if gpt_response:
                # GPT 응답을 한국어로 번역
                try:
                    korean_response = translator.translate(gpt_response, src='en', dest='ko').text
                    await message.channel.send(korean_response)
                except Exception as e:
                    print(f"Translation Error: {e}")
                    await message.channel.send(gpt_response)
            else:
                await message.channel.send("죄송합니다. 응답을 생성할 수 없습니다.")

    async def time_func(self, message):
        """현재 시간을 알려줍니다."""
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        response = f"현재 시간은 {current_time}입니다."
        await message.channel.send(response)

    async def date_func(self, message):
        """현재 날짜를 알려줍니다."""
        now = datetime.datetime.now()
        response = f"오늘 날짜는 {now.year}년 {now.month}월 {now.day}일입니다."
        await message.channel.send(response)

    async def search_wikipedia(self, message, query):
        """위키피디아를 검색하고 요약을 반환합니다."""
        try:
            wikipedia.set_lang("ko")  # 한국어 위키피디아 설정
            summary = wikipedia.summary(query, sentences=2)
            await message.channel.send(summary)
        except wikipedia.exceptions.DisambiguationError:
            await message.channel.send("여러 결과가 발견되었습니다. 더 구체적으로 말씀해 주세요.")
        except wikipedia.exceptions.PageError:
            await message.channel.send("위키피디아에서 찾을 수 없습니다.")
        except Exception as e:
            print(f"Wikipedia Error: {e}")
            await message.channel.send("위키피디아에서 정보를 가져오는 중 오류가 발생했습니다.")

    async def set_name(self, message):
        """어시스턴트의 새 이름을 설정합니다."""
        await message.channel.send("어시스턴트의 새 이름을 입력해주세요.")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            name_msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            name = name_msg.content.strip()
            if name:
                with open("assistant_name.txt", "w", encoding='utf-8') as file:
                    file.write(name)
                self.assistant_name = name
                await message.channel.send(f"알겠습니다. 이제부터 제 이름은 {name}입니다.")
            else:
                await message.channel.send("이름이 유효하지 않습니다.")
        except asyncio.TimeoutError:
            await message.channel.send("시간이 초과되었습니다. 다시 시도해주세요.")

    async def tell_joke(self, message):
        """농담을 말합니다."""
        joke = pyjokes.get_joke(language="ko", category="neutral")
        await message.channel.send(joke)

def setup(bot):
    bot.add_cog(TTS(bot))
