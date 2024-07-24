import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QStatusBar, QMenu, QStackedWidget, QMessageBox)
from PySide6.QtGui import QFont, QIcon, QFontDatabase, QMovie
from PySide6.QtCore import Qt, QSize
from weapon_library import WeaponLibrary
from character_builder import CharacterBuilder
from descendant_library import DescendantLibrary

# Update the base path for resources
RESOURCE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TFD Calculator")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e; 
                color: white;
            }
            QMenu {
                background-color: #2e2e2e;
                color: white;
                border: 1px solid white;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #3e3e3e;
            }
            QPushButton {
                background-color: #2e2e2e;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
            }
        """)
        self.setWindowIcon(QIcon(os.path.join(RESOURCE_PATH, "ui", "icon.png")))
        
        # Load custom font
        font_id = QFontDatabase.addApplicationFont(os.path.join(RESOURCE_PATH, "font", "Orbitron", "Orbitron-VariableFont_wght.ttf"))
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.custom_font = QFont(font_family)
        else:
            self.custom_font = QFont("Arial")  # Fallback font
        
        self.create_widgets()

    def create_widgets(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top bar
        top_bar = self.create_top_bar()
        main_layout.addLayout(top_bar)

        # Add trim below top bar
        trim = QWidget()
        trim.setFixedHeight(2)
        trim.setStyleSheet("background-color: white;")
        main_layout.addWidget(trim)

        # Stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Create and add screens
        self.menu_screen = self.create_menu_screen()
        self.stacked_widget.addWidget(self.menu_screen)

        print("Initializing WeaponLibrary...")
        try:
            self.weapon_library = WeaponLibrary()
            self.stacked_widget.addWidget(self.weapon_library)
        except Exception as e:
            print(f"Error initializing WeaponLibrary: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to initialize Weapon Library: {str(e)}")
            self.weapon_library = None

        print("Initializing CharacterBuilder...")
        try:
            self.character_builder = CharacterBuilder()
            self.stacked_widget.addWidget(self.character_builder)
        except Exception as e:
            print(f"Error initializing CharacterBuilder: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to initialize Character Builder: {str(e)}")
            self.character_builder = None

        print("Initializing DescendantLibrary...")
        try:
            self.descendant_library = DescendantLibrary()
            self.stacked_widget.addWidget(self.descendant_library)
        except Exception as e:
            print(f"Error initializing DescendantLibrary: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to initialize Descendant Library: {str(e)}")
            self.descendant_library = None

        # Set the initial screen to the menu
        self.stacked_widget.setCurrentWidget(self.menu_screen)

        self.setStatusBar(QStatusBar())

    def create_top_bar(self):
        top_bar = QHBoxLayout()
        
        # Menu button
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon(os.path.join(RESOURCE_PATH, "ui", "icon.png")))
        self.menu_button.setFixedSize(50, 50)
        self.menu_button.setIconSize(QSize(40, 40))
        self.menu_button.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid white;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.menu_button.clicked.connect(self.show_tools_menu)
        top_bar.addWidget(self.menu_button)
        
        top_bar.addStretch(1)  # Add stretch to push greeting to center
        
        # Left GIF
        self.left_gif = QLabel()
        self.setup_gif(self.left_gif, os.path.join(RESOURCE_PATH, "ui", "morning.gif"))
        top_bar.addWidget(self.left_gif)
        
        # Greeting
        self.greeting_label = QLabel("Welcome Descendant")
        self.greeting_label.setFont(self.custom_font)
        self.greeting_label.setStyleSheet("font-size: 24px;")
        top_bar.addWidget(self.greeting_label)
        
        # Right GIF
        self.right_gif = QLabel()
        self.setup_gif(self.right_gif, os.path.join(RESOURCE_PATH, "ui", "morning.gif"))
        top_bar.addWidget(self.right_gif)
        
        top_bar.addStretch(1)  # Add stretch to push settings button to right
        
        # Settings button
        settings_button = QPushButton("SETTINGS")
        settings_button.setFixedSize(100, 50)
        settings_button.setFont(self.custom_font)
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #2e2e2e;
                color: white;
                border: none;
                padding: 5px;
                font-size: 14px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
            }
        """)
        settings_button.clicked.connect(self.open_settings)
        top_bar.addWidget(settings_button)

        return top_bar

    def create_menu_screen(self):
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)
        
        calculators = [
            "Weapon Library",
            "Character Builder",
            "Descendant Library",
            "Skill Calculator",
            "Reactor Calculator",
            "External Components Calculator"
        ]
        
        for calculator in calculators:
            button = QPushButton(calculator)
            button.setFont(self.custom_font)
            button.clicked.connect(lambda checked, name=calculator: self.open_calculator(name))
            menu_layout.addWidget(button)
        
        return menu_widget

    def setup_gif(self, label, gif_path):
        movie = QMovie(gif_path)
        movie.setScaledSize(QSize(50, 50))
        label.setMovie(movie)
        movie.start()

    def open_settings(self):
        # Implement settings dialog here
        pass

    def show_tools_menu(self):
        menu = QMenu(self)
        calculators = [
            "Home",
            "Weapon Library",
            "Character Builder",
            "Descendant Library",
            "Skill Calculator",
            "Reactor Calculator",
            "External Components Calculator"
        ]
        for calculator in calculators:
            action = menu.addAction(calculator)
            action.triggered.connect(lambda checked, name=calculator: self.open_calculator(name))
        menu.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def open_calculator(self, name):
        if name == "Home":
            self.stacked_widget.setCurrentWidget(self.menu_screen)
        elif name == "Weapon Library":
            print("Opening Weapon Library...")
            if self.weapon_library:
                self.stacked_widget.setCurrentWidget(self.weapon_library)
            else:
                QMessageBox.warning(self, "Warning", "Weapon Library is not available.")
        elif name == "Character Builder":
            print("Opening Character Builder...")
            if self.character_builder:
                self.stacked_widget.setCurrentWidget(self.character_builder)
            else:
                QMessageBox.warning(self, "Warning", "Character Builder is not available.")
        elif name == "Descendant Library":
            print("Opening Descendant Library...")
            if self.descendant_library:
                self.stacked_widget.setCurrentWidget(self.descendant_library)
            else:
                QMessageBox.warning(self, "Warning", "Descendant Library is not available.")
        else:
            # For now, just return to the menu for other calculators
            QMessageBox.information(self, "Info", f"{name} is not implemented yet.")
            self.stacked_widget.setCurrentWidget(self.menu_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())