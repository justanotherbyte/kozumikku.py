__title__ = "kozumikku.py"
__author__ = "justanotherbyte"
__version__ = "1.0.0a"

from .image import Image, ImageEndpoint
from .client import KozumikkuClient
from .errors import *
from .genshin import (
    GenshinCharacter,
    CharacterImage,
    CharacterInfo
)
