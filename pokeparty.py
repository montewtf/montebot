import math
import random
import json

class party:
    def __init__(self, party):
        self.decon(party)
        
    def decon(self, party):
        self.p1 = party["1"]
        self.p2 = party["2"]
        self.p3 = party["3"]
        self.p4 = party["4"]
        self.p5 = party["5"]
        self.p6 = party["6"]
        if "7" in party:
            self.p7 = party["7"]
        else: self.p7 = None
        
    def recon(self):
        party = {"1":self.p1,
                 "2":self.p2,
                 "3":self.p3,
                 "4":self.p4,
                 "5":self.p5,
                 "6":self.p6,
                 }
        if self.p7 != None:
            party["7"] = self.p7
        return party
    
    def swap(self, s1:int, s2:int):
        if s1>6 or s2>6:
            return 1
        party = self.recon()
        if not party.get(str(s1)) or not party.get(str(s2)):
            return 1
        swap = party.get(str(s1))
        party[str(s1)] = party[str(s2)]
        party[str(s2)] = swap
        self.decon(party)
        return 0
    
    def remove(self, r1):
        if r1>6:
            return 1
        i=r1
        while i<6:
            if self.swap(i, i+1):
                break
            i+=1
        party=self.recon()
        party[str(i)] = None
        self.decon(party)
        return 0
    
    def add(self, a1):
        party = self.recon()
        if party["6"]!=None:
            return 0
        i=1
        while i<7:
            if party[str(i)] == None:
                party[str(i)] = a1
                self.decon(party)
                return i
            i+=1

class pokemon:
    def __init__(self, poke={}, species={}, level=0, hploss=0, name=None):
        if poke == {}:
            self.id = species["id"]
            self.species = species["name"]
            self.types = species["type"]
            self.base = species["base"]
            self.level = int(level)
            self.name = name
            self.status = None
            self.genIV()
            self.getStats()
            self.curhp = self.hp - hploss
            self.move1 = None
            self.move2 = None
            self.move3 = None
            self.move4 = None
            self.getMoves()
            self.catch = None
        else:
            self.id = poke["id"]
            self.species = poke["species"]
            self.types = poke["types"]
            self.base = poke["base"]
            self.level = poke["level"]
            self.name = poke["name"]
            self.status = poke["status"]
            iv = poke["iv"]
            self.ivattack = iv["Attack"]
            self.ivdefense = iv["Defense"]
            self.ivspeed = iv["Speed"]
            self.ivspecial = iv["Special"]
            self.ivhp = iv["HP"]
            self.getStats()
            self.curhp = poke["stats"].get("CurHP") - hploss
            moves = poke["moves"]
            self.move1 = moves["move1"]
            self.move2 = moves["move2"]
            self.move3 = moves["move3"]
            self.move4 = moves["move4"]
            if "catch" in poke:
                self.catch=poke["catch"]
            else: self.catch = None
            
    def genIV(self):
        self.ivattack = random.randint(0,15)
        self.ivdefense = random.randint(0,15)
        self.ivspeed = random.randint(0,15)
        self.ivspecial = random.randint(0,15)
        self.ivhp = (self.ivattack%2)*8+(self.ivdefense%2)*4+(self.ivspeed%2)*2+(self.ivspecial%2)*1

    def getStats(self):
        self.hp = math.floor((((self.base["HP"]+self.ivhp)*2+(math.sqrt(65535)/4))*(self.level/100))+self.level+10)
        self.attack = math.floor((((self.base["Attack"]+self.ivattack)*2+(math.sqrt(65535)/4))*(self.level/100))+5)
        self.defense = math.floor((((self.base["Defense"]+self.ivdefense)*2+(math.sqrt(65535)/4))*(self.level/100))+5)
        self.speed = math.floor((((self.base["Speed"]+self.ivspeed)*2+(math.sqrt(65535)/4))*(self.level/100))+5)
        self.special = math.floor((((self.base["Special"]+self.ivspecial)*2+(math.sqrt(65535)/4))*(self.level/100))+5)
        
    def getMoves(self):
        with open("json/movedex.json") as f_obj:
            dex = json.load(f_obj)
        moves=dex.get(self.species)
        i=self.level
        while i>0:
            if i==1 and isinstance(moves.get("1"), list):
                level1 = moves.get("1")
                if self.move1 in level1:
                    level1.pop(level1.index(self.move1))
                if self.move2 in level1:
                    level1.pop(level1.index(self.move2))
                if self.move3 in level1:
                    level1.pop(level1.index(self.move3))
                if self.move4 in level1:
                    level1.pop(level1.index(self.move4))
                while len(level1)>0:
                    if self.addMoves(level1.pop(0)):
                        break                    
            elif str(i) in moves:
                if self.addMoves(moves.get(str(i))):
                    break
            i-=1

    def addMoves(self, move):
        if self.move1 == None:
            self.move1 = move
            return 0
        elif self.move2 == None:
            self.move2 = move
            return 0
        elif self.move3 == None:
            self.move3 = move
            return 0
        elif self.move4 == None:
            self.move4 = move
            return 0
        else:
            return 1
        
    def export(self):
        summary = {
        "id" : self.id,
        "name" : self.name,
        "species" : self.species,
        "level" : self.level,
        "types" : self.types,
        "status" : self.status,
        "stats" : {
            "CurHP" : self.curhp,
            "HP" : self.hp,
            "Attack" : self.attack,
            "Defense" : self.defense,
            "Speed" : self.speed,
            "Special" : self.special,
            },
        "moves" : {
            "move1" : self.move1,
            "move2" : self.move2,
            "move3" : self.move3,
            "move4" : self.move4,
            },
        "iv" : {
            "HP" : self.ivhp,
            "Attack" : self.ivattack,
            "Defense" : self.ivdefense,
            "Speed" : self.ivspeed,
            "Special" : self.ivspecial,
            },
        "base" : self.base 
        }
        if self.catch != None:
            summary["catch"] = self.catch
            summary["run"] = 1
        return summary
    
