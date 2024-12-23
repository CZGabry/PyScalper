import requests
from bs4 import BeautifulSoup
import json
from Classes.Ticket import Ticket

tickets = "Queens of the stone age"
title = ""
def set_tickets():
           
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
   
    url = config['url']
    
    session = requests.Session()
    session.headers.update(config['headers'])

    response = session.get(url, timeout=10)
    if response.status_code == 200:
        html = BeautifulSoup(response.text, 'html.parser')
        title = html.title
        return html
    else:
        print("Failed to retrieve the page. Status Code:", response.status_code)
        html = BeautifulSoup(response.text, "html.parser")
        return html

def find_tickets(html):
    tickets_array = []
    for tag in html.find_all("li", class_="QuickwinEntry"):
        availableTickets = tag.find("div", class_="DetailBEntry-AvailableTickets AvailableTickets").text.strip()
        seatDescription = tag.find("div", class_="DetailBEntry-SeatDescription SeatDescription").text.strip()
        ticket= Ticket(quantity=availableTickets, ticket_type=seatDescription)
        tickets_array.append(ticket)
    return tickets_array

def get_tickets():
    tickets_list = find_tickets(html)
    
    return tickets_list


html = set_tickets()
tickets = find_tickets(html)
