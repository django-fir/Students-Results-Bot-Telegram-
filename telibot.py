import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters
from telegram import InputMediaPhoto
import requests


TOKEN = "*****************************************"
usn = ''
caht_id = ''
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


import base64
import io
from telegram import InputMediaDocument

prev_text = {"data":""}

def csv_data(url):
    data = requests.get(url+'&csv=csv').text
    prev_text["data"] = data
    

    

def send_base64(url):    
    file_data = requests.get(url).json()
    

    # decode base64 data
    decoded_file_data = base64.b64decode(file_data)

    # create a file object from decoded data
    file_obj = io.BytesIO(decoded_file_data)
    return file_obj





async def button(update, context):
    
    keyboard = [
        [
            InlineKeyboardButton("Sem 1", callback_data='1'),
            InlineKeyboardButton("Sem 2", callback_data='2'),
            InlineKeyboardButton("Sem 3", callback_data='3'),
            InlineKeyboardButton("Sem 4", callback_data='4')
        ],
        [
            InlineKeyboardButton("Sem 5", callback_data='5'),
            InlineKeyboardButton("Sem 6", callback_data='6'),
            InlineKeyboardButton("Sem 7", callback_data='7'),
            InlineKeyboardButton("Sem 8", callback_data='8')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose SEM:', reply_markup=reply_markup)
   

async def button_callback(update, context):
    query = update.callback_query  
      
    photo_url = f'http://127.0.0.1:8000/chat/?usn={globals()["usn"]}&sem={query.data}&m=a'
    photo = send_base64(photo_url)
    await context.bot.send_photo(chat_id=globals()['caht_id'], photo=photo)
    # await query.edit_message_text(text=f"Selected option: {query.data}")












async def send_image(update, context):
    globals()['caht_id'] = update.message.chat_id
    
    usn = context.args[0]
    globals()['usn'] = usn
    await button(update,context)    



def send_chart(update,context):
    pass



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="HEY I'm a bot, please talk to me!")

async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=f"HEY I'm a bot, please talk to me! {context.args}")    
    await send_image(update,context)

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    arg = context.args[0]
    url = f'http://127.0.0.1:8000/chat/?usn={arg}&m=gp'
    data = send_base64(url)
    await context.bot.send_document(chat_id=chat_id, document=data,filename=f'{arg}.html')

async def excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    arg = context.args[0]
    url = f'http://127.0.0.1:8000/chat/?usn={arg}&m=ex'
    data = send_base64(url)
    csv_data(url)

    
    await context.bot.send_document(chat_id=chat_id, document=data,filename=f'{arg}.xlsx')


async def chart_callback(update, context):
    query = update.callback_query    
    
    await query.answer()    
    # photo_url = f'http://127.0.0.1:8000/chat/?usn={globals()["usn"]}&sem={query.data}&m=a'
    # photo = requests.get(photo_url)
    # await context.bot.send_photo(chat_id=globals()['caht_id'], photo=photo.content,reply_markup=reply_markup)
    await query.edit_message_text(text=f"Selected option: {query.data}")


from pprint import pformat

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f'http://127.0.0.1:8000/wget/?q={context.args[0]}'
    test = requests.get(url).json()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=pformat(test))

async def edu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f'http://127.0.0.1:8000/wget/?q={context.args[0]}&m=e'
    test = requests.get(url).json()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=pformat(test))


async def clas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = context.args
    url = f'http://127.0.0.1:8000/chat1/?s={m[0]}&m=as&br={m[1]}&bat={m[2]}'
    chat_id = update.message.chat_id       
    data = send_base64(url)
    csv_data(url)
    await context.bot.send_document(chat_id=chat_id, document=data,filename=f'{m[1]}.xlsx')


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = context.args
    url = f'http://127.0.0.1:8000/wsearch/?q={m[0]}&br={m[1]}&ba={m[2]}'
         
    test = requests.get(url).json()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=test)


async def dear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = " ".join(context.args)
    pp = prev_text["data"]
    if pp:
        m = pp + m
    url = f'http://127.0.0.1:5001/chat?q={m}'
         
    test = requests.get(url).text
    prev_text["data"]= ""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=test)


async def toper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = context.args
    url = f'http://127.0.0.1:8000/chat1/?s={m[0]}&m=c&br={m[1]}&bat={m[2]}'
    chat_id = update.message.chat_id       
    data = send_base64(url)
    csv_data(url)
    await context.bot.send_document(chat_id=chat_id, document=data,filename=f'topers({m[0]}).xlsx')

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.[Button]")

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler










if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    result_handler = CommandHandler('result', result)
    application.add_handler(result_handler)
    button_handler = CommandHandler('button', button)
    application.add_handler(button_handler)
    application.add_handler(CallbackQueryHandler(button_callback))
    chart_handler = CommandHandler('chart', chart)
    application.add_handler(chart_handler)
    excel_handler = CommandHandler('excel', excel)
    application.add_handler(excel_handler)
    info_handler = CommandHandler('info', info)
    application.add_handler(info_handler)
    edu_handler = CommandHandler('edu', edu)
    application.add_handler(edu_handler)
    clas_handler = CommandHandler('class', clas)
    application.add_handler(clas_handler)
    search_handler = CommandHandler('search', search)
    application.add_handler(search_handler)
    toper_handler = CommandHandler('toper', toper)
    application.add_handler(toper_handler)
    chat_handler = CommandHandler('dear', dear)
    application.add_handler(chat_handler)
    application.add_handler(CallbackQueryHandler(chart_callback))
    
    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)


    application.run_polling()


    



    # send document
