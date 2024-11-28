# Define themes as dictionaries
THEMES = {
    'light': {
        'PRIMARY_COLOR': "#1B065E",
        'PRIMARY_DARK': "#005F99",
        'SECONDARY_COLOR': "#5cb85c",
        'TERTIARY_COLOR': "#d9534f",
        'BACKGROUND_COLOR': "#cdcdff",
        'TEXT_COLOR': "#333333",
        'ACCENT_COLOR': "#FF5722",
        'TITLE_COLOR': "#005F99",
        'SUCCESS_COLOR': "#28A745",
        'ERROR_COLOR': "#DC3545",
    },
    'pink': {
        'PRIMARY_COLOR': "#D81B60",
        'PRIMARY_DARK': "#AD1457",
        'SECONDARY_COLOR': "#F06292",
        'TERTIARY_COLOR': "#880E4F",
        'BACKGROUND_COLOR': "#FFC1E3",
        'TEXT_COLOR': "#3E2723",
        'ACCENT_COLOR': "#FF4081",
        'TITLE_COLOR': "#AD1457",
        'SUCCESS_COLOR': "#388E3C",
        'ERROR_COLOR': "#B71C1C",
    },
        'teal': {
        'PRIMARY_COLOR': "#009688",
        'PRIMARY_DARK': "#00796B",
        'SECONDARY_COLOR': "#4DB6AC",
        'TERTIARY_COLOR': "#00796B",
        'BACKGROUND_COLOR': "#E0F2F1",
        'TEXT_COLOR': "#004D40",
        'ACCENT_COLOR': "#26A69A",
        'TITLE_COLOR': "#004D40",
        'SUCCESS_COLOR': "#2E7D32",
        'ERROR_COLOR': "#C62828",
    },
}

# Fonts
FONT_FAMILY = "Segoe UI"
FONT_SIZE_TITLE = "24px"
FONT_SIZE_SUBTITLE = "18px"
FONT_SIZE_NORMAL = "14px"

# Styles
class StyleManager:
    def __init__(self):
        self.themes = THEMES
        self.current_theme = 'light'
        self.update_styles()

    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.update_styles()

    def update_styles(self):
        theme = self.themes[self.current_theme]
        self.stylesheet = f"""
        * {{
            font-family: {FONT_FAMILY};
        }}
        QMainWindow {{
            background-color: {theme['BACKGROUND_COLOR']};
        }}
        QPushButton {{
            background-color: {theme['PRIMARY_COLOR']};
            color: white;
            font-size: {FONT_SIZE_NORMAL};
            padding: 10px;
            border: none;
            border-radius: 5px;
        }}
        QPushButton:hover {{
            background-color: {theme['PRIMARY_DARK']};
        }}
        QLabel {{
            font-size: {FONT_SIZE_NORMAL};
            color: {theme['TEXT_COLOR']};
        }}
        QLabel#title {{
            font-size: {FONT_SIZE_TITLE};
            font-weight: bold;
            color: {theme['TITLE_COLOR']};
        }}
        QLabel#subtitle {{
            font-size: {FONT_SIZE_SUBTITLE};
            font-weight: bold;
            color: {theme['TEXT_COLOR']};
        }}
        QLabel#success {{
            font-size: {FONT_SIZE_NORMAL};
            font-weight: bold;
            color: {theme['SUCCESS_COLOR']};
        }}
        QLabel#error {{
            font-size: {FONT_SIZE_NORMAL};
            font-weight: bold;
            color: {theme['ERROR_COLOR']};
        }}
        QLineEdit {{
            padding: 10px;
            font-size: {FONT_SIZE_NORMAL};
            border: 1px solid #CCCCCC;
            border-radius: 5px;
        }}
        QSlider::groove:horizontal {{
            border: 1px solid #bbb;
            background: white;
            height: 10px;
            border-radius: 4px;
        }}
        QSlider::sub-page:horizontal {{
            background: {theme['PRIMARY_COLOR']};
            border: 1px solid #777;
            height: 10px;
            border-radius: 4px;
        }}
        QSlider::handle:horizontal {{
            background: {theme['PRIMARY_COLOR']};
            border: 1px solid {theme['PRIMARY_DARK']};
            width: 20px;
            margin-top: -5px;
            margin-bottom: -5px;
            border-radius: 9px;
        }}
        QSlider::handle:horizontal:hover {{
            background: {theme['PRIMARY_DARK']};
            border: 1px solid {theme['PRIMARY_DARK']};
        }}
        QTabWidget::pane {{
            border: 1px solid #CCCCCC;
        }}
        QTabBar::tab {{
            background: {theme['BACKGROUND_COLOR']};
            padding: 10px;
            font-size: {FONT_SIZE_NORMAL};
        }}
        QTabBar::tab:selected {{
            background: white;
            border-bottom: 2px solid {theme['PRIMARY_COLOR']};
        }}
        QScrollBar:vertical {{
            background: {theme['BACKGROUND_COLOR']};
            width: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {theme['PRIMARY_COLOR']};
            min-height: 20px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {theme['PRIMARY_DARK']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            background: none;
            height: 0px;
        }}
        """
