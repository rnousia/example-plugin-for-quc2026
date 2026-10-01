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

from typing import TYPE_CHECKING

import pytest
from qgis.gui import QgsMapToolPan

from painter_plugin import classFactory

if TYPE_CHECKING:
    from collections.abc import Iterator

    from qgis.gui import QgisInterface, QgsMapCanvas

    from painter_plugin.plugin import PainterPlugin


@pytest.fixture
def plugin_loaded(qgis_iface: "QgisInterface") -> "Iterator[PainterPlugin]":
    plugin = classFactory(qgis_iface)
    plugin.initGui()

    yield plugin

    plugin.unload()


def test_plugin_loads_without_errors(plugin_loaded: "PainterPlugin") -> None:
    assert plugin_loaded.toolbar is not None


def test_trigger_painter_tool_action_activates_tool(
    plugin_loaded: "PainterPlugin",
    qgis_canvas: "QgsMapCanvas",
) -> None:

    assert plugin_loaded.painter_tool_action
    plugin_loaded.painter_tool_action.trigger()

    assert qgis_canvas.mapTool() == plugin_loaded.painter_tool
    assert plugin_loaded.painter_tool.previous_tool is None


def test_trigger_painter_tool_action_saves_previous_tool(
    plugin_loaded: "PainterPlugin",
    qgis_canvas: "QgsMapCanvas",
) -> None:
    map_tool = QgsMapToolPan(qgis_canvas)
    qgis_canvas.setMapTool(map_tool)

    assert plugin_loaded.painter_tool_action
    plugin_loaded.painter_tool_action.trigger()

    assert qgis_canvas.mapTool() == plugin_loaded.painter_tool
    assert plugin_loaded.painter_tool.previous_tool == map_tool
