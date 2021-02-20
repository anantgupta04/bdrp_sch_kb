def neatstr(string):
    return string.replace(' ', '').strip().lower()

def capletter(string):
    string = string.strip()
    return string[0] + string[1:].lower()

def maincol(classname, cols):
    
    for idx, col in enumerate(cols):
        if (classname in col) and ('name' in col) or ('title' in col):
            return idx

    