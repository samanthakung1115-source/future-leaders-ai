
from dataclasses import dataclass
import os

@dataclass
class AppConfig:
    app_name:str="Future Leaders AI"
    version:str="v1.2 RC"
    live_price_ttl:int=60
    enable_live_price:bool=True
    enable_auto_refresh:bool=True
    google_sheet_url:str=""

def load_config()->AppConfig:
    return AppConfig(
        app_name=os.getenv("FL_APP_NAME","Future Leaders AI"),
        version=os.getenv("FL_VERSION","v1.2 RC"),
        live_price_ttl=int(os.getenv("FL_LIVE_PRICE_TTL","60")),
        enable_live_price=os.getenv("FL_ENABLE_LIVE_PRICE","true").lower()=="true",
        enable_auto_refresh=os.getenv("FL_ENABLE_AUTO_REFRESH","true").lower()=="true",
        google_sheet_url=os.getenv("FL_GOOGLE_SHEET_URL",""),
    )
