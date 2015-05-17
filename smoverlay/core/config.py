from functools import wraps
from collections import OrderedDict
import yaml
import os

from smoverlay.plugins import monitors

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
    return yaml.load(stream, OrderedLoader)


@wraps(yaml.dump_all)
def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)

def loadConfig(filepath):
    path = os.path.expanduser(filepath)
    if not os.path.isfile(path):
        print("No configuration file found under %s" % path)
        return None

    cfg = None
    with open(path) as f:
        cfg = ordered_load(f, yaml.SafeLoader)
    return cfg

def dumpConfig(filepath, config):
    path = os.path.expanduser(filepath)
    if os.path.exists(path):
        print("Overriding existing file %s" % path)
        # XXX add a warning?
        pass

    data = ordered_dump(config, Dumper=yaml.SafeDumper)
    with open(path, "w+") as f:
        f.write(data)

def generateConfig():
    config = OrderedDict()

    print("Autodetecting configuration")
    plugins = []
    for name, cls in monitors.items():
        mon = cls()
        moncfg = mon.defaultConfig()
        if not moncfg:
            # this monitor doesn't have any configuration meaning it's not
            # supported
            # XXX raise UnsupportedMonitor
            continue
        config[name] = moncfg
        plugins.append({ name: {
            "plugin": name,
            "config": config[name]
        }})
    config["plugins"] = plugins
    print(config)
    return config

