from plugin import *
from qfluentwidgets import (RoundMenu, Action, StateToolTip)

# ```sh
# # Windows:

# # Linux:
# sudo apt install tesseract-ocr
# sudo apt install tesseract-ocr-chi-sim
# sudo apt install ocrmypdf
# ````

class SetPdfOcrEnv(PluginInterface):
    @property
    def name(self):
        return "SetPdfOcrEnv"

    @property
    def desc(self):
        return "设置PdfOcr环境"

    @property
    def displayName(self):
        return "设置pdf-ocr环境变量"

    @property
    def author(self) -> str:
        return "yaoxuanzhi"

    @property
    def version(self) -> str:
        return "v0.0.1"

    @property
    def url(self) -> str:
        return "http://interwovencode.xyz/"

    @property
    def tags(self) -> list:
        return ["环境变量"]

    def onChangeEnabled(self):
        if self.enable:
            os.environ["venv_path"] = "D:/ProgramData/Miniconda3/envs/ocrmypdf_env/"
            os.environ["tesseract_path"] = "D:/GreenSoftware/Tesseract-OCR"
            self.log("修改Pdf-Ocr环境变量成功")
        else:
            os.environ.pop("venv_path")
            os.environ.pop("tesseract_path")
            self.log("取消Pdf-Ocr环境变量设置")