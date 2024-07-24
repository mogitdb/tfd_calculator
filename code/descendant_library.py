import os
import json
import requests
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                               QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from stat_mapping import get_readable_name, get_readable_stat, load_processed_data, STAT_MAPPING

class DescendantLibrary(QWidget):
    descendantSelected = Signal(dict)  # Signal to emit when a descendant is selected

    def __init__(self, parent=None):
        super().__init__(parent)
        self.descendants = load_processed_data("processed_descendant_data.json")
        self.selected_descendant = None
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter the name of a descendant to search...")
        self.search_bar.textChanged.connect(self.filter_table)
        layout.addWidget(self.search_bar)

        # Descendants table
        self.table = QTableWidget()
        self.table.setStyleSheet("QTableWidget {border: 1px solid #3a3a3a; gridline-color: #3a3a3a;}"
                                 "QHeaderView::section {background-color: #3a3a3a; color: white;}")
        self.table.cellClicked.connect(self.show_descendant_details)
        self.table.horizontalHeader().sectionClicked.connect(self.sort_table)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Save Descendant Choice button
        self.save_button = QPushButton("Save Descendant Choice")
        self.save_button.clicked.connect(self.save_descendant_choice)
        buttons_layout.addWidget(self.save_button)

        # Clear Descendant button
        self.clear_button = QPushButton("Clear Descendant")
        self.clear_button.clicked.connect(self.clear_descendant)
        buttons_layout.addWidget(self.clear_button)

        layout.addLayout(buttons_layout)

        # Descendant details
        self.details_scroll = QScrollArea()
        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout(self.details_widget)
        self.details_scroll.setWidget(self.details_widget)
        self.details_scroll.setWidgetResizable(True)
        layout.addWidget(self.details_scroll)

    def update_table(self):
        if not self.descendants:
            print("No descendants data available to display.")
            return

        print("Updating table with descendant data...")
        self.table.setRowCount(len(self.descendants))
        
        columns = ["descendant_name", "element_type", "arche_type"]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels([get_readable_name(col) for col in columns])

        for row, descendant in enumerate(self.descendants):
            for col, attr in enumerate(columns):
                if attr in ["element_type", "arche_type"]:
                    value = descendant["descendant_skill"][0].get(attr, 'N/A')
                else:
                    value = descendant.get(attr, 'N/A')
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.table.resizeColumnsToContents()
        print("Table updated successfully.")

    def sort_table(self, column_index):
        self.table.sortItems(column_index, Qt.AscendingOrder)

    def show_descendant_details(self, row, col):
        descendant = self.descendants[row]
        self.selected_descendant = descendant
        self.update_descendant_details(descendant)
        self.descendantSelected.emit(descendant)  # Emit signal with selected descendant data

    def filter_table(self):
        search_text = self.search_bar.text().lower()
        for row in range(self.table.rowCount()):
            descendant = self.descendants[row]
            if search_text in descendant['descendant_name'].lower():
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def update_descendant_details(self, descendant):
        # Clear existing layout
        for i in reversed(range(self.details_layout.count())): 
            self.details_layout.itemAt(i).widget().setParent(None)

        # Descendant image and basic info
        top_layout = QHBoxLayout()
        
        # Image
        image_label = QLabel()
        pixmap = QPixmap()
        image_url = descendant.get('descendant_image_url')
        if image_url:
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                pixmap.loadFromData(response.content)
                image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            except requests.RequestException:
                image_label.setText("Image not available")
        else:
            image_label.setText("No image URL provided")
        top_layout.addWidget(image_label)

        # Basic info
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"Name: {descendant['descendant_name']}"))
        info_layout.addWidget(QLabel(f"ID: {descendant['descendant_id']}"))
        top_layout.addLayout(info_layout)

        self.details_layout.addLayout(top_layout)

        # Stats at level 40
        level_40_stats = next((level for level in descendant['descendant_stat'] if level['level'] == 40), None)
        if level_40_stats:
            self.details_layout.addWidget(QLabel("Stats at Level 40:"))
            for stat in level_40_stats['stat_detail']:
                self.details_layout.addWidget(QLabel(f"{stat['stat_type']}: {stat['stat_value']}"))

        # Skills
        self.details_layout.addWidget(QLabel("Skills:"))
        for skill in descendant['descendant_skill']:
            skill_layout = QVBoxLayout()
            skill_layout.addWidget(QLabel(f"Name: {skill['skill_name']}"))
            skill_layout.addWidget(QLabel(f"Type: {skill['skill_type']}"))
            skill_layout.addWidget(QLabel(f"Element: {skill['element_type']}"))
            skill_layout.addWidget(QLabel(f"Arche: {skill['arche_type']}"))
            skill_layout.addWidget(QLabel(f"Description: {skill['skill_description']}"))
            
            # Skill image
            skill_image_label = QLabel()
            skill_pixmap = QPixmap()
            skill_image_url = skill.get('skill_image_url')
            if skill_image_url:
                try:
                    response = requests.get(skill_image_url)
                    response.raise_for_status()
                    skill_pixmap.loadFromData(response.content)
                    skill_image_label.setPixmap(skill_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                except requests.RequestException:
                    skill_image_label.setText("Skill image not available")
            else:
                skill_image_label.setText("No skill image URL provided")
            skill_layout.addWidget(skill_image_label)

            self.details_layout.addLayout(skill_layout)
            self.details_layout.addWidget(QLabel(""))  # Spacer

    def save_descendant_choice(self):
        if self.selected_descendant:
            user_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "user")
            os.makedirs(user_dir, exist_ok=True)
            save_path = os.path.join(user_dir, "descendant_choice.json")
            
            with open(save_path, "w") as f:
                json.dump(self.selected_descendant, f, indent=2)
            
            QMessageBox.information(self, "Saved", f"Descendant choice has been saved.")
        else:
            QMessageBox.warning(self, "Warning", "No descendant selected.")

    def clear_descendant(self):
        self.selected_descendant = None
        self.update_descendant_details(None)
        QMessageBox.information(self, "Cleared", "Descendant choice has been cleared.")

    def load_saved_descendant(self):
        user_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "user")
        load_path = os.path.join(user_dir, "descendant_choice.json")
        
        if os.path.exists(load_path):
            with open(load_path, "r") as f:
                saved_descendant = json.load(f)
            
            matching_descendant = next((d for d in self.descendants if d['descendant_id'] == saved_descendant['descendant_id']), None)
            if matching_descendant:
                self.selected_descendant = matching_descendant
                self.update_descendant_details(matching_descendant)
                QMessageBox.information(self, "Loaded", "Saved descendant choice has been loaded.")
            else:
                QMessageBox.warning(self, "Warning", "Saved descendant not found in current data.")
        else:
            QMessageBox.information(self, "Info", "No saved descendant choice found.")