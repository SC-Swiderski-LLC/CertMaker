
# CertMaker

![CertMaker Logo](assets/certmaker_logo.png)

**CertMaker** is a Python-based GUI tool designed to streamline the creation of self-signed SSL/TLS certificates for application deployments, particularly in Microsoft Intune-managed environments. This tool simplifies certificate generation, offering an intuitive interface for IT professionals and developers.

---

## 🚀 Features

- **User-Friendly Interface**: Powered by PyQt5 with an optional dark mode for ease of use.
- **Customizable Certificates**: Configure Common Name (CN), key size, and validity period.
- **Secure Key Management**: Generates RSA keys with customizable sizes (1024 to 4096 bits).
- **Quick Output**: Save PEM-encoded certificate and key files in a specified directory.
- **Overwrite Protection**: Alerts you if files already exist, giving the option to overwrite.
- **Dark Mode Support**: Detects system dark mode settings for better usability.

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or newer
- The following Python libraries:
  - `PyQt5`
  - `cryptography`

Install the required libraries using pip:

```bash
pip install PyQt5 cryptography
```

### Running the Application

Clone this repository and run the main script:

```bash
git clone https://github.com/your-repo/certmaker.git
cd certmaker
python certmaker.py
```

For packaged deployment, use PyInstaller to generate a standalone executable:

```bash
pyinstaller --onefile --noconsole CertMaker.spec
```

---

## 🖥️ Usage

1. **Fill Out the Form**:
   - Enter a **Common Name (CN)**.
   - Select the **key size** (default: 2048 bits).
   - Set the **validity period** in days (default: 365 days).
2. **Choose an Output Folder**:
   - Browse to select a directory to save the generated certificate files.
3. **Generate Certificate**:
   - Click the `Generate Certificate` button.
   - PEM-encoded certificate and key files are saved in the specified folder.

---

## 📂 Project Structure

```plaintext
CertMaker/
├── assets/
│   ├── certmaker_logo.png    # Application logo
│   └── icon.ico              # Application icon
├── core/
│   ├── cert_generator.py     # Certificate generation logic
│   ├── utils.py              # Utility functions for resource management
│   └── Computer Error Alert-SoundBible.com-783113881.wav # Alert sound
├── gui/
│   └── main_window.py        # GUI implementation
├── tests/                    # Unit tests (empty placeholder)
├── CertMaker.spec            # PyInstaller configuration
├── README.md                 # Documentation
├── certmaker.py              # Entry point for the application
└── library_check.py          # Library check script
```

---

## 🧩 Modules Overview

### `cert_generator.py`
Handles the core logic for generating self-signed certificates using the `cryptography` library.

### `main_window.py`
Defines the PyQt5-based GUI, offering dark mode support and an intuitive interface.

### `utils.py`
Provides utility functions for resource management, ensuring compatibility with PyInstaller.

---

## 🛡️ License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

For questions, feedback, or contributions, feel free to reach out at [your-email@example.com](mailto:your-email@example.com).

Happy Certifying! ✨
