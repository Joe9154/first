import requests
import urllib.parse
import time
from bs4 import BeautifulSoup
from datetime import datetime

# variables
url = "https://www.avto.net/Ads/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=1000&cenaMax=5000&letnikMin=2007&letnikMax=2090&bencin=201&starost2=999&oblika=0&ccmMin=0&ccmMax=2500&mocMin=0&mocMax=999999&kmMin=0&kmMax=200000&kwMin=0&kwMax=999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&EToznaka=0&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1000100020&EQ8=101000000&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PIAOut=&PSLO=&akcija=0&paketgarancije=&broker=0&prikazkategorije=0&kategorija=0&ONLvid=0&ONLnak=0&zaloga=10&arhiv=0&presort=3&tipsort=DESC&stran=1"
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}
carsNazivi = []
starttime = time.time()

# add all cars to list
def addAllCarsToList():
    print("Adding all cars to list")

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    cars = soup.find_all('div', {'class': 'GO-Results-Row'})
    for car in cars:
        naziv = car.find("div", {"class":"GO-Results-Naziv"}).span.text
        carsNazivi.append(naziv)

# send notification
def sendNotification(title, message, action):
    id = 'YxhKmpstf'
    title = urllib.parse.quote(title)
    message = message
    action = urllib.parse.quote(action)
    type = 'push'
    url = f"https://wirepusher.com/send?id={id}&title={title}&message={message}&type={type}&action={action}"
    r = requests.get(url)
    if r.status_code == 200:
        print('Successfully sent notification')
    elif r.status_code == 404:
        print('Error sending notification')


# check the website, if new car (thats not on list yet), send notif.
def checkWebsite():
    print("Checking for new cars - ", str(datetime.now())[:-7])
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    cars = soup.find_all('div', {'class': 'GO-Results-Row'})
    for car in cars:
        naziv = car.find("div", {"class":"GO-Results-Naziv"}).span.text
        if naziv not in carsNazivi:
            print("Found new car:", naziv)
            #add to list
            carsNazivi.append(naziv)
            #send notif
            link = "https://www.avto.net/" + car.find_all('a', {'class':'stretched-link'})[0]['href'][3:]
            letnik = car.find("tbody").find_all("tr")[0].find_all("td")[1].text 
            prevozenih = car.find("tbody").find_all("tr")[1].find_all("td")[1].text 
            gorivo = car.find("tbody").find_all("tr")[2].find_all("td")[1].text.split(" ")[0] 
            menjalnik = car.find("tbody").find_all("tr")[3].find_all("td")[1].text 
            cena = car.find_all('div', {'class': 'GO-Results-Price-Mid'})
            if cena == []:
                cena = car.find_all('div', {'class': 'GO-Results-Top-Price-Mid'})[0].text[1:-1]
            else:
                cena = car.find_all('div', {'class': 'GO-Results-Price-Mid'})[0].text[1:-1]
            sendMessage = f"Letnik {letnik}, {prevozenih}, {gorivo}, {menjalnik}, {cena}"
            # posljemo notification
            sendNotification(title=naziv, message=sendMessage, action=link)
            a = ""

addAllCarsToList()
seconds = 10.0

while True:
    checkWebsite()
    time.sleep(seconds - ((time.time() - starttime) % seconds))

print("ENDING SCRIPT")
