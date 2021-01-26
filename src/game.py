from random import random
from src import database, io
from time import sleep
import math

# ! Why use 'random' instead of 'randint'?
# I have encountered multiple very similar and predictable values with 'randint'
# So I have taken an approach similar in other languages which is generating
# A float between 0 and 1 and using it to ouput a random value.
def better_randint(min, max):
    return math.floor(random() * max) + min

def roll_dice_tie_breaker(turn, total_score):
    io.cout(f"GAME (Player {turn})", "Please roll one dice (enter).")        
    input()
    io.cout(f"GAME (Player {turn})", "Rolling...")

    sleep(1)
    
    dice_one = better_randint(1, 6)

    total_score = total_score + dice_one

    io.cout(f"GAME (Player {turn})", f"The dice has landed on {dice_one}{'.' if dice_one < 5 else '!'}")

    sleep(0.3)

    io.brk()
    io.cout(f"GAME (Player {turn})", f"Turn concluded. You have gained {dice_one} points.")
    io.cout(f"GAME (Player {turn})", f"Your total score is {total_score}.")
    io.brk()

    return total_score


def roll_dice_sequence(turn, total_score):
    io.cout(f"GAME (Player {turn})", "Please roll the two dices (enter).")        
    
    input()
    
    io.cout(f"GAME (Player {turn})", "Rolling...")
    io.brk()

    sleep(1)
    
    dice_one = better_randint(1, 6)

    io.cout(f"GAME (Player {turn})", f"Dice one landed on {dice_one}{'.' if dice_one < 5 else '!'}")

    sleep(1)

    dice_two = better_randint(1, 6)

    io.cout(f"GAME (Player {turn})", f"Dice two landed on {dice_two}{'.' if dice_two < 5 else '!'}")

    dice_total = dice_one + dice_two

    sleep(0.5)

    io.cout(f"GAME (Player {turn})", f"The total value of both dice is {dice_total}{'.' if dice_total < 10 else '. Phenomenal!'}")
    io.brk()

    score = total_score + dice_total
    turn_total = dice_total

    sleep(0.5)

    # ? Game conditions.
    
    # Number is even/odd.
    if (score % 2) == 0:
        io.cout(f"GAME (Player {turn})", "Your score total is even! Added 10 points to your score.")
        score += 10
        turn_total += 10
    else:
        io.cout(f"GAME (Player {turn})", "Your score total is odd. Subtracted 5 points from your score.")
        score -= 5
        turn_total -= 5

    sleep(0.5)

    # If both dices score the same
    if dice_one == dice_two:
        io.cout(f"GAME (Player {turn})", f"Both of the dices have rolled {dice_one}! Please roll an extra dice (enter).")

        input()

        io.cout(f"GAME (Player {turn})", "Rolling...")

        sleep(1)

        dice_three = better_randint(1, 6)

        io.cout(f"GAME (Player {turn})", f"Your extra dice has landed on {dice_three}{', not bad!' if dice_three < 4 else '. Good roll!'}")

        score += dice_three
        turn_total += dice_three

    sleep(0.3)

    io.cout(f"GAME (Player {turn})", f"Turn concluded. You have {'lost' if turn_total < 0 else 'gained'} {abs(turn_total)} points. {'Unlucky!' if turn_total < 1 else ''}")
    io.cout(f"GAME (Player {turn})", f"Your total score is {score}.")

    io.brk()

    return 0 if score < 0 else score


def start(first_user, second_user):
    io.brk()
    io.cout("GAME", "Welcome to the NEA Dice Game! Here is some information:", [
        "- Game info is on the to-do list"
    ])

    first_player_score = 0
    second_player_score = 0

    first_players_turn = False

    turns = 0
    round = 1

    tie_breaker_mode = False

    while True:
        if first_players_turn == True:
            first_players_turn = False
        else:
            first_players_turn = True
        
        # End round.
        if turns >= 2:
            round += 1
            turns = 0

        turns += 1

        if round > 5:
            if first_player_score == second_player_score:
                io.brk()
                io.cout("GAME", "Starting additional round due to both players' scores being the same.")
                tie_breaker_mode = True
            else:
                round -= 1
                break

        # Initial round start script.
        if round == 1 and turns <= 1:
            io.brk()
            io.cout("GAME", "The game has officially begun. Good luck!")
            io.brk()
            
        # Otherwise...
        else:
            io.brk()

        if turns <= 1:
            io.cout("GAME", f"Round {round}.")
            io.brk()


        if tie_breaker_mode == False:
            # First players turn.
            if first_players_turn == True:
                io.cout("GAME", f"Player 1 ({first_user['username']}), it is now your turn.")
                io.brk()

                first_player_score = roll_dice_sequence(1, first_player_score)

            # Second players turn.
            else:
                io.cout("GAME", f"Player 2 ({second_user['username']}), it is now your turn.")
                io.brk()

                second_player_score = roll_dice_sequence(2, second_player_score)

        # Tie breaker mode is on.
        else:
            # First players turn.
            if first_players_turn == True:
                io.cout("GAME", f"Player 1 ({first_user['username']}), it is now your turn.")
                io.brk()

                first_player_score = roll_dice_tie_breaker(1, first_player_score)

            # Second players turn.
            else:
                io.cout("GAME", f"Player 2 ({second_user['username']}), it is now your turn.")
                io.brk()

                second_player_score = roll_dice_tie_breaker(2, second_player_score)

    io.brk()
    io.cout("GAME", f"Game session concluded. There was a total of {round} rounds.")
    io.brk()

    io.cout("GAME", f"The winner of this session is...")
    sleep(2)

    if first_player_score > second_player_score:
        points_ahead = first_player_score - second_player_score

        io.cout("GAME", f"{first_user['username']}! Congratulations.")
        io.cout("GAME", f"You were {points_ahead} point{'' if points_ahead == 1 else 's'} ahead of {second_user['username']}.")
    else:
        points_ahead = second_player_score - first_player_score

        io.cout("GAME", f"{second_user['username']}! Congratulations.")
        io.cout("GAME", f"You were {points_ahead} point{'' if points_ahead == 1 else 's'} ahead of {first_user['username']}.")

    database.update_user_score(first_user["username"], first_user["score"] + first_player_score)
    database.update_user_score(second_user["username"], second_user["score"] + second_player_score)

    io.brk()
    io.cout("GAME", "All of your scores have been updated. Type 'leaderboard' in the menu to look at them!")
    io.cout("GAME", "Returning to menu...")
