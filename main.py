from turtle import Screen
from paddle import Paddle

screen = Screen()
screen.setup(width=800, height=800)
screen.bgcolor("black")
screen.title("PONG")
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))

screen.listen()

game_on = True

while game_on:
    screen.update()
    screen.onkey(l_paddle.up, "w")
    screen.onkey(l_paddle.down, "s")
    screen.onkey(r_paddle.up, "i")
    screen.onkey(r_paddle.down, "k")


screen.exitonclick()
