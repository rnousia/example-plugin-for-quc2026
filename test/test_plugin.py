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

from collections.abc import Iterator
from typing import TYPE_CHECKING

import pytest
from pytest_mock import MockerFixture
from qgis.PyQt.QtWidgets import QMessageBox

from painter_plugin import classFactory

if TYPE_CHECKING:
    from unittest.mock import MagicMock

    from pytest_mock import MockerFixture
    from pytest_qgis import QgisInterface

    from painter_plugin.plugin import Plugin


@pytest.fixture(autouse=True)
def mock_message_box_ok(mocker: "MockerFixture") -> "MagicMock":
    return mocker.patch.object(
        QMessageBox, "information", return_value=QMessageBox.StandardButton.Ok
    )


@pytest.fixture
def plugin_loaded(qgis_iface: "QgisInterface") -> Iterator["Plugin"]:
    plugin = classFactory(qgis_iface)
    plugin.initGui()

    yield plugin

    plugin.unload()


def test_plugin_loads_without_errors(
    mock_message_box_ok: "MagicMock", plugin_loaded: "Plugin"
) -> None:
    mock_message_box_ok.assert_called_once()

    # TODO: assert components initialized etc.
    # assert plugin_loaded.toolbar is not None
