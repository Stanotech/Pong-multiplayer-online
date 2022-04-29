from score import *
from paddle import Paddle
from ball import Ball
from turtle import *
import turtle as tur
import tkinter as tk
from tkinter import simpledialog
import time
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory  # , PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


def my_publish_callback(envelope, status):  # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel('channel1').message('logged').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):  # listener for massage
        # Handle new message stored in message.message
        print(message.message)
        global message_in
        message_in = message.message


def paddle_bounce_check():
    if (r_paddle.ycor() + 50 >= ball.ycor() >= r_paddle.ycor() - 50 and ball.xcor() >= r_paddle.xcor() - 20)\
            or l_paddle.ycor() + 50 >= ball.ycor() >= l_paddle.ycor() - 50 and ball.xcor() <= l_paddle.xcor() + 20:

        ball.gain_speed()
        ball.x_speed *= -1


def goal_check():
    if ball.xcor() < -380:
        ball.setpos(0, 0)
        score_board.r_point()
        ball.x_speed = 1
        ball.y_speed = 1

    elif ball.xcor() > 380:
        ball.setpos(0, 0)
        score_board.l_point()
        ball.x_speed = 1
        ball.y_speed = 1

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
username = simpledialog.askstring(title="Test", prompt="What's your Username:")
friend_username = simpledialog.askstring(title="Test", prompt="What's your friend username:")

screen = Screen()
screen.setup(width=800, height=800)
screen.bgcolor("black")
screen.title("PONG")
screen.tracer(0)
screen.listen()
score_board = Scoreboard()

band_up = Paddle((0, 320))
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

pubnub.add_listener(MySubscribeCallback())  # listener starts
pubnub.subscribe().channels('channel1').execute()  # logging in
message_out[username] = 500  # creating first message
time.sleep(2)

player_paddle = l_paddle
opponent_paddle = r_paddle  # DO WYJEBANIA

# if friend_username in message_in:
#     player_paddle = l_paddle
#     opponent_paddle = r_paddle
#
# else:
#     player_paddle = r_paddle
#     opponent_paddle = l_paddle
#     while True:
#         if friend_username in message_in:
#             break
#         print("waiting")
#         pubnub.publish().channel("channel1").message(message_out).pn_async(my_publish_callback)
#         time.sleep(1)


game_on = True
while game_on:
    screen.update()
    ball.move()
    paddle_bounce_check()

    canvas = tur.getcanvas()  # getting mouse y position
    y = canvas.winfo_pointery()
    message_out[username] = y  # creating message_out position variable for sending y position of paddle
    # time.sleep(1)
    # pubnub.publish().channel("channel1").message(message_out).pn_async(my_publish_callback)
    position(y, player_paddle)  # update player paddle position
    position(y, opponent_paddle)   # delete
    if friend_username in message_in:
        position(int(message_in[friend_username]), opponent_paddle)  # update opponent paddle position
    goal_check()

screen.exitonclick()
