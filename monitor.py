import requests
import urllib3
from bs4 import BeautifulSoup
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import os

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://drh.sante.gov.ma/Pages/Concours_Ex_D_ParaMedical_D.aspx"

old_links = []
first_run = True

while True:
    print("جاري الفحص...")

    html = requests.get(URL, verify=False).text
    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a", href=True):

        text = a.get_text(strip=True)

        if "Liste" in text or "Résultat" in text:

            link = requests.compat.urljoin(URL, a["href"])

            if link not in old_links:

                old_links.append(link)

                if not first_run:

                    requests.get(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        params={
                            "chat_id": CHAT_ID,
                            "text": f"📢 جديد!\n\n{text}\n{link}"
                        }
                    )

                    print("✅ تم إرسال إشعار")

    first_run = False

    time.sleep(300)   # يفحص كل 5 دقائق
