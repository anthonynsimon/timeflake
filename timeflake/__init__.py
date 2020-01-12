from timeflake.flake import Timeflake

__version__ = "0.1.3"

# Global instance
_global_instance = Timeflake()
EPOCH = _global_instance.epoch
random = _global_instance.random
parse = _global_instance.parse
