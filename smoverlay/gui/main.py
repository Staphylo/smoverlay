#!/usr/bin/env python3

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QSurface, QSurfaceFormat, QColor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QJSValue, qmlRegisterType, QQmlListProperty

#from smoverlay.gui.qmonitor import QMonitor
from smoverlay.plugins import qmonitors
from smoverlay.gui.remotecast import Remotecast

def listScreens(desktop):
    for i in range(desktop.screenCount()):
        rect = desktop.screenGeometry(i)
        if i == desktop.primaryScreen():
            print("primary ", end="")
        print("screen %d: %dx%d" % (i, rect.width(), rect.height()))

def main():
    app = QApplication(sys.argv)

    desktop = QApplication.desktop()
    listScreens(desktop)

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
    rc = Remotecast()
    rc.setGeometry(desktop.screenGeometry(desktop.primaryScreen()))
    context.setContextProperty('cast', rc)
    context.setContextProperty('view', view)

    # :: storage
    #qsm = QStorageMonitor()
    qsm = qmonitors["storage"]()
    sm = qsm.monitor
    sm.watch("/")
    sm.watch("/tmp")

    # :: memory
    #qmm = QMemoryMonitor()
    qmm = qmonitors["memory"]()
    #mm = qmm.monitor

    # :: network
    qnm = qmonitors["network"]()
    #qnm = QNetworkMonitor()

    monitors = {
        "Storage": qsm,
        "Memory": qmm,
        "Network": qnm
    }

    #types = [
    #    QMonitor,
    #    QMemoryMonitor, QMemory,
    #    QStorageMonitor, QDisk,
    #    QNetworkMonitor, QInterface,
    #]

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
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
