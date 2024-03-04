"""
CS 5001 Final Project
Aamer Syed 
Due Date: December 08, 2023
"""



import turtle
import random
import time


screen = turtle.Screen()
screen.title( "Mastermind - made by Aamer")
screen.setup(width = 700, height = 600)
screen.bgcolor("white")


screen.addshape('checkbutton.gif')
screen.addshape('file_error.gif')
screen.addshape('leaderboard_error.gif')
screen.addshape('Lose.gif')
screen.addshape('quit.gif')
screen.addshape('quitmsg.gif')
screen.addshape('winner.gif')
screen.addshape('xbutton.gif')


secret_code = []
attempts = 0
Max_Attempts = 10
player_name = ''
score = 0
current_guess = []
guess_number = 0
marbles = []


draw_turtle = turtle.Turtle()
draw_turtle.speed(0)
draw_turtle.hideturtle()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Marble:
    def __init__(self, color, x, y):
        self.color = color
        self.position = Point(x, y)
        self.turtle = turtle.Turtle()
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.shape("circle")
        self.turtle.color(color)


    def draw(self):
        self.turtle.stamp()


    def is_clicked(self, x, y):
        distance = ((self.position.x - x)**2 + (self.position.y - y)**2)**0.5
        return distance < 20


def generate_secret_code():
    global secret_code
    colors = ["red", "green", "blue", "yellow", "purple", "orange"]
    secret_code = random.sample(colors, 4)
    print(f"Secret Code: {secret_code}")
    return secret_code


def draw_game_board():
    draw_turtle.penup()
    for i in range (Max_Attempts):
        draw_turtle.goto(-200, 250 - i * 50)
        for j in range(4):
            draw_turtle.dot(20, "white")
            draw_turtle.forward(50)


def setup_marbles():
    colors = ["red", "green", "blue", "yellow", "purple", "orange"]
    x, y = -300, -250
    for color in colors:
        marble = Marble(color, x, y)
        marble.draw()
        marbles.append(marble)
        x += 50


def marble_click(x, y):
    global current_guess, guess_number
    for marble in marbles:
        if marble.is_clicked(x, y):
            current_guess.append(marble.color)

            draw_turtle.penup()
            draw_turtle.goto(-200 + len(current_guess) * 50, 250 - guess_number * 50)
            draw_turtle.dot(20, marble.color)

            if len(current_guess) == 4:
                process_guess()
                current_guess.clear()
                guess_number += 1
                check_game_end()

            break

def calculate_score(guess):
    black_pegs = sum(g == s for g, s in zip(guess, secret_code))
    white_pegs = sum(min(guess.count(c), secret_code.count(c)) for c in set(guess)) - black_pegs
    return black_pegs, white_pegs


def process_guess():
    global guess_number, attempts
    score = calculate_score(current_guess)
    display_scoring_pegs(score, guess_number)
    attempts += 1
    if check_game_end():
        turtle.onscreenclick(None)


def display_scoring_pegs(score, guess_row):
    black_pegs, white_pegs = score
    peg_x, peg_y = 250, 250 - guess_row * 50
    for _ in range (black_pegs):
        draw_turtle.goto(peg_x, peg_y)
        draw_turtle.dot(10, "black")
        peg_x += 15
    for _ in range(white_pegs):
        draw_turtle.goto(peg_x, peg_y)
        draw_turtle.dot(10, "white")
        peg_x += 15


def check_game_end():
    global attempts, Max_Attempts, current_guess, secret_code
    if current_guess == secret_code:
        show_winner_popup()
        return True
    elif attempts >= Max_Attempts:
        show_loser_popup()
        return True
    return False

def show_winner_popup():
    winner_turtle = turtle.Turtle()
    winner_turtle.shape('winner.gif')
    winner_turtle.penup()
    winner_turtle.goto(0, 0)
    winner_turtle.stamp()


def show_loser_popup():
    loser_turtle = turtle.Turtle()
    loser_turtle.shape('Lose.gif')
    loser_turtle.penup()
    loser_turtle.goto(0, 0)
    loser_turtle.stamp()


def show_quit_message():
    quit_msg_turtle = turtle.Turtle()
    quit_msg_turtle.shape('quitmsg.gif')
    quit_msg_turtle.penup()
    quit_msg_turtle.goto(0, 0)
    quit_msg_turtle.stamp()
    turtle.done()


def quit_game():
   time.sleep(3)
   screen.bye()


def log_error(message):
    with open("mastermind_errors.err", "a") as error_file:
        error_file.write(f"{message}\n")


def update_leaderboard(player_name, score):
    try:
        with open("leaderboard.txt", "a+") as file:
            file.write(f"{player_name}: {score}\n")
    except IOError:
        log_error("Could not update leaderboard. Help!")


def display_leaderboard():
    try:
        with open("leaderboard.txt", "a+") as file:
            leaderboard = file.readlines()
            leaderboard.sort(reverse = True)

    except IOError:
        log_error("Could not show leaderboard. Help!")


def capture_player_name():
    return turtle.textinput ("Mastermind", "Enter your name: ")


def main():
    global player_name
    player_name = capture_player_name()
    draw_game_board()
    secret_code = generate_secret_code()
    setup_marbles()
    screen.onscreenclick(marble_click)

    quit_button = turtle.Turtle()
    quit_button.shape('quit.gif')
    quit_button.penup()
    quit_button.goto(200, -250)
    quit_button.onclick(lambda x, y: show_quit_message())


    screen.mainloop()


if __name__ == "__main__":
    main()

