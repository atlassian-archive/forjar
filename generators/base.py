import random
import pickle
import os

thisdir = os.path.abspath(os.path.dirname(__file__)) + '/'

loaders_dir = os.path.join(thisdir, '../loaders/')


def load_data(name):
    return pickle.load(open(os.path.join(loaders_dir, '%s.p' % name), 'rb'))


