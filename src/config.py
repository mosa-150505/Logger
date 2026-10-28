
import json
from dataclasses import dataclass
from pathlib import Path

from src.constants import CONFIG_PATH


class ConfigError(Exception):
    """Configuration absente ou invalide."""


@dataclass(frozen=True)
class Config:
    email: str
    password: str


def load_config(path: Path = CONFIG_PATH) -> Config:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"Fichier introuvable : {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"JSON invalide dans {path} : {exc}") from exc

    missing = [key for key in ("email", "password") if not data.get(key)]
    if missing:
        raise ConfigError(f"Clés manquantes dans {path} : {', '.join(missing)}")

    return Config(email=data["email"], password=data["password"])
