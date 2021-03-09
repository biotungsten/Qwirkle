# Copyright (c) 2021 David Sauer

def symbol(char):
    if char == "star":
        return "✷"
    elif char == "rhombus":
        return "◆"
    elif char == "flower":
        return "✣"
    elif char == "cross":
        return "✚"
    elif char == "circle":
        return "●"
    elif char == "square":
        return "■"
    elif char == None:
        return "NA"
    else:
        return None

def color(char):
    if char == "red":
        return "🟥"
    elif char == "green":
        return "🟩"
    elif char == "orange":
        return "🟧"
    elif char == "blue":
        return "🟦"
    elif char == "yellow":
        return "🟨"
    elif char == "pink":
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
    s = symbol(listOfChars[0])
    c = color(listOfChars[1])
    if (s and c):
        return s+c
    else:
        raise RuntimeError("Invalid stone chars: {}".format(listOfChars))