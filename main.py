import asyncio
from scalper import get_tickets
from telegram import Bot
import json
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

bot_token = config['bot_token']
chat_id = config['chat_id']

counter = 0
reset_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(days=1)

async def send_message_to_bot(tickets):
    ticketstring = ""
    bot = Bot(token=bot_token)
    
    if len(tickets) > 0:
        for t in tickets:
            ticketstring += t.quantity + ", " + t.ticket_type + "\n"
    else:
        ticketstring = "Nessun biglietto disponibile"
        
    message = "Queens of the Stone Age MILANO 06/07/2024 17:00 Biglietti - TicketOne\n\n" + ticketstring + "\n\nhttps://www.ticketone.it/event/queens-of-the-stone-age-i-days-2024-ippodromo-snai-san-siro-17761875/?gclid=Cj0KCQiAy9msBhD0ARIsANbk0A_cNEJIl7cYN6S0qSEV__7De9oYLjVaEcnjWSZMvmwKwf6Cg_ogeXQaAkf8EALw_wcB"
    
    await bot.send_message(chat_id=chat_id, text=message)


async def send_message():
    global counter
    tickets = get_tickets()
    counter += 1
    if any(t.ticket_type != "Posto Unico" for t in tickets):
        await send_message_to_bot(tickets)

async def reset_counter_loop():
    global counter, reset_time
    while True:
        now = datetime.now()
        if now >= reset_time:
            counter = 0
            reset_time = datetime.combine(now.date(), datetime.min.time()) + timedelta(days=1)
            tickets = get_tickets()
            await send_message_to_bot(tickets)
        await asyncio.sleep(60)  # Sleep for 60 seconds before the next iteration

async def send_message_loop():
    while True:
        await send_message()
        await asyncio.sleep(180)  # Sleep for 600 seconds before the next iteration

if __name__ == '__main__':
    t1 = Thread(target=lambda: asyncio.run(send_message_loop()), daemon=True)
    t1.start()
    t2 = Thread(target=lambda: asyncio.run(reset_counter_loop()), daemon=True)
    t2.start()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
