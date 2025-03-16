import sys
import os
import pexpect
import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTabWidget, QToolBar, QTextEdit
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtGui import QFont, QIcon
import platform
import distro
import shutil  

# Developed By MSCHelp

# Defini um cache temporário para aumentar a velocidade, mas ele é apagado ao fechar a janela do navegador.
# Assim garantindo a segurança dos dados do usuário
cache_dir = os.path.expanduser('~/.cache/navegador_matrix')
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = f"--disk-cache-dir={cache_dir} --enable-webgl --disable-gpu"

# Se ficar muito lento, substituir a linha de os.environ pela abaixo.
# os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer --disable-gpu-compositing --disable-accelerated-video-decode --enable-fast-unload --disable-http2"



# Estilo CSS Matrix
ESTILO_MATRIX = """
    QMainWindow { background-color: #000000; }
    QToolBar { background-color: #111111; border: 1px solid #00ff00; padding: 2px; }
    QPushButton { background-color: #00ff00; color: #000000; border: 1px solid #00ff00; padding: 5px; font-family: "Courier New"; font-size: 20px; }  /* Aumente o font-size aqui */
    QPushButton:hover { background-color: #000000; color: #00ff00; }
    QLineEdit { background-color: #000000; color: #00ff00; border: 1px solid #00ff00; padding: 5px; font-family: "Courier New"; font-size: 14px; }
    QTabWidget::pane { border: 1px solid #00ff00; background-color: #000000; }
    QTabBar::tab { background-color: #111111; color: #00ff00; border: 1px solid #00ff00; padding: 5px; font-family: "Courier New"; font-size: 14px; }
    QTabBar::tab:selected { background-color: #00ff00; color: #000000; }
    QTextEdit { background-color: #000000; color: #00ff00; border: 1px solid #00ff00; font-family: "Courier New"; font-size: 14px; }
"""

def criar_navegador():
    navegador = QWebEngineView()
    navegador.setUrl(QUrl("https://www.google.com"))
    return navegador

def remover_escape_ansi(texto):
    ansi_escape = re.compile(r'(\x1B\[|\x9B)[0-?]*[ -/]*[@-~]|\x1B]0;.*?\x07')
    return ansi_escape.sub("", texto)

class TerminalTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setFont(QFont("Courier New", 12))  
        self.terminal_output.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)  
        self.layout.addWidget(self.terminal_output)

        self.terminal_input = QLineEdit()
        self.terminal_input.returnPressed.connect(self.enviar_comando)
        self.layout.addWidget(self.terminal_input)

        self.process = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.ler_saida)
        self.timer.start(100)  

    def iniciar_processo(self):
        self.process = pexpect.spawn("/bin/bash", encoding="utf-8")
        self.process.expect("\\$")
        sistema = platform.system()
        if sistema == "Linux":
            sistema = f"{distro.name()} {distro.version()}"
        self.terminal_output.append("Bem-vindo ao Terminal Integrado!")
        self.terminal_output.append(f"Sistema operacional: {sistema} {platform.release()}")
        self.terminal_output.append(f"Diretório atual: {os.getcwd()}")
        self.terminal_output.append("Digite 'help' para ver os comandos disponíveis.\n")
        self.terminal_output.append("🖥️nav@matrix:~$ ")

    def enviar_comando(self):
        comando = self.terminal_input.text().strip()
        
        if comando.lower() == "clear":
            self.terminal_output.clear()
        else:
            self.terminal_output.append(f"🖥️nav@matrix:~$ {comando}")
            self.process.sendline(comando)
        
        self.terminal_input.clear()

    def ler_saida(self):
        if self.process and self.process.isalive():
            try:
                saida = self.process.read_nonblocking(size=1000, timeout=0)
                saida_limpa = remover_escape_ansi(saida).strip()
                self.terminal_output.append(saida_limpa)

            except pexpect.exceptions.TIMEOUT:
                pass
            except pexpect.exceptions.EOF:
                self.terminal_output.append("Processo finalizado.")
                self.timer.stop()

class Navegador(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navegador - Matrix")
        self.setGeometry(100, 100, 1200, 700)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(BASE_DIR, "imagens", "icon.png")
        self.setWindowIcon(QIcon(icon_path))
        self.setStyleSheet(ESTILO_MATRIX)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.btn_voltar = QPushButton("◀️")
        self.btn_avancar = QPushButton("▶️")
        self.btn_atualizar = QPushButton("🔄")
        self.btn_inicio = QPushButton("🏠")
        self.url_bar = QLineEdit()
        self.btn_nova_aba = QPushButton("➕")
        self.btn_terminal = QPushButton("💻")

        for btn in [self.btn_voltar, self.btn_avancar, self.btn_atualizar, self.btn_inicio, self.url_bar, self.btn_nova_aba, self.btn_terminal]:
            self.toolbar.addWidget(btn)

        self.abas = QTabWidget()
        self.abas.setTabsClosable(True)
        self.abas.tabCloseRequested.connect(self.fechar_aba)
        self.setCentralWidget(self.abas)

        self.adicionar_nova_aba(QUrl("https://www.google.com"), "Início")

        self.btn_voltar.clicked.connect(lambda: self.abas.currentWidget().back())
        self.btn_avancar.clicked.connect(lambda: self.abas.currentWidget().forward())
        self.btn_atualizar.clicked.connect(lambda: self.abas.currentWidget().reload())
        self.btn_inicio.clicked.connect(lambda: self.abas.currentWidget().setUrl(QUrl("https://www.google.com")))
        self.btn_nova_aba.clicked.connect(lambda: self.adicionar_nova_aba(QUrl("about:blank"), "Nova Aba"))
        self.btn_terminal.clicked.connect(self.mostrar_terminal)
        self.url_bar.returnPressed.connect(self.navegar_url)

    def adicionar_nova_aba(self, url, titulo):
        navegador = QWebEngineView()  
        navegador.setUrl(url)
        indice = self.abas.addTab(navegador, titulo)
        self.abas.setCurrentIndex(indice)

        navegador.urlChanged.connect(lambda u: self.atualizar_titulo_aba(indice, u))

    def atualizar_titulo_aba(self, indice, url):
     
        navegador = self.abas.widget(indice)
        if isinstance(navegador, QWebEngineView):
            navegador.page().titleChanged.connect(lambda title: self.abas.setTabText(indice, title))

    def fechar_aba(self, indice):
        widget = self.abas.widget(indice)
        self.abas.removeTab(indice)

    def navegar_url(self):
        url_texto = self.url_bar.text()
        if not url_texto.startswith("http"):
            url_texto = "http://" + url_texto

        if self.abas.count() == 0:
            self.adicionar_nova_aba(QUrl(url_texto), "Nova Aba")
        else:
            self.abas.currentWidget().setUrl(QUrl(url_texto))

    def mostrar_terminal(self):
        terminal_tab = TerminalTab()
        indice = self.abas.addTab(terminal_tab, "Terminal")
        self.abas.setCurrentIndex(indice)
        terminal_tab.iniciar_processo()

    def closeEvent(self, event):
   
        self.limpar_cache()
        event.accept()

    def limpar_cache(self):
   
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
    

if __name__ == "__main__":
    app_navegadormatrix = QApplication(sys.argv)
    janela = Navegador()
    janela.show()
    sys.exit(app_navegadormatrix.exec())
