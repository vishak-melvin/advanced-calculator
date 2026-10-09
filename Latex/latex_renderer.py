from pathlib import Path
import json

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

class LatexRenderer(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        katexDir = Path(__file__).parent / "vendor" / "katex"
        htmlPath = Path(__file__).parent / "preview.html"
        self._ready = False
        self._pending_latex = ""

        html = htmlPath.read_text(encoding="utf-8")
        self.loadFinished.connect(self._on_load_finished)
        self.setHtml(html, QUrl.fromLocalFile(str(katexDir.resolve()) + "/"))

    def _on_load_finished(self,success):
        if not success:
            return

        self._ready = True
        self.set_latex(self._pending_latex)

    def set_latex(self, latex):
        self._pending_latex = latex

        if not self._ready:
            return

        encoded_latex = json.dumps(latex)
        script = f"window.renderMath({encoded_latex});"
        self.page().runJavaScript(script)

    def set_darkmode(self, enabled):
        if not self._ready:
            return

        self.page().runJavaScript(f"window.setDarkMode({str(enabled).lower()});")
