# Example plugin for QGIS User Conference 2026

QGIS Plugin for workshop, generated using [qgis-plugin-copier-template](https://github.com/osgeosuomi/qgis-plugin-copier-template.git).

## Development

See [development readme](./DEVELOPMENT.md).

### Translating with QT Linguistic

The translation files are in [i18n](./src/painter_plugin/resources/i18n) folder. Translatable
content in python files is code such as `tr(u"Hello World")`.

Translation files can be updated with `qpdt transup` or wait them to be updated automatically with "update-translations"
pre-commit hook.

After updating ts files, you can open file you wish to translate with Qt Linguist or code editor, make the changes and
compile the translations to .qm files using `qpdt transcompile` (works only on Linux, on Windows use Qt Linguist's File -> Release menu action).
