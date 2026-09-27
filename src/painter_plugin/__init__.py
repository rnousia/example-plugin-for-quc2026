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

import typing

from qgis.utils import plugins

from painter_plugin.utils import i18n_utils

if typing.TYPE_CHECKING:
    from qgis.PyQt import QtCore

    from painter_plugin.plugin import PainterPlugin

TRANSLATORS: "list[QtCore.QTranslator]" = []


def classFactory(_) -> "PainterPlugin":  # noqa: ANN001, N802
    """Class factory."""
    TRANSLATORS.extend(i18n_utils.setup_all_translators())

    from painter_plugin.plugin import PainterPlugin  # noqa: PLC0415

    return PainterPlugin()


def get_instance() -> "PainterPlugin | None":
    """Get instance."""
    return plugins.get(__name__)
