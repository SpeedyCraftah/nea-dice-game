import random
from src import database, io
from time import sleep
import math

# Script dedicated for the tie breaker.
def roll_dice_tie_breaker(turn, total_score):
    io.cout(f"GAME (Player {turn})", "Please roll one dice (enter).")        
    input()
    io.cout(f"GAME (Player {turn})", "Rolling...")

    sleep(1)
    
    # Generate a random number (roll dice).
    dice_one = random.randint(1, 6)

    # Append the roll of the dice to the total score.
    total_score = total_score + dice_one

    io.cout(f"GAME (Player {turn})", f"The dice has landed on {dice_one}{'.' if dice_one < 5 else '!'}")

    sleep(0.3)

    io.brk()
    io.cout(f"GAME (Player {turn})", f"Turn concluded. You have gained {dice_one} points.")
    io.cout(f"GAME (Player {turn})", f"Your total score is {total_score}.")
    io.brk()

    # Return the score for further processing.
    return total_score


# Script dedicated for the normal game.
def roll_dice_sequence(turn, total_score):
    io.cout(f"GAME (Player {turn})", "Please roll the two dices (enter).")        
    
    input()
    
    io.cout(f"GAME (Player {turn})", "Rolling...")
    io.brk()

    sleep(1)
    
    # Generate a random number (first dice).
    dice_one = random.randint(1, 6)

    io.cout(f"GAME (Player {turn})", f"Dice one landed on {dice_one}{'.' if dice_one < 5 else '!'}")

    sleep(1)

    # Generate a random number (second dice).
    dice_two = random.randint(1, 6)

    io.cout(f"GAME (Player {turn})", f"Dice two landed on {dice_two}{'.' if dice_two < 5 else '!'}")

    # Create a dice total variable for further processing.
    dice_total = dice_one + dice_two

    sleep(0.5)

    io.cout(f"GAME (Player {turn})", f"The total value of both dice is {dice_total}{'.' if dice_total < 10 else '. Phenomenal!'}")
    io.brk()

    # Append the points of the rolled dices to the total score.
    score = total_score + dice_total

    # Create a separate variable, cloning the dice_total variable which will be used
    # to keep track of the gained/lost points (purely for cosmetic purposes).
    turn_total = dice_total

    sleep(0.5)

    # ? Game conditions.
    
    # Number is even/odd.
    if (score % 2) == 0:
        # Add 10 points as per the game condition.

        io.cout(f"GAME (Player {turn})", "Your score total is even! Added 10 points to your score.")
        
        score += 10
        turn_total += 10
    else:
        # Subtract 5 points as per the game condition.

        io.cout(f"GAME (Player {turn})", "Your score total is odd. Subtracted 5 points from your score.")
        
        score -= 5
        turn_total -= 5

    sleep(0.5)

    # If both dices score the same
    if dice_one == dice_two:
        # Roll an extra dice as per the game condition.

        io.cout(f"GAME (Player {turn})", f"Both of the dices have rolled {dice_one}! Please roll an extra dice (enter).")

        input()

        io.cout(f"GAME (Player {turn})", "Rolling...")

        sleep(1)

        # Generate a random number (dice roll).
        dice_three = random.randint(1, 6)

        io.cout(f"GAME (Player {turn})", f"Your extra dice has landed on {dice_three}{', not bad!' if dice_three < 4 else '. Good roll!'}")

        score += dice_three
        turn_total += dice_three

    sleep(0.3)

    io.cout(f"GAME (Player {turn})", f"Turn concluded. You have {'lost' if turn_total < 0 else 'gained'} {abs(turn_total)} points. {'Unlucky!' if turn_total < 1 else ''}")
    io.cout(f"GAME (Player {turn})", f"Your total score is {score}.")

    io.brk()

    # Do not allow the score to dip below zero.
    # Return 0 if the total score is below 0.
    return 0 if score < 0 else score


def start(first_user, second_user):
    io.brk()
    io.cout("GAME", "Welcome to the NEA Dice Game! Here is some information:", [
        "- Each player rolls a 6-sided dice each",
        "- There are 5 rounds (a round being each player playing once)",
        "- If both players have the same score at the end of round 5, additional tie-breaker rounds will endure where each player rolls a dice until someone wins"
    ])

    io.brk()
    io.cout("GAME", "Here are the game conditions which are determined on your total score:", [
        "- If your score is even, 10 points will be added to your score",
        "- If your score is odd, 5 points will be subtracted from your score",
        "- If the two rolled dices are the same, the player will roll one additional dice which will be added to your score"
    ])

    io.brk()
    io.cout("GAME", "Have fun! (press enter to start the game).")
    io.brk()
    input()

    # Initialize both players scores (start at 0).
    first_player_score = 0
    second_player_score = 0

    # Keep track of each player's turn (used to determine when to end a round).
    first_players_turn = False

    # Keeps track of the amount of turns in the round (cleared to 0 on a new round).
    turns = 0

    # Keeps track of the round.
    round = 1

    # Determines if tie-breaker mode should be activated, set to true on the same score by two players.
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
