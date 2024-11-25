
# Colors
PRIMARY_COLOR = "#007ACC"
PRIMARY_DARK = "#005F99"
SECONDARY_COLOR = "#5cb85c"
TERTIARY_COLOR = "#d9534f"
BACKGROUND_COLOR = "#f0f0f0"
TEXT_COLOR = "#333333"
ACCENT_COLOR = "#FF5722"

# Fonts
FONT_FAMILY = "Segoe UI"
FONT_SIZE_TITLE = "24px"
FONT_SIZE_SUBTITLE = "18px"
FONT_SIZE_NORMAL = "14px"

# Styles
WINDOW_STYLE = f"""
QMainWindow {{
    background-color: {BACKGROUND_COLOR};
}}
"""

BUTTON_STYLE = f"""
QPushButton {{
    background-color: {PRIMARY_COLOR};
    color: white;
    font-size: {FONT_SIZE_NORMAL};
    padding: 10px;
    border: none;
    border-radius: 5px;
}}
QPushButton:hover {{
    background-color: {PRIMARY_DARK};
}}
"""

SECONDARY_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {SECONDARY_COLOR};
    color: white;
    font-size: {FONT_SIZE_NORMAL};
    padding: 10px;
    border: none;
    border-radius: 5px;
}}
QPushButton:hover {{
    background-color: {PRIMARY_DARK};
}}
"""

TERTIARY_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {TERTIARY_COLOR};
    color: white;
    font-size: {FONT_SIZE_NORMAL};
    padding: 10px;
    border: none;
    border-radius: 5px;
}}
QPushButton:hover {{
    background-color: {PRIMARY_DARK};
}}
"""

LABEL_TITLE_STYLE = f"""
QLabel {{
    font-size: {FONT_SIZE_TITLE};
    font-weight: bold;
    color: {TEXT_COLOR};
}}
"""

LABEL_SUBTITLE_STYLE = f"""
QLabel {{
    font-size: {FONT_SIZE_SUBTITLE};
    color: {TEXT_COLOR};
}}
"""

LABEL_NORMAL_STYLE = f"""
QLabel {{
    font-size: {FONT_SIZE_NORMAL};
    color: {TEXT_COLOR};
}}
"""

INPUT_STYLE = f"""
QLineEdit {{
    padding: 10px;
    font-size: {FONT_SIZE_NORMAL};
    border: 1px solid #CCCCCC;
    border-radius: 5px;
}}
"""

COMBOBOX_STYLE = f"""
QComboBox {{
    padding: 10px;
    font-size: {FONT_SIZE_NORMAL};
    border: 1px solid #CCCCCC;
    border-radius: 5px;
}}
"""

SLIDER_STYLE = f"""
QSlider::groove:horizontal {{
    border: 1px solid #bbb;
    background: white;
    height: 10px;
    border-radius: 4px;
}}
QSlider::sub-page:horizontal {{
    background: {PRIMARY_COLOR};
    border: 1px solid #777;
    height: 10px;
    border-radius: 4px;
}}
QSlider::handle:horizontal {{
    background: {PRIMARY_COLOR};
    border: 1px solid {PRIMARY_DARK};
    width: 20px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 9px;
}}
QSlider::handle:horizontal:hover {{
    background: {PRIMARY_DARK};
    border: 1px solid {PRIMARY_DARK};
}}
"""

TABWIDGET_STYLE = f"""
QTabWidget::pane {{
    border: 1px solid #CCCCCC;
}}
QTabBar::tab {{
    background: {BACKGROUND_COLOR};
    padding: 10px;
    font-size: {FONT_SIZE_NORMAL};
}}
QTabBar::tab:selected {{
    background: white;
    border-bottom: 2px solid {PRIMARY_COLOR};
}}
"""

