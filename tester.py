import json
from bs4 import BeautifulSoup
import requests
dic={}
with open("json/moves.json") as f_obj:
    dic = json.load(f_obj)
for movename in dic:
    move=dic.get(movename)
    if move.get("category")!="status":
        if move.get("type") in ["water", "fire", "grass", "ice", "electric", "psychic", "dragon", "dark"]:
            move["category"]="special"
        else:
            move["category"]="physical"
    if "effects" in move:
        move["effect"]= move.get("effects")
        del move["effects"]
    dic[movename] = move
with open("json/moves.json", "w") as f_obj:
    json.dump(dic, f_obj, indent=4)

'''
with open("pokedex.json") as f_obj:
    dic = json.load(f_obj)
dex={}
i=0
while i<151:
    print(i+1)
    pokemon = dic[i]
    name=pokemon.get("name")
    r=requests.get("https://pokemondb.net/pokedex/"+name+"/moves/1")
    soup = BeautifulSoup(r.content, "html.parser")
    list1=[]
    for element in soup.find("h3").previous_element.find_all("td"):
        list1.append(repr(element.string))
    pdex={}
    while len(list1)>0:
        level=list1.pop(0)
        move=list1.pop(0)
        for j in range(4):
            list1.pop(0)
        if level in pdex:
            if isinstance(pdex.get(level), list):
                list2=[]
                for p in pdex.get(level):
                    list2.append(p)
                list2.append(move)
                pdex[level]=list2
            else:
                pdex[level]=[pdex.get(level), move]
        else:
            pdex[level]=move
    dex[name] = pdex
    i+=1
with open("movedex.json", "w") as f_obj:
    json.dump(dex, f_obj, indent=4)'''