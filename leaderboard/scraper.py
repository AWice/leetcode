from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome("c:/chromedriver.exe")
URL = "https://leetcode.com/contest/{}/ranking/{}/"

# Populate contests[]
contests = ["warm-up-contest"]

for d in range(2, 10):
    contests.append("leetcode-weekly-contest-" + str(d))

for d in range(1, 5):
    e = ("-" + str(d)) if d > 1 else ""
    contests.append("smarking-algorithm-contest" + e)

for d in range(10, 16):
    contests.append("leetcode-weekly-contest-" + str(d))

for d in ("16a", "16b", "17", "18a", "18b"):
    contests.append("leetcode-weekly-contest-" + d)

for d in range(19, 58):
    contests.append("leetcode-weekly-contest-" + str(d))

for d in range(58, 62):
    contests.append("weekly-contest-" + str(d))

contests.append("weekly-contest-by-app-academy")

for d in range(63, 139):
    contests.append("weekly-contest-" + str(d))

d0 = 139
for d in range(1, 42):
    contests.append("biweekly-contest-" + str(d))
    contests.append("weekly-contest-" + str(d0))
    d0 += 1
    contests.append("weekly-contest-" + str(d0))
    d0 += 1

#contests.pop()
#contests.pop()

# Read results
ZERO = "###@@@ZERO@@@###"
for i, contest in enumerate(contests):
    fname = str(i).zfill(3) + contest + ".txt"
    fname = "c:/leetcode/leaderboard/scraped/" + fname
    try:
        with open(fname, encoding="utf-8") as fi:
            res = fi.read()
        if res:
            print("skipping", fname)
            continue
    except:
        pass

    print("starting", fname)
    results = []
    firstzero = False
    for d in range(1, 11111):
        url = URL.format(contest, str(d))
        browser.get(url)
        try:
            myElem = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ranking-username"))
            )
        except:
            break
        soup = BS(browser.page_source, "html.parser")
        names = soup.find_all("a", {"class": "ranking-username"})
        found = False
        for name in names:
            found = True
            if firstzero is False:
                score = name.text #next_element.next_element.next_element.next_element.next_element.text

                if score == "0":
                    results.append(ZERO)
                    firstzero = True
            results.append(name.text)

        if not found:
            break

    print("!", contest, len(results))
    with open(fname, "w", encoding="utf-8") as fo:
        fo.write("\n".join(results))

print("done")
