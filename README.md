# Example plugin for QGIS User Conference 2026

[![prek](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

QGIS Plugin for workshop, generated using [qgis-plugin-copier-template](https://github.com/osgeosuomi/qgis-plugin-copier-template.git).

A geopackage with a polygon and raster data for the workshop is found from [example folder](./example).

## Development

See [development readme](./DEVELOPMENT.md).

### Translating with Qt Linguist

The translation files are in [i18n](./src/painter_plugin/resources/i18n)
folder. Translatable content in python files is code such as `tr("Hello World")`.

Translation files can be updated with `qpdt transup` or wait them to be updated
automatically with "update-translations" pre-commit hook.

After updating ts files, you can open file you wish to translate with Qt Linguist or
code editor, make the changes and compile the translations to .qm files using
`qpdt transcompile` (works only on Linux, on Windows use Qt Linguist's File ->
Release menu action).
