import os
import json
import requests
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                               QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QScrollArea,
                               QTabWidget, QAbstractItemView, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from stat_mapping import get_readable_name, get_readable_stat, load_processed_data, STAT_MAPPING

class WeaponLibrary(QWidget):
    weaponSelected = Signal(dict)  # Signal to emit when a weapon is selected

    def __init__(self, parent=None):
        super().__init__(parent)
        self.weapons = load_processed_data("processed_weapon_data.json")
        self.selected_weapons = [None, None, None]  # Initialize with None for each slot
        self.create_widgets()
        self.update_table()
        self.create_blank_weapon_slots()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter the name of a weapon or select it from the list below to begin modifying it.")
        self.search_bar.textChanged.connect(self.filter_table)
        layout.addWidget(self.search_bar)

        # Weapons table
        self.table = QTableWidget()
        self.table.setStyleSheet("QTableWidget {border: 1px solid #3a3a3a; gridline-color: #3a3a3a;}"
                                 "QHeaderView::section {background-color: #3a3a3a; color: white;}")
        self.table.cellClicked.connect(self.show_weapon_details)
        self.table.horizontalHeader().sectionClicked.connect(self.sort_table)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.table)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Add button
        self.add_button = QPushButton("ADD+")
        self.add_button.clicked.connect(self.add_selected_weapon)
        buttons_layout.addWidget(self.add_button)

        # Save Loadout button
        self.save_loadout_button = QPushButton("Save Loadout")
        self.save_loadout_button.clicked.connect(self.save_loadout)
        buttons_layout.addWidget(self.save_loadout_button)

        # Load Loadout button
        self.load_loadout_button = QPushButton("Load Loadout")
        self.load_loadout_button.clicked.connect(self.load_saved_weapons)
        buttons_layout.addWidget(self.load_loadout_button)

        # Clear Loadout button
        self.clear_loadout_button = QPushButton("Clear Loadout")
        self.clear_loadout_button.clicked.connect(self.clear_loadout)
        buttons_layout.addWidget(self.clear_loadout_button)

        layout.addLayout(buttons_layout)

        # Selected weapons tabs
        self.selected_weapons_tabs = QTabWidget()
        layout.addWidget(self.selected_weapons_tabs)

    def update_table(self):
        if not self.weapons:
            print("No weapons data available to display.")
            return

        print("Updating table with weapon data...")
        self.table.setRowCount(len(self.weapons))
        
        columns = ["weapon_name", "weapon_type", "weapon_tier", "weapon_rounds_type", 
                   "firearm_atk_105000026", "105000023", "105000030", "105000031", 
                   "105000035", "105000095", "105000170", "weapon_perk_ability_name"]
        
        # Add new stats to the columns
        new_stats = ["105000069", "105000073", "105000194", "105000195", "105000032", "105000174", "105000200"]
        columns.extend(new_stats)
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels([get_readable_name(col) for col in columns])

        for row, weapon in enumerate(self.weapons):
            for col, attr in enumerate(columns):
                value = weapon.get(attr, 'N/A')
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.table.resizeColumnsToContents()
        print("Table updated successfully.")

    def create_blank_weapon_slots(self):
        self.selected_weapons_tabs.clear()
        for i in range(3):
            self.add_blank_weapon_tab(f"Weapon {i+1}")

    def add_blank_weapon_tab(self, name):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        label = QLabel(f"No weapon selected.\nClick 'ADD+' to add a weapon to this slot.")
        label.setAlignment(Qt.AlignCenter)
        tab_layout.addWidget(label)

        self.selected_weapons_tabs.addTab(tab, name)

    def sort_table(self, column_index):
        self.table.sortItems(column_index, Qt.AscendingOrder)

    def show_weapon_details(self, row, col):
        weapon = self.weapons[row]
        self.weaponSelected.emit(weapon)  # Emit signal with selected weapon data

    def filter_table(self):
        search_text = self.search_bar.text().lower()
        for row in range(self.table.rowCount()):
            weapon = self.weapons[row]
            if search_text in weapon['weapon_name'].lower():
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def add_selected_weapon(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select a weapon first.")
            return

        selected_row = selected_rows[0].row()
        selected_weapon = self.weapons[selected_row]

        # Find the first empty slot
        for i, weapon in enumerate(self.selected_weapons):
            if weapon is None:
                self.selected_weapons[i] = selected_weapon
                self.update_weapon_tab(i, selected_weapon)
                return

        # If all slots are full, ask the user which slot to replace
        reply = QMessageBox.question(self, "Replace Weapon", 
                                     "All slots are full. Which weapon do you want to replace?",
                                     "Weapon 1", "Weapon 2", "Weapon 3", "Cancel")
        if reply < 3:  # 0, 1, or 2 for weapons, 3 for Cancel
            self.selected_weapons[reply] = selected_weapon
            self.update_weapon_tab(reply, selected_weapon)

    def update_weapon_tab(self, index, weapon):
        tab = self.selected_weapons_tabs.widget(index)
        
        # Clear existing layout if it exists
        if tab.layout():
            QWidget().setLayout(tab.layout())
        
        tab_layout = QVBoxLayout(tab)

        # Weapon image and perk ability information
        top_layout = QHBoxLayout()
        
        # Image
        image_label = QLabel()
        pixmap = QPixmap()
        image_url = weapon.get('image_url')
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

        # Perk ability information
        right_layout = QVBoxLayout()
        
        perk_name = weapon.get('weapon_perk_ability_name', 'N/A')
        perk_desc = weapon.get('weapon_perk_ability_description', 'N/A')
        perk_label = QLabel(f"Weapon Perk Ability: {perk_name}\n\n{perk_desc}")
        perk_label.setWordWrap(True)
        perk_label.setMinimumWidth(200)
        right_layout.addWidget(perk_label)

        top_layout.addLayout(right_layout)
        tab_layout.addLayout(top_layout)

        # Weapon details
        details_label = QLabel(f"Name: {weapon['weapon_name']}\n"
                               f"Type: {weapon['weapon_type']}\n"
                               f"Tier: {weapon['weapon_tier']}\n"
                               f"Rounds Type: {weapon['weapon_rounds_type']}\n"
                               f"Level: 100")
        tab_layout.addWidget(details_label)

        # Stats
        stats_scroll = QScrollArea()
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)

        for key in STAT_MAPPING.keys():
            if key in weapon and key not in ['weapon_name', 'weapon_type', 'weapon_tier', 'weapon_rounds_type', 'image_url', 'weapon_id', 'weapon_perk_ability_name', 'weapon_perk_ability_description']:
                stat_label = QLabel(get_readable_stat(weapon, key))
                stats_layout.addWidget(stat_label)

        stats_widget.setLayout(stats_layout)
        stats_scroll.setWidget(stats_widget)
        stats_scroll.setWidgetResizable(True)
        tab_layout.addWidget(stats_scroll)

        self.selected_weapons_tabs.setTabText(index, f"{weapon['weapon_name']} (Weapon {index + 1})")

        print(f"Added weapon: {weapon['weapon_name']}")
        print(f"Weapon Perk Ability Name: {perk_name}")
        print(f"Weapon Perk Ability Description: {perk_desc}")

    def save_loadout(self):
        loadout_file = "descendant_loadout.py"
        loadout_data = [
            {k: v for k, v in weapon.items() if k in STAT_MAPPING}
            for weapon in self.selected_weapons if weapon is not None
        ]

        with open(loadout_file, "w") as f:
            json.dump(loadout_data, f, indent=2)

        QMessageBox.information(self, "Saved", f"Loadout with {len(loadout_data)} weapons has been saved.")

    def load_saved_weapons(self):
        loadout_file = "descendant_loadout.py"
        try:
            with open(loadout_file, "r") as f:
                saved_weapons = json.load(f)

            self.selected_weapons = [None, None, None]
            self.create_blank_weapon_slots()
            
            for i, weapon_data in enumerate(saved_weapons):
                if i >= 3:
                    break
                matching_weapon = next((w for w in self.weapons if w['weapon_id'] == weapon_data['weapon_id']), None)
                if matching_weapon:
                    self.selected_weapons[i] = matching_weapon
                    self.update_weapon_tab(i, matching_weapon)

            QMessageBox.information(self, "Loaded", f"Loadout with {len(saved_weapons)} weapons has been loaded.")

        except FileNotFoundError:
            QMessageBox.warning(self, "Warning", "No saved loadout found.")

    def clear_loadout(self):
        reply = QMessageBox.question(self, "Clear Loadout", 
                                     "Are you sure you want to clear the entire loadout?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.selected_weapons = [None, None, None]
            self.create_blank_weapon_slots()
            QMessageBox.information(self, "Cleared", "Loadout has been cleared.")

    def clear_selected_weapons(self):
        self.selected_weapons = [None, None, None]
        self.create_blank_weapon_slots()