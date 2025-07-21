from config.settings import TELEGRAM_TOKEN
from config.constants import FECHA_ERROR
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from cohere_integration.cohere_utils import get_event

# Programación asíncrona
# async -> método asincrónico: pausa su ejecución para esperar mientras realiza tareas que toman tiempo
# await -> espera el resultado de la operación sin que el programa se congele.

# update -> objeto que representa el evento que disparó el handler
# context -> data del user

WAITING_FOR_EVENT = 1
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Agendar evento", callback_data="agendar")],
        [InlineKeyboardButton("📖 Ver eventos", callback_data="ver")],
        [InlineKeyboardButton("🗑️ Borrar evento", callback_data="borrar")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("Hola 👋 ¿Qué querés hacer?", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text("Hola 👋 ¿Qué querés hacer?", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    if query.data == "agendar":
        user_state[user_id] = WAITING_FOR_EVENT
        await query.message.reply_text("Escribí el nombre del evento que querés agendar [(fecha),(evento)]:")
    elif query.data == "ver":
        await query.edit_message_text("Aquí están tus eventos.")
    elif query.data == "borrar":
        await query.edit_message_text("¿Qué evento querés borrar?")

async def event_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_state.get(user_id) != WAITING_FOR_EVENT:
        return 

    text = update.message.text
    json_response = get_event(text)

    if json_response["fecha"] == "??/??":
        await update.message.reply_text(FECHA_ERROR)
    else:
        event = json_response['evento']
        mensaje = (
            f"🗓 Evento: {event.title()}\n"
            f"📅 Fecha: {json_response['fecha']}\n"
            f"⏰ Hora: {json_response['hora']}"
        )
        await update.message.reply_text(mensaje)

    # Resetear estado y volver al menú
    user_state[user_id] = None
    await start(update, context)

def start_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    # /start
    app.add_handler(CommandHandler("start", start))
    # Botón presionado
    app.add_handler(CallbackQueryHandler(handle_callback))
    # Texto normal enviado 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, event_register))
    app.run_polling()