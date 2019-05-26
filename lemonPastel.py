import argparse
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

######################### CONSTANT VALUES #################################
URL = "https://eksisozluk.com"
HEADLESS_PATH = (os.getcwd() + "/" + "chromedriver")
# Put your chrome driver to same folder with script itself.
######################### Selenium Config #################################
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=HEADLESS_PATH)
######################### ArgParser Config #################################
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--thread", help="Aradığınız thread'in \
ismini girdi olarak veriniz. Birden fazla kelime ile arama yaparken \
araya '-' koyunuz.")
parser.add_argument(
    "-kw",
    "--keyword",
    help="Thread içinde arama yapmak için bir keyword veriniz.")
parser.add_argument(
    "-bw",
    "--between",
    nargs=2,
    type=int,
    help="Bir thread içinde belirli sayfalar arasını girdi olarak veriniz.")
parser.add_argument(
    "-u",
    "--user",
    help="Thread içinde arama yapmak için bir keyword veriniz.")
args = parser.parse_args()
"""
I added this kwargs dict because i cant iterate through a class.
"""
configArgs = {
    "thread": args.thread,
    "searchKeyword": args.keyword,
    "between": args.between,
    "user": args.user,
}
##################### Functions for Every Parameter #####################


def main(**kwargs):
    if ((kwargs["thread"] is None) and (kwargs["searchKeyword"] is None) and
        (kwargs["user"] is None) and (kwargs["between"] is None)):
            gundem()

    elif ((kwargs["thread"] is not None) and
        (kwargs["searchKeyword"] is None) and
        (kwargs["user"] is None) and (kwargs["between"] is None)):
            threadArg(kwargs["thread"])

    elif ((kwargs["thread"] is not None) and
        (kwargs["searchKeyword"] is None) and
        (kwargs["user"] is None) and
        (kwargs["between"] is not None)):
            threadBetweenArg(kwargs["thread"], kwargs["between"])

    elif ((kwargs["thread"] is not None) and
        (kwargs["searchKeyword"] is not None) and
        (kwargs["user"] is None) and
        (kwargs["between"] is None)):
            threadKeywordArg(kwargs["thread"], kwargs["searchKeyword"])

    elif ((kwargs["thread"] is None) and
        (kwargs["searchKeyword"] is None) and
        (kwargs["user"] is not None) and
        (kwargs["between"] is None)):
            userArg(kwargs["user"])

    else:
        print("""
        Sadece şu şekilde kullanabilirsiniz.
        -t thread name
        -t thread name -kw keyword
        -t thread name -bw first page last page
        -u username
        """)


"""
- This is the function that executes if we are giving no argument to program.
"""


def gundem():

    print("Lütfen kaynak kod alırken bekleyin.")
    driver.get(URL)
    source = driver.page_source
    print("Kaynak kod parçalara ayırılıyor.")
    soup = BeautifulSoup(source, "html.parser")
    threadList = []
    threadListHTML = soup.find("ul", class_="topic-list")
    threadLinks = threadListHTML.find_all("a")

    for link in threadLinks:
        startNumber = link["href"].find("--") + 3
        link["href"] = link["href"][:startNumber]
        threadList.append(URL + link["href"])

    for link in threadList:
        print(link + "\n")

    print(str(len(threadList)) + " tane link sağlandı.")


"""
- This is the function that executes
if we are giving thread argument to program.
- It prints the whole thread to a .txt file
with authors of comments and timestamps.
"""


def threadArg(thread):
    driver.get(URL + "/" + thread)
    threadUrl = driver.current_url
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    pageCount = int(soup.find("a", {"class": "last"}).get_text())
    content = []
    author = []
    timestamp = []

    for page in range(pageCount):
        driver.get(threadUrl + "?p=" + str(page + 1))
        threadSource = driver.page_source
        soupThread = BeautifulSoup(threadSource, "html.parser")
        content.append(soupThread.find_all("div", {"class": "content"}))
        author.append(soupThread.find_all("a", {"class": "entry-author"}))
        timestamp.append(soupThread.find_all("a", {"class": "entry-date"}))

    threadText = open("{}.txt".format(thread), "x")
    threadText.write(
        "\t\t\t\t########### {} ############\t\t\t\t\n".format(thread).upper())
    for a, b, c in zip(author, content, timestamp):
        for aut, cont, time in zip(a, b, c):
            threadText.write(
            "{}: \
            \n\t{} \
            \n\t\t\t\t\t\t{} \
            \n".format(aut.get_text(),
                cont.get_text(),
                time.get_text()))


