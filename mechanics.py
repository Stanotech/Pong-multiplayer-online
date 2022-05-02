def paddle_bounce_check(paddle_r, paddle_l, ball):
    if (paddle_r.ycor() + 50 >= ball.ycor() >= paddle_r.ycor() - 50 and ball.xcor() >= paddle_r.xcor() - 20)\
            or paddle_l.ycor() + 50 >= ball.ycor() >= paddle_l.ycor() - 50 and ball.xcor() <= paddle_l.xcor() + 20:

        ball.gain_speed()
        ball.x_speed *= -1


def goal_check(ball, score_board):
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