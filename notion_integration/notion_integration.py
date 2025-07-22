from config.settings import NOTION_TOKEN,DATABASE_ID
from notion_client import Client
from datetime import datetime

notion = Client(auth=NOTION_TOKEN)

try:
    response = notion.databases.retrieve(database_id=DATABASE_ID)
    print("✅ Conexión exitosa con la base de datos:")
except Exception as e:
    print("❌ Error al conectar con Notion:")
    print(e)

def convert_to_iso_date(date_str: str, hour_str: str) -> str:
    day, month = map(int, date_str.replace("-","/").split("/"))
    current_year = datetime.now().year
    iso_datetime = datetime(current_year, month, day, *map(int,hour_str.split(":")))
    return iso_datetime.isoformat()

def create_event_notion(event: str, date: str, hour: str):
    start_time = convert_to_iso_date(date, hour)
    try:
        response = notion.pages.create(
            parent={"database_id":DATABASE_ID},
            properties={
                "Evento":{
                    "title":[
                        {
                            "text":{
                                "content": event
                            }
                        }
                    ]
                },
                "Fecha":{
                    "date":{
                        "start":start_time
                    }
                }
            }
        )
        return True
    except Exception as e:
        print("❌ Error al crear evento en Notion:", e)
        return False