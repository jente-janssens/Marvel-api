#importing modules
#pip3 install pyfiglet voor banners te maken
import pyfiglet
import urllib.parse
import requests
import hashlib
import time

#create banners
Goodbye_banner = pyfiglet.figlet_format("Goodbye")
welcome_banner = pyfiglet.figlet_format("Welcome")
NotFound_banner = pyfiglet.figlet_format("No Results")

#de link voor de API
api = "http://gateway.marvel.com/v1/public/characters?"
#Api keys provide your own.
public_key = ""
private_key = ""
#zet tijd op huidige tijd
time=time.time()
timestamp = str(time)
#MD5 Hash word gebruikt om een correcte URL te maken voor data in te lezen
pre_hash = timestamp + private_key + public_key
result = hashlib.md5(pre_hash.encode())
#maakt banner aan om gebruiker te verwelkomen
print(welcome_banner)
#zichtbaar programma begint hier
while True:
    #gaat aan de gebruiker de naam van het character opvragen
    name = input("What is the name of the character u want to look up? (empty to quit)")
    #gaat het programma afsluiten als er een blank word gestuurt
    if name == "":
        print(Goodbye_banner)
        break
    #gaat de URL createren waar we de data gaan zoeken
    url = api + urllib.parse.urlencode({"name": name, "ts":timestamp, "apikey":public_key, "hash":result.hexdigest()})
    #Api data in JSON format
    data = requests.get(url).json()
    status = data["code"]
    #gaat zien ofdat API status 200 geeft. Dit is de code voor een geslaagde request
    if status == 200:
        #Als er geen resultaten waren maar geen fout code (naam bestaat niet of is niet gevonden door API)
        if data["data"]["total"] == 0:
            print(NotFound_banner)
            print(name+" was not found. Are you sure they exist in the marvel universe?")
            #gaat de ID,Naam,Omschrijven laten zien van de character als deze gevonden is
        else:
            print("API status: " + str(status))
            print("Name: " + name)
            print("Description: " + str(data["data"]["results"][0]["description"]))
            print(name + " appears in these comics.")
            print("")
            #Geeft een lijst van alle verhalen waar de character inzit
            for each in data["data"]["results"][0]["comics"]["items"]:
                print(each["name"])
            print("")
    