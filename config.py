import os
from dotenv import load_dotenv
from typing import Any

load_dotenv()

class Config:
    _ENV_KEYS: dict[str, dict[str, str]] = {
        'dev_key': {
            'aqkanji2koe': 'DEV_KEY_AQKANJI2KOE',
            'aquestalk10': 'DEV_KEY_AQUESTALK10'
        }
    }

    @classmethod
    def load_config(cls) -> dict[str, Any]:
        dev = {}
        for key, env_name in cls._ENV_KEYS['dev_key'].items():
            value = os.environ.get(env_name)
            dev[key] = value
        return {'dev_key': dev}
