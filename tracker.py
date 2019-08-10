import string
import time

import requests
from bs4 import BeautifulSoup

import helper
import json


def checkPrice(data_dict):
    """
    Checks the price of the product and sends email if discount is sufficient.

    Parameter:
        data_dict (dict): Dictionary containing user data
    """
    headers = {}
    headers["User-Agent"] = data_dict["user_agent"]
    page = requests.get(data_dict["URL"], headers=headers)

    json_file = open("details.json", "r+")
    json_data = json.load(json_file) 

    soup = BeautifulSoup(page.content, "html.parser")
    data_dict["title"] = soup.find(id="productTitle").get_text().strip()

    for id in json_data["price_id"]:
        try:
            data_dict["price"] = float(
                soup.find(id=id).get_text()[1:])
            break
        except:
            pass
            
    try:
        for id in json_data["savings_id"]:
            try:
                savings = soup.find(id=id).get_text()
                break
            except:
                pass

        data_dict["savings"] = savings.replace("£", "GBP ")
        start = data_dict["savings"].index("(")
        stop = data_dict["savings"].index("%")

        # percentage discount
        data_dict["per_savings"] = float(data_dict["savings"][start + 1: stop])
        print("Discount available:", data_dict["per_savings"], "%")
    except:
        print("No discount is currently available!")
        data_dict["savings"] = "\nNo savings at the moment."
        data_dict["per_savings"] = 0

    if data_dict["per_savings"] >= data_dict["discount"]:
        # send email if discount criteria is met
        sendEmail(data_dict)
    else:
        helper.login(data_dict["username"], data_dict["password"])
        print("\nSorry, the product is currently not available at the desired price!")
        print("NAME:", data_dict["title"])
        print("CURRENT PRICE: GBP", data_dict["price"], "\n")

    json_file.close()


def sendEmail(data_dict):
    """
    Sends email from user's email ID to themself.

    Parameter:
        data_dict (dict): Dictionary containing user data
    """
    # login to email
    server = helper.login(data_dict["username"], data_dict["password"])

    # write the email subject and body
    subject = "PRICE DROP: \"" + \
        data_dict["title"][:30] + "...\" available now for GBP " + \
        str(data_dict["price"])

    body = "The following product that you were interested in is now available at a discount!" +\
        "\n\nName: " + data_dict["title"] + \
        "\nCurrent price: GBP " + str(data_dict["price"]) + \
        data_dict["savings"] + \
        "\nCheck out this link:\n" + data_dict["URL"]

    # form the email message
    msg = "Subject: {0}\n\n{1}".format(subject, body)

    # send the message using the SMTP object, server
    server.sendmail(data_dict["username"], data_dict["username"], msg)

    # exit from loop in __main__ if email is sent
    print("...Email sent successfully!")
    server.quit()
    exit()

