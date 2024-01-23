from bs4 import BeautifulSoup
import requests
import time
import csv

stat_names = ["HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"]
#with open("pokemon.csv", "w") as dummy:
#    dummy.write("No,Species,Type,HP,Atk,Def,SpA,SpD,Spe,Total\n")

for pokedex_no in range(494,650):
    pokemon = {}
    pokemon["no"] = f"{pokedex_no:03}"
    url = f"https://www.serebii.net/pokedex-bw/{pokedex_no:03}.shtml"
    request = requests.get(url)
    soup = BeautifulSoup(request.content, "html.parser")

    info_panel = soup.main.div.div.find_all("table", class_="dextable")[1].find_all("td", class_="fooinfo")
    pokemon["name"] = info_panel[0].text
    if "Nidoran" in pokemon["name"]:
        if pokemon["name"][-1] == "♀":
            gender = "-F"
        else:
            gender = "-M"
        pokemon["name"] = pokemon["name"][:-1] + gender

    type_links = info_panel[4].find_all("a")
    pokemon["type"] = ""
    for i, type in enumerate(type_links):
        if i == 1:
            pokemon["type"] += "/"
        pokemon["type"] += type["href"][12:-6].capitalize()

    abilities = info_panel[5].find_all("a")
    pokemon["abilities"] = ""
    for i, ability in enumerate(abilities):
        if i > 0:
            pokemon["abilities"] += "/"
        pokemon["abilities"] += ability.text

    stats = soup.find_all("table", class_="dextable")[-1].find_all("td", class_="fooinfo")[1:7]
    bst = 0
    for stat, name in zip(stats, stat_names):
        pokemon[name] = stat.text
        bst += int(stat.text)
    pokemon["BST"] = str(bst)
    print(pokemon.values())
    with open("pokemon.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(pokemon.values())

    