__version__ = "0.1.3"

from timeflake.flake import Timeflake

# Global instance
_global_instance = Timeflake()
EPOCH = _global_instance.epoch
random = _global_instance.random
next = _global_instance.next
parse = _global_instance.parse
