"""
Main Window for PyComix Application

This module contains the main window class that serves as the primary UI container
for the PyComix comic reader application.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMenuBar,
    QToolBar,
    QStatusBar,
    QLabel,
    QFileDialog,
    QMessageBox,
    QSplitter,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPixmap


class MainWindow(QMainWindow):
    """
    Main window class for PyComix application.

    Provides the primary user interface with menu bar, toolbar, status bar,
    and central widget area for comic viewing.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyComix - Comic Reader")
        self.setMinimumSize(QSize(800, 600))
        self.resize(1200, 800)

        # Initialize UI components
        self._setup_central_widget()
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_status_bar()

        # Show welcome message
        self.status_bar.showMessage("PyComix 시작됨 - 만화 파일을 열어보세요")

    def _setup_central_widget(self):
        """Set up the central widget area."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)

        # Create a splitter for future panels
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(self.splitter)

        # Main content area (where comic will be displayed)
        self.content_area = QLabel(
            "PyComix에 오신 것을 환영합니다!\n\n"
            + "만화를 읽으려면 파일 메뉴에서 '열기'를 선택하세요."
        )
        self.content_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_area.setStyleSheet(
            """
            QLabel {
                background-color: #f0f0f0;
                border: 2px dashed #ccc;
                border-radius: 10px;
                font-size: 16px;
                color: #666;
                padding: 20px;
            }
        """
        )

        self.splitter.addWidget(self.content_area)

        # Set splitter proportions (content area takes most space)
        self.splitter.setSizes([800])

    def _setup_menu_bar(self):
        """Set up the menu bar with all necessary menus."""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("파일(&F)")

        # Open action
        open_action = QAction("열기(&O)", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("만화 파일 열기")
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("종료(&X)", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip("애플리케이션 종료")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View Menu
        view_menu = menubar.addMenu("보기(&V)")

        # Fullscreen action
        fullscreen_action = QAction("전체화면(&F)", self)
        fullscreen_action.setShortcut(QKeySequence.StandardKey.FullScreen)
        fullscreen_action.setStatusTip("전체화면 모드 토글")
        fullscreen_action.triggered.connect(self._toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        # Help Menu
        help_menu = menubar.addMenu("도움말(&H)")

        # About action
        about_action = QAction("정보(&A)", self)
        about_action.setStatusTip("PyComix 정보")
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_toolbar(self):
        """Set up the toolbar with common actions."""
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # Open file action (reuse from menu)
        open_action = QAction("열기", self)
        open_action.setStatusTip("만화 파일 열기")
        open_action.triggered.connect(self._open_file)
        self.toolbar.addAction(open_action)

        self.toolbar.addSeparator()

        # Navigation actions (placeholder for future implementation)
        prev_action = QAction("이전", self)
        prev_action.setStatusTip("이전 페이지")
        prev_action.setEnabled(False)  # Disabled for now
        self.toolbar.addAction(prev_action)

        next_action = QAction("다음", self)
        next_action.setStatusTip("다음 페이지")
        next_action.setEnabled(False)  # Disabled for now
        self.toolbar.addAction(next_action)

    def _setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Add permanent widgets to status bar
        self.page_label = QLabel("페이지: 0/0")
        self.status_bar.addPermanentWidget(self.page_label)

        self.zoom_label = QLabel("확대: 100%")
        self.status_bar.addPermanentWidget(self.zoom_label)

    def _open_file(self):
        """Handle file opening."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "만화 파일 열기",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.tiff);;All Files (*)",
        )

        if file_path:
            self.status_bar.showMessage(f"파일 로딩 중: {file_path}")
            self._load_image(file_path)

    def _load_image(self, file_path):
        """Load and display an image file."""
        try:
            # QPixmap으로 이미지 로드
            pixmap = QPixmap(file_path)

            if pixmap.isNull():
                self.status_bar.showMessage("이미지를 로드할 수 없습니다.")
                self.content_area.setText("이미지를 로드할 수 없습니다.")
                return

            # QLabel 크기에 맞게 이미지 크기 조정 (비율 유지하면서)
            label_size = self.content_area.size()
            scaled_pixmap = pixmap.scaled(
                label_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # QLabel에 이미지 설정
            self.content_area.setPixmap(scaled_pixmap)
            self.content_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # 상태바 업데이트
            self.status_bar.showMessage(f"이미지 로드 완료: {file_path}")

        except Exception as e:
            self.status_bar.showMessage(f"이미지 로드 실패: {str(e)}")
            self.content_area.setText(f"이미지 로드 실패:\n{str(e)}")

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
            self.status_bar.showMessage("일반 화면 모드")
        else:
            self.showFullScreen()
            self.status_bar.showMessage("전체화면 모드")

    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "PyComix 정보",
            """<h2>PyComix</h2>
            <p>버전: 0.1.0</p>
            <p>PyQt6로 만든 현대적인 만화 리더 애플리케이션</p>
            <p>개발자: PyComix Team</p>
            """,
        )

    def closeEvent(self, event):
        """Handle window close event."""
        self.status_bar.showMessage("PyComix 종료 중...")
        event.accept()
