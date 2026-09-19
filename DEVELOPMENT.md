# Development environment setup

## Create and configure a virtual environment

On Linux:

* Install [uv](https://docs.astral.sh/uv/) if not already available: `pip install uv`
* Create a Python virtual environment with access to the libraries provided by
  the QGIS installation:
  `uv venv .venv --system-site-packages`

On Windows:

* You can use the [qgis-venv-creator tool](https://github.com/GispoCoding/qgis-venv-creator)
  to make sure the virtual environment is configured correctly for QGIS
* Install `uv` to the virtual environment: `pip install uv`

When virtual environment is ready and activated:

* Install dependencies: `uv sync`
* Install pre-commit hooks: `prek install`
* Run tests: `pytest`

## Running QGIS in development mode

Before starting development, create a `.env` file by copying `.env.example` and updating the configuration values as needed.

Start QGIS with the plugin loaded in development mode:

```bash
qgis-plugin-dev-tools start

# Short form
qpdt s
```

For more information about the development workflow, see the [qgis-plugin-dev-tools documentation](https://github.com/nlsfi/qgis-plugin-dev-tools#plugin-development-mode).

## Managing dependencies

This project uses [uv](https://docs.astral.sh/uv/concepts/projects/dependencies/) for dependency management.

## Code quality and style

The included `painter-plugin.code-workspace` file is preconfigured for VS Code and provides recommended settings for:

* Formatting
* Linting
* Type checking
* Test execution
* Recommended extensions

## Commit message convention

Commit messages should follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) convention.
