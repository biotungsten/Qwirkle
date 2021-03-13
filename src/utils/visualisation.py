# Copyright (c) 2021 David Sauer

def color(char):
    if char == "R":
        return "🟥"
    elif char == "G":
        return "🟩"
    elif char == "O":
        return "🟧"
    elif char == "B":
        return "🟦"
    elif char == "Y":
        return "🟨"
    elif char == "P":
        return "🟪"
    elif char == None:
        return "NA"
    else:
        return None

def stone(listOfChars):
    """Returns a string corresponding to the given stone

    Args:
        listOfChars ([Str]): element 1 - symbol character, element 2 - color character, further elements are discarded
    """
    s = listOfChars[0]
    c = color(listOfChars[1])
    if (s and c):
        return s+c
    else:
        raise RuntimeError("Invalid stone chars: {}".format(listOfChars))