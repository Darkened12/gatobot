import asyncio
import os
from typing import Tuple

from app.controllers.links_controller import LinksController
from app.controllers.keywords_controller import KeywordsController
from app.controllers.emojis_controller import EmojisController
from database_service import DatabaseService
from dotenv import load_dotenv

load_dotenv()


async def database_setup() -> Tuple[KeywordsController, EmojisController, LinksController]:
    database = await DatabaseService(dsn_connector='sqlite+aiosqlite:///../../', dsn=os.environ.get('DATABASE'))
    kw_controller = KeywordsController(database)
    emojis_controller = EmojisController(database)
    links_controller = LinksController(database)
    return kw_controller, emojis_controller, links_controller


def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix-based
        os.system('clear')


def is_choice_valid(input_text: str, choice_size: int):
    try:
        parsed_input = int(input_text)
    except TypeError:
        return False

    if parsed_input < 1 or parsed_input > choice_size:
        return False
    return True


def home_page() -> int:
    while True:
        clear_screen()
        print("Choose an option:")
        print("1. Add keyword")
        print("2. Add emoji")
        print("3. Add URL")
        print("4. Link emoji to keyword table")
        print("5. Link URL to keyword table")
        print("6. Quit")
        input_text = input('> ')

        if not is_choice_valid(input_text, 6):
            continue
        return int(input_text)


async def page_one(kw_controller: KeywordsController):
    while True:
        clear_screen()
        print('Keyword name:')
        input_text = input('> ')
        await kw_controller.add_keyword(input_text)
        while True:
            clear_screen()
            print(f'Keyword "{input_text}" Added! Want to add another one or go back?')
            print('1. Continue')
            print('2. Go back')
            input_text_2 = input('> ')

            if not is_choice_valid(input_text_2, 2):
                continue

            if int(input_text_2) == 1:
                return await page_one(kw_controller)
            else:
                return


async def page_two(emojis_controller: EmojisController):
    while True:
        clear_screen()
        print('Emoji name:')
        input_text = input('> ')
        await emojis_controller.add_emoji(input_text)
        while True:
            clear_screen()
            print(f'Emoji "{input_text}" Added! Want to add another one or go back?')
            print('1. Continue')
            print('2. Go back')
            input_text_2 = input('> ')

            if not is_choice_valid(input_text_2, 2):
                continue

            if int(input_text_2) == 1:
                return await page_two(emojis_controller)
            else:
                return


async def page_three(links_controller: LinksController):
    while True:
        clear_screen()
        print('URL name:')
        input_text = input('> ')
        await links_controller.add_link(input_text)
        while True:
            clear_screen()
            print(f'URL "{input_text}" Added! Want to add another one or go back?')
            print('1. Continue')
            print('2. Go back')
            input_text_2 = input('> ')

            if not is_choice_valid(input_text_2, 2):
                continue

            if int(input_text_2) == 1:
                return await page_three(links_controller)
            else:
                return


async def page_four(emojis_controller: EmojisController):
    while True:
        clear_screen()
        print('Type the emoji name to link')
        emoji = input('> ')
        clear_screen()

        print(f'Great!, now type the keyword for the emoji "{emoji}":')
        keyword = input('> ')
        await emojis_controller.link_emoji_to_keyword(emoji, keyword)

        while True:
            clear_screen()
            print(f'Emoji "{emoji}" has successfully been linked to the keyword "{keyword}"!')
            print('Link another one or go back?')
            print('1. Continue')
            print('2. Go back')
            input_text = input('> ')

            if not is_choice_valid(input_text, 2):
                continue

            if int(input_text) == 1:
                return await page_four(emojis_controller)
            else:
                return


async def page_five(links_controller: LinksController):
    while True:
        clear_screen()
        print('Type the URL name to link')
        url = input('> ')
        clear_screen()

        print(f'Great!, now type the keyword for the URL "{url}":')
        keyword = input('> ')
        await links_controller.link_url_to_keyword(url, keyword)

        while True:
            clear_screen()
            print(f'URL "{url}" has successfully been linked to the keyword "{keyword}"!')
            print('Link another one or go back?')
            print('1. Continue')
            print('2. Go back')
            input_text = input('> ')

            if not is_choice_valid(input_text, 2):
                continue

            if int(input_text) == 1:
                return await page_five(links_controller)
            else:
                return


async def main_loop():
    kw_controller, emojis_controller, links_controller = await database_setup()
    while True:
        page_input = home_page()

        if page_input == 1:
            await page_one(kw_controller)
            continue
        elif page_input == 2:
            await page_two(emojis_controller)
            continue
        elif page_input == 3:
            await page_three(links_controller)
            continue
        elif page_input == 4:
            await page_four(emojis_controller)
            continue
        elif page_input == 5:
            await page_five(links_controller)
            continue
        elif page_input == 6:
            return


if __name__ == '__main__':
    asyncio.run(main_loop())