class battle:
    def __init__(self, poke1, poke2):
        self.user = poke1
        self.target = poke2
        
    def attacks2(self, move1, move2):
        if self.user.speed > self.target.speed:
            self.attacks1(move1=move1)
            if self.target.curhp==0: return 0
            self.attacks1(move2=move2)
            return 1
        elif self.user.speed < self.target.speed:
            self.attacks1(move2=move2)
            if self.user.curhp==0: return 0
            self.attacks1(move1=move1)
            return 2
        else:
            if random.randint(0,1):
                self.attacks1(move1=move1)
                if self.target.curhp==0: return 0
                self.attacks1(move2=move2)
                return 1
            else:
                self.attacks1(move2=move2)
                if self.user.curhp==0: return 0
                self.attacks1(move1=move1)
                return 2
    
    def attacks1(self, move1=None, move2=None):
        if move1 != None:
            if move1["type"] in self.user.types:stab=1.5
            else:stab=1
            if False:
                typee="this is where type effectiveness goes"
            else:typee=1
            modifier=stab*typee*(random.randint(85,100)/100)
            if move1["category"]=="special":
                damage=math.floor(((2*self.user.level/5+2)*move1["power"]*self.user.special/self.target.special/50+2)*modifier)
                if damage==0: damage=1
            elif move1["category"]=="physical":
                damage=math.floor(((2*self.user.level/5+2)*move1["power"]*self.user.attack/self.target.defense/50+2)*modifier)
                if damage==0: damage=1
            else: damage=0
            self.target.curhp-=damage
            if self.target.curhp<0:self.target.curhp=0
        elif move2 != None:
            if move2["type"] in self.target.types:stab=1.5
            else:stab=1
            if False:
                typee="this is where type effectiveness goes"
            else:typee=1
            modifier=stab*typee*(random.randint(85,100)/100)
            if move2["category"]=="special":
                damage=math.floor(((2*self.target.level/5+2)*move2["power"]*self.target.special/self.user.special/50+2)*modifier)
                if damage==0: damage=1
            elif move2["category"]=="physical":
                damage=math.floor(((2*self.target.level/5+2)*move2["power"]*self.target.attack/self.user.defense/50+2)*modifier)
                if damage==0: damage=1
            else: damage=0
            self.user.curhp-=damage
            if self.user.curhp<0:self.user.curhp=0
    
    def attacks0(self):
        pass