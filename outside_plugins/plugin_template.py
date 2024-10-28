from plugin import *

class Plugin1(PluginInterface):
    @property
    def name(self):
        return "PluginName"

    @property
    def desc(self):
        return "PluginDesc"

    def handleEvent(self, eventName, *args, **kwargs):
        return super().handleEvent(eventName, *args, **kwargs)