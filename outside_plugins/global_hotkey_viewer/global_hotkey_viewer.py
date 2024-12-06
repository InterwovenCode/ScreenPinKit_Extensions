from plugin import *

class GlobalHotkeyViewerPlugin(PluginInterface):
    def __init__(self):
        super().__init__()
        self._runtimePath = os.path.dirname(os.path.abspath(__file__))
    
    @property
    def runtimePath(self):
        return self._runtimePath

    @property
    def name(self):
        return "GlobalHotkeyViewerPlugin"

    @property
    def displayName(self):
        return "全局快捷键查看器"

    @property
    def desc(self):
        return "打印快捷键信息"

    @property
    def author(self) -> str:
        return "yaoxuanzhi"

    @property
    def icon(self):
        return QIcon(self.runtimePath + "/icons/hotkey_viewer.svg")

    @property
    def version(self) -> str:
        return "v1.0.0"

    @property
    def url(self) -> str:
        return "https://github.com/InterwovenCode/ScreenPinKit_Extensions/blob/main/outside_plugins/global_hotkey_viewer.py"

    @property
    def tags(self) -> list:
        return ["热键", "日志"]

    def handleEvent(self, eventName: GlobalEventEnum, *args, **kwargs):
        if eventName == GlobalEventEnum.GlobalHotKeyRegisterEnd:
            keyboard:KeyboardEx = kwargs["keyboard"]
            self.log(f"已注册快捷键：{keyboard.hotkeyBinds.keys()}")
        pass