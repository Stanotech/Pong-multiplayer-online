from paddle import Paddle
from ball import Ball
from turtle import *
import turtle as tur
# from urllib.parse import urlencode
from requests import get
from tkinter import messagebox
import socket
import time


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
answer = screen.textinput("Welcome to Ping Pong!", "Do you want to be a server of client?")
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


if answer == "server":
    HOST = get('https://api.ipify.org').content.decode('utf8')  # getting my public IP address, and decode to UTF
    messagebox.showinfo("yours ip address", HOST)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))  # binding ip and port to socket connection
        s.listen()  # listening for connection
        conn, addr = s.accept()  # return connection and address connected
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                # if not data:
                #     break
                str1 = data.decode('UTF-8')  # converting from bytes to string
                print(str1)
                conn.sendall(data + b" oddaje")

elif answer == "client":
    HOST = screen.textinput("Host address", "Please type in the host ip address")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            s.sendall(b"Hello, world")
            data = s.recv(1024)
            time.sleep(1)
            print(f"Received {data!r}")


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
