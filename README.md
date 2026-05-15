# Ledger Document Capture System

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A Python-based, hardware-integrated GUI application captures high-resolution, raw images of handwritten ledger documents and carbon copies. The system builds datasets for Machine Learning (OCR/HTR) models and maintains secure, legally compliant digital audit trails. [cite_start]Capturing and storing raw images correctly ensures the integrity of the dataset for training Machine Learning models and maintaining legal audit trails[cite: 149].

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

* [cite_start]**File Format Selection:** The application utilizes lossless image formats to preserve the integrity of faint handwritten strokes and carbon-copy artifacts[cite: 151]. [cite_start]PNG acts as the industry standard for raw document capture in machine learning pipelines[cite: 152]. [cite_start]The system completely avoids JPEG formats, as lossy compression introduces visual artifacts that degrade Handwritten Text Recognition (HTR) accuracy[cite: 153].
* [cite_start]**Resolution and Quality Preservation:** The system saves images at the native resolution of the capture device[cite: 155]. [cite_start]It maintains a minimum of 300 DPI to guarantee sufficient pixel density[cite: 156].
* [cite_start]**Systematic Naming Conventions:** The application implements a rigorous, programmatic naming schema to prevent data loss and ensure exact traceability back to the physical ledger[cite: 161]. 
* [cite_start]**Metadata Association:** The script stores corresponding capture metadata alongside every raw image file[cite: 164, 165].
* [cite_start]**Data Immutability:** The system isolates raw images in a dedicated, read-only directory[cite: 169]. 

---

## ⚙️ Prerequisites

**Hardware Requirements:**
* PC, Laptop, or Raspberry Pi (Windows or Linux).
* USB Camera (12MP+ recommended for carbon copies).
* Fixed copy stand with an LED ring light.

**Software Dependencies:**
The system requires Python 3.8+ installation. Install the required libraries via terminal:

```bash
pip install opencv-python Pillow
