import smtplib
from getpass import getpass


def inputDetails():
    data_dict = {}
    print("~ Amazon UK Price Tracker ~")

    data_dict["user_agent"] = input("Enter your user agent (Google it!):\n")
    data_dict["URL"] = input("Enter product URL:\n")

    disc = ""
    while(True):
        try:
            disc = float(input("Enter the discount % required: "))
            break
        except:
            pass
    data_dict["discount"] = float(disc)

    data_dict["often"] = float(
        input("Enter (in secs.) how often you'd like to check the price: "))

    data_dict["username"] = input("Enter your g-mail ID: ")
    data_dict["password"] = getpass("Enter your password: ")
    return data_dict


def login(username, password):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.ehlo()
    try:
        server.login(username, password)
    except:
        raise Exception("\n\nPlease ensure that either ONE of the following is complete:"
                        "\n1. Enable Less Secure Apps on your Google Account"
                        "\n2. Enable Two-Factor Authentication, and generate a new app password for Mail."
                        "\n\nThen recheck your password and try again!")
    return server


def getTime(t):
    if t >= 3600:
        s = str(round(t // (3600), 2)) + " hours.\n"
    elif t >= 60:
        s = str(t // 60) + " mins, " + str(t % 60) + " secs.\n"
    else:
        s = str(t) + " secs.\n"
    return s
