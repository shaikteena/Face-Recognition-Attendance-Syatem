# Face Recognition Attendance System

A simple Python project that uses a webcam and face recognition to mark student attendance automatically in a CSV file.

## Features

- Webcam-based face detection
- Face recognition against registered student photos
- Automatic attendance recording
- Prevents duplicate attendance on the same date
- CSV output with name, date, and time
- Simple project structure suitable for a college demonstration

## Project Structure

```text
Face_Recognition_Attendance_System/
├── attendance.py
├── requirements.txt
├── README.md
├── .gitignore
├── Attendance.csv              # created automatically; ignored by Git
└── known_faces/
    └── .gitkeep
```

## Requirements

- Python 3.9–3.12 recommended
- Working webcam
- Clear student photos
- Internet access for installing Python packages

## Installation

Create a virtual environment (recommended):

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Add Student Photos

Place one clear photo for each student in `known_faces/`.

Example:

```text
known_faces/
├── Anjali.jpg
├── Rahul.jpg
└── Priya.jpg
```

The filename becomes the student's name.

For best results, use a clear front-facing photo containing exactly one face.

Only use photos with appropriate permission and follow your institution's privacy rules.

## Run

```bash
python attendance.py
```

The webcam window will open.

- Recognized student → attendance is recorded.
- Unknown person → shown as `Unknown`.
- Press **Q** to close the camera.

## Attendance Output

After the first successful recognition, `Attendance.csv` is created:

```csv
Name,Date,Time
Anjali,2026-09-13,09:15:22
Rahul,2026-09-13,09:16:04
```

A student can only be marked once per day.

## Troubleshooting

### Camera does not open

Change this line in `attendance.py`:

```python
CAMERA_INDEX = 0
```

Try `1` if your computer has another camera.

### Student is not recognized

- Use a clearer reference photo.
- Make sure the reference photo has exactly one face.
- Improve lighting.
- Keep the face visible.
- Adjust `TOLERANCE` carefully. A lower value is stricter.

### Installation problems with face-recognition

The `face-recognition` package depends on `dlib`. Installation can vary by operating system and Python version. If installation fails, use a supported Python version and follow the package's official installation guidance.

## Privacy and Responsible Use

This project is intended as an educational demonstration. Face recognition is biometric processing. Before using it for real attendance:

- Obtain appropriate consent/authorization.
- Inform students how biometric data is used.
- Store data securely.
- Limit access to attendance records.
- Follow applicable laws and institutional policies.
- Provide a manual attendance/correction process.
- Consider liveness/anti-spoofing protection for real deployments.

Do not commit real student photos or attendance records to a public GitHub repository without proper authorization.

## License

This project is provided for educational purposes. Add a license appropriate to your intended use before publishing.
