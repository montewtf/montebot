import math
import random
import json

class party:
    def __init__(self, party):
        self.tdata = party["0"]
        self.order = self.tdata["order"]
        self.p1 = pokemon(party["1"])
        if party["2"]!=None: self.p2 = pokemon(party["2"])
        else: self.p2=None
        if party["3"]!=None: self.p3 = pokemon(party["3"])
        else: self.p3=None
        if party["4"]!=None: self.p4 = pokemon(party["4"])
        else: self.p4=None
        if party["5"]!=None: self.p5 = pokemon(party["5"])
        else: self.p5=None
        if party["6"]!=None: self.p6 = pokemon(party["6"])
        else: self.p6=None
        if "7" in party:
            self.p7 = pokemon(party["7"])
        else: self.p7 = None
        if "level" in self.tdata:
            self.setlevel(self.tdata["level"])
        else:
            self.setlevel()
        
    def recon(self):
        self.tdata = {"order":self.order,
                      "level":self.level}
        party = {"0":self.tdata,
                 "1":self.p1.export()}
        if self.p2 != None: party["2"] = self.p2.export()
        else: party["2"]=None
        if self.p3 != None: party["3"] = self.p3.export()
        else: party["3"]=None
        if self.p4 != None: party["4"] = self.p4.export()
        else: party["4"]=None
        if self.p5 != None: party["5"] = self.p5.export()
        else: party["5"]=None
        if self.p6 != None: party["6"] = self.p6.export()
        else: party["6"]=None
        if self.p7 != None: party["7"] = self.p7.export()
        return party
    
    def get(self, slot:int):
        if slot==1: return self.p1
        elif slot==2: return self.p2
        elif slot==3: return self.p3
        elif slot==4: return self.p4
        elif slot==5: return self.p5
        elif slot==6: return self.p6
        elif slot==7: return self.p7
        else: return None
        
    def setp(self, slot:int, p):
        if slot==1: self.p1=p
        elif slot==2: self.p2=p
        elif slot==3: self.p3=p
        elif slot==4: self.p4=p
        elif slot==5: self.p5=p
        elif slot==6: self.p6=p
        elif slot==7: self.p7=p
        else: return None
        
    def setlevel(self, level=0):
        self.level=level
        i=1
        while i<7:
            if self.get(i)==None:
                break
            if self.level<self.get(i).level: self.level=self.get(i).level
            i+=1
    
    def swap(self, s1, s2=1):
        if s1>6 or s2>6:
            return 1
        array=[self.p1,self.p2,self.p3,self.p4,self.p5,self.p6]
        t1=self.get(s1)
        t2=self.get(s2)
        if t1==None or t2==None:
            return 1
        self.setp(s1,t2)
        self.setp(s2,t1)
        self.order[s1-1], self.order[s2-1] = self.order[s2-1], self.order[s1-1]
        return 0
    
    def remove(self, r1):
        i=r1
        while i<7:
            if self.swap(i, i+1):
                break
            i+=1
        self.setp(i,None)
    
    def add(self, a1):
        if self.p6!=None:
            return 0
        i=1
        while i<7:
            if self.get(i) == None:
                self.setp(i,a1)
                return i
            i+=1
            
    def unswap(self):
        i=1
        while i<6:
            j=i
            while j>0 and self.order[j-1]>self.order[j]:
                self.swap(j+1,j)
                j-=1
            i+=1
        self.reorder()
    
    def reorder(self):
        self.order = [1,2,3,4,5,6]

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
            self.run=1
            self.run2=None
            self.level = int(level)
            self.curxp = self.__getXP(self.level)
            self.nextxp = self.__getXP(self.level+1)
            self.name = name
            self.status = None
            self.__genIV()
            self.evhp = self.evattack = self.evdefense = self.evspeed = self.evspecial = 0
            self.modaccuracy = self.modevasion = self.modattack = self.moddefense = self.modspeed = self.modspecial = 0
            self.getStats()
            self.curhp = self.hp
            self.move1 = None
            self.move2 = None
            self.move3 = None
            self.move4 = None
            self.__genMoves()
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
            ev = poke["ev"]
            self.evattack = ev["Attack"]
            self.evdefense = ev["Defense"]
            self.evspeed = ev["Speed"]
            self.evspecial = ev["Special"]
            self.evhp = ev["HP"]
            if "mod" in poke:
                mod = poke["mod"]
                self.modattack = mod["Attack"]
                self.moddefense = mod["Defense"]
                self.modspeed = mod["Speed"]
                self.modspecial = mod["Special"]
                self.modaccuracy = mod["Accuracy"]
                self.modevasion = mod["Evasion"]
            else:
                self.modaccuracy = self.modevasion = self.modattack = self.moddefense = self.modspeed = self.modspecial = 0
            self.curhp = poke["stats"]["CurHP"]
            self.hp = poke["stats"]["HP"]
            self.attack = poke["stats"]["Attack"]
            self.defense = poke["stats"]["Defense"]
            self.speed = poke["stats"]["Speed"]
            self.special = poke["stats"]["Special"]
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
            if "run" in poke:
                self.run=poke["run"]
            else: self.run = None
            if "run2" in poke:
                self.run2 = True
            else: self.run2 = None
            
    def __genIV(self):
        self.ivattack = random.randint(0,15)
        self.ivdefense = random.randint(0,15)
        self.ivspeed = random.randint(0,15)
        self.ivspecial = random.randint(0,15)
        self.ivhp = (self.ivattack%2)*8+(self.ivdefense%2)*4+(self.ivspeed%2)*2+(self.ivspecial%2)*1

    def getEV(self):
        return {"HP":self.evhp,
                "Attack":self.evattack,
                "Defense":self.evdefense,
                "Speed":self.evspeed,
                "Special":self.evspecial}
    
    def setEV(self, dic):
        for key in dic:
            if dic[key]>65535: dic[key]=65535
        self.evhp=dic["HP"]
        self.evattack=dic["Attack"]
        self.evdefense=dic["Defense"]
        self.evspeed=dic["Speed"]
        self.evspecial=dic["Special"]
        
    def getMod(self, para):
        if para=="moddic":
            return {"Attack" : self.modattack,
                    "Defense" : self.moddefense,
                    "Speed" : self.modspeed,
                    "Special" : self.modspecial,
                    "Accuracy" : self.modaccuracy,
                    "Evasion" : self.modevasion}
        elif para=="modstat":
            return {"Attack" : self.attack*max(2, 2+self.modattack)/max(2, 2-self.modattack),
                    "Defense" : self.defense*max(2, 2+self.moddefense)/max(2, 2-self.moddefense),
                    "Special" : self.special*max(2, 2+self.modspecial)/max(2, 2-self.modspecial),
                    }
        elif para=="modspeed": return round(self.speed*max(2, 2+self.modspeed)/max(2, 2-self.modspeed))
        elif para=="accuracy": return max(2, 2+self.modaccuracy)/max(2, 2-self.modaccuracy)*max(2, 2-self.modevasion)/max(2, 2+self.modevasion)
    
    def setMod(self, stat, stages):
        if stat=="attack":
            self.modattack+=stages
            if self.modattack>6:
                self.modattack=6
                return "toohigh"
            elif self.modattack<-6:
                self.modattack=-6
                return "toolow"
        elif stat=="defense":
            self.moddefense+=stages
            if self.moddefense>6:
                self.moddefense=6
                return "toohigh"
            elif self.moddefense<-6:
                self.moddefense=-6
                return "toolow"
        elif stat=="speed":
            self.modspeed+=stages
            if self.modspeed>6:
                self.modspeed=6
                return "toohigh"
            elif self.modspeed<-6:
                self.modspeed=-6
                return "toolow"
        elif stat=="special":
            self.modspecial+=stages
            if self.modspecial>6:
                self.modspecial=6
                return "toohigh"
            elif self.modspecial<-6:
                self.modspecial=-6
                return "toolow"
        elif stat=="evasiveness":
            self.modevasion+=stages
            if self.modevasion>6:
                self.modevasion=6
                return "toohigh"
            elif self.modevasion<-6:
                self.modevasion=-6
                return "toolow"
        elif stat=="accuracy":
            self.modaccuracy+=stages
            if self.modaccuracy>6:
                self.modaccuracy=6
                return "toohigh"
            elif self.modaccuracy<-6:
                self.modaccuracy=-6
                return "toolow"
        return ""
    
    def getStats(self):
        self.hp = math.floor((((self.base["HP"]+self.ivhp)*2+(math.sqrt(self.evhp)/4))*(self.level/100))+self.level+10)
        self.attack = math.floor((((self.base["Attack"]+self.ivattack)*2+(math.sqrt(self.evattack)/4))*(self.level/100))+5)
        self.defense = math.floor((((self.base["Defense"]+self.ivdefense)*2+(math.sqrt(self.evdefense)/4))*(self.level/100))+5)
        self.speed = math.floor((((self.base["Speed"]+self.ivspeed)*2+(math.sqrt(self.evspeed)/4))*(self.level/100))+5)
        self.special = math.floor((((self.base["Special"]+self.ivspecial)*2+(math.sqrt(self.evspecial)/4))*(self.level/100))+5)
        
    def __genMoves(self):
        with open("json/movedex.json") as f_obj:
            dex = json.load(f_obj)
        moves=dex.get(self.species)
        i=self.level
        while i>0:
            if i==1 and isinstance(moves.get("1"), list):
                level1 = moves.get("1")
                if self.move1!=None:
                    if self.move1.name.title() in level1:
                        level1.pop(level1.index(self.move1.name.title()))
                if self.move2!=None:
                    if self.move2.name.title() in level1:
                        level1.pop(level1.index(self.move2.name.title()))
                if self.move3!=None:
                    if self.move3.name.title() in level1:
                        level1.pop(level1.index(self.move3.name.title()))
                if self.move4!=None:
                    if self.move4.name.title() in level1:
                        level1.pop(level1.index(self.move4.name.title()))
                while len(level1)>0:
                    if self.addMove(level1.pop(0)): break                    
            elif str(i) in moves:
                if self.addMove(moves.get(str(i))):  break
            i-=1
    
    def addMove(self, nmove, slot=None):
        if slot == None:
            if self.move1 == None:
                self.move1 = move(nmove.lower())
                return 0
            else:
                if self.move1.name == nmove.lower(): return 3
            if self.move2 == None:
                self.move2 = move(nmove.lower())
                return 0
            else:
                if self.move2.name == nmove.lower(): return 3
            if self.move3 == None:
                self.move3 = move(nmove.lower())
                return 0
            else:
                if self.move3.name == nmove.lower(): return 3
            if self.move4 == None:
                self.move4 = move(nmove.lower())
                return 0
            else:
                if self.move4.name == nmove.lower(): return 3
                else: return 1
        else:
            if slot>0 and slot<=4:
                self.setMove(slot, move(nmove.lower()))
                return 2
            
    def getMove(self, slot):
        if slot==1:return self.move1
        elif slot==2:return self.move2
        elif slot==3:return self.move3
        elif slot==4:return self.move4
        
    def setMove(self, slot, move):
        if slot==1:self.move1=move
        elif slot==2:self.move2=move
        elif slot==3:self.move3=move
        elif slot==4:self.move4=move
            
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
            stats=[self.hp, self.attack, self.defense, self.speed, self.special]
            self.getStats()
            nstats=[self.hp, self.attack, self.defense, self.speed, self.special]
            statdif=[]
            i=0
            while i<5:
                statdif.append(nstats[i]-stats[i])
                i+=1
            self.curhp+=statdif[0]
            if str(self.level) in movedex:
                if self.addMove(movedex.get(str(self.level)))==0:
                    return [result,1,movedex.get(str(self.level)),statdif]
                else:
                    return [result,2,movedex.get(str(self.level)),statdif]
                
            else: return [result,0,None,statdif]
        else: return [0]

    def evolve(self, nspecies):
        self.id = nspecies["id"]
        self.species = nspecies["name"]
        self.types = nspecies["type"]
        self.base = nspecies["base"]
        oldhp=self.hp
        self.getStats()
        self.curhp+=(self.hp-oldhp)
    
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
         "ev" : {
            "HP" : self.evhp,
            "Attack" : self.evattack,
            "Defense" : self.evdefense,
            "Speed" : self.evspeed,
            "Special" : self.evspecial,
            },
        "mod" : {
            "Attack" : self.modattack,
            "Defense" : self.moddefense,
            "Speed" : self.modspeed,
            "Special" : self.modspecial,
            "Accuracy" : self.modaccuracy,
            "Evasion" : self.modevasion,
            },
        "base" : self.base,
        "xp" : {
            "xptype" : self.xptype,
            "cur" : self.curxp,
            "next" : self.nextxp,
            },
        }
        if self.catch != None: summary["catch"] = self.catch
        if self.xpyield != None: summary["xpyield"] = self.xpyield
        if self.part != None: summary["participated"] = self.part
        if self.run != None: summary["run"] = self.run
        if self.run2 != None: summary["run2"] = self.run2
        return summary
    
