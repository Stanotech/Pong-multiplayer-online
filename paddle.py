from turtle import Turtle


class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(5, 1)
        self.penup()
        self.goto(position)
        
    def up(self):
        new_y = self.ycor() + 30
        self.sety(new_y)

    def down(self):
        new_y = self.ycor() - 30
        self.sety(new_y)
