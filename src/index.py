import atexit
from src import database, io, game, authentication as auth

def main():
    print("========== Competitive Dice Game ==========")

    # Register an event callback that automatically gets called on program SIGINT/SIGTERM (exit).
    # Handled globally (not just on an exit command issued by the user).
    def on_process_exit():
        io.brk()

        io.cout("PROCESS", "Gracefully closing database connection...")
        database.close_connection()
        
        io.cout("PROCESS", "Goodbye!")

    atexit.register(on_process_exit)


    # Start the 'ask for command' loop.
    start_handler_loop()


def start_handler_loop():
    io.brk()
    io.cout("CMD HANDLER", "Please enter a command. For help enter 'help'")

    while True:
        io.brk()
        
        # Ask the user for a command and block until one has been provided.
        command = io.cin("Command")

        # If the user has entered nothing...
        if not command:
            io.cout("CMD HANDLER", "You have not entered anything.")
            continue
           
        # Parse to a lower case (efficiently ignoring case).
        # Safe to do now as some kind of input is now guaranteed.
        command = command.lower()

        # Help command - prints all commands that can be processed.
        if command == "help":
            io.cout("CMD HANDLER", "", [
                "=== List of Commands ===",
                "help - shows this prompt.",
                "play - starts the game!",
                "leaderboard - shows the top users sorted by most of least score.",
                "exit - exit the program.",
                "=== List of Commands ==="
            ])

        # Exit command - breaks out of the command loop and letting the program
        # exit passively/naturally.
        # The rest will be handled by the exit event listener.
        elif command == "exit":
            # Stop the command loop from asking for a command.
            break
                
        # Play command - starts the game (authentication firstly).
        elif command == "play":
            io.brk()

            # Begin with the process of asking both users to authenticate.
            io.cout("GAME", "Welcome! To play, both players will need to login.")
            
            # Authenticate the first user.
            io.cout("GAME", "Launching login prompt for first user...")

            first_user = auth.attempt_authentication()

            # If the variable does not exist (user has exited the authentication prompt).
            if not first_user:
                io.cout("GAME", "Authentication failed. Type 'play' once you are ready to play.")
                continue

            io.cout("GAME", f"Hello {first_user['username']}! You are player one.")

            # Authenticate the second user.
            io.cout("GAME", "Launching login prompt for second user...")

            second_user = auth.attempt_authentication()

            # If the variable does not exist (user has exited the authentication prompt).
            if not second_user:
                io.cout("GAME", "Authentication failed. Type 'play' once you are ready to play.")
                continue

            # Check if both authenticated users are the same by comparing their internal IDs.
            if second_user["id"] == first_user["id"]:
                io.cout("GAME", "You cannot authenticate with the same account! Type 'play' once you are ready to play.")
                continue

            io.cout("GAME", f"Hello {second_user['username']}! You are player two.")

            io.cout("GAME", "Starting...")

            # Start the game and pass the authenticated users.
            game.start(first_user, second_user)

        elif command == "leaderboard":
            # Fetch the users with the highest score (top 5).
            top_users = database.fetch_leaderboard()

            # If there is no users...
            if len(top_users) == 0:
                io.cout("LEADERBOARD", "There is nothing to display.")
                continue

            leaderboard_users_parsed = []

            # Iterate over all users and insert a friendly parsed leaderboard row into the array.
            for user in top_users:
                leaderboard_users_parsed.append(f"{user['position']}. {user['username']} - {user['score']} points")

            # Pass the parsed array of leaderboard rows and display them conveniently with the
            # io#cout function.
            io.cout("LEADERBOARD", "Top 5 users with the highest score", [
                "=== Leaderboard ===",
            ] + leaderboard_users_parsed + [
                "=== Leaderboard ==="
            ])
                    

        # If input has not satisfied any condition...
        else:
            io.cout("CMD HANDLER", "Invalid command. Please try again.")
            # A continue statement is not required as this is the end of the while loop.
        
