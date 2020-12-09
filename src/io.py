# Used to make quick new lines.
def brk():
    print()

# A simple 'print' command but made in a way to show the user what kind of prompt the user is on.
# Also allows multi-line output as a list (for better looking code).
def cout(name: str, content: str, multiline_output: list = []):
    print(f"[{name}]: {content}")
    
    # Iterate over the multiline output list if it exists.
    for line in multiline_output:
        print(line)

# A simple 'input' command but made in a more stylish way to include a word that describes the data the user should enter.
def cin(type: str):
    return input(f"{type} => ")
