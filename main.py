from bot.telegram_bot import start_bot
from notion_client import Client
from config.settings import NOTION_TOKEN, DATABASE_ID

if __name__ == "__main__":
    #start_bot()
    
    notion = Client(auth=NOTION_TOKEN)

    try:
        response = notion.databases.retrieve(database_id=DATABASE_ID)
        print("✅ Conexión exitosa con la base de datos:")
        print("Nombre:", response["title"][0]["plain_text"])
    except Exception as e:
        print("❌ Error al conectar con Notion:")
        print(e)