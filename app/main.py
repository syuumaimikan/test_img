import os
import asyncio
from datetime import datetime, timedelta
import discord
from discord import app_commands
from dotenv import load_dotenv

from server import server_thread

load_dotenv()

def main():
    # Discordのクライアントを初期化
    intents = discord.Intents.default()
    intents.message_content = True  # メッセージ内容を取得するために有効化
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    async def send_message_at_time(channel_id, target_time):
        """指定した時刻にメッセージを送信する"""
        now = datetime.now()
        target_datetime = datetime.combine(now.date(), target_time)
        if target_datetime < now:
            target_datetime += timedelta(days=1)  # 翌日に設定

        wait_time = (target_datetime - now).total_seconds()
        print(f"メッセージ送信まで {wait_time} 秒待機します")
        await asyncio.sleep(wait_time)

        channel = client.get_channel(channel_id)
        if channel:
            embed = discord.Embed(title="抜いてもらおうか", color=0x969696)
            embed.set_author(name="チェンバー", icon_url="https://raw.githubusercontent.com/syuumaimikan/test_img/refs/heads/main/chamber.png")
            embed.set_thumbnail(url="https://raw.githubusercontent.com/syuumaimikan/test_img/refs/heads/main/chamber.png")
            await channel.send(embed=embed)
        else:
            print(f"エラー: チャンネルID {channel_id} が見つかりません")

    @client.event
    async def on_ready():
        print(f"起動完了: {client.user} でログインしています")
        await tree.sync()  # スラッシュコマンドを同期
        # 特定のチャンネルでメッセージを送信
        channel_id = 1347843619570319400  # ここに送信したいチャンネルのIDを入力
        channel = client.get_channel(channel_id)
        embed = discord.Embed(title="消えてもらおうか", color=0x969696)
        embed.set_author(name="チェンバー", icon_url="https://raw.githubusercontent.com/syuumaimikan/test_img/refs/heads/main/chamber.png")
        embed.set_thumbnail(url="https://raw.githubusercontent.com/syuumaimikan/test_img/refs/heads/main/chamber.png")
        if channel:
            await channel.send(embed=embed)
        else:
            print(f"エラー: チャンネルID {channel_id} が見つかりません")
                # メッセージを送信する時刻を設定 (例: 15:30)
        target_time = datetime.strptime("20:00", "%H:%M").time()
        channel_id = 1347843619570319400  # ここに送信したいチャンネルのIDを入力
        client.loop.create_task(send_message_at_time(channel_id, target_time))

    @tree.command(name="test", description="テスト")
    async def test_command(interaction: discord.Interaction):
        embed = discord.Embed(title="遊びたいのか？相手になろう", color=0x969696)
        embed.set_author(name="チェンバー", icon_url="https://raw.githubusercontent.com/syuumaimikan/test_img/refs/heads/main/chamber.png")
        embed.set_thumbnail(url="https://raw.githubusercontent.com/syuumaimikan/test_img/refs/heads/main/chamber.png")
        await interaction.response.send_message(embed=embed)

    token = os.environ.get('TOKEN')
    server_thread()
    # Botを起動
    client.run(token)

if __name__ == '__main__':
    main()
