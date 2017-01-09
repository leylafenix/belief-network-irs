from PyQt4.QtGui import *
from UI.main import Ui_MainWindow
from modeling import BeliefNetwork
import evaluating
import benchmarking
import sys
import os


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.browseBtn.clicked.connect(self.on_browse_clicked)
        self.buildBtn.clicked.connect(self.on_build_clicked)
        self.queryBtn.clicked.connect(self.on_query_clicked)

        self.dir = None

        self.belief_network = BeliefNetwork()

    def on_browse_clicked(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder')
        if self.folder_path:
            self.pathLineEdit.setText(str(self.folder_path))

    def on_build_clicked(self):
        self.folder_path = str(self.pathLineEdit.text())
        try:
            self.queryBtn.setEnabled(True)

            # TODO poner un combobox con los idiomas en processing.languages_available + (inferir None) y asignarselo a la variable
            language = 'english'

            self.belief_network.build(self.folder_path, language)
            self.names = [str(name) for name in os.listdir(self.folder_path) if name.endswith('.pdf') or name.endswith('.txt')]
        except:
            QMessageBox.critical(self, "Error", "Wrong path", QMessageBox.Ok)

    def on_query_clicked(self):
        query = str(self.queryLineEdit.text())
        count = self.numberSpinBox.value()

        #TODO Poner valor de checkbox
        expand_query = False

        #TODO Poner expanded_query en un label
        results, expanded_query = self.belief_network.query(query, expand_query)
        results = results[:min(len(results), count)]

        relevant = benchmarking.load_results(self.folder_path, query)

        if relevant:
            eval = evaluating.evaluate(relevant_documents=relevant, retrieved_documents=results)
            self.statisticslistWidget.clear()
            self.statisticslistWidget.addItems([str(k) + ': ' + str(v) for k, v in eval.items()])

        self.resultslistWidget.clear()
        self.resultslistWidget.addItems([str(t[0]) + ': ' + str(t[1]) for t in results])

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = MainWindow()
	w.show()
	app.exec_()