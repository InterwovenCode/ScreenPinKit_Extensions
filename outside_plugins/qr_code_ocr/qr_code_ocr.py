from plugin import *
from qfluentwidgets import (InfoBar, InfoBarIcon, InfoBarPosition, Action, FluentIcon as FIF, TransparentToolButton)
from cv2.wechat_qrcode import WeChatQRCode
import os

class QrCodeOCR(PluginInterface):
    def __init__(self):
        super().__init__()
        self._runtimePath = os.path.dirname(os.path.abspath(__file__))
    
    @property
    def runtimePath(self):
        return self._runtimePath

    @property
    def name(self):
        return "QrCodeOCR"

    @property
    def displayName(self):
        return "二维码识别"

    @property
    def desc(self):
        return "右键菜单提供二维码识别菜单项，可以识别隐藏的二维码水印"

    @property
    def icon(self):
        return QIcon(self.runtimePath + "/icons/qr_code.svg")

    @property
    def version(self):
        return "1.0.0"

    @property
    def url(self) -> str:
        return "https://github.com/InterwovenCode/ScreenPinKit_Extensions/blob/main/outside_plugins/qr_code_ocr.py"

    @property
    def tags(self) -> list:
        return ["二维码", "ocr"]

    @property
    def author(self):
        return "yaoxuanzhi"

    def extractWatermarkText(self, sourcePixmap:QPixmap, outputPath:str = None) -> str:
        '''提取二维码上的文本'''
        image:Image = Image.fromqpixmap(sourcePixmap)
        if image.mode != "RGBA":
            image = image.convert("RGB")

        if not hasattr(self, "detector"):
            self.detector = WeChatQRCode(
                f"{self.runtimePath}/model/detect.prototxt", 
                f"{self.runtimePath}/model/detect.caffemodel",
                f"{self.runtimePath}/model/sr.prototxt",
                f"{self.runtimePath}/model/sr.caffemodel")

        res, _points = self.detector.detectAndDecode(np.array(image))
        if len(res) > 0:
            return "\n".join(res)

        width = image.size[0]
        height = image.size[1]
        watermarkSize = (width, height)
        watermark = Image.new("L", watermarkSize)

        imagePixels = image.load()
        watermarkPixels = watermark.load()

        for i in range(watermarkSize[0]):
            for j in range(watermarkSize[1]):
                if image.mode == "RGBA":
                    r, g, b, a = imagePixels[i, j]
                else:
                    r, g, b = imagePixels[i, j]

                # 从图像的RGB通道中提取水印的最低有效位
                w = ((r & 0x01) << 7) | ((g & 0x01) << 6) | ((b & 0x01) << 5)
                watermarkPixels[i, j] = w

        # 保存提取的水印
        if not outputPath == None:
            watermark.save(outputPath)

        res, _points = self.detector.detectAndDecode(np.array(watermark))
        return "\n".join(res)

    def handleEvent(self, eventName, *args, **kwargs):
        if eventName == GlobalEventEnum.RegisterContextMenuEvent:
        # if eventName == GlobalEventEnum.RegisterToolbarMenuEvent:
            actions:list = kwargs["actions"]
            pixmap:QPixmap = kwargs["pixmap"]
            parentWidget:QWidget = kwargs["parent"]
            actions.append(Action(self.icon, "二维码识别", triggered=lambda: self.tryQrCodeOcr(parentWidget, pixmap)))

    def tryQrCodeOcr(self, parentWidget:QWidget, pixmap:QPixmap):
        text = self.extractWatermarkText(pixmap)
        if len(text) == 0:
            InfoBar.info(
                title='没有检测到二维码',
                content="",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=2000,    # won't disappear automatically
                parent=parentWidget,
            )
        else:
            infoBar = InfoBar(
                icon=InfoBarIcon.SUCCESS,
                title='二维码识别成功',
                content=text,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,    # won't disappear automatically
                parent=parentWidget,
            )

            copyButton = TransparentToolButton(FIF.COPY, parentWidget)
            copyButton.setFixedSize(36, 36)
            copyButton.setIconSize(QSize(12, 12))
            copyButton.setCursor(Qt.PointingHandCursor)
            copyButton.setVisible(True)
            copyButton.clicked.connect(lambda: self.copyText(infoBar))
            infoBar.addWidget(copyButton)
            infoBar.show()

    def copyText(self, infoBar:InfoBar):
        text = infoBar.contentLabel.text()
        QApplication.clipboard().setText(text)