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
    def __init__(self, poke={}, species={}, level=0, name=None):
        if poke == {}:
            self.id = species["id"]
            self.species = species["name"]
            self.types = species["type"]
            self.base = species["base"]
            self.catch = species["catch"]
            self.xptype = species["xptype"]
            self.xpyield = species["xpyield"]
            self.level = int(level)
            self.curxp = self.__getXP(self.level)
            self.nextxp = self.__getXP(self.level+1)
            self.name = name
            self.status = None
            self.__genIV()
            self.__getStats()
            self.curhp = self.hp
            self.move1 = None
            self.move2 = None
            self.move3 = None
            self.move4 = None
            self.__getMoves()
            self.part = None
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
            self.__getStats()
            self.curhp = poke["stats"].get("CurHP")
            moves = poke["moves"]
            self.move1 = move(moves["move1"]["name"],moves["move1"]["pp"])
            if moves["move2"]!=None:self.move2 = move(moves["move2"]["name"],moves["move2"]["pp"])
            else: self.move2=None
            if moves["move3"]!=None:self.move3 = move(moves["move3"]["name"],moves["move3"]["pp"])
            else: self.move3=None
            if moves["move4"]!=None:self.move4 = move(moves["move4"]["name"],moves["move4"]["pp"])
            else: self.move4=None
            xp = poke["xp"]
            self.xptype = xp["xptype"]
            self.curxp = xp["cur"]
            self.nextxp = xp["next"]
            if "catch" in poke:
                self.catch=poke["catch"]
            else: self.catch = None
            if "xpyield" in poke:
                self.xpyield=poke["xpyield"]
            else: self.xpyield = None
            if "participated" in poke:
                self.part=poke["participated"]
            else: self.part = None
            
    def __genIV(self):
        self.ivattack = random.randint(0,15)
        self.ivdefense = random.randint(0,15)
        self.ivspeed = random.randint(0,15)
        self.ivspecial = random.randint(0,15)
        self.ivhp = (self.ivattack%2)*8+(self.ivdefense%2)*4+(self.ivspeed%2)*2+(self.ivspecial%2)*1

    def __getStats(self):
        self.hp = math.floor((((self.base["HP"]+self.ivhp)*2+(math.sqrt(65535)/4))*(self.level/100))+self.level+10)
        self.attack = math.floor((((self.base["Attack"]+self.ivattack)*2+(math.sqrt(65535)/4))*(self.level/100))+5)
        self.defense = math.floor((((self.base["Defense"]+self.ivdefense)*2+(math.sqrt(65535)/4))*(self.level/100))+5)
        self.speed = math.floor((((self.base["Speed"]+self.ivspeed)*2+(math.sqrt(65535)/4))*(self.level/100))+5)
        self.special = math.floor((((self.base["Special"]+self.ivspecial)*2+(math.sqrt(65535)/4))*(self.level/100))+5)
        
    def __getMoves(self):
        with open("json/movedex.json") as f_obj:
            dex = json.load(f_obj)
        moves=dex.get(self.species)
        i=self.level
        while i>0:
            if i==1 and isinstance(moves.get("1"), list):
                level1 = moves.get("1")
                if self.move1!=None:
                    if self.move1.name in level1:
                        level1.pop(level1.index(self.move1.name))
                if self.move2!=None:
                    if self.move2.name in level1:
                        level1.pop(level1.index(self.move2.name))
                if self.move3!=None:
                    if self.move3.name in level1:
                        level1.pop(level1.index(self.move3.name))
                if self.move4!=None:
                    if self.move4.name in level1:
                        level1.pop(level1.index(self.move4.name))
                while len(level1)>0:
                    if self.addMove(level1.pop(0)):
                        break                    
            elif str(i) in moves:
                if self.addMove(moves.get(str(i))):
                    break
            i-=1
    
    def __getXP(self, level):
        if self.xptype=="Slow":
            xp=math.floor(level**3*5/4)
        elif self.xptype=="MedSlow":
            xp=math.floor(level**3*6/5-level**2*15+level*100-140)
        elif self.xptype=="MedFast":
            xp=math.floor(level**3)
        elif self.xptype=="Fast":
            xp=math.floor(level**3*4/5)
        return xp        

    def levelup(self):
        result=0
        while self.curxp >= self.nextxp:
            self.level+=1
            self.nextxp=self.__getXP(self.level+1)
            result=1
        with open("json/movedex.json") as f_obj:
            dex = json.load(f_obj)
        movedex=dex.get(self.species)
        if result==1:
            if str(self.level) in movedex:
                if not self.addMove(movedex.get(str(self.level))):
                    return [result,1,movedex.get(str(self.level))]
                else:
                    return [result,2,movedex.get(str(self.level))]
            else: return [result,0]
        else: return [0]
        
    def addMove(self, nmove, slot=None):
        if slot == None:
            if self.move1 == None:
                self.move1 = move(nmove.lower())
                return 0
            elif self.move2 == None:
                self.move2 = move(nmove.lower())
                return 0
            elif self.move3 == None:
                self.move3 = move(nmove.lower())
                return 0
            elif self.move4 == None:
                self.move4 = move(nmove.lower())
                return 0
            else:
                return 1
        else:
            if slot==1:
                self.move1 = move(nmove.lower())
                return 2
            elif slot==2:
                self.move2 = move(nmove.lower())
                return 2
            elif slot==3:
                self.move3 = move(nmove.lower())
                return 2
            elif slot==4:
                self.move4 = move(nmove.lower())
                return 2
        
    def export(self):
        moves={}
        moves["move1"]=self.move1.export()
        if self.move2!=None: moves["move2"]=self.move2.export()
        else: moves["move2"]=None
        if self.move3!=None: moves["move3"]=self.move3.export()
        else: moves["move3"]=None
        if self.move4!=None: moves["move4"]=self.move4.export()
        else: moves["move4"]=None
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
        "moves" : moves,
        "iv" : {
            "HP" : self.ivhp,
            "Attack" : self.ivattack,
            "Defense" : self.ivdefense,
            "Speed" : self.ivspeed,
            "Special" : self.ivspecial,
            },
        "base" : self.base,
        "xp" : {
            "xptype" : self.xptype,
            "cur" : self.curxp,
            "next" : self.nextxp,
            },
        }
        if self.catch != None:
            summary["catch"] = self.catch
            summary["run"] = 1
        if self.xpyield != None:
            summary["xpyield"] = self.xpyield
        if self.part != None:
            summary["participated"] = self.part
        return summary
    
