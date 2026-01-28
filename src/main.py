import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

sys.path.insert(0, str(Path(__file__).parent))
from widgets.main_window import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()