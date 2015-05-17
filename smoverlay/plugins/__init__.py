
import os
import sys
from importlib.machinery import SourceFileLoader
from importlib import import_module

from smoverlay.core.monitor import Monitor
from smoverlay.gui.qmonitor import QMonitor

pluginspath = os.path.dirname(os.path.realpath(__file__))

plugins = []
for subdir, dirs, files in os.walk(pluginspath):
    for plugin in dirs:
        if not plugin.startswith("__"):
            plugins.append(plugin)
    break

from pathlib import Path

monitors = {}
qmonitors = {}
for plugin in plugins:
    for subdir, dirs, files in os.walk(os.path.join(pluginspath, plugin)):
        #print("Loading plugin %s" % plugin)
        parent = import_module("smoverlay.plugins." + plugin)
        for f in files:
            if f.startswith('__') or not f.endswith('.py'):
                continue
            filename = os.path.join(subdir, f)
            #print(" - %s" % filename)
            modname = "smoverlay.plugins." + plugin + "." + Path(filename).stem
            #print(" - %s" % modname)
            #sys.modules["smoverlay.plugins." + plugin] = []
            loader = SourceFileLoader(modname, filename)
            mod = loader.load_module()
            if hasattr(mod, 'PLUGIN_SKIP'):
                continue
            setattr(mod, modname, mod)
            for objname in dir(mod):
                if objname.startswith('__'):
                    continue
                obj = getattr(mod, objname)
                if hasattr(obj, '__bases__'):
                    for base in obj.__bases__:
                        if base == QMonitor:
                            qmonitors[plugin] = obj
                        elif base == Monitor:
                            monitors[plugin] = obj
        break

