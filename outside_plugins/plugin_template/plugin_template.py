from plugin import *

class PluginTemplate(PluginInterface):
    def __init__(self):
        super().__init__()
        self._runtimePath = os.path.dirname(os.path.abspath(__file__))
    
    @property
    def runtimePath(self):
        return self._runtimePath

    @property
    def name(self):
        return "InternalPluginName"

    @property
    def displayName(self):
        return "插件模板"

    @property
    def desc(self):
        return "请修改为你自己的插件描述。"

    @property
    def author(self) -> str:
        return "yaoxuanzhi"

    @property
    def icon(self):
        return QIcon(self.runtimePath + "/icons/plugin_template_logo.svg")

    @property
    def version(self) -> str:
        return "v0.0.1"

    @property
    def url(self) -> str:
        return "http://interwovencode.xyz/"

    @property
    def tags(self) -> list:
        return ["参考", "模板", "辅助开发"]

    def onChangeEnabled(self):
        self.log(f"onChangeEnabled ===> {self.name} ===> {self.enable} ")

    def handleEvent(self, eventName, *args, **kwargs):
        self.log(f"handleEvent {eventName} ===> {args} ==> {kwargs}")
        return super().handleEvent(eventName, *args, **kwargs)