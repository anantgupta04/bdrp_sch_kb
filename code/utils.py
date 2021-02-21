import numpy as np

def neatstr(string, space=''):
    return string.replace(' ', space).strip().lower()

def capletter(string):
    string = string.strip()
    return string[0] + string[1:].lower()

def maincol(classname, cols):
    cols = map(neatstr, cols)
    for idx, col in enumerate(cols):
        score = sum(c in classname.lower() for c in col) / len(classname)
        print(score)
        if (score > 0.3) and ('name' in col) or ('title' in col):
            return idx


def closest(candidate, types):
    candidate = neatstr(candidate, space='_')
    type_list = types if type(types) == list else list(types)
    closest_types = []
    # neatstr_p = partial()
    type_list = list(map(neatstr, type_list))
    for tp in type_list:
        cand_in_tp = candidate in tp
        subtypes = tp.split('_')
        tp_in_cand = sum(st in candidate for st in subtypes) / len(subtypes)
        if cand_in_tp or tp_in_cand > 0:
            closest_types.append((tp, tp_in_cand))
    if closest_types:
        closest_type = closest_types[np.transpose(closest_types)[1].argmax()][0]
        return types[type_list.index(closest_type)]
    else:
        return None


    