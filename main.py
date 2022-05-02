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


def paddle_bounce_check(paddle_r, paddle_l, baall):
    if (paddle_r.ycor() + 50 >= baall.ycor() >= paddle_r.ycor() - 50 and baall.xcor() >= paddle_r.xcor() - 20)\
            or paddle_l.ycor() + 50 >= baall.ycor() >= paddle_l.ycor() - 50 and baall.xcor() <= paddle_l.xcor() + 20:

        baall.gain_speed()
        baall.x_speed *= -1


def goal_check():
    if ball.xcor() < -380:
        ball.setpos(0, 0)
        score_board.r_point()
        ball.x_speed = 12
        ball.y_speed = 6

    elif ball.xcor() > 380:
        ball.setpos(0, 0)
        score_board.l_point()
        ball.x_speed = 12
        ball.y_speed = 6


def position(y_pos, paddle):  # paddle y pos bind to y mouse position
    if -250 <= paddle.ycor() <= 250:
        paddle.sety(-y_pos + 460)
    if paddle.ycor() <= -250:
        paddle.sety(-249)
    if paddle.ycor() >= 250:
        paddle.sety(249)


message_out = {}
message_in = {}
ROOT = tk.Tk()  # the input dialog
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

band_up = Paddle((0, 320))          # creating objects from classes
band_up.shapesize(1, 50)
band_down = Paddle((0, -320))
band_down.shapesize(1, 50)
r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-928a66b6-bf3b-11ec-8ed3-2a42de1e11b7'
pnconfig.publish_key = 'pub-c-362cb6b6-9153-4ad8-a203-28ec0e7d254b'
pnconfig.uuid = username
pubnub = PubNub(pnconfig)

pubnub.add_listener(MySubscribeCallback())          # pubnub message listener starts
pubnub.subscribe().channels('channel1').execute()   # logging in
message_out[username] = 500                         # creating first message
time.sleep(2)

if friend_username in message_in:
    player_paddle = l_paddle
    opponent_paddle = r_paddle

else:
    player_paddle = r_paddle
    opponent_paddle = l_paddle
    while True:
        if friend_username in message_in:
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
    if friend_username in message_in:
        position(int(message_in[friend_username]), opponent_paddle)  # update opponent paddle position
    goal_check()

screen.exitonclick()
