from paddle import Paddle
from ball import Ball
from turtle import *
import turtle as tur
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import os


pnconfig = PNConfiguration()

pnconfig.publish_key = 'enter your pubnub publish key here'
pnconfig.subscribe_key = 'enter your pubnub subscribe key here'
pnconfig.ssl = True

pubnub = PubNub(pnconfig)


def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass

    def status(self, pubnub, status):
        pass

    def message(self, pubnub, message):
        print("from device 2: " + message.message)


pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("chan-1").execute()

# publish a message
while True:
    msg = input("Input a message to publish: ")
    if msg == 'exit':
        os._exit(1)
    pubnub.publish().channel("chan-1").message(str(msg)).pn_async(my_publish_callback)


def right_paddle_ball_touch():
    if r_paddle.ycor() + 50 >= ball.ycor() >= r_paddle.ycor() - 50 and ball.xcor() >= r_paddle.xcor() - 20:
        return -1
    else:
        return 1


def left_paddle_ball_touch():
    if l_paddle.ycor() + 50 >= ball.ycor() >= l_paddle.ycor() - 50 and ball.xcor() <= l_paddle.xcor() + 20:
        return -1
    else:
        return 1


def position(eve):
    a = eve.y
    if -250 <= l_paddle.ycor() <= 250:
        l_paddle.sety(-a+400)
    if l_paddle.ycor() <= -250:
        l_paddle.sety(-249)
    if l_paddle.ycor() >= 250:
        l_paddle.sety(249)


screen = Screen()
screen.setup(width=800, height=800)
screen.bgcolor("black")
screen.title("PONG")
screen.tracer(0)

band_up = Paddle((0, 320))
band_up.shapesize(1, 50)
band_down = Paddle((0, -320))
band_down.shapesize(1, 50)
r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()


screen.listen()

game_on = True

while game_on:
    screen.update()
    screen.onkeypress(l_paddle.up, "w")
    screen.onkeypress(l_paddle.down, "s")
    screen.onkeypress(r_paddle.up, "i")
    screen.onkeypress(r_paddle.down, "k")
    screen.update()
    ball.move()

    ball.x_speed *= left_paddle_ball_touch()
    ball.x_speed *= right_paddle_ball_touch()

    ws = tur.getcanvas()
    ws.bind('<Motion>', position)


screen.exitonclick()
