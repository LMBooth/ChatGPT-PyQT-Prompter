import sys
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit, 
                             QPushButton, QComboBox, QMessageBox, QHBoxLayout, 
                             QLabel, QInputDialog)
from PyQt5.QtCore import pyqtSlot, QSize, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import openai
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

def loadApiKey():
    if os.path.exists("api_key.json"):
        with open("api_key.json", "r") as file:
            data = json.load(file)
            return  data.get("api_key", "")
    else:
        return ""

class GPTPrompter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.history = []
        self.apiKey = ""
        value = os.environ['OPENAI_API_KEY']
        if value is not None:
            self.apiKey = value
            self.validateApiKey()
            print(f"OPENAI_API_KEY Environment variable is set to: {value}")
        else:
            self.apiKey = loadApiKey()
            if self.apiKey == "":
                self.apiKeyStatusLabel.setText("API Key Status: None found.")
                print("key saved to local csv from previous use.")
            else:
                self.validateApiKey()
            print(f"OPENAI_API_KEY Environment variable is not set.")
        

    def initUI(self):
        self.resize(1000, 800)
        layout = QVBoxLayout()
        # API Key Status Label
        self.apiKeyStatusLabel = QLabel("API Key Status: Unknown")  # Add this label to show status
        self.apiKeyStatusLabel.setWordWrap(True)  # Enable word wrapping
        layout.addWidget(self.apiKeyStatusLabel)
        self.loadingStatusLabel = QLabel("Status: Ready", self)
        self.loadingStatusLabel.setWordWrap(True)  # Enable word wrapping
        self.loadingStatusLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loadingStatusLabel)
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
        loadApiKey()
    
    @pyqtSlot()
    def onSendClicked(self):
        model = self.modelSelection.currentText()
        prompt = self.promptInput.toPlainText()
        self.history.append(prompt)
        self.updateHistoryComboBox()

        self.loadingStatusLabel.setText("Status: Loading...")
        self.sendButton.setDisabled(True)

        self.thread = WorkerThread(self.apiKey, model, prompt)
        self.thread.responseSignal.connect(self.handleResponse)
        self.thread.start()
        
    @pyqtSlot(str, str)
    def handleResponse(self, response, error):
        self.loadingStatusLabel.setText("Status: Ready")
        self.sendButton.setDisabled(False)
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
        self.setStyleSheet("QWidget { font-size: 14pt; } QPushButton { background-color: lightgray; } QLabel { font-weight: bold; }")
    def setApiKey(self):
        text, ok = QInputDialog.getText(self, 'Set API Key', 'Enter your API key:')
        if ok and text:
            self.apiKey = text
            self.saveApiKey()
        self.validateApiKey() 

    def saveApiKey(self):
        with open("api_key.json", "w") as file:
            json.dump({"api_key": self.apiKey}, file)

    def validateApiKey(self):
        try:
            client = OpenAI(api_key=self.apiKey)
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content":"test"}])
            if response.status_code == 200 and 'choices' in response and len(response['choices']) > 0:
                return response['choices'][0]['message']['content']
            else:
                return "Invalid response structure or empty response."
        except Exception as e:
            self.apiKeyStatusLabel.setText("API Key Status: Invalid - " + str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GPTPrompter()
    ex.show()
    sys.exit(app.exec_())
