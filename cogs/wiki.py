import discord
from discord.ext import commands
import wikipedia

# 위키피디아 설정
wikipedia.set_lang("ko")  # 한국어 설정

class WikiSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wiki')
    async def search_wiki(self, ctx, *, query: str):
        """위키피디아에서 키워드를 검색하고 요약을 제공합니다."""
        try:
            # 검색 및 요약
            summary = wikipedia.summary(query, sentences=3)  # 요약: 3문장
            page_url = wikipedia.page(query).url  # 페이지 URL

            # 임베드 메시지 생성
            embed = discord.Embed(
                title=f"📖 {query} - 위키피디아 검색 결과",
                description=summary,
                color=0x3498db
            )
            embed.add_field(name="🔗 링크", value=f"[위키피디아에서 자세히 보기]({page_url})", inline=False)
            embed.set_footer(text="위키피디아 검색 결과")

            await ctx.send(embed=embed)

        except wikipedia.exceptions.DisambiguationError as e:
            # 키워드가 모호할 경우
            options = "\n".join(e.options[:5])  # 최대 5개 옵션 표시
            await ctx.send(f"'{query}'는 모호한 검색어입니다. 다음 중 하나를 선택하세요:\n{options}")

        except wikipedia.exceptions.PageError:
            # 페이지를 찾을 수 없는 경우
            await ctx.send(f"'{query}'에 대한 결과를 찾을 수 없습니다.")

        except Exception as e:
            # 기타 예외 처리
            await ctx.send("검색 중 오류가 발생했습니다. 다시 시도해주세요.")

async def setup(bot):
    """위키 검색 Cog 로드"""
    await bot.add_cog(WikiSearch(bot))
