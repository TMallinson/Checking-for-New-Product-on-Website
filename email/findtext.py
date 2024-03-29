# Import requests (to download page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

# Import Time (to add a delay between the times the scrape runs)
import time

# Import smtplib
import smtplib, ssl

# Import environment to replace confidential credentials
from os import environ

# This script downloads the Men's Worn Wear Page already filtered by size and recent adds, and if it finds some text it emails me
# If it does not find the text, it waits 10 minutes and downloads the page again

# Creating a counter to keep track of iterations
counter = 0

# While this is true (true by default)
while True:
    # Set the URL as Worn Wear, sorted by size, category, and most recently added
    url = 'https://wornwear.patagonia.com/shop/mens?category=Jackets&size=S&sort=most_recent'
    # Set the headers like we are a browser
    headers = {"Your: User Agent"}
    # Download the page
    response = requests.get(url, headers=headers)
    # Parse the downloaded homepage and grab all text
    soup = BeautifulSoup(response.text, "lxml")
    # If number of times the word "Nano Puff Hoody" occurs on the page is less than 1
    if str(soup).find("Nano Puff® Hoody") == -1:
        # Add to counter
        counter += 1
        print("Number of iterations: " + str(counter))
        # Wait 10 minutes
        time.sleep(600)
        # Continue with the script
        continue

    # But if the word "Nano Puff Hoody" occurs any number of times
    else:
        # Create an email message with just a subject line
        message = message = """\
Subject: Nano Puff Hoody is in Stock!

check out Worn Wear here: https://wornwear.patagonia.com/shop/mens?category=Jackets&size=S&sort=most_recent"""

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
