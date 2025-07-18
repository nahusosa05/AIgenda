from config.settings import TELEGRAM_TOKEN
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from cohere_integration.cohere_utils import get_event
from telegram import Update

# Programación asíncrona
# async -> método asincrónico: pausa su ejecución para esperar mientras realiza tareas que toman tiempo
# await -> espera el resultado de la operación sin que el programa se congele.

# update -> objeto que representa el evento que disparó el handler
# context -> data del user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola soy AIgenda! ¿En que te puedo ayudar?")
    
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    json_response = get_event(text)
    mensaje = (
        f"🗓 Evento: {json_response['evento']}\n"
        f"📅 Fecha: {json_response['fecha']}\n"
        f"⏰ Hora: {json_response['hora']}"
    )
    
    await update.message.reply_text(mensaje)
    
def start_bot():
    # construyo la app
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()  
    
    app.add_handler(CommandHandler("start",start)) # CommandHandler responde a comandos, en este caso /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    app.run_polling(allowed_updates=Update.ALL_TYPES) 