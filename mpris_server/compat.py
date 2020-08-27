# Python and DBus compatibility
# See:  https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/
import logging
from random import choices
from typing import Dict, Tuple, Any

from gi.repository.GLib import Variant
from unidecode import unidecode

from .base import VALID_CHARS, Metadata, DbusMetadata, DbusTypes, \
    RAND_CHARS, NAME_PREFIX


logger = logging.getLogger(__name__)

# map of DBus metadata entries and their DBus types
METADATA_TYPES: Dict[str, str] = {
    "mpris:trackid": "o",
    "mpris:length": "x",
    "mpris:artUrl": "s",
    "xesam:url": "s",
    "xesam:title": "s",
    "xesam:artist": "as",
    "xesam:album": "s",
    "xesam:albumArtist": "as",
    "xesam:discNumber": 'i',
    "xesam:trackNumber": 'i',
    "xesam:comment": "as",
}

START_WITH = "_"
FIRST_CHAR = 0

# following must be subscriptable to be used with choices()
VALID_CHARS_SUB: Tuple[str] = tuple(VALID_CHARS)


def to_ascii(text: str) -> str:
    return unidecode(text)


def random_name() -> str:
    return NAME_PREFIX + ''.join(choices(VALID_CHARS_SUB, k=RAND_CHARS))


def get_dbus_name(name: str = None) -> str:
    if not name:
        return random_name()
    
    # convert utf8 to ascii
    new_name = to_ascii(name)

    # new name shouldn't have spaces
    new_name = new_name.replace(' ', '_')

    # new name should only contain DBus valid chars
    new_name = ''.join(char for char in new_name
                       if char in VALID_CHARS)

    # DBus names can't start with numbers
    if new_name and new_name[FIRST_CHAR].isnumeric():
        # just stick an underscore in front of the number
        return START_WITH + new_name

    # but they can start with letters or underscore
    elif new_name:
        return new_name

    # if there is no name left after normalizing,
    # then make a random one and validate it
    return get_dbus_name(random_name())


def is_null_list(obj: Any) -> bool:
    if isinstance(obj, list):
        return all(item is None for item in obj)

    return False


def is_dbus_type(obj: Any) -> bool:
    return isinstance(obj, DbusTypes.__args__)


def is_valid_metadata(key: str, obj: Any) -> bool:
    if key not in METADATA_TYPES:
        return False

    return is_dbus_type(obj) and not is_null_list(obj)


def get_dbus_metadata(metadata: Metadata) -> DbusMetadata:
    return {key: Variant(METADATA_TYPES[key], val)
            for key, val in metadata.items()
            if is_valid_metadata(key, val)}