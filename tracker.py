import string
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from helper import getTime, inputDetails, login


def checkPrice(**data_dict):
    headers = {}
    headers["User-Agent"] = data_dict["user_agent"]
    page = requests.get(data_dict["URL"], headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")
    data_dict["title"] = soup.find(id="productTitle").get_text().strip()
    data_dict["price"] = float(
        soup.find(id="priceblock_ourprice").get_text()[1:])

    savings = soup.find(id="regularprice_savings").get_text()
    if savings == None:
        print("No discount is currently available!")
        data_dict["per_savings"] = 0
    else:
        data_dict["savings"] = savings.replace("£", "GBP ")
        start = data_dict["savings"].index("(")
        stop = data_dict["savings"].index("%")

        # percentage discount
        data_dict["per_savings"] = float(data_dict["savings"][start+1:stop])

    if data_dict["per_savings"] >= data_dict["discount"]:
        # send email if discount criteria is met
        sendEmail(**data_dict)
    else:
        login(data_dict["username"], data_dict["password"])
        print("\nSorry, the product isn't available at the desired price!")
        print("NAME:", data_dict["title"])
        print("CURRENT PRICE: GBP", data_dict["price"], "\n")

    return data_dict


def sendEmail(**data_dict):
    server = login(data_dict["username"], data_dict["password"])
    subject = "PRICE DROP: \"" + \
        data_dict["title"] + "\" available now for GBP " + \
        str(data_dict["price"])

    body = "The following product that you were interested in is now available at a discount!" +\
        "\n\nName: " + data_dict["title"] + \
        "\nCurrent price: GBP" + str(data_dict["price"]) + \
        data_dict["savings"] + \
        "\nCheck out this link:\n" + data_dict["URL"]

    msg = "Subject: {0}\n\n{1}".format(subject, body)

    server.sendmail(data_dict["username"], data_dict["username"], msg)

    # exit from loop in __main__ if email is sent
    print("...Email sent successfully!")
    exit()

    server.quit()


if __name__ == "__main__":
    data_dict = inputDetails()
    s = getTime(data_dict["often"])

    iters = 0
    while(True):
        iters += 1
        print("\nCheck #", iters, "on:", datetime.today())
        data_dict = checkPrice(**data_dict)
        print("Price will be checked every " + s)
        time.sleep(data_dict["often"])
