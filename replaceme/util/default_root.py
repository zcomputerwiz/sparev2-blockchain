import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("REPLACEME_ROOT", "~/.replaceme/mainnet"))).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("REPLACEME_KEYS_ROOT", "~/.replaceme_keys"))).resolve()
