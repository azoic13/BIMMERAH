"""
Utility functions and helpers
"""

import logging
from datetime import datetime


def setup_logging(log_level=logging.INFO):
    """Configure application logging"""
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("bimmerah.log")
        ]
    )


def get_timestamp() -> str:
    """Get current timestamp"""
    return datetime.now().isoformat()


def validate_port(port: str) -> bool:
    """Validate serial/USB port format"""
    if not port:
        return False
    return True
