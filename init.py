import telebot
import os

from modules.controller import Controller
from modules.helpers import *

bot = telebot.TeleBot('6100895303:AAFkidpLYJ36PZCa7Bqvw-R3ZpzVW-85SuM')

def_input = './tests/8.jpg'
def_pattern = './pattern/marker.png'
current_directory = os.getcwd()

    
def is_image(message):
    file_extension = message.document.file_name.split('.')[-1].lower()
    if file_extension not in ['png', 'jpeg']:
        bot.send_message(message.chat.id, "Invalid file type. Please send me an image file in PNG or JPEG format.")
        return False
    return True
    
def handle_photo(message):
    if message.content_type == 'photo':
        photo_file = bot.get_file(message.photo[-1].file_id)
        photo = bot.download_file(photo_file.file_path)
        
    elif message.content_type == 'document':
        if not is_image(message): return False
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        photo = bot.download_file(file_path)
        
    else:
        bot.reply_to(message, "Please send me an image in PNG or JPG format.")
    
    image_name = generate_image_name()
    input_save_location = f'{current_directory}/input_images/{image_name}'
    
    with open(input_save_location, 'wb') as f:
        f.write(photo)
        
    controller = Controller(input_save_location, def_pattern)
    
    processed_image = controller.process_image()
    
    with open(processed_image, 'rb') as processed_img:
        bot.send_photo(message.chat.id, processed_img)
        
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🖖Welcome to test bot of Hero-Detector module.\n⬆️ Just send me a photo, I will process it and return the result\n😁Happy testing") 

@bot.message_handler(content_types=['photo'])
def process_image(message):
    handle_photo(message)
    
@bot.message_handler(content_types=['document'])
def process_image(message):
    handle_photo(message)
    
# start the bot
bot.infinity_polling()