def threadKeywordArg(thread, searchKeyword):
    driver.get(URL + "/" + thread)
    threadUrl = driver.current_url
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    pageCount = int(soup.find("a", {"class": "last"}).get_text())
    content = []
    author = []
    timestamp = []

    for page in range(pageCount):
        driver.get(threadUrl + "?p=" + str(page + 1))
        threadSource = driver.page_source
        soupThread = BeautifulSoup(threadSource, "html.parser")
        content.append(soupThread.find_all("div", {"class": "content"}))
        author.append(soupThread.find_all("a", {"class": "entry-author"}))
        timestamp.append(soupThread.find_all("a", {"class": "entry-date"}))

    threadText = open("{}.txt".format(thread), "x")
    threadText.write(
        "\t\t\t\t########### {} ############\t\t\t\t\n".format(thread).upper())
    for a, b, c in zip(author, content, timestamp):
        for aut, cont, time in zip(a, b, c):
            if searchKeyword in cont.get_text():
                threadText.write("{}: \
                \n\t{} \
                \n\t\t\t\t\t\t{}\n".format(aut.get_text(),
                cont.get_text(),
                time.get_text()))


def userArg(user):
    driver.get(URL + "/biri/" + user)
    try:
        ad = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Kapat")))
        ad.click()
    except BaseException:
        print("No AD1!")
    toastClose = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "toast-close")))
    toastClose.click()
    # scrollElement = driver.find_element_by_class_name("load-more-entries")
    while True:
        driver.execute_script(
            "window.scrollBy(0, document.body.scrollHeight);")
        try:
            ad = driver.find_element_by_link_text("Kapat")
            ad.click()
        except BaseException:
            print("No AD2!")
        try:
            scrollElement = WebDriverWait(
                driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "load-more-entries")))
        except BaseException:
            pass
        if scrollElement.is_displayed():
            try:
                try:
                    scrollElement.click()
                    ad = driver.find_element_by_link_text("Kapat")
                    # find_element_by_id("interstitial-close-link")
                    ad.click()
                except BaseException:
                    print("No AD3!")
            except BaseException:
                break
        else:
            break

    thread = []
    content = []
    timestamp = []
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    thread.append(soup.find_all("span", {"itemprop": "name"}))
    content.append(soup.find_all("div", {"class": "content"}))
    timestamp.append(soup.find_all("a", {"class": "entry-date"}))
    content[0].pop(0)

    userText = open("{}.txt".format(user), "x")

    userText.write(
        "\t\t\t\t########### {} ############\t\t\t\t\n".format(user).upper())
    userText.write(
        "\t\t\t\t########### Toplam Entry : {} ############\t\t\t\t\n".format(
            soup.find(
                "li", {
                    "id": "entry-count-total"}).get_text()).upper())
    for d, b, c in zip(thread, content, timestamp):
        for thr, cont, time in zip(d, b, c):
            userText.write("{}: \
            \n\t{} \
            \n\t\t\t\t\t\t{}\n".format(thr.get_text().upper(),
            cont.get_text(),
            time.get_text()))
    userText.close()


def threadBetweenArg(thread, between):
    driver.get(URL + "/" + thread)
    threadUrl = driver.current_url
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    pageCount = int(soup.find("a", {"class": "last"}).get_text())
    if (between[0] > between[1]) or (between[1] > pageCount):
        print("Lütfen girdiğiniz değerlere dikkat edin.")
    content = []
    author = []
    timestamp = []

    for page in range(between[0] - 1, between[1]):
        driver.get(threadUrl + "?p=" + str(page + 1))
        threadSource = driver.page_source
        soupThread = BeautifulSoup(threadSource, "html.parser")
        content.append(soupThread.find_all("div", {"class": "content"}))
        author.append(soupThread.find_all("a", {"class": "entry-author"}))
        timestamp.append(soupThread.find_all("a", {"class": "entry-date"}))

    threadText = open("{}.txt".format(thread), "x")
    threadText.write(
        "\t\t\t\t########### {} ############\t\t\t\t\n".format(thread).upper())
    for a, b, c in zip(author, content, timestamp):
        for aut, cont, time in zip(a, b, c):
            threadText.write("{}: \
            \n\t{} \
            \n\t\t\t\t\t\t{}\n".format(
                aut.get_text(),
                cont.get_text(),
                time.get_text()))


main(**configArgs)

