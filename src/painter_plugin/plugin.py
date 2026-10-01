# Copyright (C) 2026 Painter Plugin Contributors.
#
#
# This file is part of Painter Plugin.
#
# Painter Plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Painter Plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Painter Plugin.  If not, see <https://www.gnu.org/licenses/>.

import logging
import typing

import qgis_plugin_tools
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolBar
from qgis.utils import iface as utils_iface
from qgis_plugin_tools.tools import custom_logging
from qgis_plugin_tools.tools.decorations import log_if_fails
from qgis_plugin_tools.tools.i18n import tr
from qgis_plugin_tools.tools.resources import resources_path
from qgis_plugin_tools.utils.typing_utils import require

import painter_plugin
from painter_plugin import env
from painter_plugin.map_tool.painter_tool import PainterTool

if typing.TYPE_CHECKING:
    from qgis.gui import QgisInterface


LOGGER = logging.getLogger(__name__)

iface = typing.cast("QgisInterface", utils_iface)


class PainterPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self) -> None:
        self._teardown_loggers = lambda: None

        self.toolbar: QToolBar | None = None
        self.painter_tool = PainterTool(require(iface.mapCanvas()))
        self.painter_tool_action: QAction | None = None

    def initGui(self) -> None:  # noqa: N802
        """Init gui."""
        global iface  # noqa: PLW0602

        self._teardown_loggers = custom_logging.setup_loggers(
            painter_plugin.__name__,
            qgis_plugin_tools.__name__,
            message_log_name=tr("Painter Plugin"),
        )

        toolbar = iface.addToolBar(
            tr("Painter Plugin Toolbar"),
        )
        if not toolbar:
            raise RuntimeError

        toolbar.setObjectName("painter-plugin-toolbar")

        self.painter_tool_action = QAction(
            QIcon(resources_path("icon/painter_tool.svg")),
            tr("Paint layers"),
            iface.mainWindow(),
        )
        self.painter_tool_action.triggered.connect(self._activate_painter_tool)

        self.painter_tool.setAction(self.painter_tool_action)

        toolbar.addAction(self.painter_tool_action)

        self.toolbar = toolbar

        if hasattr(iface, "initializationCompleted"):
            iface.initializationCompleted.connect(self.iface_initialization_completed)

        if bool(env.IS_DEVELOPMENT_MODE):
            self.iface_initialization_completed()

        LOGGER.info("Plugin initialized")

    def unload(self) -> None:
        """Unload plugin."""
        if self.painter_tool_action is not None:
            iface.removeToolBarIcon(self.painter_tool_action)
            iface.unregisterMainWindowAction(self.painter_tool_action)
            self.painter_tool_action.deleteLater()
        self.painter_tool_action = None

        if self.toolbar is not None:
            self.toolbar.deleteLater()
        self.toolbar = None

        self._teardown_loggers()
        self._teardown_loggers = lambda: None

    @log_if_fails
    def iface_initialization_completed(self) -> None:
        """Run additional setup for the plugin.

        Executed after initializationCompleted signal is emitted.
        """

    def _activate_painter_tool(self) -> None:
        """Activates painter tool."""
        canvas = require(iface.mapCanvas())
        if canvas.mapTool() is not None:
            self.painter_tool.previous_tool = canvas.mapTool()
        canvas.setMapTool(self.painter_tool)
