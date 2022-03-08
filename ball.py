import random
from turtle import Turtle


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.shapesize(1)
        self.penup()
        self.x_speed = random.uniform(0, 0.5)
        self.y_speed = random.uniform(0, 0.5)

    def move(self):
        self.setx(self.xcor() + self.x_speed)
        self.sety(self.ycor() + self.y_speed)
        if self.ycor() >= 300:
            self.y_speed *= -1
        if self.ycor() <= -300:
            self.y_speed *= -1
