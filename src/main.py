import sys
from bot import Bot
import threading

bot = Bot()

update_image = threading.Thread(target=bot.update_image)
update_image.start()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        print("Update game logic")
        bot.update()
