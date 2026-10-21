import pickle

def load_batch(blob):
    return pickle.loads(blob)

def run(blob):
    return load_batch(blob)
