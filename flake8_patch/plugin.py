from flake8_plugin_utils import Plugin

from flake8_patch import __version__
from flake8_patch.visitors.assignment import AssignmentVisitor


class PatchPlugin(Plugin[None]):
    name = "flake8-patch"
    version = __version__
    visitors = [AssignmentVisitor]
