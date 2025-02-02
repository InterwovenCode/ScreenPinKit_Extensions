from plugin import *
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "site-packages"))
from qfluentwidgets import (InfoBar, InfoBarPosition)
import os, qrcode

class CombineWaterMarke(PluginInterface):
    def __init__(self):
        super().__init__()
        self._runtimePath = os.path.dirname(os.path.abspath(__file__))
    
    @property
    def runtimePath(self):
        return self._runtimePath

    @property
    def name(self):
        return "CombineWaterMarke"

    @property
    def displayName(self):
        return "嵌入水印"

    @property
    def desc(self):
        return "该插件会在复制&保存图片的时候嵌入一个二维码水印到图像内，可以借此防止被盗用。"

    @property
    def author(self) -> str:
        return "yaoxuanzhi"

    @property
    def icon(self):
        return QIcon(self.runtimePath + "/icons/water_marke.svg")

    @property
    def version(self) -> str:
        return "v1.0.0"

    @property
    def url(self) -> str:
        return "https://github.com/InterwovenCode/ScreenPinKit_Extensions"

    @property
    def tags(self) -> list:
        return ["水印"]

    def __embedLsbWatermark(self, sourceImage:Image, watermarkImage:Image, outputPath:str = None) -> QPixmap:
        if sourceImage.mode != "RGBA":
            sourceImage = sourceImage.convert("RGB")
        # 获取图像和水印的像素数据
        imagePixels = sourceImage.load()
        watermarkPixels = watermarkImage.load()

        # 确保水印图像的尺寸小于或等于原始图像的尺寸
        if watermarkImage.size[0] > sourceImage.size[0] or watermarkImage.size[1] > sourceImage.size[1]:
            raise ValueError("Watermark size must be smaller than or equal to image size")

        # 嵌入水印
        for i in range(watermarkImage.size[0]):
            for j in range(watermarkImage.size[1]):

                if sourceImage.mode == "RGBA":
                    r, g, b, a = imagePixels[i, j]
                    w = watermarkPixels[i, j]

                    # 将水印的最低有效位嵌入到图像的RGB通道中
                    r = (r & 0xFE) | ((w >> 7) & 0x01)
                    g = (g & 0xFE) | ((w >> 6) & 0x01)
                    b = (b & 0xFE) | ((w >> 5) & 0x01)
                    # a = (b & 0xFE) | ((w >> 4) & 0x01)

                    imagePixels[i, j] = (r, g, b, a)
                else:
                    r, g, b = imagePixels[i, j]
                    w = watermarkPixels[i, j]

                    # 将水印的最低有效位嵌入到图像的RGB通道中
                    r = (r & 0xFE) | ((w >> 7) & 0x01)
                    g = (g & 0xFE) | ((w >> 6) & 0x01)
                    b = (b & 0xFE) | ((w >> 5) & 0x01)

                    imagePixels[i, j] = (r, g, b)

        # 保存嵌入水印后的图像
        if outputPath != None:
            sourceImage.save(outputPath)

        width = sourceImage.size[0]
        height = sourceImage.size[1]

        if sourceImage.mode == "RGBA":
            return QPixmap.fromImage(QImage(sourceImage.tobytes(), width, height, 4*width, QImage.Format.Format_RGBA8888))
        else:
            return QPixmap.fromImage(QImage(sourceImage.tobytes(), width, height, 3*width, QImage.Format.Format_RGB888))


    def embedWatermarkImage(self, sourcePixmap:QPixmap, watermarkPath:str, outputPath:str = None) -> QPixmap:
        '''添加图片水印'''
        # 打开图像和水印
        image:Image = Image.fromqpixmap(sourcePixmap).convert("RGB")
        watermark = Image.open(watermarkPath).convert("L")
        return self.__embedLsbWatermark(image, watermark, outputPath)

    def embedWatermarkText(self, sourcePixmap:QPixmap, text:str, outputPath:str = None) -> QPixmap:
        '''添加文本水印，先转换为二维码再插入到图片中'''
        image:Image = Image.fromqpixmap(sourcePixmap)
        watermark = self.textToQrCode(text).convert("L")
        return self.__embedLsbWatermark(image, watermark, outputPath)

    def qpixmapToMatlike(self, qpixmap:QPixmap):
        qimage = qpixmap.toImage()
        image = Image.fromqimage(qimage)
        imageArray = np.array(image)
        return imageArray

    def textToQrCode(self, text:str) -> Image:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=3, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image()
        return img

    def handleEvent(self, eventName, *args, **kwargs):
        if eventName == GlobalEventEnum.ImageCopyingEvent or eventName == GlobalEventEnum.ImageSavingEvent:
            kv = kwargs["kv"]
            sourcePixmap = kv["pixmap"]
            parentWidget:QWidget = kwargs["parent"]
            try:
                finalPixmap =self.embedWatermarkText(sourcePixmap, f"https://github.com/YaoXuanZhi/ScreenPinKit")
                kv["pixmap"] = finalPixmap
            except Exception as e:
                errorMsg = "\n".join(e.args)
                InfoBar.error(
                    title='添加水印失败',
                    content=errorMsg,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=-1,    # won't disappear automatically
                    parent=parentWidget,
                )