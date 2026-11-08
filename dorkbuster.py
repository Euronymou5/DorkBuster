"""
DorkBuster
By: Euronymou5
VERSION v2
License: MPL-2.0
"""

import requests
import re
import sys
import threading
import time
import webbrowser
from typing import Dict, List, Optional, Set

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from modulos import config_manager
from modulos.engines import (
    AVAILABLE_ENGINES,
    DEFAULT_DORK_TEMPLATES, # Removido
    deduplicate_results,
    get_default_dorks,
    normalize_url,
)
from modulos.llm import SUPPORTED_MODELS, generate_dorks_with_llm

MODERN_STYLE = """
QMainWindow {
    background-color: #121212;
}

QWidget {
    color: #f0f0f0;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}

QGroupBox {
    border: 1px solid #333333;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 14px;
    font-weight: bold;
    color: #ffffff;
    background-color: #181818;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    left: 12px;
    color: #ffffff;
}

QLineEdit, QSpinBox, QDoubleSpinBox {
    background-color: #222222;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    padding: 6px 10px;
    color: #ffffff;
    selection-background-color: #555555;
    selection-color: #ffffff;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #888888;
    background-color: #282828;
}

QLineEdit:disabled {
    background-color: #1a1a1a;
    color: #666666;
    border: 1px solid #2c2c2c;
}

QPushButton {
    background-color: #242424;
    color: #f0f0f0;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    padding: 7px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #333333;
    border-color: #666666;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #444444;
}

QPushButton#btn_search {
    background-color: #ffffff;
    color: #121212;
    border: 1px solid #ffffff;
    font-size: 14px;
    font-weight: bold;
    padding: 8px 18px;
}

QPushButton#btn_search:hover {
    background-color: #e0e0e0;
    border-color: #e0e0e0;
}

QPushButton#btn_stop {
    background-color: #242424;
    color: #ff6b6b;
    border: 1px solid #4a3030;
    font-size: 14px;
    font-weight: bold;
    padding: 8px 18px;
}

QPushButton#btn_stop:hover {
    background-color: #382424;
    border-color: #ff6b6b;
}

QPushButton#btn_stop:disabled, QPushButton#btn_search:disabled {
    background-color: #1a1a1a;
    color: #555555;
    border-color: #2a2a2a;
}

QCheckBox {
    spacing: 8px;
    color: #d0d0d0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #444444;
    background: #222222;
}

QCheckBox::indicator:checked {
    background: #ffffff;
    border: 1px solid #ffffff;
    image: none;
}

QTableWidget {
    background-color: #161616;
    border: 1px solid #2d2d2d;
    border-radius: 6px;
    gridline-color: #262626;
    color: #f0f0f0;
    selection-background-color: #333333;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #202020;
    color: #ffffff;
    font-weight: bold;
    padding: 6px;
    border: 1px solid #2d2d2d;
}

QProgressBar {
    border: 1px solid #333333;
    border-radius: 4px;
    text-align: center;
    background-color: #1c1c1c;
    color: #ffffff;
    height: 18px;
}

QProgressBar::chunk {
    background-color: #ffffff;
    border-radius: 3px;
}

QStatusBar {
    background-color: #0e0e0e;
    color: #cccccc;
    font-weight: 500;
}

QDialog, QMessageBox {
    background-color: #181818;
    color: #ffffff;
}

QMessageBox QLabel {
    color: #f0f0f0;
    background-color: transparent;
    font-size: 13px;
}

QMessageBox QPushButton {
    background-color: #242424;
    color: #ffffff;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 6px 16px;
    min-width: 75px;
}

QMessageBox QPushButton:hover {
    background-color: #383838;
    border-color: #666666;
}

QMenu {
    background-color: #1c1c1c;
    color: #ffffff;
    border: 1px solid #383838;
    border-radius: 4px;
    padding: 4px;
}

QMenu::item {
    background-color: transparent;
    padding: 6px 24px 6px 18px;
    color: #f0f0f0;
    border-radius: 3px;
}

QMenu::item:selected {
    background-color: #333333;
    color: #ffffff;
}

QMenu::separator {
    height: 1px;
    background-color: #2e2e2e;
    margin: 4px 8px;
}

QScrollBar:vertical {
    background: #161616;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #333333;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #555555;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: #161616;
    height: 12px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: #333333;
    min-width: 20px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background: #555555;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""

class SearchWorker(QThread):
    sig_status = pyqtSignal(str)
    sig_progress = pyqtSignal(int, int)
    sig_result_found = pyqtSignal(dict)
    sig_duplicate_dropped = pyqtSignal(int)
    sig_finished = pyqtSignal(int, int)
    sig_error = pyqtSignal(str)
    sig_llm_failed = pyqtSignal(str)

    def __init__(
        self,
        query: str,
        use_llm: bool,
        api_key: str,
        model: str,
        selected_engines: List[str],
        max_results: int,
        cooldown: float,
        use_proxy: bool = False,
        proxy: str = "",
        parent=None,
    ):
        super().__init__(parent)
        self.query = query.strip()
        self.use_llm = use_llm
        self.api_key = api_key.strip()
        self.model = model
        self.selected_engines = selected_engines
        self.max_results = max_results
        self.cooldown = cooldown
        self.use_proxy = use_proxy
        self.proxy = proxy.strip() if use_proxy else ""
        self.stop_event = threading.Event()

    def run(self):
        dorks_to_run: List[str] = []

        if self.use_llm:
            self.sig_status.emit(f"DorkGPT interpretando instrucción: '{self.query}'...")
            try:
                dorks_to_run = generate_dorks_with_llm(
                    target_or_prompt=self.query,
                    api_key=self.api_key,
                    model=self.model,
                )
                self.sig_status.emit(f"DorkGPT generó {len(dorks_to_run)} dorks exitosamente. Iniciando búsquedas...")
            except Exception as e:
                err_msg = str(e)
                self.sig_llm_failed.emit(err_msg)
                dorks_to_run = [self.query] if self.query else get_default_dorks(count=5)
        else:
            if self.query:
                dorks_to_run = [self.query]
            else:
                dorks_to_run = get_default_dorks(count=5)

        if not dorks_to_run:
            self.sig_status.emit("No hay dorks para ejecutar.")
            self.sig_finished.emit(0, 0)
            return

        if not self.selected_engines:
            self.sig_error.emit("No se ha seleccionado ningún motor de búsqueda.")
            self.sig_finished.emit(0, 0)
            return

        total_steps = len(dorks_to_run) * len(self.selected_engines)
        current_step = 0
        seen_normalized: Set[str] = set()
        unique_count = 0
        duplicate_count = 0

        for dork in dorks_to_run:
            if self.stop_event.is_set():
                break

            for engine_name in self.selected_engines:
                if self.stop_event.is_set():
                    break

                current_step += 1
                self.sig_progress.emit(current_step, total_steps)
                self.sig_status.emit(f"Buscando en {engine_name}: '{dork}'...")

                engine = AVAILABLE_ENGINES.get(engine_name)
                if not engine:
                    continue

                try:
                    urls = engine.search(
                        query=dork,
                        max_results=self.max_results,
                        pause=self.cooldown,
                        stop_check=self.stop_event.is_set,
                        proxy=self.proxy,
                    )
                except Exception as e:
                    urls = []

                if urls:
                    self.sig_status.emit(f"[{engine_name}] {len(urls)} resultados encontrados para '{dork}'.")
                elif getattr(engine, "last_error", None):
                    self.sig_status.emit(f"[{engine_name}] {engine.last_error}")

                for url in urls:
                    if self.stop_event.is_set():
                        break
                    if not url or not isinstance(url, str):
                        continue

                    norm = normalize_url(url)
                    if norm in seen_normalized:
                        duplicate_count += 1
                        self.sig_duplicate_dropped.emit(duplicate_count)
                        continue

                    seen_normalized.add(norm)
                    unique_count += 1
                    self.sig_result_found.emit({
                        "index": unique_count,
                        "engine": engine_name,
                        "query": dork,
                        "url": url,
                    })

                if self.cooldown > 0 and not self.stop_event.is_set():
                    sleep_slices = int(self.cooldown * 10)
                    for _ in range(sleep_slices):
                        if self.stop_event.is_set():
                            break
                        time.sleep(0.1)

        if self.stop_event.is_set():
            self.sig_status.emit("Búsqueda detenida por el usuario.")
        else:
            if unique_count > 0:
                self.sig_status.emit(
                    f"Búsqueda finalizada. Se han encontrado {unique_count} resultados únicos "
                    f"({duplicate_count} duplicados omitidos)."
                )
            else:
                self.sig_status.emit("No se han encontrado resultados. (Revisa si el motor activó bloqueo o prueba seleccionando Bing o Yahoo).")

        self.sig_finished.emit(unique_count, duplicate_count)

class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de DorkBuster")
        self.setFixedSize(540, 390)
        self.setStyleSheet("""
            QDialog {
                background-color: #141414;
                color: #ffffff;
                border: 1px solid #383838;
                border-radius: 8px;
            }
            QLabel {
                color: #e0e0e0;
                background-color: transparent;
            }
            QPushButton {
                background-color: #ffffff;
                color: #121212;
                font-weight: bold;
                border: 1px solid #ffffff;
                border-radius: 6px;
                padding: 7px 22px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 24, 26, 22)
        layout.setSpacing(14)

        title = QLabel("<h2 style='margin:0; color:#ffffff;'>DorkBuster <span style='color:#aaaaaa;'>V2.0</span></h2>")
        layout.addWidget(title)

        subtitle = QLabel("<span style='color:#999999; font-size:12px;'>OSINT Reconnaissance & DorkGPT Engine</span>")
        layout.addWidget(subtitle)

        desc = QLabel(
            "<p style='color:#cccccc; line-height: 140%;'>Herramienta avanzada de reconocimiento OSINT con interfaz gráfica moderna y generación de dorks asistida por IA.</p>"
            "<p><b style='color:#ffffff;'>Nuevas capacidades en V2:</b></p>"
            "<ul style='color:#dddddd; line-height: 150%;'>"
            "<li><b>Modo DorkGPT:</b> Escribe libremente instrucciones en lenguaje natural (ej. <i>'Exposed .env files'</i> o <i>'Crea dorks para logins en .gob'</i>) y la IA generará los dorks.</li>"
            "<li><b>Busqueda Concurrente:</b> Soporta Google-Python, Google-Requests, Yahoo, Bing y DuckDuckGo de manera simultánea.</li>"
            "<li><b>Deduplicación Cross-Engine:</b> Las URLs repetidas entre motores se descartan en tiempo real.</li>"
            "<li><b>Persistencia:</b> Clave de API y modelo guardados de forma segura en <code>config.json</code>.</li>"
            "</ul>"
            "<p style='color:#777777; font-size: 11px;'>Licencia: MPL-2.0 | Autor: Euronymou5</p>"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_close = QPushButton("Cerrar")
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)

class DorkBusterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DorkBuster")
        self.resize(980, 720)
        self.setMinimumSize(850, 600)
        self.setStyleSheet(MODERN_STYLE)

        self.config = config_manager.load_config()
        self.actual_api_key = self.config.get("api_key", "")
        self.worker: Optional[SearchWorker] = None
        self.found_results: List[Dict[str, str]] = []

        self.init_ui()
        self.load_settings_to_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(12)

        header_layout = QHBoxLayout()
        title_label = QLabel("DorkBuster")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        btn_about = QPushButton("Acerca de")
        btn_about.clicked.connect(self.show_about)
        header_layout.addWidget(btn_about)
        main_layout.addLayout(header_layout)

        self.target_group = QGroupBox("Modo Clásico (Búsqueda por Dork Directo)")
        target_layout = QVBoxLayout(self.target_group)
        target_layout.setSpacing(10)

        row_dork = QHBoxLayout()
        self.lbl_dork = QLabel("Dork de Búsqueda:")
        self.lbl_dork.setFixedWidth(210)
        self.entry_dork = QLineEdit()
        self.entry_dork.setPlaceholderText('Ej: intitle:"index of", inurl:admin.php, intext:password, filetype:sql...')
        row_dork.addWidget(self.lbl_dork)
        row_dork.addWidget(self.entry_dork)
        target_layout.addLayout(row_dork)

        self.chk_use_llm = QCheckBox("Modo IA / DorkGPT (Interpreta lenguaje natural libremente y genera dorks)")
        self.chk_use_llm.stateChanged.connect(self.toggle_llm_mode)
        target_layout.addWidget(self.chk_use_llm)

        self.llm_container = QWidget()
        llm_layout = QVBoxLayout(self.llm_container)
        llm_layout.setContentsMargins(0, 4, 0, 4)
        llm_layout.setSpacing(8)

        row_key = QHBoxLayout()
        lbl_key = QLabel("API Key OpenRouter:")
        lbl_key.setFixedWidth(160)
        self.entry_api_key = QLineEdit()
        self.entry_api_key.setEchoMode(QLineEdit.Password)
        self.entry_api_key.setPlaceholderText("sk-or-v1-...")

        self.btn_edit_key = QPushButton("Editar / Cambiar")
        self.btn_edit_key.setFixedWidth(130)
        self.btn_edit_key.clicked.connect(self.unlock_api_key_entry)

        row_key.addWidget(lbl_key)
        row_key.addWidget(self.entry_api_key)
        row_key.addWidget(self.btn_edit_key)
        llm_layout.addLayout(row_key)

        row_model = QHBoxLayout()
        lbl_model = QLabel("Modelo OpenRouter:")
        lbl_model.setFixedWidth(160)
        self.entry_model = QLineEdit()
        self.entry_model.setPlaceholderText("Ej: deepseek/deepseek-v4-flash-0731 o openai/gpt-4o-mini")
        row_model.addWidget(lbl_model)
        row_model.addWidget(self.entry_model)
        llm_layout.addLayout(row_model)

        target_layout.addWidget(self.llm_container)

        main_layout.addWidget(self.target_group)

        config_group = QGroupBox("Motores de Búsqueda y Ajustes de Red")
        config_layout = QVBoxLayout(config_group)

        row_engines = QHBoxLayout()
        lbl_engines = QLabel("Motores activos:")
        lbl_engines.setFixedWidth(120)
        row_engines.addWidget(lbl_engines)

        self.chk_engines: Dict[str, QCheckBox] = {}
        for eng_name in AVAILABLE_ENGINES.keys():
            chk = QCheckBox(eng_name)
            self.chk_engines[eng_name] = chk
            row_engines.addWidget(chk)
        row_engines.addStretch()
        config_layout.addLayout(row_engines)

        row_proxy = QHBoxLayout()
        self.chk_use_proxy = QCheckBox("Usar Proxy:")
        self.chk_use_proxy.setFixedWidth(120)
        self.chk_use_proxy.stateChanged.connect(self.toggle_proxy_input)
        row_proxy.addWidget(self.chk_use_proxy)

        self.entry_proxy = QLineEdit()
        self.entry_proxy.setPlaceholderText("Ej: http://127.0.0.1:8080 o socks5://127.0.0.1:9050 o http://usuario:pass@host:puerto")
        self.entry_proxy.setEnabled(False)
        row_proxy.addWidget(self.entry_proxy, 1)

        self.btn_test_proxy = QPushButton("Probar Conexión")
        self.btn_test_proxy.setFixedWidth(140)
        self.btn_test_proxy.setEnabled(False)
        self.btn_test_proxy.clicked.connect(self.test_proxy_connection)
        row_proxy.addWidget(self.btn_test_proxy)
        config_layout.addLayout(row_proxy)

        row_settings = QHBoxLayout()
        row_settings.setSpacing(14)

        lbl_max = QLabel("Máx. Resultados/Motor:")
        self.spin_max_results = QSpinBox()
        self.spin_max_results.setRange(1, 100)
        self.spin_max_results.setValue(10)
        row_settings.addWidget(lbl_max)
        row_settings.addWidget(self.spin_max_results)

        lbl_cool = QLabel("Cooldown (s):")
        self.spin_cooldown = QDoubleSpinBox()
        self.spin_cooldown.setRange(0.0, 30.0)
        self.spin_cooldown.setSingleStep(0.5)
        self.spin_cooldown.setValue(1.0)
        row_settings.addWidget(lbl_cool)
        row_settings.addWidget(self.spin_cooldown)

        self.chk_autosave = QCheckBox("Guardar automáticamente en .txt")
        self.chk_autosave.setChecked(True)
        row_settings.addWidget(self.chk_autosave)

        row_settings.addStretch()
        config_layout.addLayout(row_settings)
        main_layout.addWidget(config_group)

        action_layout = QHBoxLayout()
        self.btn_search = QPushButton("Buscar")
        self.btn_search.setObjectName("btn_search")
        self.btn_search.setMinimumHeight(38)
        self.btn_search.clicked.connect(self.start_search)

        self.btn_stop = QPushButton("Detener")
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setMinimumHeight(38)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_search)

        action_layout.addWidget(self.btn_search, 3)
        action_layout.addWidget(self.btn_stop, 1)
        main_layout.addLayout(action_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        main_layout.addWidget(self.progress_bar)

        results_header = QHBoxLayout()
        lbl_results = QLabel("Resultados Encontrados (Deduplicación activa):")
        lbl_results.setFont(QFont("Arial", 11, QFont.Bold))
        results_header.addWidget(lbl_results)

        self.lbl_stats = QLabel("Resultados: 0 | Duplicados descartados: 0")
        self.lbl_stats.setStyleSheet("color: #ffffff; font-weight: bold;")
        results_header.addWidget(self.lbl_stats)

        results_header.addStretch()

        btn_copy = QPushButton("Copiar URL")
        btn_copy.clicked.connect(self.copy_selected_url)
        results_header.addWidget(btn_copy)

        btn_export = QPushButton("Exportar TXT")
        btn_export.clicked.connect(self.export_results_to_txt)
        results_header.addWidget(btn_export)

        btn_clear = QPushButton("Limpiar")
        btn_clear.clicked.connect(self.clear_results)
        results_header.addWidget(btn_clear)

        main_layout.addLayout(results_header)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["#", "Motor", "Dork / Consulta", "URL Encontrada"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.setColumnWidth(2, 280)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.doubleClicked.connect(self.open_selected_url)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_table_context_menu)
        main_layout.addWidget(self.table)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Listo para buscar.")

    def load_settings_to_ui(self):
        self.spin_max_results.setValue(int(self.config.get("max_results", 10)))
        self.spin_cooldown.setValue(float(self.config.get("cooldown", 1.0)))
        self.chk_autosave.setChecked(bool(self.config.get("auto_save_txt", True)))

        saved_engines = self.config.get(
            "selected_engines", ["Bing", "Yahoo", "Google-Python-Requests", "DuckDuckGo"]
        )
        for name, chk in self.chk_engines.items():
            chk.setChecked(name in saved_engines)

        saved_model = self.config.get("model", "deepseek/deepseek-v4-flash-0731")
        self.entry_model.setText(saved_model)

        use_llm = bool(self.config.get("use_llm", False))
        self.chk_use_llm.setChecked(use_llm)

        if self.actual_api_key:
            self.entry_api_key.setText(config_manager.mask_api_key(self.actual_api_key))
            self.entry_api_key.setEnabled(False)
            self.btn_edit_key.setEnabled(True)
        else:
            self.entry_api_key.setEnabled(True)
            self.btn_edit_key.setEnabled(False)

        saved_dork = self.config.get("dork_query", "") or self.config.get("manual_dork", "")
        self.entry_dork.setText(saved_dork)

        use_proxy = bool(self.config.get("use_proxy", False))
        self.chk_use_proxy.setChecked(use_proxy)
        self.entry_proxy.setEnabled(use_proxy)
        self.btn_test_proxy.setEnabled(use_proxy)
        self.entry_proxy.setText(self.config.get("proxy_url", ""))

        self.toggle_llm_mode()

    def toggle_llm_mode(self):
        is_llm = self.chk_use_llm.isChecked()
        self.llm_container.setVisible(is_llm)

        if is_llm:
            self.target_group.setTitle("Modo DorkGPT (Inteligencia Artificial / Lenguaje Natural)")
            self.lbl_dork.setText("Instrucción o Escenario (Prompt):")
            self.entry_dork.setPlaceholderText(
                "Ej: 'Exposed .env files', 'Crea dorks para buscar logins en ciertos tld', 'Paneles de admin'..."
            )
        else:
            self.target_group.setTitle("Modo Clásico (Búsqueda por Dork Directo)")
            self.lbl_dork.setText("Dork de Búsqueda:")
            self.entry_dork.setPlaceholderText(
                'Ej: intitle:"index of", inurl:admin.php, intext:password, filetype:sql...'
            )

    def toggle_proxy_input(self):
        enabled = self.chk_use_proxy.isChecked()
        self.entry_proxy.setEnabled(enabled)
        self.btn_test_proxy.setEnabled(enabled)

    def test_proxy_connection(self):
        proxy_url = self.entry_proxy.text().strip()
        if not proxy_url:
            QMessageBox.warning(
                self,
                "Proxy No Especificado",
                "Por favor introduce la dirección del proxy antes de probar la conexión (ej. http://127.0.0.1:8080).",
            )
            return

        self.status_bar.showMessage("Probando conexión a través del proxy...")
        self.btn_test_proxy.setEnabled(False)
        QtWidgets.QApplication.processEvents()

        try:
            proxies = {"http": proxy_url, "https": proxy_url}
            resp = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=6)
            if resp.status_code == 200:
                ip_info = resp.json().get("ip", "Desconocida")
                QMessageBox.information(
                    self,
                    "Proxy Conectado Exitosamente",
                    f"¡Conexion establecida con exito a través del proxy!\n\nDireccion IP:\n{ip_info}",
                )
                self.status_bar.showMessage(f"Proxy operativo (IP de salida: {ip_info})", 5000)
            else:
                QMessageBox.warning(
                    self,
                    "Respuesta Inesperada",
                    f"El proxy respondió con código de estado HTTP {resp.status_code}.",
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Fallo al Conectar Proxy",
                f"No se pudo establecer conexión a través del proxy:\n\n{str(e)}",
            )
            self.status_bar.showMessage("Error en la verificación del proxy.", 5000)
        finally:
            self.btn_test_proxy.setEnabled(True)

    def unlock_api_key_entry(self):
        self.entry_api_key.setEnabled(True)
        self.entry_api_key.clear()
        self.entry_api_key.setFocus()
        self.actual_api_key = ""

    def save_current_settings(self):
        selected_engines = [
            name for name, chk in self.chk_engines.items() if chk.isChecked()
        ]
        text_key = self.entry_api_key.text().strip()
        if text_key and not text_key.endswith("-xxxxxxxxxx"):
            self.actual_api_key = text_key

        self.config["api_key"] = self.actual_api_key
        self.config["model"] = self.entry_model.text().strip() or "deepseek/deepseek-v4-flash-0731"
        self.config["use_llm"] = self.chk_use_llm.isChecked()
        self.config["use_proxy"] = self.chk_use_proxy.isChecked()
        self.config["proxy_url"] = self.entry_proxy.text().strip()
        self.config["max_results"] = self.spin_max_results.value()
        self.config["cooldown"] = self.spin_cooldown.value()
        self.config["selected_engines"] = selected_engines
        self.config["auto_save_txt"] = self.chk_autosave.isChecked()
        self.config["dork_query"] = self.entry_dork.text().strip()

        config_manager.save_config(self.config)

    def start_search(self):
        use_llm = self.chk_use_llm.isChecked()
        dork_text = self.entry_dork.text().strip()
        use_proxy = self.chk_use_proxy.isChecked()
        proxy_url = self.entry_proxy.text().strip()

        if use_proxy and not proxy_url:
            QMessageBox.warning(
                self,
                "Proxy Vacío",
                "Has activado la opción 'Usar Proxy', pero no has ingresado la dirección del servidor proxy.",
            )
            return

        if not dork_text:
            if use_llm:
                QMessageBox.warning(
                    self,
                    "Instrucción Requerida",
                    "Por favor introduce una instrucción o prompt para DorkGPT (ej. 'Exposed .env files' o 'Crea dorks para logins en ciertos tld').",
                )
                return
            else:
                QMessageBox.warning(
                    self,
                    "Dork Requerido",
                    'Por favor introduce un dork de búsqueda manual (ej. intitle:"index of", inurl:admin.php, intext:password).',
                )
                return

        selected_engines = [
            name for name, chk in self.chk_engines.items() if chk.isChecked()
        ]
        if not selected_engines:
            QMessageBox.warning(
                self,
                "Sin Motores",
                "Debes seleccionar al menos un motor de búsqueda.",
            )
            return

        key_input = self.entry_api_key.text().strip()
        if use_llm:
            if key_input and not key_input.endswith("-xxxxxxxxxx"):
                self.actual_api_key = key_input
            if not self.actual_api_key:
                QMessageBox.warning(
                    self,
                    "Clave de API Faltante",
                    "Has seleccionado la opción de IA pero no has configurado una API Key de OpenRouter.",
                )
                return

        self.save_current_settings()

        if self.actual_api_key:
            self.entry_api_key.setText(config_manager.mask_api_key(self.actual_api_key))
            self.entry_api_key.setEnabled(False)
            self.btn_edit_key.setEnabled(True)

        self.clear_results()
        self.btn_search.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.progress_bar.setValue(0)

        model_name = self.entry_model.text().strip() or "deepseek/deepseek-v4-flash-0731"
        self.worker = SearchWorker(
            query=dork_text,
            use_llm=use_llm,
            api_key=self.actual_api_key,
            model=model_name,
            selected_engines=selected_engines,
            max_results=self.spin_max_results.value(),
            cooldown=self.spin_cooldown.value(),
            use_proxy=use_proxy,
            proxy=proxy_url,
            parent=self,
        )
        self.worker.sig_status.connect(self.update_status)
        self.worker.sig_progress.connect(self.update_progress)
        self.worker.sig_result_found.connect(self.add_result_row)
        self.worker.sig_duplicate_dropped.connect(self.update_duplicate_stat)
        self.worker.sig_finished.connect(self.on_search_finished)
        self.worker.sig_error.connect(self.on_worker_error)
        self.worker.sig_llm_failed.connect(self.on_llm_failed)
        self.worker.start()

    def stop_search(self):
        if self.worker and self.worker.isRunning():
            self.status_bar.showMessage("Deteniendo búsqueda en curso...")
            self.worker.stop_event.set()
            self.btn_stop.setEnabled(False)

    def update_status(self, message: str):
        self.status_bar.showMessage(message)

    def update_progress(self, current: int, total: int):
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)

    def update_duplicate_stat(self, count: int):
        current_unique = len(self.found_results)
        self.lbl_stats.setText(
            f"Resultados: {current_unique} | Duplicados descartados: {count}"
        )

    def add_result_row(self, item: dict):
        self.found_results.append(item)
        row = self.table.rowCount()
        self.table.insertRow(row)

        idx_item = QTableWidgetItem(str(item.get("index", row + 1)))
        idx_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 0, idx_item)

        engine_item = QTableWidgetItem(item.get("engine", ""))
        engine_item.setTextAlignment(Qt.AlignCenter)
        engine_item.setForeground(QtGui.QBrush(QColor("#bbbbbb")))
        self.table.setItem(row, 1, engine_item)

        query_item = QTableWidgetItem(item.get("query", ""))
        self.table.setItem(row, 2, query_item)

        url_item = QTableWidgetItem(item.get("url", ""))
        url_item.setForeground(QtGui.QBrush(QColor("#ffffff")))
        self.table.setItem(row, 3, url_item)

        self.table.scrollToBottom()
        self.lbl_stats.setText(
            f"Resultados: {len(self.found_results)} | Duplicados descartados: 0"
        )

    def on_llm_failed(self, error_message: str):
        QMessageBox.critical(
            self,
            "Error de IA (OpenRouter)",
            f"Ocurrió un error al contactar con OpenRouter:\n{error_message}\n\n"
            "Se procederá a utilizar los dorks por defecto/manuales.",
        )

    def on_worker_error(self, message: str):
        QMessageBox.critical(self, "Error de Búsqueda", message)

    def on_search_finished(self, total_unique: int, total_duplicates: int):
        self.btn_search.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress_bar.setValue(100)

        self.lbl_stats.setText(
            f"Resultados: {total_unique} | Duplicados descartados: {total_duplicates}"
        )

        if self.chk_autosave.isChecked() and self.found_results:
            dork_clean = re.sub(r"[^\w\-_\.]", "_", self.entry_dork.text().strip())[:35] or "dork"
            filename = f"busqueda_{dork_clean}.txt"
            self.save_results_to_file(filename)
            self.status_bar.showMessage(
                f"Búsqueda finalizada. {total_unique} resultados guardados en '{filename}'."
            )

    def copy_selected_url(self):
        row = self.table.currentRow()
        if row >= 0:
            url_item = self.table.item(row, 3)
            if url_item:
                clipboard = QApplication.clipboard()
                clipboard.setText(url_item.text())
                self.status_bar.showMessage(f"Enlace copiado al portapapeles: {url_item.text()}")

    def open_selected_url(self):
        row = self.table.currentRow()
        if row >= 0:
            url_item = self.table.item(row, 3)
            if url_item:
                webbrowser.open(url_item.text())

    def clear_results(self):
        self.found_results.clear()
        self.table.setRowCount(0)
        self.lbl_stats.setText("Resultados: 0 | Duplicados descartados: 0")
        self.progress_bar.setValue(0)

    def save_results_to_file(self, file_path: str):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# DorkBuster V2 - Resultados de búsqueda\n")
                f.write(f"# Dork / Consulta: {self.entry_dork.text().strip()}\n")
                f.write(f"# Total únicos: {len(self.found_results)}\n\n")
                for item in self.found_results:
                    f.write(f"{item.get('url', '')}\n")
        except Exception as e:
            QMessageBox.critical(self, "Error al Guardar", f"No se pudo guardar el archivo: {e}")

    def export_results_to_txt(self):
        if not self.found_results:
            QMessageBox.information(self, "Sin Resultados", "No hay resultados para exportar.")
            return

        dork_clean = re.sub(r"[^\w\-_\.]", "_", self.entry_dork.text().strip())[:35] or "resultados"
        default_name = f"busqueda_{dork_clean}.txt"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Resultados a TXT",
            default_name,
            "Archivos de Texto (*.txt);;Todos los archivos (*)",
        )
        if file_path:
            self.save_results_to_file(file_path)
            QMessageBox.information(
                self,
                "Exportación Exitosa",
                f"Se han guardado {len(self.found_results)} resultados en:\n{file_path}",
            )

    def show_about(self):
        dlg = AboutDialog(self)
        dlg.exec_()

    def show_table_context_menu(self, pos):
        item = self.table.itemAt(pos)
        menu = QtWidgets.QMenu(self)

        act_copy = menu.addAction("Copiar URL seleccionada")
        act_open = menu.addAction("Abrir URL en el Navegador")
        act_copy_dork = menu.addAction("Copiar Dork utilizado")
        menu.addSeparator()
        act_export = menu.addAction("Exportar resultados a TXT...")
        act_clear = menu.addAction("Limpiar lista de resultados")

        action = menu.exec_(self.table.viewport().mapToGlobal(pos))
        if action == act_copy:
            self.copy_selected_url()
        elif action == act_open:
            self.open_selected_url()
        elif action == act_copy_dork:
            row = self.table.currentRow()
            if row >= 0:
                q_item = self.table.item(row, 2)
                if q_item:
                    QApplication.clipboard().setText(q_item.text())
                    self.status_bar.showMessage(f"Dork copiado al portapapeles: {q_item.text()}")
        elif action == act_export:
            self.export_results_to_txt()
        elif action == act_clear:
            self.clear_results()

    def closeEvent(self, event):
        self.save_current_settings()
        if self.worker and self.worker.isRunning():
            self.worker.stop_event.set()
            self.worker.wait(1000)
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("DorkBuster")
    window = DorkBusterWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
