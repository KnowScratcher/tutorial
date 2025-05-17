import random

kill = []

class Job:          # 大模板
    def __init__(self):
        self.name:str = None
        self.function:list = None
        self.probability:float = None
        self.isplayer:bool = False # 玩家標籤
        self.isalive:bool = True
        self.id:str = None

class Wolf(Job):    # 狼人
    def __init__(self,id):
        super().__init__()
        self.name = "狼人"
        self.function = [self.kill]
        self.probability = 1.0
        self.id = id

    def kill(self,player):
        global kill
        kill.append(player)

class Peasant(Job): # 平民
    def __init__(self,id):
        super().__init__()
        self.name = "平民"
        self.function = []
        self.probability = 1.0
        self.id = id
class Witch(Job):   # 女巫
    def __init__(self,id):
        super().__init__()
        self.name = "女巫"
        self.function = [self.kill,self.heal]
        self.probability = 0.5
        self.id = id

    def kill(self,player):
        global kill
        kill.append(player)

    def heal(self):
        global kill
        kill = []

class Prophet(Job): # 預言家
    def __init__(self,id):
        super().__init__()
        self.name = "預言家"
        self.function = [self.predict]
        self.probability = 1
        self.id = id
    
    def predict(self,id):
        for i in players.values():
            for j in i:
                if j.id == id:
                    return j.name

class Hunter(Job):  # 獵人
    def __init__(self,id):
        super().__init__()
        self.name = "獵人"
        self.function = [self.hunt("")]
        self.probability = 1
        self.id = id

    def hunt(self,player):
        pass

# {"wolf":[Wolf(),Wolf(),Wolf()]}
# 1. 依照角色起床
# 2. 怎麼投票(1.隨機/2.玩家為主/3.其他)
ids = list(range(1,10))
random.shuffle(ids)
ids = [str(x) for x in ids] # 轉成字串
players = {"wolf":[Wolf(ids[0]),Wolf(ids[1]),Wolf(ids[2])],"witch":[Witch(ids[3])],"prophet":[Prophet(ids[4])],"hunter":[Hunter(ids[5])],"peasant":[Peasant(ids[6]),Peasant(ids[7]),Peasant(ids[8])]}

wolf = [x.id for x in players["wolf"]]
witch = [x.id for x in players["witch"]]
prophet = [x.id for x in players["prophet"]]
char_build = []
characters = list(players.values())
for i in characters: # 循環整個list
    char_build.extend(i)

characters = char_build
# player = random.choice(characters) # 玩家
player = characters[0] # 玩家 #TODO: debug用
player.isplayer = True # 別標籤
print(f"你的身分是: {player.name}, id: {player.id}")

# xTODO: 1. 找到角色(型態、編號) 2 dict -型態->編號 -編號->角色
# xTODO: 2. 編號隨機 打亂串列(長度等長) 

# 遊戲迴圈
# if else => 有學過 寫比較多
# match case => 好看 寫較少
while True: # TODO: 結束條件
    kill = []
    alive = [x.id for x in characters if x.isalive] # 讀取還活著的玩家
    for k,v in players.items(): # i 是目前在玩的玩家(可能是電腦)
        match k:
            case "wolf":
                for i in v:
                    if i.isplayer: # 是人玩
                        wolf_kill = -1
                        while wolf_kill not in alive or wolf_kill in wolf:
                            wolf_kill = input(f"請輸入你要殺的人的編號(可用的: {' '.join(sorted(list(set(alive).difference(set(wolf)))))}): ")
                        i.kill(wolf_kill)
                        break
                    else:
                        wolf_kill = random.choice(list(set(alive).difference(set(wolf)).difference(set(kill))))
                        i.kill(wolf_kill)
                        break
                
            case "witch":
                for i in v:
                    if i.isplayer:
                        cmd = ""
                        while cmd not in ["h","k","救","殺"]:
                            cmd = input(f"今晚{kill}被殺了，救(h)/殺(k): ")
                            if cmd == "h" or cmd == "救":
                                i.heal()
                            elif cmd == "k" or cmd == "殺":
                                while kill not in alive or kill in witch:
                                    witch_kill = input(f"請輸入你要殺的人的編號(可用的: {' '.join(sorted(list(set(alive).difference(set(witch)))))}): ")
                                i.kill(witch_kill)
                        break
                    else: # 電腦玩
                        if random.random() < i.probability:
                            i.function[0](random.choice(list(set(alive).difference(set(witch)).difference(set(kill)))))
                            break
                        else:
                            i.function[1]()
                            break
            
            case "prophet":
                for i in v:
                    if i.isplayer:
                        predictId = None
                        while predictId not in alive or predictId in prophet:
                            predictId = input(f"請問你要預言誰的身分(可用的: {' '.join(sorted(list(set(alive).difference(set(prophet)))))}): ")
                        identity = i.predict(predictId)
                        print(f"{predictId}的身分是: {identity}")
                        break
                    else: # 電腦
                        # i.predict(random.choice(alive))
                        pass
                        
            case _:
                break
    
    print(f"今晚{' '.join(sorted(kill))}被殺了" if len(kill) != 0 else "今晚沒人被殺")
    for i in kill:
        alive.remove(i)
    if all(x in wolf for x in alive):
        print("狼人獲勝")
        break
    elif all(x not in wolf for x in alive):
        print("平民獲勝")
        break
    elif player.id not in alive:
        print("你輸了")
        break
    vote = None
    while vote not in alive or vote == player.id:
        vote = input(F"請投票(可投的人: {' '.join(sorted(list(set(alive).difference(set(player.id)))))}): ")
    if random.random() < 0.5: # 機率
        kill.append(vote)
    else:
        vote = random.choice(alive)
        kill.append(vote)
    print(f"{vote}號被投出去了")
    alive.remove(vote)
    # 殺人
    # 1. 找到id對應的人
    # 2. 把他的isalive換成False
    for i in players.values():
        for j in i:
            if j.id in kill:
                j.isalive = False

    if all(x in wolf for x in alive):
        print("狼人獲勝")
        break
    elif all(x not in wolf for x in alive):
        print("平民獲勝")
        break
    elif player.id not in alive:
        print("你輸了")
        break