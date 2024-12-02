import os
import sys
import winsound
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QLineEdit, QSpinBox, QFormLayout, QHBoxLayout, QSizePolicy,
    QMessageBox, QCheckBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings, Qt, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from core.cert_generator import generate_self_signed_cert, save_certificate
from core.utils import resource_path
from time import sleep
from cryptography.hazmat.primitives import serialization

def resource_path(relative_path):
    """Get the absolute path to a resource, works for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

dark_mode_stylesheet = """
QMainWindow {
    background-color: #2B2B2B;
    color: #FFFFFF;
}

QLabel, QLineEdit, QSpinBox, QPushButton, QCheckBox {
    color: #FFFFFF;
    background-color: #3C3F41;
    border: 1px solid #555555;
    padding: 5px;
}

QCheckBox {
    spacing: 5px;
}

QCheckBox::indicator {
    width: 15px;
    height: 15px;
    border: 1px solid #555555;
    background-color: #3C3F41;
}

QCheckBox::indicator:unchecked {
    background-color: #3C3F41; /* Unchecked state background */
    border: 1px solid #555555; /* Unchecked state border */
}

QCheckBox::indicator:checked {
    background-color: #4CAF50; /* Distinct green for checked state */
    border: 1px solid #4CAF50; /* Matching green border for checked state */
}

QCheckBox::indicator:unchecked:hover {
    background-color: #555555; /* Hover effect for unchecked state */
}

QCheckBox::indicator:checked:hover {
    background-color: #66BB6A; /* Hover effect for checked state */
}

QCheckBox:hover {
    color: #FFFFFF;
    background-color: #4C4F51;
}

/* Other components */
QPushButton:hover {
    background-color: #4C4F51;
}

QPushButton:pressed {
    background-color: #5C5F61;
}

/* QMessageBox Styling */
QMessageBox {
    background-color: #2B2B2B;
    color: #FFFFFF;
    border: 1px solid #555555;
}

QMessageBox QLabel {
    color: #FFFFFF;
}

QMessageBox QPushButton {
    color: #FFFFFF;
    background-color: #3C3F41;
    border: 1px solid #555555;
    padding: 5px;
}

QMessageBox QPushButton:hover {
    background-color: #4C4F51;
}

QMessageBox QPushButton:pressed {
    background-color: #5C5F61;
}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CertMaker")
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))  # Use the icon
        self.setGeometry(100, 100, 400, 400)

        if self.is_system_dark_mode():
            self.setStyleSheet(dark_mode_stylesheet)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Input fields
        form_layout = QFormLayout()
        self.cn_field = QLineEdit()
        self.cn_field.setPlaceholderText("Common Name (e.g., 'CertMaker')")
        form_layout.addRow("Common Name:", self.cn_field)

        self.key_size_box = QSpinBox()
        self.key_size_box.setRange(1024, 4096)
        self.key_size_box.setValue(2048)
        form_layout.addRow("Key Size:", self.key_size_box)

        self.validity_box = QSpinBox()
        self.validity_box.setRange(1, 3650)
        self.validity_box.setValue(365)
        form_layout.addRow("Validity (days):", self.validity_box)

        layout.addLayout(form_layout)

        # Output Folder Section
        output_layout = QHBoxLayout()

        # Label for Output Folder
        output_label = QLabel("Output Folder:")
        output_layout.addWidget(output_label)

        # Output Field and Browse Button
        self.output_location_field = QLineEdit()
        self.output_location_field.setPlaceholderText("Select output folder...")
        self.output_location_field.setReadOnly(True)
        self.output_location_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_output_location)

        output_layout.addWidget(self.output_location_field)
        output_layout.addWidget(self.browse_button)

        layout.addLayout(output_layout)

        # Checkbox for .cer file generation
        self.cer_checkbox = QCheckBox("Generate .cer file")
        self.cer_checkbox.setChecked(False)  # Default unchecked
        layout.addWidget(self.cer_checkbox)

        # Button
        self.generate_button = QPushButton("Generate Certificate")
        self.generate_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.generate_button.clicked.connect(self.generate_certificate)  # Connect the button
        layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)

        # Status Label
        self.label = QLabel("Fill out the form and click 'Generate'.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(self.label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_output_location(self):
        """Open a dialog to select the output folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_location_field.setText(folder)

    def generate_certificate(self):
        try:
            # Get inputs
            common_name = self.cn_field.text()
            key_size = self.key_size_box.value()
            validity_days = self.validity_box.value()
            output_folder = self.output_location_field.text()

            error_flag = False  # Track if there’s an error

            # Check for missing Common Name
            if not common_name:
                self.label.setText("Error: Common Name is required!")
                self.cn_field.setStyleSheet("border: 2px solid red;")  # Highlight field
                error_flag = True
            else:
                self.cn_field.setStyleSheet("")  # Reset style if valid

            # Check for missing Output Folder
            if not output_folder:
                self.label.setText("Error: Output location is required!")
                self.output_location_field.setStyleSheet("border: 2px solid red;")  # Highlight field
                error_flag = True
            else:
                self.output_location_field.setStyleSheet("")  # Reset style if valid

            if error_flag:
                try:
                    # Play the default Windows error sound
                    winsound.MessageBeep(winsound.MB_ICONHAND)
                except Exception as sound_error:
                    print(f"Error playing sound: {sound_error}", file=sys.stderr)
                return  # Exit if there’s an error

            # Generate base file paths
            cert_path = f"{output_folder}/{common_name}_cert.pem"
            key_path = f"{output_folder}/{common_name}_key.pem"
            cer_path = f"{output_folder}/{common_name}.cer"

            # Generate the certificate
            cert_pem, key_pem = generate_self_signed_cert(
                common_name, days_valid=validity_days, key_size=key_size
            )

            with open(cert_path, "wb") as cert_file:
                cert_file.write(cert_pem)

            with open(key_path, "wb") as key_file:
                key_file.write(key_pem)

            if self.cer_checkbox.isChecked():
                # Convert PEM to CER
                from cryptography import x509

                cert = x509.load_pem_x509_certificate(cert_pem)
                cer_bytes = cert.public_bytes(encoding=serialization.Encoding.DER)

                with open(cer_path, "wb") as cer_file:
                    cer_file.write(cer_bytes)

                self.label.setText(f"Certificate and key saved to:\n{cert_path}\n{key_path}\n{cer_path}")
            else:
                self.label.setText(f"Certificate and key saved to:\n{cert_path}\n{key_path}")

        except Exception as e:
            self.label.setText(f"Error: {str(e)}")

    def is_system_dark_mode(self):
        """Check if the system is in dark mode."""
        settings = QSettings("HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize", QSettings.NativeFormat)
        return settings.value("AppsUseLightTheme") == 0  # 0 means dark mode
