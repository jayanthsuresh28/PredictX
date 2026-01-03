# PredictX
This project is a smart AI-based surveillance system that uses computer vision to detect human intrusion in a restricted area. It monitors live video, identifies motion and human presence, triggers a siren during unauthorized entry, and logs events with date and time for security monitoring.
The system uses background subtraction to detect motion and applies the Histogram of Oriented Gradients (HOG) algorithm for accurate human detection. A specific region in the video frame is marked as a restricted zone. If a person enters this area, the system triggers an alert.
The surveillance system operates in both Day Mode and Night Mode. During night hours, any intrusion is treated as a high-risk event and an audible siren is activated. Intrusion events are logged with date and time for future reference and security analysis.
# Features
- Real-time video surveillance
- Motion detection using background subtraction
- Human detection using HOG descriptor
- Restricted area intrusion detection
- Day and Night mode operation
- Siren alert for unauthorized access
- Event logging with timestamp
# Technologies Used
- Python
- OpenCV
- HOG (Histogram of Oriented Gradients)
- Multithreading
- Winsound
