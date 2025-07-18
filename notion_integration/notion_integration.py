from config.settings import NOTION_TOKEN,DATABASE_ID
from notion_client import Client

notion = Client(auth=NOTION_TOKEN)

database_info = notion.databases.retrieve(database_id=DATABASE_ID)
