# Ledger Document Capture System

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A Python-based, hardware-integrated GUI application captures high-resolution, raw images of handwritten ledger documents and carbon copies. The system builds datasets for Machine Learning (OCR/HTR) models and maintains secure, legally compliant digital audit trails. Capturing and storing raw images correctly ensures the integrity of the dataset for training Machine Learning models and maintaining legal audit trails[cite: 149].

---

## 📋 Table of Contents
1. [Features](#-features)
2. [Standard Practices Adherence](#-standard-practices-adherence)
3. [Prerequisites](#-prerequisites)
4. [Installation](#-installation)
5. [Usage](#-usage)
6. [Output Structure](#-output-structure)
7. [Building a Standalone Executable](#-building-a-standalone-executable)

---

## 🚀 Features

* **Lossless Capture Pipeline:** The system bypasses standard camera compression to save maximum-resolution, lossless PNG files with embedded 300 DPI physical metadata.
* **Smart Camera Negotiation:** The application utilizes OS-specific hardware backends (DirectShow for Windows, V4L2 for Linux) for instant camera connection and real hardware name resolution.
* **Automated Metadata Generation:** The script generates a structured `.json` file alongside every image, logging timestamps, resolutions, orientation, and environmental assumptions.
* **Professional GUI:** A dark-themed Tkinter interface features a live, dynamic aspect-ratio video feed.
* **Hardware Interactivity:** Keyboard-bound capture (Spacebar) includes built-in debounce/cooldown logic to prevent accidental double-captures.
* **Orientation Control:** Real-time software rotation supports both Landscape and Portrait copy-stand configurations.

---

## 🛡️ Standard Practices Adherence

This system strictly enforces data immutability and machine learning data collection standards:

* **File Format Selection:** The application utilizes lossless image formats to preserve the integrity of faint handwritten strokes and carbon-copy artifacts[cite: 151]. PNG acts as the industry standard for raw document capture in machine learning pipelines[cite: 152]. The system completely avoids JPEG formats, as lossy compression introduces visual artifacts that degrade Handwritten Text Recognition (HTR) accuracy[cite: 153].
* **Resolution and Quality Preservation:** The system saves images at the native resolution of the capture device[cite: 155]. It maintains a minimum of 300 DPI to guarantee sufficient pixel density[cite: 156].
* **Systematic Naming Conventions:** The application implements a rigorous, programmatic naming schema to prevent data loss and ensure exact traceability back to the physical ledger[cite: 161]. 
* **Metadata Association:** The script stores corresponding capture metadata alongside every raw image file[cite: 164, 165].
* **Data Immutability:** The system isolates raw images in a dedicated, read-only directory[cite: 169]. 

---

## ⚙️ Prerequisites

**Hardware Requirements:**
* PC, Laptop, or Raspberry Pi (Windows or Linux).
* USB Camera (12MP+ recommended for carbon copies).
* Fixed copy stand with an LED ring light.

**Software Dependencies:**
The system requires Python 3.8+ installation. Install the required libraries via terminal:
Note for Windows environments: Install the pygrabber module to resolve real camera hardware names:

Bash
pip install pygrabber
📥 Installation
Clone the repository to a local machine:

Bash
git clone [https://github.com/username/ledger-capture-system.git](https://github.com/username/ledger-capture-system.git)
cd ledger-capture-system
Install dependencies as listed in the prerequisites.

🖥️ Usage
Execute the main application script:

Bash
python ledger_capture.py
Operational Workflow:

Directory Configuration: Select the destination folder for raw image storage (defaults to a local raw_ledger_images folder).

Hardware Selection: Choose the active USB camera from the dropdown menu and set the Aspect Factor (Landscape/Portrait).

Data Entry: Input the Ledger Book ID and the starting Page Number.

Capture Process: Click "Start Camera". Align the document in the live feed and press the [SPACEBAR] or click "Capture" to trigger the shutter. The page number increments automatically.

📁 Output Structure
For every capture event, the system generates two files following the YYYYMMDD_HHMMSS_LedgerBookID_PageNumber schema:  

Raw Image (.png): Saved with zero compression and strict 300x300 DPI header metadata.

Metadata Record (.json):

JSON
{
    "timestamp": "20260515_222500",
    "ledger_book_id": "DAIRY_MAY_2026",
    "page_number": 1,
    "file_format": "PNG",
    "resolution": "4000x3000",
    "dpi": 300,
    "color_space": "RGB",
    "orientation": "Portrait",
    "camera_name": "Logitech BRIO (Port 1)",
    "environmental_conditions": "Controlled Copy Stand",
    "lighting_parameters": "Constant LED Ring Light",
    "digital_zoom": "Disabled"
}
📦 Building a Standalone Executable (Windows)
PyInstaller packages the application into a standalone .exe for deployment on operator machines without requiring a Python installation.

Install PyInstaller:

Bash
pip install pyinstaller
Build the application:

Bash
pyinstaller --noconsole --onefile ledger_capture.py
Locate the compiled executable within the newly generated dist/ directory.

📄 License
This project operates under the MIT License.
```bash
pip install opencv-python Pillow
