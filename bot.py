import logging
from telegram.ext import Updater, CommandHandler
import telegram
import pandas as pd
import logging
import rfqSpreads


# Configure Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Solicitar TOKEN
TOKEN = "5820516027:AAGHin8jcv3CKvdZiyWRv-F-SpPwnZ-F5UI"

def tracker(update,context):
  chat_id = update.effective_chat['id']
  title = update.effective_chat['title']
  name = update.effective_user['first_name']
  logger.info(
        f"El usuario {name}, ha puesto una solicitud de spreads RFQ en el chat {title} (id = {chat_id} )")
  context.bot.sendMessage(
        chat_id=chat_id, parse_mode="HTML", text="Starting RFQ Spreads for all Coins....")
  rfqSpreads.run()

if __name__ == "__main__":
    # Obtenemos la informacion del Bot
    my_bot = telegram.Bot(token=TOKEN)

# Enlazamos nuestro updater con nuestro bot
updater = Updater(my_bot.token, use_context=True)

# Creamos un despachador
dp = updater.dispatcher
                         
 
dp.add_handler(CommandHandler("rfq_spread_tracker_all_coins", tracker ))
# Pregunta al bot si hay nuevos msjs
updater.start_polling()
                           
print("BOT CARGADO")
                           
updater.idle()  # finalizar el bot ctrl+c
