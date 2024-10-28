# ScreenPinKit 扩展
本仓库主要包含了一些[ScreenPinKit](https://github.com/YaoXuanZhi/ScreenPinKit)相关的外部OCR加载器的扩展，以及一些辅助工具和插件

## 目录结构
### outside_ocr_loaders
>外部OCR加载器目录
  - chineseocr_lite_loader_return_text.py
    >该文件实现了一个基于chineseocr_lite的OCR加载器，用于识别图像中的文本，并返回识别结果
  - deps
    >该目录包含了一些依赖库和工具，如chineseocr_lite，还提供了Tesseract-OCR、PaddleOCR等快捷集成脚本

  - outside_ocr_loader_as_html_return_filename.py
    >该文件实现了一个外部 OCR 加载器，用于将图像转换为带文本层的 HTML 文件，并返回文件名。
  - outside_ocr_loader_as_pdf_return_filename.py
    >该文件实现了一个外部 OCR 加载器，用于将图像转换为带文本层的 PDF 文件，并返回文件名。
  - outside_ocr_loader_return_json.py
    >该文件实现了一个外部 OCR 加载器，用于将图像转换为 JSON 格式的 OCR 结果，并返回结果。
  - outside_ocr_loader_return_text.py
    >该文件实现了一个外部 OCR 加载器，用于将图像转换为文本，并返回识别结果。

### outside_plugins
>外部插件目录
  - global_hotkey_viewer.py
    >该文件实现了一个全局热键查看器，可以查看当前系统中注册的全局热键。
  - plugin_template.py
    >该文件实现了一个插件示例，展示了如何开发和集成外部插件。
  - set_pdf_ocr_env.py
    >该文件用于设置ocrmypdf的环境变量，确保相关工具和依赖库能够正常工作。