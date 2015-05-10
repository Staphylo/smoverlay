"""
Usage: smoverlay [--debug] [--config filename] [--info] [--write] [--notify]

Options:
    --debug             add verbosity
    --config filename   load this configuration file [default: ~/.smoverlayrc]
    --info              display information
    --notify            send a signal to a running process
"""

import sys
from docopt import docopt
from collections import OrderedDict

from PyQt5.QtCore import *
from PyQt5.QtGui import QSurface, QSurfaceFormat, QColor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QJSValue, qmlRegisterType, QQmlListProperty

from smoverlay.plugins import qmonitors
from smoverlay.gui.remotecast import Remotecast
from smoverlay.core.config import loadConfig, generateConfig, dumpConfig

docstring = __doc__

try:
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
except ImportError:
    pass

def listScreens(desktop):
    for i in range(desktop.screenCount()):
        rect = desktop.screenGeometry(i)
        if i == desktop.primaryScreen():
            print("primary ", end="")
        print("screen %d: %dx%d" % (i, rect.width(), rect.height()))

def createWindow():

    view = QQuickView()
    view.setSurfaceType(QSurface.OpenGLSurface)

    fmt = QSurfaceFormat()
    fmt.setAlphaBufferSize(8)
    fmt.setRenderableType(QSurfaceFormat.OpenGL)
    view.setFormat(fmt)

    color = QColor()
    color.setRedF(0.0)
    color.setGreenF(0.0)
    color.setBlueF(0.0)
    color.setAlphaF(0.0)
    view.setColor(color)

    view.setClearBeforeRendering(True)
    view.setFlags(Qt.FramelessWindowHint | Qt.ToolTip | Qt.WindowStaysOnTopHint)

    context = view.rootContext()

    qmlRegisterType(Remotecast, "remotecast", 1, 0, "RemoteCast")
    return (view, context)

def runApplication(config):
    app = QApplication([sys.argv[0]])

    desktop = QApplication.desktop()
    listScreens(desktop)

    (view, context) = createWindow()

    rc = Remotecast()
    rc.setGeometry(desktop.screenGeometry(desktop.primaryScreen()))
    context.setContextProperty('cast', rc)
    context.setContextProperty('view', view)

    monitors = OrderedDict()
    for plugin in config["plugins"]:
        for name, data in plugin.items():
            m = qmonitors[data["plugin"]]()
            m.loadConfig(data["config"])
            monitors[name] = m

    types = []
    for monitor in monitors.values():
        types += monitor.types()

    print(types)

    for typ in types:
        qmlRegisterType(typ, "lol", 1, 0, typ.__name__)

    for mon in monitors.values():
        mon.update()

    monitorList = [v for k, v in monitors.items()]

    context.setContextProperty("monitors", monitorList)

    #view.setSource(QUrl("qml/main.qml"))
    view.setSource(QUrl("gui/qml/main.qml"))

    view.setResizeMode(QQuickView.SizeRootObjectToView)
    #view.rootObject().window().move(desktop.screenGeometry(1).topLeft())
    #view.rootObject.setScreen(t
    #view.setScreen(QApplication.screens()[1])
    #view.openglContext().setScreen(QApplication.screens()[1])
    view.engine().quit.connect(app.quit)

    view.show()
    return app.exec()

def information():
    print("Plugin loaded:")
    for name, cls in qmonitors.items():
        print(" - %s (%s)" % (name, cls))

def main():
    args = docopt(docstring, version="devel")

    dumpconfig = False
    if args["--info"]:
        information()
        return 0
    if args["--debug"]:
        pass
    if args["--write"]:
        dumpconfig = True

    config = loadConfig(args["--config"])
    if not config:
        config = generateConfig()
        if dumpconfig:
            dumpConfig(args["--config"], config)

    return runApplication(config)

if __name__ == "__main__":
    sys.exit(main())
