_counts = {"add": 0, "multiply": 0, "conjugate": 0, "cycle": 0}

def reset(): _counts.update({k: 0 for k in _counts})
def get_counts(): return dict(_counts)
