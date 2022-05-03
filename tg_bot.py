import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from config import token, user_id
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from main import  check_posts_update
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
   start_buttons = ["Все новости", "Последние 5 новостей", "Свежие новости"]
   keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
   keyboard.add(*start_buttons)
   await message.answer("Лента новостей", reply_markup=keyboard)

@dp.message_handler(Text(equals="Все новости"))
async def get_all_posts(message: types.Message):
    with open("posts_dict.json") as file:
        posts_dict = json.load(file)
    for k, v in sorted(posts_dict.items()):
        # posts = f"<b>{v['article_date_time']}</b>\n" \
        #         f"<u>{v['article_title']}</u>\n" \
        #         f"<code>{v['article_desc']}</code>\n" \
        #         f"{v['article_url']}"
        posts = f"{hbold(v['article_date_time'])}\n" \
                f"{hunderline(v['article_title'])}\n" \
                f"{hcode(v['article_desc'])}\n" \
                f"{hlink(v['article_title'], v['article_url'])}"
        await message.answer(posts)

@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_last_five_posts(message: types.Message):
    with open("posts_dict.json") as file:
        posts_dict = json.load(file)
    for k, v in sorted(posts_dict.items())[-5:]:
        posts = f"{hbold(v['article_date_time'])}\n" \
                f"{hunderline(v['article_title'])}\n" \
                f"{hcode(v['article_desc'])}\n" \
                f"{hlink(v['article_title'], v['article_url'])}"
        await message.answer(posts)

@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_posts(message: types.Message):
    fresh_posts = check_posts_update()
    if len(fresh_posts) >= 1:
        for k, v in sorted(fresh_posts.items())[-5:]:
            posts = f"{hbold(v['article_date_time'])}\n" \
                    f"{hunderline(v['article_title'])}\n" \
                    f"{hcode(v['article_desc'])}\n" \
                    f"{hlink(v['article_title'], v['article_url'])}"
            await message.answer(posts)
    else:
        await message.answer("Свежих новостей пока нет.")


async def posts_every_minet():
    while True:
        fresh_posts = check_posts_update()

        if len(fresh_posts) >= 1:
            for k, v in sorted(fresh_posts.items())[-5:]:
                posts = f"{hbold(v['article_date_time'])}\n" \
                        f"{hunderline(v['article_title'])}\n" \
                        f"{hcode(v['article_desc'])}\n" \
                        f"{hlink(v['article_title'], v['article_url'])}"
                await bot.send_message(user_id, posts, disable_notification=True)
        else:
            await bot.send_message(user_id, "Свежих новостей пока нет", disable_notification=True)
        await asyncio.sleep(20)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(posts_every_minet())
    executor.start_polling(dp)

