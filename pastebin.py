from bs4 import BeautifulSoup
import requests
import os.path
import time
import codecs


def grabLinks(url="http://pastebin.com/archive"):
    links = []
    soup = BeautifulSoup(requests.get(url).text)
    for link in soup.find('table').find_all('a'):
        if('archive' not in link['href']):
            links.append(link['href'][1:])
    return links


def expires(pid):
    soup = BeautifulSoup(requests.get("http://pastebin.com/" + pid).text)
    if('expires: never' in
            str(soup.find('div', class_="paste_box_line2")).lower()):
        return False
    return True


def savePastebin(pid, error=False):
    soup = BeautifulSoup(
        requests.get(
            "http://pastebin.com/raw.php?i={}".format(pid)).text)
    with codecs.open("PBArchiver/{}.txt".format(pid), "w+", 'utf-8') as pfile:
        pfile.write(str(soup))


def main(refreshRate=30):
    if(not os.path.exists("PBArchiver/")):
        print("[PBArchiver] Archives folder does not exist. Creating..")
        os.makedirs("PBArchiver/")
        print("[PBArchiver] Archives folder created!")
    else:
        print("[PBArchiver] Archives folder exists!")
    while True:
        pids = grabLinks()
        for pid in pids:
            if(expires(pid) and
                    not os.path.isfile("PBArchiver/{}.txt".format(pid))):
                print("[PBArchiver] Trying PID #{}".format(pid))
                savePastebin(pid)
        print("[PBArchiver] Sleeping for {} seconds..".format(refreshRate))
        time.sleep(refreshRate)

main()
