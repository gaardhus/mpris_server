from __future__ import annotations
from typing import NamedTuple, Any, Optional, Union, \
  cast

from gi.repository.GLib import Variant
from strenum import StrEnum

from ..base import DbusTypes, DbusMetadata, DEFAULT_TRACK_ID, \
  DbusTypes, MprisTypes, DbusType, PyType
from ..types import Final, TypedDict, is_type, get_type


DEFAULT_METADATA: Final[Metadata] = {}


MetadataEntry = str


class MetadataEntries(StrEnum):
  TRACKID: MetadataEntry = "mpris:trackid"
  LENGTH: MetadataEntry = "mpris:length"
  ART_URL: MetadataEntry = "mpris:artUrl"
  URL: MetadataEntry = "xesam:url"
  TITLE: MetadataEntry = "xesam:title"
  ARTIST: MetadataEntry = "xesam:artist"
  ALBUM: MetadataEntry = "xesam:album"
  ALBUM_ARTIST: MetadataEntry = "xesam:albumArtist"
  DISC_NUMBER: MetadataEntry = "xesam:discNumber"
  TRACK_NUMBER: MetadataEntry = "xesam:trackNumber"
  COMMENT: MetadataEntry = "xesam:comment"


# MetadataEntries: Final = _MetadataEntries()


# map of D-Bus metadata entries and their D-Bus types
METADATA_TYPES: Final[dict[MetadataEntry, DbusType]] = {
  MetadataEntries.TRACKID: DbusTypes.OBJ,
  MetadataEntries.LENGTH: DbusTypes.INT64,
  MetadataEntries.ART_URL: DbusTypes.STRING,
  MetadataEntries.URL: DbusTypes.STRING,
  MetadataEntries.TITLE: DbusTypes.STRING,
  MetadataEntries.ARTIST: DbusTypes.STRING_ARRAY,
  MetadataEntries.ALBUM: DbusTypes.STRING,
  MetadataEntries.ALBUM_ARTIST: DbusTypes.STRING_ARRAY,
  MetadataEntries.DISC_NUMBER: DbusTypes.INT32,
  MetadataEntries.TRACK_NUMBER: DbusTypes.INT32,
  MetadataEntries.COMMENT: DbusTypes.STRING_ARRAY,
}

DBUS_PY_TYPES: Final[dict[DbusType, PyType]] = {
  DbusTypes.OBJ: MprisTypes.OBJ,
  DbusTypes.STRING: MprisTypes.STRING,
  DbusTypes.INT32: MprisTypes.INT32,
  DbusTypes.INT64: MprisTypes.INT64,
  DbusTypes.UINT32: MprisTypes.UINT32,
  DbusTypes.UINT64: MprisTypes.UINT64,
  DbusTypes.DOUBLE: MprisTypes.DOUBLE,
  DbusTypes.BOOLEAN: MprisTypes.BOOLEAN,
  DbusTypes.OBJ_ARRAY: MprisTypes.OBJ_ARRAY,
  DbusTypes.STRING_ARRAY: MprisTypes.STRING_ARRAY,
}

METADATA_PY_TYPES: Final[dict[MetadataEntry, PyType]] = {
  MetadataEntries.TRACKID: DBUS_PY_TYPES[DbusTypes.OBJ],
  MetadataEntries.LENGTH: DBUS_PY_TYPES[DbusTypes.INT64],
  MetadataEntries.ART_URL: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.URL: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.TITLE: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.ARTIST: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.ALBUM: DBUS_PY_TYPES[DbusTypes.STRING],
  MetadataEntries.ALBUM_ARTIST: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY],
  MetadataEntries.DISC_NUMBER: DBUS_PY_TYPES[DbusTypes.INT32],
  MetadataEntries.TRACK_NUMBER: DBUS_PY_TYPES[DbusTypes.INT32],
  MetadataEntries.COMMENT: DBUS_PY_TYPES[DbusTypes.STRING_ARRAY]
}


class _MetadataTypes(NamedTuple):
  TRACKID: PyType = METADATA_PY_TYPES[MetadataEntries.TRACKID]
  LENGTH: PyType = METADATA_PY_TYPES[MetadataEntries.LENGTH]
  ART_URL: PyType = METADATA_PY_TYPES[MetadataEntries.ART_URL]
  URL: PyType = METADATA_PY_TYPES[MetadataEntries.URL]
  TITLE: PyType = METADATA_PY_TYPES[MetadataEntries.TITLE]
  ARTIST: PyType = METADATA_PY_TYPES[MetadataEntries.ARTIST]
  ALBUM: PyType = METADATA_PY_TYPES[MetadataEntries.ALBUM]
  ALBUM_ARTIST: PyType = METADATA_PY_TYPES[MetadataEntries.ALBUM_ARTIST]
  DISC_NUMBER: PyType = METADATA_PY_TYPES[MetadataEntries.DISC_NUMBER]
  TRACK_NUMBER: PyType = METADATA_PY_TYPES[MetadataEntries.TRACK_NUMBER]
  COMMENT: PyType = METADATA_PY_TYPES[MetadataEntries.COMMENT]


MetadataTypes: Final = _MetadataTypes()


class MetadataObj(NamedTuple):
  title: Optional[MprisTypes.STRING] = None
  artists: Optional[MprisTypes.STRING_ARRAY] = None
  album: Optional[MprisTypes.STRING] = None
  album_artists: Optional[MprisTypes.STRING_ARRAY] = None
  length: Optional[MprisTypes.LENGTH] = None
  url: Optional[MprisTypes.STRING] = None
  art_url: Optional[MprisTypes.STRING] = None
  disc_no: Optional[MprisTypes.INT32] = None
  track_no: Optional[MprisTypes.INT32] = None
  comments: Optional[MprisTypes.STRING_ARRAY] = None
  track_id: MprisTypes.TRACKID = DEFAULT_TRACK_ID

  def to_dict(self) -> Metadata:
    return {
      key: val
      for key, val in zip(MetadataEntries, self)
      if val is not None
    }


Metadata = \
  TypedDict('Metadata', METADATA_PY_TYPES, total=False)

ValidMetadata = Union[Metadata, MetadataObj]


def get_runtime_types() -> tuple[type, ...]:
  types = {
    get_type(val)
    for val in DBUS_PY_TYPES.values()
    if is_type(val)
  }

  return tuple(types)


DBUS_RUNTIME_TYPES: Final[tuple[type, ...]] = \
  get_runtime_types()


def is_null_list(obj: Any) -> bool:
  if isinstance(obj, list):
    return all(item is None for item in obj)

  return False


def is_dbus_type(obj: Any) -> bool:
  return isinstance(obj, DBUS_RUNTIME_TYPES)


def is_valid_metadata(entry: str, obj: Any) -> bool:
  if obj is None or entry not in METADATA_TYPES:
    return False

  return is_dbus_type(obj) and not is_null_list(obj)


def get_dbus_var(entry: MetadataEntry, obj: DbusType) -> Variant:
  return Variant(METADATA_TYPES[entry], obj)


def get_dbus_metadata(metadata: ValidMetadata) -> DbusMetadata:
  if isinstance(metadata, MetadataObj):
    metadata: Metadata = metadata.to_dict()

  metadata = cast(Metadata, metadata)

  return {
    entry: get_dbus_var(entry, val)
    for entry, val in metadata.items()
    if is_valid_metadata(entry, val)
  }
