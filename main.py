import sys
import csv
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                               QHeaderView, QScrollArea, QGridLayout, QFormLayout, QFileDialog,
                               QMessageBox, QMenuBar, QMenu, QStatusBar, QTabWidget, QTextEdit,
                               QCheckBox, QSplitter, QGroupBox, QDialog)
from PySide6.QtGui import QFont, QColor, QAction, QPainter
from PySide6.QtCore import Qt, Slot
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis

class WeaponComparisonDialog(QDialog):
    def __init__(self, weapons, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Weapon Comparison")
        self.setGeometry(100, 100, 1400, 800)
        layout = QVBoxLayout(self)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        content_layout = QHBoxLayout(content_widget)

        for weapon in weapons:
            weapon_widget = QGroupBox(weapon.get('Name', 'Unknown Weapon'))
            weapon_layout = QFormLayout(weapon_widget)
            for key, value in weapon.items():
                if value and key != 'Name':  # Exclude the name as it's already in the GroupBox title
                    label = QLabel(f"{key}:")
                    value_label = QLabel(str(value))
                    weapon_layout.addRow(label, value_label)
            content_layout.addWidget(weapon_widget)

    def update_chart(self, weapons, chart_view):
        chart = QChart()
        chart.setTitle("Weapon Stats Comparison")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QBarSeries()

        numeric_attrs = [
            'Firearm ATK', 'Fire Rate', 'Rounds per Magazine', 'Reload Time',
            'Reload Time Modifier', 'Firearm Critical Hit Rate', 'Firearm Critical Hit Damage',
            'Status Effect Trigger Rate', 'Weak Point Damage', 'Hip Fire Accuracy',
            'Aimed Shot Accuracy', 'Effective Range (Drop-off start)', 'ATK Drop-off Modifier',
            'Max Range', 'Chill ATK Bonus', 'Firearm ATK (vs. Order of Truth)'
        ]

        for weapon in weapons:
            bar_set = QBarSet(weapon.get('Name', 'Unknown'))
            values = []
            for attr in numeric_attrs:
                try:
                    value = weapon.get(attr, '0')
                    value = value.replace('%', '').replace('m', '').strip()  # Remove % and 'm' (meters)
                    value = float(value)
                    values.append(value)
                except (ValueError, AttributeError):
                    values.append(0)
            bar_set.append(values)
            series.append(bar_set)

        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(numeric_attrs)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        # Adjust the range of the y-axis
        max_value = max(max(bar_set.at(i) for i in range(bar_set.count())) for bar_set in series.barSets())
        axis_y.setRange(0, max_value * 1.1)  # Set the range to 110% of the maximum value

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        # Rotate x-axis labels for better readability
        axis_x.setLabelsAngle(-90)  # Increased angle for better fit

        chart_view.setChart(chart)

    def update_chart(self, weapons, chart_view):
        chart = QChart()
        chart.setTitle("Weapon Stats Comparison")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QBarSeries()

        numeric_attrs = ['Firearm ATK', 'Fire rate', 'Magazine capacity', 'Reload time',
                         'Crit chance', 'Crit damage', 'Status chance', 'Weakpoint damage',
                         'Base DPS', 'Crit DPS', 'Weakpoint DPS']

        for weapon in weapons:
            bar_set = QBarSet(weapon['Name'])
            values = []
            for attr in numeric_attrs:
                try:
                    value = float(weapon[attr].replace('%', ''))  # Remove percentage sign if present
                    values.append(value)
                except (ValueError, KeyError, AttributeError):
                    values.append(0)
            bar_set.append(values)
            series.append(bar_set)

        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(numeric_attrs)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        # Adjust the range of the y-axis
        max_value = max(max(bar_set.at(i) for i in range(bar_set.count())) for bar_set in series.barSets())
        axis_y.setRange(0, max_value * 1.1)  # Set the range to 110% of the maximum value

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        # Rotate x-axis labels for better readability
        axis_x.setLabelsAngle(-45)

        chart_view.setChart(chart)

    def update_chart(self, weapons, chart_view):
        chart = QChart()
        chart.setTitle("Weapon Stats Comparison")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QBarSeries()

        numeric_attrs = ['Firearm ATK', 'Fire rate', 'Magazine capacity', 'Reload time',
                         'Crit chance', 'Crit damage', 'Status chance', 'Weakpoint damage',
                         'Base DPS', 'Crit DPS', 'Weakpoint DPS']

        for weapon in weapons:
            bar_set = QBarSet(weapon['Name'])
            values = []
            for attr in numeric_attrs:
                try:
                    value = float(weapon[attr])
                    values.append(value)
                except (ValueError, KeyError):
                    values.append(0)
            bar_set.append(values)
            series.append(bar_set)

        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(numeric_attrs)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view.setChart(chart)

    def update_chart(self, weapons, chart_view):
        chart = QChart()
        chart.setTitle("Weapon Stats Comparison")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QBarSeries()

        numeric_attrs = ['Firearm ATK', 'Fire rate', 'Magazine capacity', 'Reload time',
                        'Crit chance', 'Crit damage', 'Status chance', 'Weakpoint damage',
                        'Base DPS', 'Crit DPS', 'Weakpoint DPS']

        for weapon in weapons:
            bar_set = QBarSet(weapon['Name'])
            values = []
            for attr in numeric_attrs:
                try:
                    value = float(weapon[attr])
                    values.append(value)
                except (ValueError, KeyError):
                    values.append(0)
            bar_set.append(values)
            series.append(bar_set)

        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(numeric_attrs)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view.setChart(chart)

from PySide6.QtGui import QIcon

class WeaponAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The First Descendant Weapon Analyzer")
        self.setGeometry(100, 100, 1600, 900)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        # Set the window icon
        self.setWindowIcon(QIcon('icon.png'))  # Make sure to have an 'icon.png' file in the same directory

        self.weapons = []
        self.module_modifiers = {}
        self.create_widgets()
        self.create_menu()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    # ... (rest of the class remains unchanged)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open CSV", self)
        open_action.triggered.connect(self.load_csv)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save CSV", self)
        save_action.triggered.connect(self.save_csv)
        file_menu.addAction(save_action)

    def create_widgets(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search weapons...")
        self.search_bar.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_bar)
        main_layout.addLayout(search_layout)

        # Splitter for 50/50 layout
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)

        # Top half: Weapons table
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        self.table.setStyleSheet("QTableWidget {border: 1px solid #3a3a3a; gridline-color: #3a3a3a;}"
                                 "QHeaderView::section {background-color: #3a3a3a; color: white;}")
        self.table.itemSelectionChanged.connect(self.on_weapon_select)
        table_layout.addWidget(self.table)
        splitter.addWidget(table_widget)

        # Bottom half: Details and module system
        details_widget = QWidget()
        details_layout = QHBoxLayout(details_widget)

        # Selected weapons display
        selected_weapons_container = QWidget()
        selected_weapons_layout = QVBoxLayout(selected_weapons_container)
        
        compare_button = QPushButton("Compare Selected Weapons")
        compare_button.clicked.connect(self.open_comparison_dialog)  # Connect button to comparison dialog
        selected_weapons_layout.addWidget(compare_button)
        
        self.selected_weapons_tabs = QTabWidget()  # Create tab widget for selected weapons
        selected_weapons_layout.addWidget(self.selected_weapons_tabs)
        
        details_layout.addWidget(selected_weapons_container)

        # Tab widget for detailed weapon info
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("QTabWidget::pane { border: 1px solid #3a3a3a; }"
                                      "QTabBar::tab { background-color: #2b2b2b; color: white; padding: 5px; }"
                                      "QTabBar::tab:selected { background-color: #3a3a3a; }")
        

        # Module system tab
        self.module_widget = QScrollArea()
        self.module_widget.setWidgetResizable(True)
        self.module_content = QWidget()
        self.module_layout = QFormLayout(self.module_content)
        self.module_widget.setWidget(self.module_content)
        self.tab_widget.addTab(self.module_widget, "Module System")

        details_layout.addWidget(self.tab_widget)
        splitter.addWidget(details_widget)

        # Set initial sizes for splitter
        splitter.setSizes([int(self.height() * 0.5), int(self.height() * 0.5)])

    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.weapons = list(reader)
                self.update_table()
                self.create_module_inputs()
                self.statusBar.showMessage(f"Loaded {len(self.weapons)} weapons from {file_name}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV file: {str(e)}")
                print(f"Detailed error: {e}")  # More detailed error in console

    def save_csv(self):
        if not self.weapons:
            QMessageBox.warning(self, "Warning", "No data to save.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        if file_name:
            try:
                with open(file_name, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=self.weapons[0].keys())
                    writer.writeheader()
                    writer.writerows(self.weapons)
                self.statusBar.showMessage(f"Saved {len(self.weapons)} weapons to {file_name}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save CSV file: {str(e)}")

    def update_table(self):
        if not self.weapons:
            return

        self.table.setColumnCount(len(self.weapons[0].keys()) + 1)  # +1 for checkbox
        self.table.setRowCount(len(self.weapons))
        headers = ['Select'] + list(self.weapons[0].keys())
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, weapon in enumerate(self.weapons):
            checkbox = QCheckBox()
            self.table.setCellWidget(row, 0, checkbox)
            checkbox.stateChanged.connect(lambda state, r=row: self.on_checkbox_changed(state, r))

            for col, (key, value) in enumerate(weapon.items(), start=1):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.table.resizeColumnsToContents()
        print(f"Updated table with {len(self.weapons)} rows")  # Debug print

    @Slot()
    def on_weapon_select(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            weapon = self.weapons[row]
            self.update_stats(weapon)
            self.update_chart(weapon)
        self.update_selected_weapons_display()  # Update selected weapons display

    def update_selected_weapons_display(self):
        self.selected_weapons_tabs.clear()  # Clear previous tabs

        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                weapon = self.weapons[row]
                modified_weapon = {}
                for key, value in weapon.items():
                    if value:  # Only display non-empty values
                        modified_value = self.apply_module_modifiers(key, value)
                        modified_weapon[key] = modified_value
                weapon_widget = QWidget()
                weapon_layout = QFormLayout(weapon_widget)
                for key, value in modified_weapon.items():
                    if value:  # Only display non-empty values
                        label = QLabel(f"{key}:")
                        value_label = QLabel(str(value))
                        weapon_layout.addRow(label, value_label)
                self.selected_weapons_tabs.addTab(weapon_widget, weapon['Name'])  # Add weapon tab

    def filter_table(self):
        search_text = self.search_bar.text().lower()
        for row in range(self.table.rowCount()):
            row_hidden = True
            for col in range(1, self.table.columnCount()):  # Start from 1 to skip checkbox column
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    row_hidden = False
                    break
            self.table.setRowHidden(row, row_hidden)

    def create_module_inputs(self):
        # Clear previous content
        for i in reversed(range(self.module_layout.rowCount())):
            self.module_layout.removeRow(i)

        attributes = [
            'Firearm ATK', 'Fire rate', 'Magazine capacity', 'Reload time',
            'Crit chance', 'Crit damage', 'Status chance', 'Weakpoint damage'
        ]

        for attr in attributes:
            label = QLabel(f"{attr}:")
            flat_input = QLineEdit()
            flat_input.setPlaceholderText("Enter flat modifier (e.g., +10, -5)")  # Set placeholder text
            percent_input = QLineEdit()
            percent_input.setPlaceholderText("Enter percentage (e.g., 10, -5)")  # Set placeholder text

            flat_input.textChanged.connect(lambda text, a=attr: self.update_module_modifier(a, text, False))
            percent_input.textChanged.connect(lambda text, a=attr: self.update_module_modifier(a, text, True))

            input_layout = QHBoxLayout()
            input_layout.addWidget(flat_input)
            input_layout.addWidget(percent_input)

            self.module_layout.addRow(label, input_layout)

    def update_module_modifier(self, attribute, modifier, is_percent):
        if attribute not in self.module_modifiers:
            self.module_modifiers[attribute] = {}
        
        if modifier:
            try:
                value = float(modifier)
                if is_percent:
                    self.module_modifiers[attribute]['percent'] = value / 100
                else:
                    self.module_modifiers[attribute]['flat'] = value
            except ValueError:
                if is_percent:
                    self.module_modifiers[attribute].pop('percent', None)
                else:
                    self.module_modifiers[attribute].pop('flat', None)
        else:
            if is_percent:
                self.module_modifiers[attribute].pop('percent', None)
            else:
                self.module_modifiers[attribute].pop('flat', None)
        
        if not self.module_modifiers[attribute]:
            self.module_modifiers.pop(attribute, None)
        
        self.update_all_weapons()

    def apply_module_modifiers(self, attribute, value):
        if attribute in self.module_modifiers:
            modifier = self.module_modifiers[attribute]
            try:
                if isinstance(value, str):
                    value = value.replace('%', '').replace('x', '').replace('s', '').strip()
                    value = float(value)
                else:
                    value = float(value)
                
                if 'flat' in modifier:
                    value += modifier['flat']
                if 'percent' in modifier:
                    value *= (1 + modifier['percent'])
                return f"{value:.2f}"
            except ValueError:
                return value  # Return original value if conversion fails
        return value

    def update_all_weapons(self):
        for row in range(self.table.rowCount()):
            weapon = self.weapons[row]
            for col, (key, value) in enumerate(weapon.items(), start=1):
                if key in self.module_modifiers:
                    try:
                        original_value = value
                        modified_value = self.apply_module_modifiers(key, value)
                        self.table.item(row, col).setText(f"{original_value} → {modified_value}")
                    except ValueError:
                        pass  # Skip if the value is not a number

        # Update the currently selected weapon's stats
        selected_items = self.table.selectedItems()
        if selected_items:
            self.on_weapon_select()

        # Update the selected weapons display
        self.update_selected_weapons_display()

    def on_checkbox_changed(self, state, row):
        if state == Qt.Checked:
            weapon = self.weapons[row]
            self.update_stats(weapon)
            self.update_chart(weapon)
        self.update_selected_weapons_display()  # Update selected weapons display

    def open_comparison_dialog(self):
        selected_weapons = [self.weapons[row] for row in range(self.table.rowCount())
                            if self.table.cellWidget(row, 0).isChecked()]
        if selected_weapons:
            # Apply module modifiers to the selected weapons
            modified_weapons = []
            for weapon in selected_weapons:
                modified_weapon = {}
                for key, value in weapon.items():
                    base_value = float(value) if value.replace('.', '').isdigit() else value
                    modified_value = self.apply_module_modifiers(key, base_value)
                    modified_weapon[key] = modified_value
                modified_weapons.append(modified_weapon)

            dialog = WeaponComparisonDialog(modified_weapons, self)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "No Selection", "Please select weapons to compare.")

app = QApplication(sys.argv)
app.setStyle("Fusion")  # Use Fusion style for a more modern look
window = WeaponAnalyzer()
window.show()
sys.exit(app.exec())