import math
import random
import json

class party:
    def __init__(self, party):
        self.tdata = party["0"]
        self.order = self.tdata["order"]
        self.box = self.tdata["box"]
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
        self.setlevel(self.tdata["level"])
        
    def export(self):
        self.tdata = {"order":self.order,
                      "level":self.level,
                      "box":self.box}
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
        self.reorder()
        poke = self.get(i)
        self.setp(i,None)
        return poke
    
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
    
class pc:
    def __init__(self, boxes=None, main=1):
        if boxes == None:
            self.box1 = []
            self.box2 = []
            self.box3 = []
            self.box4 = []
            self.box5 = []
            self.box6 = []
            self.box7 = []
            self.box8 = []
        else:
            self.box1 = boxes[0]
            self.box2 = boxes[1]
            self.box3 = boxes[2]
            self.box4 = boxes[3]
            self.box5 = boxes[4]
            self.box6 = boxes[5]
            self.box7 = boxes[6]
            self.box8 = boxes[7]
        self.main = main
    
    def export(self):
        return [self.box1, self.box2, self.box3, self.box4, self.box5, self.box6, self.box7, self.box8]
        
    def get_box(self, num=0):
        if num == 0: num = self.main
        if num == 1: return self.box1
        elif num == 2: return self.box2
        elif num == 3: return self.box3
        elif num == 4: return self.box4
        elif num == 5: return self.box5
        elif num == 6: return self.box6
        elif num == 7: return self.box7
        elif num == 8: return self.box8
        
    def set_box(self, num, box):
        if num == 1: self.box1 = box
        elif num == 2: self.box2 = box
        elif num == 3: self.box3 = box
        elif num == 4: self.box4 = box
        elif num == 5: self.box5 = box
        elif num == 6: self.box6 = box
        elif num == 7: self.box7 = box
        elif num == 8: self.box8 = box
        
    def is_not_full(self):
        box = self.get_box(self.main)
        if len(box)<30: return True
        
    def withdraw(self, slot):
        box = self.get_box(self.main)
        poke = box.pop(slot-1)
        self.set_box(self.main, box)
        return poke
    
    def deposit(self, poke):
        if self.is_not_full():
            box = self.get_box(self.main)
            poke = box.append(poke)
            self.set_box(self.main, box)
        else: return False
    
    def release(self, slot):
        box = self.get_box(self.main)
        box.pop(slot-1)
        self.set_box(self.main, box)

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
            self.status = {}
            self.run=1
            self.run2=None
            self.level = int(level)
            self.curxp = self.__getXP(self.level)
            self.nextxp = self.__getXP(self.level+1)
            self.name = name
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
        elif False:
            pass
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
            mod = poke["mod"]
            self.modattack = mod["Attack"]
            self.moddefense = mod["Defense"]
            self.modspeed = mod["Speed"]
            self.modspecial = mod["Special"]
            self.modaccuracy = mod["Accuracy"]
            self.modevasion = mod["Evasion"]
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
    
    def getvolstatus(self):
        keys=self.status.keys()
        if "freeze" in keys: return " (FRZ)"
        elif "paralysis" in keys: return " (PAR)"
        elif "burn" in keys: return " (BRN)"
        elif "sleep" in keys: return " (SLP)"
        elif "poison" in keys or "toxic" in keys: return " (PSN)"
        elif "fainted" in keys: return " (FNT)"
        else: return ""
    
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
        elif para=="modspeed":
            if "paralysis" in self.status:
                return round(self.speed/4*max(2, 2+self.modspeed)/max(2, 2-self.modspeed))
            else:
                return round(self.speed*max(2, 2+self.modspeed)/max(2, 2-self.modspeed))
        elif para=="accuracy": return max(2, 2+self.modaccuracy)/max(2, 2-self.modaccuracy)*max(2, 2-self.modevasion)/max(2, 2+self.modevasion)
    
    def resetMod(self):
        self.modaccuracy = self.modevasion = self.modattack = self.moddefense = self.modspeed = self.modspecial = 0
        
    def setMod(self, stat, stages):
        if stat=="attack":
            self.modattack+=stages
            if self.modattack>6: self.modattack=6
            elif self.modattack<-6: self.modattack=-6
        elif stat=="defense":
            self.moddefense+=stages
            if self.moddefense>6: self.moddefense=6
            elif self.moddefense<-6: self.moddefense=-6
        elif stat=="speed":
            self.modspeed+=stages
            if self.modspeed>6: self.modspeed=6
            elif self.modspeed<-6: self.modspeed=-6
        elif stat=="special":
            self.modspecial+=stages
            if self.modspecial>6: self.modspecial=6
            elif self.modspecial<-6: self.modspecial=-6
        elif stat=="evasiveness":
            self.modevasion+=stages
            if self.modevasion>6: self.modevasion=6
            elif self.modevasion<-6: self.modevasion=-6
        elif stat=="accuracy":
            self.modaccuracy+=stages
            if self.modaccuracy>6: self.modaccuracy=6
            elif self.modaccuracy<-6: self.modaccuracy=-6
    
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
        else: return slot
        
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
        self.returnstring = ""
        self.end = False
        
    def turn(self, movenum1=None, movenum2=None):
        if movenum1==None:
            self.target, self.user, string = self.attack(movenum2, self.target, self.user)
            return string
        elif movenum2==None:
            self.user, self.target, string = self.attack(movenum1, self.user, self.target)
            return string
        else:
            if movenum1 == 0: move1 = pokeparty.move("struggle")
            else: move1 = self.user.getMove(movenum1)
            if movenum2 == 0: move2 = pokeparty.move("struggle")
            else: move2 = self.target.getMove(movenum2)
            first=""
            userspeed=self.user.getMod("modspeed")
            targetspeed=self.target.getMod("modspeed")
            if userspeed > targetspeed:
                first = "user"
            elif userspeed < targetspeed:
                first = "target"
            else:
                if random.randint(0,1):
                    first = "user"
                else:
                    first = "target"
            if "priority" in move1.effect or "priority" in move2.effect:
                if "priority" in move1.effect:
                    priority1 = move1.effect["priority"]
                else: priority1 = 0
                if "priority" in move2.effect:
                    priority2 = move2.effect["priority"]
                else: priority2 = 0
                if priority1 == priority2: pass
                elif priority1 > priority2:
                    first = "user"
                else:
                    first = "target"
            if first == "user":
                self.user, self.target, string = self.attack(movenum1, self.user, self.target)
                returnstring = string
                if not self.end:
                    self.target, self.user, string = self.attack(movenum2, self.target, self.user, turn=1)
                    returnstring += "\n" + string
            elif first == "target":
                self.target, self.user, string = self.attack(movenum2, self.target, self.user, turn=1)
                returnstring = string
                if not self.end:
                    self.user, self.target, string = self.attack(movenum1, self.user, self.target)
                    returnstring += "\n" + string
        return returnstring
    
    def attack(self, movenum, attacking, defending, turn=0):
        if movenum == 0: move = pokeparty.move("struggle")
        else: move = attacking.getMove(movenum)
        targetres=defending.getMod("modstat")
        targetdefense, targetspecial = targetres["Defense"], targetres["Special"]
        userres=attacking.getMod("modstat")
        userattack, userdefense, userspecial = userres["Attack"], userres["Defense"],userres["Special"]
        if "reflect" in defending.status: userattack /= 2
        if "light screen" in defending.status: userspecial /= 2
        if "burn" in attacking.status: userattack /= 2
        attacks = True
        if "sleep" in attacking.status:
            attacks = False
            if attacking.status["sleep"]>1:
                string = attacking.species+" is fast asleep. "
                attacking.status["sleep"]-=1
            elif attacking.status["sleep"]==1:
                string = attacking.species+" woke up. "
                del attacking.status["sleep"]
        elif "freeze" in attacking.status:
            attacks = False
            string=attacking.species+" is frozen solid. "
        elif "flinch" in attacking.status:
            attacks = False
            string=attacking.species+" flinched. "
        elif "confused" in attacking.status:
            if attacking.status["confused"]>0:
                string = attacking.species+" is confused. "
                attacking.status["confused"]-=1
                if random.choice((True, False)):
                    attacks = False
                    string += attacking.species+" hurt itself in confusion! "
                    damage=math.floor(((2*attacking.level/5+2)*40*userattack/userdefense/50+2))
                    if damage==0: damage=1
                    attacking.curhp-=damage
                    if attacking.curhp<=0:
                        attacking.curhp=0
                        string += attacking.species+" fainted! "
                        self.end = True
            elif attacking.status["confused"]==0:
                string = attacking.species+" snapped out of confusion! "
                del attacking.status["confused"]
        if attacks and "paralysis" in attacking.status:
            if random.randint(1,4)==1:
                attacks = False
                string = attacking.species+" is fully paralyzed! "
        if attacks:
            move.curpp-=1
            attacking.setMove(movenum, move)
            string = attacking.species+" used "+move.name.title()+". "
            if "ohko" in move.effect:
                if attacking.getMod("modspeed") < defending.getMod("modspeed"):
                    string += "But it failed. "
                    attacks = False
            if "dream" in move.effect and "sleep" not in defending.status:
                string += "But it failed. "
                attacks = False
            if attacks and self.accuracy(move, attacking.getMod("accuracy"))=="miss":
                string += "The attack missed. "
                attacks = False
                if move.name in ["self-destruct","explosion"]:
                    attacking.curhp = 0
                    string += attacking.species+" fainted!"
                    self.end = True
                if crash in move.effect:
                    attacking.curhp -= 1
                    string += attacking.species+" kept going and crashed! "
        if attacks:
            if "fixed" in move.effect:
                fixed = move.effect["fixed"]
                if isinstance(fixed, int):
                    damage = fixed
                elif isinstance(fixed, float):
                    damage = math.floor(fixed * defending.curhp)
                    if damage == 0: damage = 1
                elif fixed == "level":
                    damage = attacking.level
                elif fixed == "psywave":
                    damage = random.randint(1,math.floor(1.5*attacking.level))
            else:
                if move.type in attacking.types:stab=1.5
                else:stab=1
                if move.category!="status":
                    t=self.types(move.type,defending.types)
                    if self.crit(attacking, move) and t!=0:
                        string+="Critical hit! "
                        crit = True
                    else: crit = False
                    if t==0:string+="It's not effective. "
                    elif t<1:string+="It's not very effective. "
                    elif t>1:string+="It's super effective. "
                else:
                    t=1
                if "ohko" in move.effect:
                    if t == 0: damage = 0
                    else:
                        damage = defending.hp
                        string += "One-hit KO! "
                else:
                    modifier=stab*t*(random.randint(85,100)/100)
                    if move.category=="special":
                        if crit:
                            damage=math.floor((((4*attacking.level/5+2)*move.power*attacking.special/defending.special)/50+2)*modifier)
                        else:
                            damage=math.floor((((2*attacking.level/5+2)*move.power*userspecial/targetspecial)/50+2)*modifier)
                        if damage==0 and t!=0: damage=1
                    elif move.category=="physical":
                        if crit:
                            damage=math.floor((((4*attacking.level/5+2)*move.power*attacking.attack/defending.defense)/50+2)*modifier)
                        else:
                            damage=math.floor((((2*attacking.level/5+2)*move.power*userattack/targetdefense)/50+2)*modifier)
                        if damage==0 and t!=0: damage=1
                    else: damage=0
            if damage > defending.curhp:
                damage = defending.curhp
            defending.curhp-=damage
            if "multi" in move.effect and t!=0:
                if move.effect["multi"]==2:
                    multi = 2
                elif move.effect["multi"]==5:
                    multi = random.choice((2,2,2,3,3,3,4,5))
                i = 1
                while defending.curhp > 0 and i < multi:
                    defending.curhp-=damage
                    i+=1
                string += "Hit the enemy "+str(i)+" times. "
            attacking, defending, effectstring = self.effects(move, attacking, defending, turn, damage)
            string += effectstring
        if defending.curhp<=0:
            defending.curhp=0
            string += defending.species+" fainted! "
            self.end = True
        if not self.end:
            if "freeze" in defending.status:
                if move.type == "fire" and move.name != "fire spin":
                    del defending.status["freeze"]
                    string += defending.species+" was thawed! "
            elif "burn" in attacking.status:
                burn_damage=math.floor(attacking.hp/16)
                if burn_damage == 0: burn_damage = 1
                attacking.curhp -= burn_damage
                string += attacking.species+" is hurt by the burn. "
            elif "poison" in attacking.status:
                pois_damage=math.floor(attacking.hp/16)
                if pois_damage == 0: pois_damage = 1
                attacking.curhp -= pois_damage
                string += attacking.species+" is hurt by poison. "
            elif "toxic" in attacking.status:
                pois_damage=math.floor(attacking.status["toxic"] * attacking.hp / 16)
                attacking.status["toxic"] += 1
                if pois_damage == 0: pois_damage = 1
                attacking.curhp -= pois_damage
                string += attacking.species+" is hurt by poison. "
            if "seeded" in attacking.status:
                seed_damage = math.floor(attacking.hp/16)
                if seed_damage == 0: seed_damage = 1
                if seed_damage > attacking.curhp:
                    seed_damage = attacking.curhp
                attacking.curhp -= seed_damage
                defending.curhp += seed_damage
                string += "Leech Seed saps "+attacking.species+"! "
            if attacking.curhp<=0:
                attacking.curhp=0
                string += attacking.species+" fainted!"
                self.end = True
        return attacking, defending, string
    
    def accuracy(self, move, a2):
        if move.accuracy==None: return "hits"
        a=round(move.accuracy*255*a2)
        r=random.randint(0,255)
        if r<a: return "hits"
        else: return "miss"
        
    def crit(self, user, move):
        if "focus" in user.status:
            threshold = math.floor(user.base["Speed"]+236/4)*2
        else:
            threshold = math.floor(user.base["Speed"]+76/4)
        if move.effect != None:
            if "crit" in move.effect:
                threshold *= 8
        if threshold > 255:
            threshhold = 255
        if random.randint(0, 255) < threshold:
            return True
        else: return False
        
    def effects(self, move, attacking, defending, turn, damage):
        effect=move.effect
        tpoke="user"
        if "chance" in effect:
            if effect["chance"]<random.random():return attacking, defending, ""
        effectstring = ""
        if "stat" in effect and not self.end:
            if "mist" in defending.status and move.category=="status":
                effectstring += "But it failed. "
            else:
                realstat=effect["stat"]
                if realstat.startswith("o"):
                    tpoke="target"
                    poke2=defending
                    realstat=realstat[1:]
                else:
                    poke2=attacking
                oldmod=poke2.getMod("moddic")[realstat.title()]
                poke2.setMod(realstat, effect["stages"])
                realstage=poke2.getMod("moddic")[realstat.title()]-oldmod
                effectstring = poke2.species+"'s "+realstat
                if realstage==2: effectstring+=" greatly rose! "
                elif realstage==1: effectstring+=" rose! "
                elif realstage==-1: effectstring+=" fell! "
                elif realstage==-2: effectstring+=" greatly fell! "
                elif realstage==0 and move.category=="status":
                    effectstring="Nothing happened! "
                elif realstage==0:
                    effectstring=""
                if tpoke=="user": attacking=poke2
                elif tpoke=="target": defending=poke2
        elif "status" in effect and not self.end:
            status=effect["status"]
            if "not" in effect:
                if effect["not"] in defending.types:return attacking, defending, ""
            nonvolatile = ["freeze", "paralysis", "burn", "sleep", "poison", "toxic"]
            if status in nonvolatile:
                curstatus=set(defending.status.keys()).intersection(nonvolatile)
                if curstatus != set():
                    if move.category != "status": effectstring = ""
                    else: effectstring += "But it failed. "
                else:
                    if status == "freeze":
                        defending.status["freeze"] = None
                        effectstring += defending.species+" was frozen solid! "
                    elif status == "paralysis":
                        defending.status["paralysis"] = None
                        effectstring += defending.species+" was paralyzed! It may not attack! "
                    elif status == "burn":
                        defending.status["burn"] = None
                        effectstring += defending.species+" was burned! "
                    elif status == "sleep":
                        defending.status["sleep"] = random.randint(1,7)
                        effectstring += defending.species+" fell asleep! "
                    elif status == "poison":
                        defending.status["poison"] = None
                        effectstring += defending.species+" was poisoned! "
                    elif status == "toxic":
                        defending.status["toxic"] = 1
                        effectstring += defending.species+" was badly posioned! "
            elif status in ["flinch", "confused", "seeded", "bound", "reflect", "light screen"]:
                if status == "flinch":
                    defending.status["flinch"] = None
                elif status == "confused":
                    if "confused" in defending.status:
                        effectstring += "But it failed. "
                    else:
                        defending.status["confused"] = random.randint(2,5)
                        effectstring += defending.species+" was confused! "
                elif status == "seeded":
                    if "seeded" in defending.status:
                        effectstring += "But it failed. "
                    else:
                        defending.status["seeded"] = None
                        effectstring += defending.species+" was seeded! "
                elif status == "reflect":
                    if "reflect" in attacking.status:
                        effectstring += "But it failed. "
                    else:
                        attacking.status["reflect"] = None
                        effectstring += attacking.species+" gained armor! "
                elif status == "light screen":
                    if "light screen" in attacking.status:
                        effectstring += "But it failed. "
                    else:
                        attacking.status["light screen"] = None
                        effectstring += attacking.species+" is protected against special attacks! "
        elif "recoil" in effect:
            recoil = effect["recoil"]
            recoil_damage = math.floor(damage * recoil)
            if recoil_damage == 0: recoil_damage = 1
            attacking.curhp += recoil_damage
            if attacking.curhp <= 0:
                attacking.curhp = 0
                self.end = True
            if attacking.curhp > attacking.hp:
                attacking.curhp = attacking.hp
            if recoil > 0:
                effectstring += "Sucked health from "+defending.species+"! "
            elif recoil < 0:
                effectstring += attacking.species+" is hit with recoil! "
                if attacking.curhp == 0:
                    effectstring += attacking.species+" fainted! "
        if "rest" in effect:
            if attacking.curhp != attacking.hp:
                attacking.status = {"sleep": random.randint(1,7)}
                effectstring += attacking.species+" started sleeping! "
        if "heal" in effect:
            heal = 0
            if attacking.curhp == attacking.hp and effect["heal"]>0:
                effectstring += "But it failed. "
            else:
                heal = math.floor(effect["heal"]*attacking.hp)
                attacking.curhp += heal
            if attacking.curhp <= 0:
                attacking.curhp = 0
                self.end = True
            if attacking.curhp > attacking.hp:
                attacking.curhp = attacking.hp
            if heal > 0:
                effectstring += attacking.species+" regained healthl! "
            elif heal < 0:
                effectstring += attacking.species+" fainted! "
        if "focus" in effect:
            attacking.status["focus"] = None
            effectstring += attacking.species+" is getting pumped! "
        if "mist" in effect:
            attacking.status["mist"] = None
            effectstring += attacking.species+" is shrouded in mist! "
        return attacking, defending, effectstring
    
    def types(self, atype, dtypes):
        with open("json/types.json") as f_obj:
            types = json.load(f_obj)
        typee = 1
        for dtype in dtypes:
            if dtype.lower() in types[atype]:
                typee*=types[atype][dtype.lower()]
        return typee
            
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
        else: self.effect={}
    
    def export(self):
        dic={
        "name": self.name,
        "pp": self.curpp/self.maxpp,
        }
        return dic