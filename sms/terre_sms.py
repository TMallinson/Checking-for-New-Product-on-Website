# Import requests (to download page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

# Import Time (to add a delay between the times the scrape runs)
import time

# Impost twilio to send SMS messages
from twilio.rest import Client

# Creating a counter to keep track of iterations
counter = 0

# While this is true (true by default)
while True:
    # Set the URL as Worn Wear, sorted by size, category, and most recently added
    url = 'https://wornwear.patagonia.com/shop/mens-just-added?category=Pants&size=30&size=S'
    # Set the headers like we are a browser
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
    # Download the page
    response = requests.get(url, headers=headers)
    # Parse the downloaded homepage and grab all text
    soup = BeautifulSoup(response.text, "lxml")
    # If number of times the word "Terrebonne Joggers" occurs on the page is less than 1
    if str(soup).find("Terrebonne Joggers") == -1:
        # Add to counter
        counter += 1
        print("Number of iterations: " + str(counter))
        # Wait 10 minutes
        time.sleep(600)
        # Continue with the script
        continue

    # But if the word "Terrebonne Joggers" occurs any number of times
    else:
        # Send a text to my phone notifying me
        account_sid = TWILIO_ACCOUNT_SID
        auth_token = TWILIO_AUTH_TOKEN
        number = TWILIO_NUMBER

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="your_number",
            from_= number,
            body="Patagonia Terrebonne Joggers are in stock on Worn Wear! Follow this link to order: https://wornwear.patagonia.com/shop/mens-just-added?category=Pants&size=30&size=S")

        print(message.sid)

        break
