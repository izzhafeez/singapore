import re

def check_float(s):
    try:
        float(s)
        return True
    except:
        return False

def check_all_float(*s):
    return all([check_float(x) for x in s])