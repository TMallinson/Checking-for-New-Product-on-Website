# Import requests (to download page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

# Import Time (to add a delay between the times the scrape runs)
import time

# Import smtplib
import smtplib, ssl

# Import environment to replace confidential credentials
import os
from os import environ

# This script downloads the Men's Worn Wear Page already filtered by size and recent adds, and if it finds some text it emails me
# If it does not find the text, it waits 10 minutes and downloads the page again

# Creating a counter to keep track of iterations
counter = 0

# While this is true (true by default)
while True:
    # Set the URL as Worn Wear, sorted by size, category, and most recently added
    url = 'https://wornwear.patagonia.com/shop/mens-shorts?size=30&size=S&sort=most_recent'
    # Set the headers like we are a browser
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
    # Download the page
    response = requests.get(url, headers=headers)
    # Parse the downloaded homepage and grab all text
    soup = BeautifulSoup(response.text, "lxml")
    # If number of times the word "Quandary Shorts" occurs on the page is less than 1
    if str(soup).find("Quandary Shorts") == -1:
        # Add to counter
        counter += 1
        print("Number of iterations: " + str(counter))
        # Wait 10 minutes
        time.sleep(600)
        # Continue with the script
        continue

    # But if the word "Quandary Shorts" occurs any number of times
    else:
        # Create an email message with just a subject line
        message = message = """\
Subject: Quandary Shorts is in Stock!

check out Worn Wear here: https://wornwear.patagonia.com/shop/mens-shorts?size=30&size=S&sort=most_recent"""

        # Set the sender address and password
        sender_email = environ["SENDER_EMAIL"]
        password = environ["SENDER_PASSWORD"]
        # Set the receiver address
        receiver_email = environ["RECEIVER_EMAIL"]

        # Setup the email server
        smtp_server = "smtp.gmail.com"
        port = 465 # For SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

        # Print the email's contents
        print('From: ' + sender_email)
        print('To: ' + str(receiver_email))
        print('Message: ' + message)

        break
