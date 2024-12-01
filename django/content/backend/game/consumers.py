import json
from channels.generic.websocket import AsyncWebsocketConsumer
from queue import Queue
import time

channel_counter = Queue()
Game = []
GamePlay = []
second_player = False
x = 0

def CreateGameName():
    global second_player, x
    if second_player == False :
        name =  "pair" + str(x)
        GamePlay.append(name)
        second_player = True
        return GamePlay[x]
    else :
        second_player = False
        x += 1
        return GamePlay[x - 1]

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.index = x
        self.info = None
        self.BallStepX = 5
        self.BallStepY = 5
    async def connect(self):
        channel_counter.put(self.channel_name)
        self.group_name = CreateGameName()
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        # print(channel_counter.qsize())
        if channel_counter.qsize() == 2:
            Game.append([channel_counter.get(), channel_counter.get()])
            await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": self.group_name,
                "TITLE" : "start",
            }
        )
        else :
            await self.channel_layer.group_send(
            self.group_name,
            {
                "type" : "chat_message", 
                "message" : self.group_name,
                "TITLE" : "wait",
            }
        )

    async def disconnect(self,code):
        # channel_counter.pop()
        pass

    async def receive(self, text_data):
        game = json.loads(text_data)
        if Game :
            if game["TITLE"] == "move_ball" and Game[self.index][0] == self.channel_name:
                print("ballY = ", self.info["ball"]["y"], "player2Y = " ,self.info["player2"]["y"] )
                # time.sleep(1)
                if self.info["ball"]["x"] + self.BallStepX * 4 > self.info["canvas_width"] :
                    if self.info["ball"]["y"] > self.info["player2"]["y"] and self.info["ball"]["y"] < self.info["player2"]["y"] + self.info["paddleHeight"]:
                        self.BallStepX *= -1
                    else :
                        print("game over")
                if self.info["ball"]["x"] + self.BallStepX * 3 <= 0 :
                    self.BallStepX *= -1
                self.info["ball"]["x"] += self.BallStepX
                if self.info["ball"]["y"] + self.BallStepY * 3 > self.info["canvas_height"] or self.info["ball"]["y"] + self.BallStepY * 1 <= 0 :
                    self.BallStepY *= -1
                self.info["ball"]["y"] += self.BallStepY
                await self.channel_layer.group_send(
                self.group_name,
                {
                    "type" : "move_ball",
                    "group" : self.group_name,
                    "TITLE" : "move_ball",
                    "ballx" : self.info["ball"]["x"],
                    "bally" : self.info["ball"]["y"] 
                }
                )
            elif game["TITLE"] == "info":
                self.info = game
            elif game["TITLE"] == "move_player":
                if "down" == game["player_direction"]:
                    step = 5
                else :
                    step = -5
                if Game[self.index][0] == self.channel_name:
                    if step == 5:
                        if self.info["player1"]["y"] < self.info["canvas_height"]- self.info["paddleHeight"]:
                            self.info["player1"]["y"] += step
                    else:
                        if self.info["player1"]["y"] > 0:
                            self.info["player1"]["y"] += step
                    position = self.info["player1"]["y"] 
                    player = "player1"
                else :
                    if step == 5:
                        if self.info["player2"]["y"] < self.info["canvas_height"] - self.info["paddleHeight"]:
                            self.info["player2"]["y"] += step
                    else:
                        if self.info["player2"]["y"] > 0:
                            self.info["player2"]["y"] += step
                    position = self.info["player2"]["y"] 
                    player = "playe2"
                await self.channel_layer.group_send(
                self.group_name,
                {
                    "type" : "move_player",
                    "group" : self.group_name,
                    "TITLE" : "move_player",
                    "player" : player,
                    "position" : position,
                }
                )
                # print("-/-/-/-/-/-/", self.info["ball"]["y"], self.info["player2"]["y"])
                
    
    async def move_player(self, event):
        TITLE = event["TITLE"]
        PLAYER = event["player"]
        POSTION = event["position"]
        await self.send(text_data=json.dumps({"TITLE": TITLE, "player" : PLAYER , "position" : POSTION}))
    
    async def chat_message(self, event):
        message = event["message"]
        TITLE = event["TITLE"]

        await self.send(text_data=json.dumps({"TITLE": TITLE,
        "message" : message}))

    async def move_ball(self, event) :
        ballX = event["ballx"]
        ballY = event["bally"]
        TITLE =  event["TITLE"]

        await self.send(text_data=json.dumps({ "ballX" : ballX, "ballY" : ballY, "TITLE" : TITLE}))