class battle:
    def __init__(self, poke1, poke2):
        self.user = poke1
        self.target = poke2
        
    def attacks2(self, move1, move2):
        if self.user.speed > self.target.speed:
            t1=self.attacks1(move1=move1)
            if self.target.curhp==0: return [0, t1]
            t2=self.attacks1(move2=move2)
            return [1, t1, t2]
        elif self.user.speed < self.target.speed:
            t1=self.attacks1(move2=move2)
            if self.user.curhp==0: return [0, t1]
            t2=self.attacks1(move1=move1)
            return [2, t1, t2]
        else:
            if random.randint(0,1):
                t1=self.attacks1(move1=move1)
                if self.target.curhp==0: return [0, t1]
                t2=self.attacks1(move2=move2)
                return [1, t1, t2]
            else:
                t1=self.attacks1(move2=move2)
                if self.user.curhp==0: return [0, t1]
                t2=self.attacks1(move1=move1)
                return [2, t1, t2]
    
    def attacks1(self, move1=None, move2=None):
        if move1 != None:
            if move1.type in self.user.types:stab=1.5
            else:stab=1
            typee=self.types(move1.type,self.target.types)
            modifier=stab*typee*(random.randint(85,100)/100)
            if move1.category=="special":
                damage=math.floor(((2*self.user.level/5+2)*move1.power*self.user.special/self.target.special/50+2)*modifier)
                if damage==0: damage=1
            elif move1.category=="physical":
                damage=math.floor(((2*self.user.level/5+2)*move1.power*self.user.attack/self.target.defense/50+2)*modifier)
                if damage==0: damage=1
            else: damage=0
            self.target.curhp-=damage
            if self.target.curhp<0:self.target.curhp=0
            return typee
        elif move2 != None:
            if move2.type in self.target.types:stab=1.5
            else:stab=1
            typee=self.types(move2.type,self.user.types)
            modifier=stab*typee*(random.randint(85,100)/100)
            if move2.category=="special":
                damage=math.floor(((2*self.target.level/5+2)*move2.power*self.target.special/self.user.special/50+2)*modifier)
                if damage==0 and typee!=0: damage=1
            elif move2.category=="physical":
                damage=math.floor(((2*self.target.level/5+2)*move2.power*self.target.attack/self.user.defense/50+2)*modifier)
                if damage==0 and typee!=0: damage=1
            else: damage=0
            self.user.curhp-=damage
            if self.user.curhp<0:self.user.curhp=0
            return typee
    
    def types(self, atype, dtypes):
        with open("json/types.json") as f_obj:
            types = json.load(f_obj)
        typee = 1
        for dtype in dtypes:
            if dtype.lower() in types[atype]:
                typee*=types[atype][dtype.lower()]
        return typee
    
    def xp(self):
        pass
    
class move:
    def __init__(self, name, pp=1):
        with open("json/moves.json") as f_obj:
            moves = json.load(f_obj)
        move = moves[name]
        self.name=name
        self.type=move["type"]
        self.category=move["category"]
        self.power=move["power"]
        self.accuracy=move["accuracy"]
        self.maxpp=move["pp"]
        self.curpp=round(self.maxpp*pp)
        if "effect" in move:
            self.effect=move["effect"]
    
    def export(self):
        dic={
        "name": self.name,
        "pp": self.curpp/self.maxpp,
        }
        return dic