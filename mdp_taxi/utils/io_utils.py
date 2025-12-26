"""Configuration loading and I/O utilities."""
import os
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def get_default_config_path() -> Path:
    """Get path to default configuration file.

    Returns:
        Path to default_config.yaml
    """
    return Path(__file__).parent.parent / "config" / "default_config.yaml"


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from YAML file.

    Args:
        config_path: Path to config file. If None, loads default config.

    Returns:
        Configuration dictionary

    Raises:
        ImportError: If PyYAML is not available
        FileNotFoundError: If config file doesn't exist
    """
    if not YAML_AVAILABLE:
        raise ImportError("PyYAML is required for configuration loading. Install with: pip install PyYAML")

    if config_path is None:
        config_path = get_default_config_path()
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration to YAML file.

    Args:
        config: Configuration dictionary
        config_path: Path to output file

    Raises:
        ImportError: If PyYAML is not available
    """
    if not YAML_AVAILABLE:
        raise ImportError("PyYAML is required for configuration saving. Install with: pip install PyYAML")

    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def get_config_value(config: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """Get a value from nested config using dot notation.

    Args:
        config: Configuration dictionary
        key_path: Dot-separated path (e.g., "mdp.grid_size")
        default: Default value if key not found

    Returns:
        Configuration value or default

    Example:
        >>> config = {'mdp': {'grid_size': 5}}
        >>> get_config_value(config, 'mdp.grid_size')
        5
        >>> get_config_value(config, 'mdp.missing', 10)
        10
    """
    keys = key_path.split(".")
    value = config

    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default

    return value


def merge_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two configuration dictionaries.

    Override values take precedence over base values.
    Nested dictionaries are merged recursively.

    Args:
        base: Base configuration
        override: Override configuration

    Returns:
        Merged configuration
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result


def find_config_file() -> Optional[Path]:
    """Find configuration file in standard locations.

    Searches in order:
    1. Current directory (config.yaml)
    2. User home directory (.mdp_taxi/config.yaml)
    3. Package default (mdp_taxi/config/default_config.yaml)

    Returns:
        Path to config file if found, None otherwise
    """
    search_paths = [
        Path.cwd() / "config.yaml",
        Path.home() / ".mdp_taxi" / "config.yaml",
        get_default_config_path(),
    ]

    for path in search_paths:
        if path.exists():
            return path

    return None
