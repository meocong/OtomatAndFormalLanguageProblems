def star_state(string:str):
    if (string == "e"):
        return "e"
    if (len(string) == 1 or (string[0] == "(" and string[-1] == ")")):
        return string + "*"
    else:
        return "(" + string + ")*"

def multiply(a:str,b:str):
    if (a == "e"):
        if (b == "e"):
            return "e"
        else:
            return b

    if (b == "e"):
        if (a == "e"):
            return "e"
        else:
            return a

    temp = ""
    if (len(a) == 1 or (a[0] == "(" and a[-1] == ")")):
        temp += a
    else:
        temp += "(" + a + ")"

    if (len(b) == 1 or (b[0] == "(" and b[-1] == ")")):
        temp += b
    else:
        temp += "(" + b + ")"
    return temp

def plus(a:str,b:str):
    if (a == "e"):
        return b

    if (b == "e"):
        return a

    return a + "+" + b