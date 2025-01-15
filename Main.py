#Main___File

import discord as d
from discord.ext import commands
import os

#intent 설정: 봇의 권한을 설정함 - 최적화를 위해 불필요한 권한 삭제
intents = d.Intents.default()
intents.message_content = True  #메세지 접근 허용
intents.members = True          #멤버 접근 허용

firefly = commands.Bot(command_prefix="/", intents=intents)

@firefly.event
async def on_ready():           #봇이 준비 완료됨
    print(f"Logged in as {firefly.user}")

@firefly.command()
async def hello(ctx):           #/hello에 응답하는 함수
    await ctx.send(f"안녕! 나는 반디야. 반가워 {ctx.author.display_name}")

@firefly.command()              #서버 입구 지정
async def Reactionrole(ctx, channel_id: int, log_id: int, role_id: int, emoji: str):
    channel = firefly.get_channel(channel_id)
    log_channel = firefly.get_channel(log_id)
    role = ctx.guild.get_role(role_id)

    if not channel:
        await ctx.send("유효하지 않은 채널이야.")
        return

    if not log_channel:
        await ctx.send("유효하지 않은 채널이야.")
        return

    if not role:
        await ctx.send("유효하지 않은 역할이야.")
        return
    
    greeting = f"종합병동에 온걸 환영해. \n이 서버에서는 이름을 OO노예 형태로 지정해야해. \n규칙을 안지키면 불이익이 생길 수 있어. \n확인했으면 아래의 이모지를 눌러줘."
    message =  await channel.send(greeting)
    await message.add_reaction(emoji)
    await log_channel.send(f"채널 {channel.name}에 메시지를 전송했어. 로그는 {log_channel.name}에 기록할께.")

    @firefly.event                  #이모지 체크 및 역할 부여
    async def on_raw_reaction_add(payload):
        if payload.member.bot:
            return
        
        if payload.channel_id == channel_id and str(payload.emoji) == emoji:
            guild = firefly.get_guild(payload.guild_id)
            member = payload.member

            if role:
                    await member.add_roles(role)
                    await log_channel.send(f"{member.display_name}에게 역할 {role.name}을 부여했어.")

            channel = firefly.get_channel(payload.channel_id)
            if channel:                 #이모지 제거
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji, member)            

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await firefly.load_extension(f"cogs.{filename[:-3]}")

# 비동기 실행
async def main():
    async with firefly:
        await load_extensions()
        with open("token.txt", "r") as token_file:
            TOKEN = token_file.read().strip()
        await firefly.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())