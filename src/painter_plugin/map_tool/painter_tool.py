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
from typing import (
    TYPE_CHECKING,
    cast,
)

from qgis.core import (
    QgsGeometry,
    QgsSingleSymbolRenderer,
    QgsSymbol,
    QgsVectorLayer,
)
from qgis.gui import (
    QgsMapCanvas,
    QgsMapMouseEvent,
    QgsMapToolIdentify,
)
from qgis.PyQt.QtGui import QColor, QCursor
from qgis.utils import iface as utils_iface
from qgis_plugin_tools.tools.i18n import tr
from qgis_plugin_tools.utils.typing_utils import require

if TYPE_CHECKING:
    from qgis.core import QgsPointXY, QgsVectorLayer
    from qgis.gui import QgisInterface, QgsMapTool

iface = cast("QgisInterface", utils_iface)

LOGGER = logging.getLogger(__name__)


class PainterTool(QgsMapToolIdentify):
    """Map tool to repaint layers styled by simple fill."""

    PAINT_COLOR = QColor("#002F6C")

    def __init__(
        self,
        canvas: "QgsMapCanvas | None",
    ) -> None:
        super().__init__(canvas)

        self.setCursor(QCursor())
        self.previous_tool: QgsMapTool | None = None

    @typing.override
    def canvasReleaseEvent(self, e: "QgsMapMouseEvent | None") -> None:
        self._paint_layer_at_location(self._point_xy_from_mouse_event(e))

    def _point_xy_from_mouse_event(
        self, mouse_event: "QgsMapMouseEvent | None"
    ) -> "QgsPointXY":
        return self.toMapCoordinates(require(mouse_event).pos())  # noqa: SC200

    def _paint_layer_at_location(self, location: "QgsPointXY") -> None:
        layer_to_paint = self._find_top_layer_at_location(location)

        if layer_to_paint is not None:
            LOGGER.info(tr("Repainting layer {} to blue", layer_to_paint.name()))
            self._repaint_layer(layer_to_paint)

            if self.previous_tool is not None:
                require(iface.mapCanvas()).setMapTool(self.previous_tool)

    def _find_top_layer_at_location(
        self, location: "QgsPointXY"
    ) -> "QgsVectorLayer | None":
        identify_results = self.identify(
            geometry=QgsGeometry.fromPointXY(location),
            mode=QgsMapToolIdentify.IdentifyMode.TopDownStopAtFirst,
            layerType=QgsMapToolIdentify.Type.AllLayers,
        )

        if len(identify_results) < 1:
            return None

        identify_result = identify_results[0]
        layer, _feature = (
            cast("QgsVectorLayer", identify_result.mLayer),
            identify_result.mFeature,
        )

        return layer

    def _repaint_layer(self, layer: "QgsVectorLayer") -> None:
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        if symbol is not None:
            symbol.setColor(self.PAINT_COLOR)
            layer.setRenderer(QgsSingleSymbolRenderer(symbol))
            layer.triggerRepaint()
