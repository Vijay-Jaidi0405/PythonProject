"""main.py — SOFR Interest Calculator entry point."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QColor, QPainter, QFont

from core.database import init_db, get_conn
from ui.main_window import MainWindow


def make_splash() -> QSplashScreen:
    pix = QPixmap(480, 280)
    pix.fill(QColor("#1B3A6B"))
    painter = QPainter(pix)
    painter.setPen(QColor("#FFFFFF"))
    f = QFont("Segoe UI", 28, QFont.Bold)
    painter.setFont(f)
    painter.drawText(pix.rect(), Qt.AlignCenter | Qt.AlignTop,
                     "\n\n\nSOFR Interest Calculator")
    f2 = QFont("Segoe UI", 12)
    painter.setFont(f2)
    painter.setPen(QColor("#7aaddd"))
    painter.drawText(pix.rect(), Qt.AlignCenter,
                     "\n\n\n\n\nCompounded · Simple Average · SOFR Index")
    f3 = QFont("Segoe UI", 10)
    painter.setFont(f3)
    painter.setPen(QColor("#4a6fa5"))
    painter.drawText(pix.rect(), Qt.AlignBottom | Qt.AlignHCenter,
                     "Initialising database…  \n ")
    painter.end()
    return QSplashScreen(pix)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SOFR Interest Calculator")
    app.setOrganizationName("FinTech")

    splash = make_splash()
    splash.show()
    app.processEvents()

    # Initialise database and auto-mature past-maturity deals
    init_db()
    from core.database import auto_mature_deals
    with get_conn() as conn:
        n = auto_mature_deals(conn)
        if n:
            print(f"Auto-matured {n} deals past their maturity date.")

    window = MainWindow(get_conn)
    QTimer.singleShot(800, splash.close)
    QTimer.singleShot(850, window.show)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
