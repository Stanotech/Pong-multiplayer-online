from turtle import Screen
from paddle import Paddle
from ball import Ball

screen = Screen()
screen.setup(width=800, height=800)
screen.bgcolor("black")
screen.title("PONG")
screen.tracer(0)

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
    if r_paddle.ycor() + 50 >= ball.ycor() >= r_paddle.ycor() - 50 and ball.xcor() >= r_paddle.xcor() - 20\
            or l_paddle.ycor() + 50 >= ball.ycor() >= l_paddle.ycor() - 50 and ball.xcor() <= l_paddle.xcor() + 20:
        ball.x_speed *= -1


screen.exitonclick()
