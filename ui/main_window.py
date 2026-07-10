import shutil
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QPushButton,
    QFileDialog,
    QLabel,
    QCheckBox,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QInputDialog,
    QMessageBox,
    QAbstractItemView,
    QHeaderView,
    QRadioButton
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QThread
from PySide6.QtWebEngineWidgets import QWebEngineView
from widgets.dataframe_model import DataFrameModel
from core.pac_reporting import (create_practice_distribution_chart, boxgraph)
from config.settings_manager import (
    load_settings,
    save_settings_file
)
from workers.report_worker import (
    ReportWorker
)
from core.update_checker import (
    check_for_updates)
from version import APP_VERSION
from utils.paths import get_base_path

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(
            QIcon("assets/pac_metrics.ico")
        )
        self.loading_settings = True
        self.setWindowTitle("PAC Metrics")
        self.resize(1400, 900)
        self.setWindowTitle(
            f"PAC Metrics v{APP_VERSION}")

        self.settings = load_settings()
        self.settings_dirty = False
        self.base_path = get_base_path()

        self.tabs = QTabWidget()

        self.settings_tab = QWidget()
        self.icb_tab = QWidget()
        self.extended_tab = QWidget()
        self.pac_ended_tab = QWidget()
        self.pcsp_tab = QWidget()
        self.graphs_tab = QWidget()
        self.boxgraph = QWidget()

        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.icb_tab, "ICB Report")
        self.tabs.addTab(self.extended_tab, "Numbers Report")
        self.tabs.addTab(self.pac_ended_tab, "Missing PAC Ended")
        self.tabs.addTab(self.pcsp_tab, "Missing PCSP")
        self.tabs.addTab(self.graphs_tab, "New Case Distribtion")
        self.tabs.addTab(self.boxgraph, "Outcomes Analysis")

        self.setCentralWidget(self.tabs)

        self.build_settings_tab()
        self.build_results_tabs()

        self.load_settings_into_ui()
        self.loading_settings = False
        self.settings_dirty = False
        self.check_updates()

        self.set_generate_highlight()

        # Disable all result tabs initially
        self.tabs.setTabEnabled(1, False)  # ICB Report
        self.tabs.setTabEnabled(2, False)  # Extended Report
        self.tabs.setTabEnabled(3, False)  # Missing PAC Ended
        self.tabs.setTabEnabled(4, False)  # Missing PCSP
        self.tabs.setTabEnabled(5, False)  # Graphs
        self.tabs.setTabEnabled(6, False)  # Graphs

    def build_settings_tab(self):

        layout = QVBoxLayout()

        # -----------------------------
        # PRACTICES
        # -----------------------------

        layout.addWidget(
            QLabel("Practice Configuration")
        )

        self.practice_table = QTableWidget()

        self.practice_table.setColumnCount(3)

        self.practice_table.setHorizontalHeaderLabels([
            "Practice",
            "Search File",
            ""
        ])

        self.practice_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.practice_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        header = self.practice_table.horizontalHeader()

        header.setStretchLastSection(False)

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        self.practice_table.setColumnWidth(
            2,
            40
            )

        layout.addWidget(
            self.practice_table
        )

        self.add_practice_button = QPushButton(
            "Add Practice Report File"
        )

        self.remove_practice_button = QPushButton(
            "Remove Practice Report File"
        )

        layout.addWidget(
            self.add_practice_button
        )

        layout.addWidget(
            self.remove_practice_button
        )

        self.export_template_button = QPushButton(
            "Download Search Template For EMIS"
        )

        self.export_template_button.clicked.connect(
            self.export_emis_template
        )

        layout.addWidget(
            self.export_template_button
        )

        # -----------------------------
        # PAC STAFF
        # -----------------------------

        layout.addWidget(
            QLabel("PAC Staff")
        )

        self.staff_table = QTableWidget()

        self.staff_table.setColumnCount(2)

        self.staff_table.setHorizontalHeaderLabels([
            "Forename",
            "Surname"
        ])

        layout.addWidget(
            self.staff_table
        )

        self.add_staff_button = QPushButton(
            "Add Staff Member"
        )

        self.remove_staff_button = QPushButton(
            "Remove Staff Member"
        )

        layout.addWidget(
            self.add_staff_button
        )

        layout.addWidget(
            self.remove_staff_button
        )

        self.staff_table.itemChanged.connect(
            self.mark_settings_dirty
        )
        # -----------------------------
        # OTHER SETTINGS
        # -----------------------------

        self.exclude_minor = QCheckBox(
            "Exclude Minor Interventions"
        )

        layout.addWidget(
            self.exclude_minor
        )

        self.exclude_minor.stateChanged.connect(
            self.mark_settings_dirty
        )

        self.save_settings_button = QPushButton(
            "Save Settings"
        )

        self.generate_button = QPushButton(
            "Generate PAC Report"
        )

        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #ffb000;
                color: black;
                font-weight: bold;
                font-size: 14px;
                padding: 8px;
                border: 2px solid #cc8a00;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #ffc233;
            }

            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

        layout.addWidget(
            self.save_settings_button
        )

        layout.addWidget(
            self.generate_button
        )

        self.add_practice_button.clicked.connect(
            self.add_practice_row
        )

        self.remove_practice_button.clicked.connect(
            self.remove_practice_row
        )

        self.add_staff_button.clicked.connect(
            self.add_staff_row
        )

        self.remove_staff_button.clicked.connect(
            self.remove_staff_row
        )

        self.save_settings_button.clicked.connect(
            self.save_settings
        )

        self.generate_button.clicked.connect(
            self.generate_report
        )

        self.status_label = QLabel(
            "Ready"
        )

        layout.addWidget(
            self.status_label
        )

        self.settings_tab.setLayout(layout)

    def set_generate_highlight(self):

        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #ffb000;
                color: black;
                font-weight: bold;
                font-size: 14px;
                padding: 8px;
                border: 2px solid #cc8a00;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #ffc233;
            }

            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)


    def clear_generate_highlight(self):

        self.generate_button.setStyleSheet("")

    def build_results_tabs(self):

        self.icb_table = QTableView()

        self.export_icb_button = QPushButton(
            "Export ICB Report"
        )

        self.export_icb_button.clicked.connect(
            self.export_icb_report
        )

        icb_layout = QVBoxLayout()

        icb_layout.addWidget(
            self.export_icb_button
        )

        icb_layout.addWidget(
            self.icb_table
        )

        self.icb_tab.setLayout(
            icb_layout
        )

        self.extended_table = QTableView()

        extended_layout = QVBoxLayout()
        extended_layout.addWidget(
            self.extended_table
        )

        self.extended_tab.setLayout(
            extended_layout
        )

        self.pac_table = QTableView()

        pac_layout = QVBoxLayout()
        pac_layout.addWidget(
            self.pac_table
        )

        self.pac_ended_tab.setLayout(
            pac_layout
        )

        self.pcsp_table = QTableView()

        pcsp_layout = QVBoxLayout()
        pcsp_layout.addWidget(
            self.pcsp_table
        )

        self.pcsp_tab.setLayout(
            pcsp_layout
        )

        graphs_layout = QVBoxLayout()

        self.graph_view = QWebEngineView()

        graphs_layout.addWidget(
            self.graph_view
        )

        self.graphs_tab.setLayout(
            graphs_layout
        )

        outcomes_layout = QVBoxLayout()

        self.no_split_radio = QRadioButton(
            "No Split"
        )

        self.brave_split_radio = QRadioButton(
            "Brave vs Referred"
        )

        self.pcsp_split_radio = QRadioButton(
            "PCSP Present"
        )

        self.tep_split_radio = QRadioButton(
            "TEP Present"
        )

        self.no_split_radio.setChecked(True)

        outcomes_layout.addWidget(
            self.no_split_radio
        )

        outcomes_layout.addWidget(
            self.brave_split_radio
        )

        outcomes_layout.addWidget(
            self.pcsp_split_radio
        )

        outcomes_layout.addWidget(
            self.tep_split_radio
        )

        self.outcomes_graph = QWebEngineView()

        outcomes_layout.addWidget(
            self.outcomes_graph
        )

        self.boxgraph.setLayout(
            outcomes_layout
        )

        self.no_split_radio.toggled.connect(
            self.update_outcomes_chart
        )

        self.brave_split_radio.toggled.connect(
            self.update_outcomes_chart
        )

        self.pcsp_split_radio.toggled.connect(
            self.update_outcomes_chart
        )

        self.tep_split_radio.toggled.connect(
            self.update_outcomes_chart
        )

    def add_practice_row(self):

        practice_name, ok = QInputDialog.getText(
            self,
            "Practice Name",
            "Enter Practice Name"
        )

        if not ok or not practice_name:
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Practice Report",
            "",
            "HTML Files (*.html)"
        )

        if not file_path:
            return

        row = self.practice_table.rowCount()

        self.practice_table.insertRow(row)

        self.practice_table.setItem(
            row,
            0,
            QTableWidgetItem(practice_name)
        )

        self.practice_table.setItem(
            row,
            1,
            QTableWidgetItem(file_path)
        )

        button = QPushButton("...")

        button.clicked.connect(
            self.change_practice_file
        )

        self.practice_table.setCellWidget(
            row,
            2,
            button
        )
        self.set_generate_highlight()
        self.mark_settings_dirty()


    def remove_practice_row(self):

        row = self.practice_table.currentRow()

        if row >= 0:
            self.practice_table.removeRow(row)
        self.set_generate_highlight()
        self.mark_settings_dirty()

    def add_staff_row(self):

        row = self.staff_table.rowCount()

        self.staff_table.insertRow(row)

        self.set_generate_highlight()
        self.mark_settings_dirty()

    def remove_staff_row(self):

        row = self.staff_table.currentRow()

        if row >= 0:
            self.staff_table.removeRow(row)
        self.set_generate_highlight()
        self.mark_settings_dirty()

    def save_settings(self):

        practices = []

        for row in range(
            self.practice_table.rowCount()
        ):

            practice_item = self.practice_table.item(row, 0)
            path_item = self.practice_table.item(row, 1)

            if practice_item and path_item:

                practices.append({
                    "name": practice_item.text(),
                    "path": path_item.text()
                })

        staff = []

        for row in range(
            self.staff_table.rowCount()
        ):

            forename_item = self.staff_table.item(row, 0)
            surname_item = self.staff_table.item(row, 1)

            if forename_item and surname_item:

                staff.append({
                    "forename": forename_item.text(),
                    "surname": surname_item.text()
                })

        settings = {

            "exclude_minor":
                self.exclude_minor.isChecked(),

            "practices":
                practices,

            "pac_staff":
                staff
        }

        save_settings_file(settings)
        self.settings_dirty = False

        QMessageBox.information(
            self,
            "Settings Saved",
            "Settings saved successfully."
        )

    def load_settings_into_ui(self):

        self.exclude_minor.setChecked(
            self.settings.get(
                "exclude_minor",
                False
            )
        )

        for practice in self.settings.get(
            "practices",
            []
        ):

            row = self.practice_table.rowCount()

            self.practice_table.insertRow(row)

            self.practice_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    practice["name"]
                )
            )

            self.practice_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    practice["path"]
                )
            )

            button = QPushButton("...")

            button.setProperty(
                "row",
                row
            )

            button.clicked.connect(
                self.change_practice_file
            )

            self.practice_table.setCellWidget(
                row,
                2,
                button
            )

        for staff_member in self.settings.get(
            "pac_staff",
            []
        ):

            row = self.staff_table.rowCount()

            self.staff_table.insertRow(row)

            self.staff_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    staff_member["forename"]
                )
            )

            self.staff_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    staff_member["surname"]
                )
            )

    def generate_report(self):

        reports = []

        for row in range(
            self.practice_table.rowCount()
        ):

            practice_item = self.practice_table.item(row, 0)
            path_item = self.practice_table.item(row, 1)

            if practice_item and path_item:

                reports.append({
                    "practice": practice_item.text(),
                    "path": path_item.text()
                })

        pac_staff = []

        for row in range(
            self.staff_table.rowCount()
        ):

            forename_item = self.staff_table.item(
                row,
                0
            )

            surname_item = self.staff_table.item(
                row,
                1
            )

            if forename_item and surname_item:

                pac_staff.append(
                    (
                        forename_item.text(),
                        surname_item.text()
                    )
                )

        self.generate_button.setEnabled(False)

        self.status_label.setText(
            "Generating report..."
        )

        self.thread = QThread()

        self.worker = ReportWorker(
            reports,
            pac_staff,
            self.exclude_minor.isChecked()
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.report_complete
        )

        self.worker.error.connect(
            self.report_error
        )

        self.thread.start()

    def report_complete(self, dfs):
        self.dfs = dfs
        self.icb_report_export = dfs["icb_report_export"]
        self.icb_table.setModel(
            DataFrameModel(
                self.icb_report_export
            )
        )
        
        self.extended_table.setModel(
            DataFrameModel(
                dfs["extended_report_export"]
            )
        )

        self.pac_table.setModel(
            DataFrameModel(
                dfs["missing_pac_ended"]
            )
        )

        self.pcsp_table.setModel(
            DataFrameModel(
                dfs["missing_pcsp"]
            )
        )

        self.status_label.setText(
            "Report Complete"
        )

        self.generate_button.setEnabled(True)
        self.clear_generate_highlight()
        self.tabs.setTabEnabled(1, True)
        self.tabs.setTabEnabled(2, True)
        self.tabs.setTabEnabled(3, True)
        self.tabs.setTabEnabled(4, True)
        self.tabs.setTabEnabled(5, True)
        self.tabs.setTabEnabled(6, True)
        self.tabs.setCurrentIndex(1)   # jump to ICB tab

        fig = create_practice_distribution_chart(
            dfs["case_summary"]
        )

        self.graph_view.setHtml(
            fig.to_html(
                include_plotlyjs="cdn"
            )
        )
        self.update_outcomes_chart()
        self.thread.quit()

    def report_error(self, message):

        QMessageBox.critical(
            self,
            "Error",
            message
        )

        self.status_label.setText(
            "Failed"
        )

        self.generate_button.setEnabled(True)

        self.thread.quit()

    def mark_settings_dirty(self):

        if getattr(self, "loading_settings", False):
            return

        self.settings_dirty = True

        self.set_generate_highlight()

    def closeEvent(self, event):

        if not self.settings_dirty:

            event.accept()
            return

        reply = QMessageBox.question(
            self,
            "Unsaved Settings",
            "You have unsaved settings changes.\n\nSave before exiting?",
            QMessageBox.Save |
            QMessageBox.Discard |
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Save:

            self.save_settings()

            event.accept()

        elif reply == QMessageBox.Discard:

            event.accept()

        else:

            event.ignore()

    def change_practice_file(self):

        button = self.sender()

        index = self.practice_table.indexAt(
            button.pos()
        )

        row = index.row()

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Practice Report",
            "",
            "HTML Files (*.html)"
        )

        if not file_path:
            return

        self.practice_table.setItem(
            row,
            1,
            QTableWidgetItem(file_path)
        )

        self.mark_settings_dirty()
    
    def check_updates(self):

        update_info = check_for_updates()

        if not update_info:
            return

        if update_info["update_available"]:

            QMessageBox.information(
                self,
                "Update Available",
                f"""
    Current Version:
    {update_info['current']}

    Latest Version:
    {update_info['latest']}

    Please download the latest version
    from GitHub: 
    https://github.com/Defiancegames/PAC_Reporting_App/archive/refs/heads/main.zip.
    """
            )
    
    def update_outcomes_chart(self):

        print("update_outcomes_chart called")

        if not hasattr(self, "dfs"):
            return

        if self.no_split_radio.isChecked():

            split = "none"

        elif self.brave_split_radio.isChecked():

            split = "brave"

        elif self.pcsp_split_radio.isChecked():

            split = "pcsp"

        else:

            split = "tep"

        try:

            fig = boxgraph(
                self.dfs,
                split_by=split
            )

            self.outcomes_graph.setHtml(
                fig.to_html(
                    include_plotlyjs="cdn"
                )
            )

        except Exception as e:

            print(e)
        
    def export_icb_report(self):

        if not hasattr(
            self,
            "icb_report_export"
        ):
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save ICB Report",
            "PAC_ICB_Report.xlsx",
            "Excel Files (*.xlsx)"
        )

        if not file_path:
            return

        try:

            self.icb_report_export.to_excel(
                file_path,
                engine="openpyxl"
            )

            QMessageBox.information(
                self,
                "Export Complete",
                f"Report saved to:\n{file_path}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Export Failed",
                str(e)
            )

    def export_emis_template(self):

        template_source = (
            self.base_path /
            "templates" /
            "PAC V2.xml"
        )

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save EMIS Template",
            "PAC V2.xml",
            "XML Files (*.xml)"
        )

        if not file_path:
            return

        try:

            shutil.copyfile(
                template_source,
                file_path
            )

            QMessageBox.information(
                self,
                "Template Exported",
                f"Template saved to:\n{file_path}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Export Failed",
                str(e)
            )
        