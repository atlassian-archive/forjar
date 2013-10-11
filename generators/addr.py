from forjar.generators.base import *

addr = load_data('address')

def gen_address():
    return random.choice(addr)
