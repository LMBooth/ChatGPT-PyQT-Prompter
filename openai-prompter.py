import sys
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit, 
                             QPushButton, QComboBox, QMessageBox, QHBoxLayout, 
                             QLabel, QInputDialog)
from PyQt5.QtCore import pyqtSlot, QSize, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from openai import OpenAI
import json
import os

class WorkerThread(QThread):
    responseSignal = pyqtSignal(str, str)

    def __init__(self, api_key, model, prompt):
        QThread.__init__(self)
        self.api_key = api_key
        self.model = model
        self.prompt = prompt

    def run(self):
        try:
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(model=self.model, messages=[{"role": "user", "content": self.prompt}])
            self.responseSignal.emit(response.choices[0].message.content, None)
        except Exception as e:
            self.responseSignal.emit(None, str(e))

class GPTPrompter(QWidget):
    def __init__(self):
        super().__init__()
        self.history = []
        self.apiKey = ""
        self.initUI()

    def initUI(self):
        self.resize(1000, 800)
        layout = QVBoxLayout()

        # API Key Button
        self.apiKeyButton = QPushButton("Set API Key", self)
        self.apiKeyButton.clicked.connect(self.setApiKey)
        layout.addWidget(self.apiKeyButton)

        # Model Selection
        self.modelSelection = QComboBox(self)
        self.modelSelection.addItems(["gpt-3.5-turbo","gpt-3.5-turbo-1106", "gpt-4", "gpt-4-1106-preview"])
        layout.addWidget(self.modelSelection)

         # Multi-Line Prompt Input
        self.promptInput = QTextEdit(self)
        self.promptInput.setPlaceholderText("Enter your prompt")
        layout.addWidget(self.promptInput)

        # Send Button
        self.sendButton = QPushButton("Send", self)
        self.sendButton.clicked.connect(self.onSendClicked)
        layout.addWidget(self.sendButton)

        # Response Display
        self.responseText = QTextEdit(self)
        self.responseText.setReadOnly(True)
        layout.addWidget(self.responseText)

        # History Feature
        self.historyLabel = QLabel("History")
        self.historyComboBox = QComboBox(self)
        self.historyComboBox.activated[str].connect(self.onHistorySelected)
        historyLayout = QHBoxLayout()
        historyLayout.addWidget(self.historyLabel)
        historyLayout.addWidget(self.historyComboBox)
        layout.addLayout(historyLayout)

        # Apply Styling
        self.applyStyling()

        self.setLayout(layout)
        self.setWindowTitle("GPT Turbo Prompter")
        self.loadApiKey()

    @pyqtSlot()
    def onSendClicked(self):
        model = self.modelSelection.currentText()
        prompt = self.promptInput.toPlainText()
        self.history.append(prompt)
        self.updateHistoryComboBox()

        self.thread = WorkerThread(self.apiKey, model, prompt)
        self.thread.responseSignal.connect(self.handleResponse)
        self.thread.start()

    @pyqtSlot(str, str)
    def handleResponse(self, response, error):
        if error:
            QMessageBox.critical(self, "Error", str(error))
        else:
            self.responseText.append(">> " + self.promptInput.toPlainText())
            self.responseText.append(response)
            self.promptInput.clear()

    def onHistorySelected(self, text):
        self.promptInput.setText(text)

    def updateHistoryComboBox(self):
        self.historyComboBox.clear()
        self.historyComboBox.addItems(self.history)

    def applyStyling(self):
        self.setStyleSheet("QWidget { font-size: 14pt; } QPushButton { background-color: lightgray; }")

    def setApiKey(self):
        text, ok = QInputDialog.getText(self, 'Set API Key', 'Enter your API key:')
        if ok and text:
            self.apiKey = text
            self.saveApiKey()

    def loadApiKey(self):
        if os.path.exists("api_key.json"):
            with open("api_key.json", "r") as file:
                data = json.load(file)
                self.apiKey = data.get("api_key", "")

    def saveApiKey(self):
        with open("api_key.json", "w") as file:
            json.dump({"api_key": self.apiKey}, file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GPTPrompter()
    ex.show()
    sys.exit(app.exec_())
