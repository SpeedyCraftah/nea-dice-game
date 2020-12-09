import sys

# Required python version (3.6).
required_version = (3, 6)

# Get the python version (not using python 3.6 static type features yet as it will not work on < 3.6).
version = sys.version_info

# If the interpreter python version is higher or equal to 3.6, continue.
if version >= required_version:
    # Import the 'real' main file.
    from src import index

    # Start the 'real' program.
    index.main()
else:
    # If the version is not python 3.6, print and quit.
    print("You are not running python 3.6 or above which is required. Please upgrade.")
