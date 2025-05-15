
# 🧾 Order Management System

> This is my first large-scale project completed in Winter 2024 as part of my training in embedded programming and Python.

## 📌 Objective

This project is an extension of an initial order management system, enhanced with advanced features such as:

- User interface built with Pygame and Tkinter
- Order status management: Pending, In Progress, Shipped
- Logging in CSV and JSON files
- Automatic email notifications for specific actions
- PIN-based authentication to confirm an order as "Shipped"
- Display of current time and temperature using the OpenWeatherMap API
- Physical interaction through buttons, LEDs, and buzzer via GPIO on Raspberry Pi
- Introduction to modular architecture in Python

## 🗂️ Project Structure

📁 Fichiers_json_csv_log/          ← Contains logs and order files  
📁 Gestionnaire de commandes/      ← Main source code, organized in modules  
📄 config.yaml                     ← YAML configuration file (GPIO, API)  
📄 Diagramme_etat.pdf              ← State diagram of order status  
📄 schema_de_montage.pdf           ← Wiring diagram of GPIO components  
🖼️ icon_*.png                      ← Icons used in the interface  

### 📁 Main Modules

- `main.py`: main application entry point
- `gpio_manager.py`: handles physical input/output (buttons, LEDs, buzzer)
- `tkinter_manager.py`: numeric keypad, confirmation dialogs
- `pillow_manager.py`: image display using PIL
- `email_manager.py`: email sending via SMTP
- `weather_manager.py`: fetches weather data using OpenWeatherMap
- `logger_manager.py`: logging management
- `status.py`: order status logic
- `table_manager.py`: order file read/write
- `config_loader.py`: loads YAML configuration
- `utils.py`: utility functions

## 📦 Dependencies

yaml  
smtplib  
time  
RPi.GPIO  
gpiozero  
json  
os  
uuid  
logging  
pygame  
sys  
threading  
csv  
PIL  
enum  
tkinter  
requests  
io  

### Installing dependencies:

```bash
pip install pyyaml pygame pillow requests gpiozero
sudo apt install python3-tk
```

⚠️ RPi.GPIO is specific to Raspberry Pi. If you're developing on Windows, consider using mocks to avoid GPIO errors.

## 🚀 Launch

```bash
python Gestionnaire\ de\ commandes/main.py
```

## 🔐 Security

- Transitioning an order to the "Shipped" status requires PIN authentication.
- Configuration (GPIO, weather API key) is managed via a YAML file.

## 👩‍💻 Authors

Project created by:  
- Nadia Simard Villa, student in IoT and Artificial Intelligence AEC program  
- Sophie Mercier, student in IoT and Artificial Intelligence AEC program
    
    Under the supervision of Khalil Loghlam, teacher, Eng. in Electrical and Software Engineering

