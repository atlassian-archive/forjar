from forjar.generators.base import *

names = load_data('names')

def gen_firstname():
    return random.choice(names['first'])

def gen_lastname():
    return random.choice(names['last'])

def gen_user_fullname(middle=False):
    if middle:
        return "%s %s. %s" % (gen_firstname(), random.choice(string.uppercase), gen_lastname())
    return "%s %s" % (gen_firstname(), gen_lastname())
