from config.settings import TELEGRAM_TOKEN
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# async -> método asincrónico: pausa su ejecución para esperar mientras realiza tareas que toman tiempo
# await -> espera el resultado de la operación sin que el programa se congele.

# update -> objeto que representa el evento que disparó el handler

async def start(update, context):
    await update.message.reply_text("¡Hola soy AIgenda! ¿En que te puedo ayudar?")
    
async def echo(update, context):
    texto = update.message.text
    await update.message.reply_text(f"Me dijiste: [{texto}]")
    
def start_bot():
    # construyo la app
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()  
    
    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Bot andando..")
    app.run_polling()