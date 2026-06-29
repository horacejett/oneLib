from importlib import metadata

from onelib.core.cache import cache_manager
from onelib.interface.custom.custom_component import CustomComponent

# from onelib.processing.process import load_flow_from_json  # noqa: E402

try:
    # SetujuciGo to automatic modification
    __version__ = '2.4.0-beta1-fix'
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ''
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = ['cache_manager', 'CustomComponent']
