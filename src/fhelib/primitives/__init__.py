_counts = {"add": 0, "multiply": 0, "conjugate": 0, "cycle": 0}

def reset(): _counts.update({k: 0 for k in _counts})
def get_counts(): return dict(_counts)

from fhelib.primitives.add import add
from fhelib.primitives.multiply import multiply
from fhelib.primitives.conjugate import conjugate
from fhelib.primitives.cycle import cycle

__all__ = ["add", "multiply", "conjugate", "cycle", "reset", "get_counts"]