class battle:
    def __init__(self, poke1, poke2):
        self.user = poke1
        self.target = poke2
        self.case = 0
        self.typee1 = ""
        self.typee2 = ""
        self.miss1 = False
        self.miss2 = False
        self.effect1 = ""
        self.effect2 = ""
        
    def turn(self, move1=None, move2=None):
        if move1==None:
            self.target.setMove(move2, self.attack(move2=self.target.getMove(move2)))
            self.case = 0
            return self.returnstring(move2=self.target.getMove(move2))
        elif move2==None:
            self.user.setMove(move1, self.attack(move1=self.user.getMove(move1)))
            self.case = 0
            return self.returnstring(move1=self.user.getMove(move1))
        else:
            userspeed=self.user.getMod("modspeed")
            targetspeed=self.target.getMod("modspeed")
            if userspeed > targetspeed:
                self.user.setMove(move1, self.attack(move1=self.user.getMove(move1)))
                if self.target.curhp==0: self.case = 3
                else:
                    self.target.setMove(move2, self.attack(move2=self.target.getMove(move2)))
                    self.case = 1
            elif userspeed < targetspeed:
                self.target.setMove(move2, self.attack(move2=self.target.getMove(move2)))
                if self.user.curhp==0: self.case = 4
                else:
                    self.user.setMove(move1, self.attack(move1=self.user.getMove(move1)))
                    self.case = 2
            else:
                if random.randint(0,1):
                    self.user.setMove(move1, self.attack(move1=self.user.getMove(move1)))
                    if self.target.curhp==0: self.case = 3
                    else:
                        self.target.setMove(move2, self.attack(move2=self.target.getMove(move2)))
                        self.case = 1
                else:
                    self.target.setMove(move2, self.attack(move2=self.target.getMove(move2)))
                    if self.user.curhp==0: self.case = 4
                    else:
                        self.user.setMove(move1, self.attack(move1=self.user.getMove(move1)))
                        self.case = 2
        return self.returnstring(self.user.getMove(move1),self.target.getMove(move2))
    
    def attack(self, move1=None, move2=None):
        targetres=self.target.getMod("modstat")
        targetattack, targetdefense, targetspecial = targetres["Attack"], targetres["Defense"], targetres["Special"]
        userres=self.user.getMod("modstat")
        userattack, userdefense, userspecial = userres["Attack"], userres["Defense"], userres["Special"]
        if move1 != None:
            move1.curpp-=1
            if self.accuracy(move1, self.user.getMod("accuracy"))=="miss":
                self.miss1 = True
                return
            else: self.miss1 = False
            if move1.type in self.user.types:stab=1.5
            else:stab=1
            if move1.category!="status":
                t1=self.types(move1.type,self.target.types)
                if t1==0:self.typee1="It's not effective. "
                elif t1<1:self.typee1="It's not very effective. "
                elif t1>1:self.typee1="It's super effective. "
            else:
                t1=1
            modifier=stab*t1*(random.randint(85,100)/100)
            if move1.category=="special":
                damage=math.floor(((2*self.user.level/5+2)*move1.power*userspecial/targetspecial/50+2)*modifier)
                if damage==0: damage=1
            elif move1.category=="physical":
                damage=math.floor(((2*self.user.level/5+2)*move1.power*userattack/targetdefense/50+2)*modifier)
                if damage==0: damage=1
            else: damage=0
            self.target.curhp-=damage
            if self.target.curhp<=0:
                self.target.curhp=0
            else: self.effects(move1=move1)
            return move1
        elif move2 != None:
            move2.curpp-=1
            if self.accuracy(move2, self.target.getMod("accuracy"))=="miss":
                self.miss2 = True
                return
            else: self.miss2 = False
            if move2.type in self.target.types:stab=1.5
            else:stab=1
            if move2.category!="status":
                t2=self.types(move2.type,self.user.types)
                if t2==0:self.typee2="It's not effective. "
                elif t2<1:self.typee2="It's not very effective. "
                elif t2>1:self.typee2="It's super effective. "
            else:
                t2=1
            modifier=stab*t2*(random.randint(85,100)/100)
            if move2.category=="special":
                damage=math.floor(((2*self.target.level/5+2)*move2.power*targetspecial/userspecial/50+2)*modifier)
                if damage==0 and typee!=0: damage=1
            elif move2.category=="physical":
                damage=math.floor(((2*self.target.level/5+2)*move2.power*targetattack/userdefense/50+2)*modifier)
                if damage==0 and typee!=0: damage=1
            else: damage=0
            self.user.curhp-=damage
            if self.user.curhp<=0:
                self.user.curhp=0
            else: self.effects(move2=move2)
            return move2
    
    def accuracy(self, move, a2):
        if move.accuracy==None: return "hits"
        a=round(move.accuracy*255*a2)
        r=random.randint(0,255)
        if r<a: return "hits"
        else: return "miss"
        
    def effects(self, move1=None, move2=None):
        if move1!=None:
            effect=move1.effect
            poke=poke2="user"
        elif move2!=None:
            effect=move2.effect
            poke=poke2="target"
        if effect==None: return
        if "chance" in effect:
            if effect["chance"]<random.random():return
        if "stat" in effect:
            stat=effect["stat"]
            if poke=="user":
                if stat.startswith("o"):
                    poke2="target"
                    ostat=stat[1:]
                    result=self.target.setMod(ostat, effect["stages"])
                else: result=self.user.setMod(stat, effect["stages"])
                if poke2=="target":
                    if effect["stages"]==2: self.effect1=self.target.species+"'s "+ostat+" greatly rose! "
                    elif effect["stages"]==1: self.effect1=self.target.species+"'s "+ostat+" rose! "
                    elif effect["stages"]==-1: self.effect1=self.target.species+"'s "+ostat+" fell! "
                    elif effect["stages"]==-2: self.effect1=self.target.species+"'s "+ostat+" greatly fell! "
                elif poke2=="user":
                    if effect["stages"]==2: self.effect1=self.user.species+"'s "+stat+" greatly rose! "
                    elif effect["stages"]==1: self.effect1=self.user.species+"'s "+stat+" rose! "
                    elif effect["stages"]==-1: self.effect1=self.user.species+"'s "+stat+" fell! "
                    elif effect["stages"]==-2: self.effect1=self.user.species+"'s "+stat+" greatly fell! "
                if result.startswith("too") and move1.category=="status":
                    self.effect1="Nothing happened! "
                elif result.startswith("too"):
                    self.effect1=""
            elif poke=="target":
                if stat.startswith("o"):
                    poke2="user"
                    ostat=stat[1:]
                    result=self.user.setMod(ostat, effect["stages"])
                else: result=self.target.setMod(stat, effect["stages"])
                if poke2=="target":
                    if effect["stages"]==2: self.effect2=self.target.species+"'s "+stat+" greatly rose! "
                    elif effect["stages"]==1: self.effect2=self.target.species+"'s "+stat+" rose! "
                    elif effect["stages"]==-1: self.effect2=self.target.species+"'s "+stat+" fell! "
                    elif effect["stages"]==-2: self.effect2=self.target.species+"'s "+stat+" greatly fell! "
                elif poke2=="user":
                    if effect["stages"]==2: self.effect2=self.user.species+"'s "+ostat+" greatly rose! "
                    elif effect["stages"]==1: self.effect2=self.user.species+"'s "+ostat+" rose! "
                    elif effect["stages"]==-1: self.effect2=self.user.species+"'s "+ostat+" fell! "
                    elif effect["stages"]==-2: self.effect2=self.user.species+"'s "+ostat+" greatly fell! "
                if result.startswith("too") and move2.category=="status":
                    self.effect2="Nothing happened! "
                elif result.startswith("too"):
                    self.effect2=""
    
    def types(self, atype, dtypes):
        with open("json/types.json") as f_obj:
            types = json.load(f_obj)
        typee = 1
        for dtype in dtypes:
            if dtype.lower() in types[atype]:
                typee*=types[atype][dtype.lower()]
        return typee
    
    def returnstring(self, move1=None, move2=None):
        string=""
        if self.case%2==1:
            string+=self.user.species+" used "+move1.name.title()+". "
            if self.miss1: string+="The attack missed.\n"
            else:
                string+=self.typee1+self.effect1+"\n"
                if self.target.curhp==0:
                    string+=self.target.species+" fainted"
                    return string
            string+=self.target.species+" used "+move2.name.title()+". "
            if self.miss2: string+="The attack missed."
            else:
                string+=self.typee2+self.effect2
                if self.user.curhp==0:
                    string+=self.user.species+" fainted"
                    return string
        else:
            string+=self.target.species+" used "+move2.name.title()+". "
            if self.miss2: string+="The attack missed.\n"
            else:
                string+=self.typee2+self.effect2+"\n"
                if self.user.curhp==0:
                    string+=self.user.species+" fainted"
                    return string
                if self.case==0: return string
            string+=self.user.species+" used "+move1.name.title()+". "
            if self.miss1: string+="The attack missed."
            else:
                string+=self.typee1+self.effect1
                if self.target.curhp==0:
                    string+=self.target.species+" fainted"
                    return string
        return string
            
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
        else: self.effect=None
    
    def export(self):
        dic={
        "name": self.name,
        "pp": self.curpp/self.maxpp,
        }
        return dic