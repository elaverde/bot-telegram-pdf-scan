import os
import subprocess
import telebot
import time
from flask import Flask, request, render_template
from dotenv import load_dotenv
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route('/'+API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    PATH ='/app'
    bot.reply_to(message, "Convirtiendo archivo")
    file_name = message.document.file_name
    file_name_aux = file_name.replace(" ","_")
    #validando que el archivo sea un pdf
    if file_name.split('.')[1] == 'pdf':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        #guardamos el archivo
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        #renombramos el archivo le quitamos los espacios
        os.rename(file_name, file_name_aux)
        #generamos nuevo nombre del archivo con el filtro
        new_file="convert_scan_"+file_name_aux
        #lo convertimos a pdf con el filtro
        completed = subprocess.check_call('convert -density 130 '+file_name_aux+' -rotate 0.33 -attenuate 0.15 +noise Multiplicative -colorspace Gray '+new_file, shell=True, cwd=PATH)
        #lo enviamos al solicitante
        doc_file = open(new_file, "rb")
        print(completed)
        bot.send_document(message.chat.id, doc_file)
        #eliminamos los dos archivos ya no son necesarios
        time.sleep(60)
        bot.reply_to(message, "Eliminando copias del archivo")
        os.remove(file_name_aux)
        os.remove(new_file)
        #alternativa no utilizada archivo en la nuve
        #bot.send_document(message.chat.id, 'https://atikegalle.com/uploads/1514125303.pdf')
    else:
        bot.send_message(message, "El archivo no es un pdf")

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://app-pdf-scan.herokuapp.com/'+API_TOKEN)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get('PORT', 5000)))