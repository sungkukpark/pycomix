"""
Main Window for PyComix Application

This module contains the main window class that serves as the primary UI container
for the PyComix comic reader application.
"""

import os
from pathlib import Path

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
    QListWidget,
    QListWidgetItem,
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

        # Initialize data attributes
        self.current_folder = None
        self.image_files = []
        self.supported_formats = {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".bmp",
            ".tiff",
            ".webp",
        }

        # Initialize UI components
        self._setup_central_widget()
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_status_bar()

        # Show welcome message
        self.status_bar.showMessage("PyComix 시작됨 - 만화 폴더를 열어보세요")

    def _setup_central_widget(self):
        """Set up the central widget area."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)

        # Create a horizontal splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(self.splitter)

        # Left panel: File list
        self.file_list = QListWidget()
        self.file_list.setMaximumWidth(300)
        self.file_list.setMinimumWidth(200)
        self.file_list.itemClicked.connect(self._on_file_selected)
        self.file_list.setStyleSheet(
            """
            QListWidget {
                background-color: #fafafa;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #007acc;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #e6f3ff;
            }
        """
        )

        # Right panel: Image display area
        self.content_area = QLabel(
            "PyComix에 오신 것을 환영합니다!\n\n"
            + "만화를 읽으려면 파일 메뉴에서 '폴더 열기'를 선택하세요."
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

        # Add widgets to splitter
        self.splitter.addWidget(self.file_list)
        self.splitter.addWidget(self.content_area)

        # Set splitter proportions (file list: 300px, content area: rest)
        self.splitter.setSizes([300, 800])

    def _setup_menu_bar(self):
        """Set up the menu bar with all necessary menus."""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("파일(&F)")

        # Open folder action
        open_action = QAction("폴더 열기(&O)", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("만화 폴더 열기")
        open_action.triggered.connect(self._open_folder)
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

        # Open folder action (reuse from menu)
        open_action = QAction("폴더 열기", self)
        open_action.setStatusTip("만화 폴더 열기")
        open_action.triggered.connect(self._open_folder)
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

    def _open_folder(self):
        """Handle folder opening."""
        folder_path = QFileDialog.getExistingDirectory(
            self, "만화 폴더 선택", "", QFileDialog.Option.ShowDirsOnly
        )

        if folder_path:
            self.status_bar.showMessage(f"폴더 로딩 중: {folder_path}")
            self._load_folder(folder_path)

    def _load_folder(self, folder_path):
        """Load folder and populate file list with image files."""
        try:
            self.current_folder = Path(folder_path)
            self.image_files = []

            # Find all image files in the folder
            for file_path in self.current_folder.iterdir():
                if (
                    file_path.is_file()
                    and file_path.suffix.lower() in self.supported_formats
                ):
                    self.image_files.append(file_path)

            # Sort files by name (ascending)
            self.image_files.sort(key=lambda x: x.name.lower())

            if self.image_files:
                self._populate_file_list()
                # Load the first image automatically
                self._load_image_by_path(self.image_files[0])
                # Select the first item in the list
                self.file_list.setCurrentRow(0)
                self.status_bar.showMessage(
                    f"폴더 로드 완료: {len(self.image_files)}개 이미지 파일 발견"
                )
            else:
                self.file_list.clear()
                self.content_area.setText("선택한 폴더에 이미지 파일이 없습니다.")
                self.status_bar.showMessage("이미지 파일이 없습니다.")

        except Exception as e:
            self.status_bar.showMessage(f"폴더 로드 실패: {str(e)}")
            self.content_area.setText(f"폴더 로드 실패:\n{str(e)}")

    def _populate_file_list(self):
        """Populate the file list widget with image files."""
        self.file_list.clear()
        for file_path in self.image_files:
            item = QListWidgetItem(file_path.name)
            item.setData(Qt.ItemDataRole.UserRole, str(file_path))
            self.file_list.addItem(item)

    def _on_file_selected(self, item):
        """Handle file selection from the list."""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        if file_path:
            self._load_image_by_path(Path(file_path))

    def _load_image_by_path(self, file_path):
        """Load and display an image file by path."""
        try:
            # QPixmap으로 이미지 로드
            pixmap = QPixmap(str(file_path))

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
            current_index = (
                self.image_files.index(file_path) + 1
                if file_path in self.image_files
                else 0
            )
            total_files = len(self.image_files)
            self.page_label.setText(f"페이지: {current_index}/{total_files}")
            self.status_bar.showMessage(f"이미지 로드 완료: {file_path.name}")

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
