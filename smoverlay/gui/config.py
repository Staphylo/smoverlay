
from .qmlobject import QmlObject, QObject, qmlProperty

class UIStyle(QmlObject):
    background = qmlProperty('QString')
    textcolor = qmlProperty('QString')
    fontsize = qmlProperty('QString')

    def __init__(self, style):
        QObject.__init__(self)
        self.background_ = style["background"]
        self.textcolor_ = style["text"]
        self.fontsize_ = style["fontsize"]

    @staticmethod
    def defaultConfig():
        return {
            "background": "black",
            "text": "white",
            "fontsize": "12px"
        }

class UIConfig(QmlObject):
    screen = qmlProperty(int)
    hideDelay = qmlProperty(int)
    showDelay = qmlProperty(int)
    screenWidth = qmlProperty(int)
    screenHeight = qmlProperty(int)
    overlayWidth = qmlProperty(int)
    overlayHeight = qmlProperty(int)
    overlayShowX = qmlProperty(int)
    overlayHideX = qmlProperty(int)
    opacityShow = qmlProperty(float)
    opacityHide = qmlProperty(float)

    style = qmlProperty(UIStyle)

    def __init__(self, config):
        QObject.__init__(self)
        self.screenWidth_ = 0
        self.screenHeight_ = 0
        self.overlayWidth_ = 0
        self.overlayHeight_ = 0
        self.screen_ = config["screen"] # TODO: check if valid. setdefault?
        self.position_ = config["position"] # TODO: same everywhere
        self.overlayWidth_ = config["width"]
        self.opacityShow = config["opacity_show"]
        self.opacityHide = config["opacity_hide"]
        self.showDelay = config["show_delay"] * 1000
        self.hideDelay = config["hide_delay"] * 1000

        self.style_ = UIStyle(config["style"])

    def setGeometry(self, desktop):
        rect = desktop.screenGeometry(self.screen_)
        self.screenHeight = rect.height()
        self.screenWidth = rect.width()
        self.overlayHeight = self.screenHeight

        if self.position_ == "right":
            self.overlayHideX = self.screenWidth - 1
            self.overlayShowX = self.screenWidth - self.overlayWidth
        else:
            self.overlayHideX = -self.overlayWidth + 1
            self.overlayShowX = 0

    @staticmethod
    def defaultConfig(desktop):
        return {
            "opacity_show": 1,
            "opacity_hide": 0,
            "show_delay": 0.2,
            "hide_delay": 0.5,
            "width": 250,
            "position": "left",
            "screen": desktop.primaryScreen(),
            "style": UIStyle.defaultConfig()
        }
