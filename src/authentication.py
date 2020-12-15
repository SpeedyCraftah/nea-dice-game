from src import database, io  

#szymon is bad

def attempt_authentication():
    io.brk()
    io.cout("SECURITY", "Hello user. Please type 'login' to authenticate yourself. If you do not have an account, type 'register' to create an account now. You can type 'exit' at any point to exit and go back to the main menu.")
    
    while True:
        io.brk()

        choice = io.cin("Login/Register/Exit")

        if not choice:
            io.cout("SECURITY", "You have not entered anything.")
            continue

        choice = choice.lower()

        if choice == "login":
            return attempt_login()

        elif choice == "register":
            return attempt_registration()

        elif choice == "exit":
            io.brk()
            break

        else:
            io.cout("SECURITY", "Incorrect option.")


def attempt_login():
    io.cout("SECURITY", "Please enter your username.")

    # Ask for the username.
    while True:
        io.brk()

        username = io.cin("Username")

        # Validate if the user has entered something.
        if not username:
            io.cout("SECURITY", "You have not entered anything.")
            continue

        # Check if the user wants to exit.
        if username.lower() == "exit":
            io.brk()
            return


        # Valide if the username exists.
        user = database.fetch_user_by_username(username)

        # If it does not...
        if not user:
            io.cout("SECURITY", "An account belonging to this username could not be found.")
            continue

        break

    io.brk()
    io.cout("SECURITY", "Please enter your password.")

    # Ask for the password.
    while True:
        io.brk()

        password = io.cin(f"Password [{user['username']}]")

        # Validate if the user has entered something.
        if not password:
            io.cout("SECURITY", "You have not entered anything.")
            continue

        # Check if the user wants to exit.
        if password.lower() == "exit":
            io.brk()
            return
            

        # If the users password does not match the entered password...
        if user["password"] != password:
            io.cout("SECURITY", "Password does not match.")
            continue

        break

    io.brk()

    # At this point the user is authenticated.
    # Return the user dict.
    return user



def attempt_registration():
    io.cout("SECURITY", "Please enter your desired username. It has to be at least 3 characters and no longer than 30.")

    # Ask for username.
    while True:
        io.brk()

        username = io.cin("Username")

        # Validate if the user has entered something.
        if not username:
            io.cout("SECURITY", "You have not entered anything.")
            continue

        # Check if the user wants to exit.
        if username.lower() == "exit":
            io.brk()
            return

        # If the username is shorter than 3 characters or longer than 30...
        if len(username) < 3 or len(username) > 30:
            io.cout("SECURITY", "This username is either shorter than 3 characters or longer than 30.")
            continue

        # Check if the username is already taken (SQLite will ignore case).
        user = database.fetch_user_by_username(username)

        # If the account does indeed exist...
        if user:
            io.cout("SECURITY", "This username is already taken.")
            continue

        break
    
    io.brk()
    io.cout("SECURITY", "Please enter your desired password. Make sure it's strong!")

    # Ask for password.
    while True:
        io.brk()

        password = io.cin("Password")

        # Validate if the user has entered something.
        if not password:
            io.cout("SECURITY", "You have not entered anything.")
            continue

        # Check if the user wants to exit.
        if password.lower() == "exit":
            io.brk()
            return

        break

    io.brk()

    # Create the account.
    user = database.create_user(username, password)

    # Return the user, completing the registration process.
    # The user is authenticated.
    return user
