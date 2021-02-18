def neatstr(string):
    return string.replace(' ', '').strip().lower()

def capletter(string):
    string = string.strip()
    return string[0] + string[1:].lower()