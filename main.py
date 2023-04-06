from score import *
from paddle import Paddle
from ball import Ball
from turtle import * 
import turtle as tur
import tkinter as tk
from tkinter import simpledialog
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from PubNubb import *
from mechanics import *
import config


message_out = {}
config.message_in = {}
ROOT = tk.Tk()                                          # the input dialog
ROOT.withdraw()
username = simpledialog.askstring(title=" ", prompt="What's your username:")
friend_username = simpledialog.askstring(title=" ", prompt="What's your friend username:")

screen = Screen()                       # creating game window
screen.setup(width=800, height=800)
screen.bgcolor("black")
screen.title("PONG")
screen.tracer(0)
screen.listen()
score_board = Scoreboard()              # creating scoreboard object

band_up = Paddle((0, 320))          # creating objects
band_up.shapesize(1, 50)
band_down = Paddle((0, -320))
band_down.shapesize(1, 50)
r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-928a66b6-bf3b-11ec-8ed3-2a42de1e11b7'       # subscription key
pnconfig.publish_key = 'pub-c-362cb6b6-9153-4ad8-a203-28ec0e7d254b'
pnconfig.uuid = username
pubnub = PubNub(pnconfig)

pubnub.add_listener(MySubscribeCallback())          # pubnub message listener starts
pubnub.subscribe().channels('channel1').execute()   # logging in
message_out[username] = 500                         # creating first message
time.sleep(2)

if friend_username in config.message_in:           # checking if message contains friends username(friend logged in)
    player_paddle = l_paddle
    opponent_paddle = r_paddle

else:                                       # if not, user takes right side and waits till friend will log in
    player_paddle = r_paddle
    opponent_paddle = l_paddle
    while True:
        print(friend_username)
        print(config.message_in)
        
        if friend_username in config.message_in:
            break
        print("waiting")
        pubnub.publish().channel("channel1").message(message_out).pn_async(my_publish_callback)
        time.sleep(1)


game_on = True
while game_on:
    screen.update()
    ball.move()
    paddle_bounce_check(r_paddle, l_paddle, ball)

    canvas = tur.getcanvas()        # getting mouse y position
    y = canvas.winfo_pointery()
    message_out[username] = y       # creating message_out position variable for sending y position of paddle
    time.sleep(0.025)
    pubnub.publish().channel("channel1").message(message_out).pn_async(my_publish_callback)
    # sending message with y pos 
    position(y, player_paddle)      # update player paddle position
    if friend_username in config.message_in:
        position(int(config.message_in[friend_username]), opponent_paddle)  # update opponent paddle position
    goal_check(ball, score_board)

screen.exitonclick()
