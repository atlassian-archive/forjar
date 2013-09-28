from forjar.generators.base import *

sites = load_data('sites')

def gen_email(name):
    return "%s@%s" % (name.split(' ')[0].lower(), random.choice(sites))
