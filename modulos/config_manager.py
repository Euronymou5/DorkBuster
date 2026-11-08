import json
import logging
import os
from typing import Any, Dict

logger = logging.getLogger("DorkBuster.Config")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "api_key": "",
    "model": "deepseek/deepseek-v4-flash-0731",
    "use_llm": False,
    "max_results": 10,
    "cooldown": 1,
    "selected_engines": ["Bing", "Yahoo", "Google-Python-Requests", "DuckDuckGo"],
    "auto_save_txt": True,
    "txt_filename_pattern": "busqueda_{target}.txt",
    "dork_query": "",
    "use_proxy": False,
    "proxy_url": "",
}

def mask_api_key(key: str) -> str:
    if not key or not key.strip():
        return ""
    key = key.strip()
    if len(key) <= 8:
        return "apikey-xxxxxxxxxx"
    prefix = key[:6]
    return f"{prefix}-xxxxxxxxxx"

def load_config(file_path: str = CONFIG_FILE) -> Dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    if os.path.exists(file_path):
        try:
            if os.path.getsize(file_path) > 0:
                with open(file_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        if "api_key" in loaded and isinstance(loaded["api_key"], str):
                            if loaded["api_key"].endswith("-xxxxxxxxxx"):
                                loaded["api_key"] = ""
                        config.update(loaded)
            else:
                save_config(config, file_path)
        except Exception as e:
            logger.error(f"Error cargando archivo de configuración {file_path}: {e}")
            try:
                save_config(config, file_path)
            except Exception:
                pass
    else:
        try:
            save_config(config, file_path)
        except Exception:
            pass

    return config

def save_config(config_data: Dict[str, Any], file_path: str = CONFIG_FILE) -> bool:
    try:
        clean_data = dict(config_data)
        if isinstance(clean_data.get("api_key"), str) and clean_data["api_key"].endswith("-xxxxxxxxxx"):
            clean_data["api_key"] = ""

        serialized = json.dumps(clean_data, indent=4, ensure_ascii=False)
        temp_file = f"{file_path}.tmp"
        
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(serialized)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_file, file_path)
        return True
    except Exception as e:
        logger.error(f"Error guardando archivo de configuración {file_path}: {e}")
        return False