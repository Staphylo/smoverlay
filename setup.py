from setuptools import setup, find_packages

setup(
    name = "smoverlay",
    version = "0.1",
    packages = find_packages(),
    entry_points = {
        "console_scripts": [
            "smoverlay-cli = smoverlay.cli.main:main",
        ],
        "gui_scripts": [
            "smoverlay = smoverlay.gui.main:main",
        ],
    },
    package_data = {
        'smoverlay.gui': ['qml/**/*.qml', 'icons/**/*.svg', 'icons/**/*.png' ],
    },
)
