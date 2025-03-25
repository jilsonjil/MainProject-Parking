# Parking Management System with Fee Collection Based on Number Plate Detection

This project implements an automated parking management system that uses image processing and license plate recognition to manage parking and calculate fees based on the duration a vehicle spends in the parking lot.

---

## Features

- **License Plate Recognition**: Detect and extract the license plate number from vehicle images.
- **Character Segmentation**: Segments the characters on the license plate for accurate recognition.
- **Fee Calculation**: Calculates parking fees based on the number of hours the vehicle spends in the parking area.
- **Database Integration**: Uses MySQL to store vehicle data, entry/exit times, and fee information.
- **Web Interface**: User-friendly web interface using HTML, CSS, and JavaScript.
- **Backend**: Python-based backend with Flask to handle server operations and integrate with the database.

---

## Tech Stack

- **Java**: Image processing and license plate recognition.
- **Python**: Backend server for handling operations and integrating with the database.
- **MySQL**: Database management system for storing vehicle data and transaction records.
- **HTML/CSS/JavaScript**: Frontend web technologies for user interaction.
- **Flask**: Python web framework for API and server management.
- **XML**: Data exchange and integration between system components.

---

## How It Works

1. **Image Capture**: The system captures an image of the vehicle entering the parking area.
2. **License Plate Recognition**: The system processes the image and extracts the license plate number.
3. **Character Segmentation**: The license plate characters are segmented and recognized using Optical Character Recognition (OCR).
4. **Entry Time Logging**: The vehicle's entry time is stored in the database.
5. **Exit and Fee Calculation**: Upon exit, the total time spent is calculated, and a parking fee is determined based on the duration.
6. **Fee Collection**: The user can view the calculated fee through the web interface and complete the payment.

---

## Database Schema

### Tables:
1. **Vehicles Table**:
   - `VehicleID` (Primary Key)
   - `LicensePlate` (VARCHAR)
   - `EntryTime` (DATETIME)
   - `ExitTime` (DATETIME)
   - `Fee` (DECIMAL)

---

## Installation

### Prerequisites
- Python 3.x
- MySQL server
- Java (for image processing)


