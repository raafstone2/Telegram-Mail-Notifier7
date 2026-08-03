import requests
from bs4 import BeautifulSoup
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


CHANNEL_NAME = "کانال ۷ تلگرام - V2ghostvpn"

CHANNEL_URL = "https://t.me/s/V2ghostvpn"

LAST_FILE = "last_message.txt"


GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_TO = os.environ.get("GMAIL_TO")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")


headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_messages():

    r = requests.get(
        CHANNEL_URL,
        headers=headers,
        timeout=20
    )

    soup = BeautifulSoup(
        r.text,
        "html.parser"
    )

    messages = soup.find_all(
        "div",
        class_="tgme_widget_message_text"
    )

    result = []

    for msg in messages[-20:]:

        result.append(
            msg.get_text(
                "\n",
                strip=True
            )
        )

    return result



def extract_configs(text):

    pattern = (
        r"(?:vless|vmess|trojan|ss|ssr)://[^\s]+"
    )

    configs = re.findall(
        pattern,
        text
    )

    return configs



def read_old_message():

    if os.path.exists(LAST_FILE):

        with open(
            LAST_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    return ""



def save_message(message):

    with open(
        LAST_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(message)



def send_email(configs):

    msg = MIMEMultipart()

    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_TO

    msg["Subject"] = (
        CHANNEL_NAME
        +
        " - کانفیگ جدید V2Ray"
    )


    body = (
        "کانفیگ جدید پیدا شد:\n\n"
        "منبع:\n"
        +
        CHANNEL_NAME
        +
        "\n\n-----------------\n\n"
        +
        "\n\n".join(configs)
    )


    msg.attach(
        MIMEText(
            body,
            "plain",
            "utf-8"
        )
    )


    server = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    )


    server.login(
        GMAIL_USER,
        GMAIL_APP_PASSWORD
    )


    server.sendmail(
        GMAIL_USER,
        GMAIL_TO,
        msg.as_string()
    )


    server.quit()



messages = get_messages()


all_text = "\n\n".join(messages)


configs = extract_configs(
    all_text
)


if not configs:

    print(
        "هیچ کانفیگی پیدا نشد"
    )

    exit()



config_text = "\n\n".join(configs)


old_message = read_old_message()



if config_text != old_message:


    save_message(
        config_text
    )


    send_email(
        configs
    )


    print(
        "ایمیل ارسال شد"
    )


else:

    print(
        "کانفیگ جدیدی وجود ندارد"
    )
