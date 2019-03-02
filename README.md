# smoverlay

## brief

This project is an overlay pane that slides from one of the sides.
When the mouse reach the side of the screen the pane will show some monitoring
information.

The initial goal was to play with python + Qml + Qt. It's also plugin based so
adding another element in the overlay is relatively straightforward.

The fun part of the project has been done so it's now dead.

## run me

python 3

```sh
# require qt5-python
virtualenv --system-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py develop

# for Qt gui
smoverlay
# for Cli
smoverlay-cli
```

## money shot

![smoverlay](https://i.imgur.com/3lnScG1.png "Screenshot of smoverlay")
