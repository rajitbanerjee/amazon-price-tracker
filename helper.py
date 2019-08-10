import smtplib
from getpass import getpass
import json


def inputDetails():
    """
    Inputs user details.

    Returns:
        data_dict (dict): Dictionary containing user data
    """
    data_dict = {}
    with open("user_details.json", "r+") as json_file:
        json_data = json.load(json_file)
        if "user_agent" in json_data:
            data_dict["user_agent"] = json_data["user_agent"]
        else:
            data_dict["user_agent"] = input("Enter your user agent (Google it!):\n")
            json_data["user_agent"] = data_dict["user_agent"]
            json.dump(json_data, json_file)

        data_dict["URL"] = input("\nEnter product URL:\n")
        disc = ""
        while(True):
            # Continuously ask for input until valid figure is provided
            try:
                disc = float(input("\nEnter the discount % required: "))
                break
            except:
                pass

        data_dict["discount"] = float(disc)
        data_dict["often"] = float(
            input("\nEnter (in secs.) how often you'd like to check the price: "))

        # input username or load from json
        takeInput = False
        if "username" in json_data:
            print("Gmail ID:", json_data["username"])
            ch = input("Proceed? (y/ n")
            if ch in ['Y', 'y']:
                data_dict["username"] = json_data["username"]
            else:
                takeInput = True
        elif "username" not in json_data or takeInput:
            data_dict["username"] = input("\nEnter your Gmail ID: ")
            json_data["username"] = data_dict["username"]
            json.dump(json_data, json_file)
        # input password safely
        data_dict["password"] = getpass("Enter your password: ")

    return data_dict


def login(username, password):
    """
    Attempts to login to user's Gmail account.

    Parameters:
        username (str): User's email ID
        password (str): User's email password
    Returns:
        server (smtplib.SMTP): SMTP object after logging in to email
    """
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
    """
    Returns a string after converting time in seconds to hours/mins/secs

    Paramters:
        t (float): time in seconds
    Returns:
        s (str): number of hours, if more than 1 hour
                number of minutes and seconds, if more than 1 minute
                number of seconds, otherwise
    """
    if t >= 3600:
        s = str(round(t // (3600), 2)) + " hours.\n"
    elif t >= 60:
        s = str(t // 60) + " mins, " + str(t % 60) + " secs.\n"
    else:
        s = str(t) + " secs.\n"
    return s
