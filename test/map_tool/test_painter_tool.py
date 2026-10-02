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

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsGeometry,
    QgsPointXY,
    QgsProject,
    QgsRasterLayer,
    QgsSingleSymbolRenderer,
    QgsVectorLayer,
    QgsVectorLayerUtils,
)
from qgis.gui import QgsMapToolIdentify, QgsMapToolPan
from qgis_plugin_tools.utils.typing_utils import require

from painter_plugin.map_tool.painter_tool import PainterTool

if TYPE_CHECKING:
    from qgis.gui import QgsMapCanvas


MOUSE_LOCATION = QgsPointXY(1, 1)


# Adapted from https://github.com/nlsfi/pickLayer/blob/main/test/unit/test_set_active_layer_tool.py
@pytest.fixture
def test_layers() -> dict[Qgis.GeometryType, QgsVectorLayer]:
    layers = [
        QgsVectorLayer("PointZ", "point_layer", "memory"),
        QgsVectorLayer("LineStringZ", "line_layer", "memory"),
        QgsVectorLayer("PolygonZ", "polygon_layer", "memory"),
    ]

    wkt_geom_collection = [
        ("Point (-1 0)", "Point (-2 0)"),
        ("LineString (1 0, 1 5)", "LineString (2 0, 2 5)"),
        (
            "Polygon ((1 1, 1 2, 2 2, 2 1, 1 1))",
            "Polygon ((2 0, 2 3, 3 3, 3 0, 2 0))",
        ),
    ]

    for layer, wkt_geoms in zip(layers, wkt_geom_collection, strict=True):
        features = [
            QgsVectorLayerUtils.createFeature(layer, QgsGeometry.fromWkt(wkt_geoms[0])),
            QgsVectorLayerUtils.createFeature(layer, QgsGeometry.fromWkt(wkt_geoms[1])),
        ]

        assert all(not feature.geometry().isNull() for feature in features)
        success, _ = require(layer.dataProvider()).addFeatures(features)
        assert success

        require(QgsProject.instance()).addMapLayer(layer)
    return {layer.geometryType(): layer for layer in layers}


@pytest.fixture
def painter_tool(qgis_canvas: "QgsMapCanvas") -> PainterTool:
    map_tool = PainterTool(qgis_canvas)

    # Set search radius to 0 for tests
    if Qgis.versionInt() >= 34200:
        overrides = QgsMapToolIdentify.IdentifyProperties()
        overrides.searchRadiusMapUnits = 0.0
        map_tool.setPropertiesOverrides(overrides)
    else:
        map_tool.setCanvasPropertiesOverrides(0.0)

    return map_tool


def test_paint_layer_at_location_changes_layer_fill_color(
    painter_tool: PainterTool, test_layers: dict[Qgis.GeometryType, QgsVectorLayer]
):
    painter_tool._paint_layer_at_location(QgsPointXY(3, 3))

    renderer = test_layers[Qgis.GeometryType.Polygon].renderer()
    assert isinstance(renderer, QgsSingleSymbolRenderer)
    symbol = renderer.symbol()
    assert symbol is not None
    assert symbol.color() == painter_tool.PAINT_COLOR


def test_paint_layer_at_location_does_nothing_if_no_layer_found_at_location(
    qgis_canvas: "QgsMapCanvas",
    painter_tool: PainterTool,
    test_layers: dict[Qgis.GeometryType, QgsVectorLayer],
):
    previous_tool = QgsMapToolPan(qgis_canvas)
    painter_tool.previous_tool = previous_tool
    assert qgis_canvas.mapTool() is None

    painter_tool._paint_layer_at_location(QgsPointXY(100, 100))

    for layer in test_layers.values():
        renderer = layer.renderer()
        assert isinstance(renderer, QgsSingleSymbolRenderer)
        symbol = renderer.symbol()
        assert symbol is not None
        assert symbol.color() != painter_tool.PAINT_COLOR

    assert qgis_canvas.mapTool() is None


@pytest.mark.usefixtures("test_layers")
def test_paint_layer_at_location_restores_previous_tool_if_tool_was_selected(
    qgis_canvas: "QgsMapCanvas", painter_tool: PainterTool
):
    previous_tool = QgsMapToolPan(qgis_canvas)
    painter_tool.previous_tool = previous_tool
    assert qgis_canvas.mapTool() is None

    painter_tool._paint_layer_at_location(QgsPointXY(-1, 0))

    assert qgis_canvas.mapTool() == previous_tool


@pytest.mark.usefixtures("test_layers")
@pytest.mark.parametrize(
    ("at_location", "expected_layer_type"),
    [
        (QgsPointXY(-1, 0), Qgis.GeometryType.Point),
        (QgsPointXY(2, 0), Qgis.GeometryType.Line),
        (QgsPointXY(3, 3), Qgis.GeometryType.Polygon),
    ],
    ids=[
        "point layer",
        "line layer on top of polygon layer",
        "polygon layer",
    ],
)
def test_find_top_layer_at_location(
    painter_tool: PainterTool,
    at_location: QgsPointXY,
    expected_layer_type: Qgis.GeometryType,
):
    resulting_layer = painter_tool._find_top_layer_at_location(at_location)

    assert resulting_layer is not None
    assert resulting_layer.geometryType() == expected_layer_type


def test_paint_layer_at_location_does_nothing_if_raster_clicked(
    painter_tool: PainterTool,
):
    # Setup adapted from https://github.com/nlsfi/pickLayer/blob/main/test/unit/test_set_active_layer_tool.py
    # Raster file has 1,1 -> 2,2 bbox (EPSG:4326)
    raster_layer = QgsRasterLayer(
        str(Path(__file__).parents[1] / "data/raster/image.tif")
    )
    assert raster_layer.isValid()

    require(QgsProject.instance()).addMapLayer(raster_layer)
    require(QgsProject.instance()).setCrs(QgsCoordinateReferenceSystem.fromEpsgId(4326))
    require(painter_tool.canvas()).setDestinationCrs(
        QgsCoordinateReferenceSystem.fromEpsgId(4326)
    )

    # Add function call to test here with correct arguments
    # Check raster file extent with debugger using raster_layer.extent()
