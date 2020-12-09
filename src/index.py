from src import database, io, authentication as auth

def main():
    print("========== Competitive Dice Game ==========")

    # Start the 'ask for command' loop.
    start_handler_loop()


def start_handler_loop():
    io.brk()
    io.cout("CMD HANDLER", "Please enter a command. For help enter 'help'")

    while True:
        io.brk()

        command = io.cin("Command")

        # If the user has entered nothing...
        if not command:
            io.cout("CMD HANDLER", "You have not entered anything.")
            continue
           
        # Parse to a lower case (efficiently ignoring case).
        # Safe to do now as some kind of input is now guaranteed.
        command = command.lower()

        if command == "help":
            io.cout("CMD HANDLER", "", [
                "=== List of Commands ===",
                "help - shows this prompt.",
                "play - starts the game!",
                "leaderboard - shows the top users sorted by most of least score.",
                "exit - exit the program.",
                "=== List of Commands ==="
            ])

        elif command == "exit":
            io.cout("PROCESS", "Shutting down database...")
            database.close_connection()
                
            io.cout("PROCESS", "Goodbye!")

            # Stop the command loop from asking for a command.
            break
                
        # Begin with the process of asking both users to authenticate.
        elif command == "play":
            io.brk()

            io.cout("GAME", "Welcome! To play, both players will need to login.")
            io.cout("GAME", "Launching login prompt for first user...")

            # Authenticate the first user.
            first_user = auth.attempt_authentication()

            if not first_user:
                io.cout("GAME", "Authentication failed. Type 'play' once you are ready to play.")
                continue

            io.cout("GAME", f"Welcome {first_user['username']}! You are player one.")

            # Authenticate the second user.
            


        elif command == "leaderboard":
            2

        # If input has not satisfied any condition...
        else:
            io.cout("CMD HANDLER", "Invalid command. Please try again.")
        

