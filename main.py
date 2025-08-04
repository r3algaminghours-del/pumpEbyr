import time
import threading
import logging
from telegram import Bot
from pumpfun_api import fetch_latest_tokens, fetch_token_info, minutes_since
from filter import is_promising

TELEGRAM_TOKEN = "8180214699:AAEU79Dd8N_kCZZFXoqdifB3u0-B1BxiHgQ"
CHANNEL_ID = 1758725762  # твой Telegram ID
bot = Bot(token=TELEGRAM_TOKEN)

seen = set()

def check_tokens():
    while True:
        tokens = fetch_latest_tokens()
        for token in tokens:
            mint = token.get("address")
            if mint in seen:
                continue
            seen.add(mint)

            info = fetch_token_info(mint)
            if not info:
                continue

            age_min = minutes_since(info.get("created_at", 0))
            if age_min > 30:
                continue

            if is_promising(info):
                link = f"https://pump.fun/{mint}"
                mc = info.get("marketCap", 0)
                holders = info.get("holders", 0)
                dev_hold = info.get("devTokenPercentage", 0)
                inflow = info.get("netflow5m", 0)
                vol = info.get("volume5m", 0)
                name = info.get("name", "")
                symbol = info.get("symbol", "")

                msg = f"""🚀 <b>Новый токен на Pump.fun!</b>
<b>{name}</b> (<a href="{link}">${symbol}</a>)

📈 MC: ${int(mc):,}
👛 Холдят: {holders}
💸 Dev Hold: {dev_hold:.2f}%
📊 5m Volume: ${int(vol):,}
📈 Net Inflow: ${int(inflow):,}
⏳ Age: {int(age_min)} мин
"""
                bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode="HTML")

        time.sleep(60)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    threading.Thread(target=check_tokens).start()
