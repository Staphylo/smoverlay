#
# This source comes from the following gist
# https://gist.github.com/mrzechonek/bd7c059b5742a9c1a7fd
#

from PyQt5.QtCore import QObject, pyqtWrapperType, pyqtProperty, pyqtSignal

class qmlProperty:
    """
        Just a placeholder, it gets replaced with pyqtProperty
        when creating the object. Used to customise signal name.
    """
    def __init__(self, property_type, signal=None):
        self.property_type = property_type
        self.signal= signal

class qmlWrapperType(pyqtWrapperType):
    def __new__(meta, name, bases, dct):
        def qml_property(prop_type, prop_name, notify, notify_name):
            """
                Create pyqtProperty object with value captured in the closure
                and a 'notify' signal attached.

                You need to pass both:
                    - unbound signal, because pyqtProperty needs it
                    - signal name to allow setter to find the *bound* signal
                      and emit it.
            """

            prop_name += '_'

            def getter(self):
                return getattr(self, prop_name)

            def setter(self, value):
                # FIXME this guard is useless if every field initialized from
                # prop_name before
                if hasattr(self, prop_name) and value == getattr(self, prop_name):
                    return
                setattr(self, prop_name, value)
                getattr(self, notify_name).emit(value)

            prop = pyqtProperty(
                type=prop_type,
                fget=getter,
                fset=setter,
                notify=notify)

            return prop

        # don't touch attributes other than qmlProperties
        properties = list(
            filter(
                lambda i: isinstance(i[1], qmlProperty),
                dct.items()
            )
        )

        for property_name, p in properties:
            # FIXME the signal is the same for every instance
            signal = pyqtSignal(p.property_type)
            signal_name = p.signal or property_name + "Changed"

            # create dedicated signal for each property
            dct[signal_name] = signal

            # substitute qmlProperty placeholder with real pyqtProperty
            dct[property_name] = qml_property(
                p.property_type,
                property_name,
                signal,
                signal_name
            )

        return super().__new__(meta, name, bases, dct)


class QmlObject(QObject, metaclass=qmlWrapperType):
    pass
