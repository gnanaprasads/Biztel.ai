Document Word Finder
A Python application with a graphical user interface that finds words within a specified bounding box in a document. The application processes normalized word coordinates from a JSON file and allows users to input document dimensions and bounding box coordinates to locate words in specific regions.
Features

User-friendly graphical interface
JSON file input support
Coordinate scaling from normalized (0-1) to actual document dimensions
Real-time word detection within specified bounding boxes
Error handling and user feedback
Scrollable results display

Requirements

Python 3.x
tkinter (usually comes with Python installation)
JSON support (built into Python)

Usage

Run the application:

bashCopypython word_finder_gui.py

Input the required information:

Document Width (e.g., 1263)
Document Height (e.g., 1644)
Bounding Box Coordinates:

x1: Top-left x coordinate
y1: Top-left y coordinate
x2: Bottom-right x coordinate
y2: Bottom-right y coordinate




Click "Find Words" and select your JSON input file when prompted.
