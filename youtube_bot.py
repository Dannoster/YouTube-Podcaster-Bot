import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, filters
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
import processing
import urllib

# Adding allowed users
ALLOWED_USERS = ("USERNAME1", "USERNAME2", "USERNAME3",)
class CheckUser(filters.Filter):
    async def __call__(self, message: types.Message):
        print(message.from_user.username)
        return message.from_user.username in ALLOWED_USERS

# Turn on logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token="<YOUR_TOKEN>")
dp = Dispatcher()

@dp.message(CheckUser(), Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello! I'm YouTube Podcasting bot. Send me any YouTube video link to get audio version of content.")

@dp.message(CheckUser(), F.text.contains("youtube.com/") | F.text.contains("youtu.be/"))
async def send_podcast(message: types.Message):
    counter = 0
    while True:
        try:
            await bot.send_chat_action(message.chat.id, "typing")
            link = message.text
            folder = youtube_podcasting.STORE_FOLDER
            lenth = youtube_podcasting.getting_lenth(link)
            if lenth > 2900:
                alert = await message.answer("Long video processing may take some time. Relax while waiting ☕️")
            title, channel = youtube_podcasting.getting_audio(link)
            photo = FSInputFile(f"{folder}/out.jpg")
            await message.answer_photo(
                photo=photo, 
                caption=f"{title} — {channel}"
            )
            await bot.send_chat_action(message.chat.id, "upload_document")
            audio = FSInputFile(f"{folder}/out.mp3")
            await message.answer_audio(
                audio=audio,
                title=title,
                performer=channel,
                thumbnail=photo,
            )
            youtube_podcasting.clean(title)
            break
        except urllib.error.HTTPError as e:
            counter += 1
            if counter == 10:
                await message.answer(f"Oops, I can't create an audio: {e}")
                break
        except Exception as e:
            folder = youtube_podcasting.STORE_FOLDER
            await message.answer(f"Oops, I can't create an audio: {e}".replace(folder,""))
            break
        except:
            await message.answer("Critical Error")
            break

@dp.message(CheckUser(), F.text.not_contains("youtube.com/") | F.text.not_contains("youtu.be/"))
async def non_youtube(message: types.Message):
    await message.answer("Sorry! I only work with YouTube links.")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
