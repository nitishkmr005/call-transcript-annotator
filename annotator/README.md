# Project Requirement Document

## Project Title
**Call Transcript Annotation Tool**

## Description
This project is a Streamlit-based web application designed to annotate and validate call transcripts. It provides an interactive interface for annotators to view, edit, and validate call details, client profiles, and other related data. The tool supports filtering, dynamic form generation, and data visualization.

---

## Features
1. **Wide Layout**: The app is optimized for a wide layout for better visualization.
2. **Custom Styling**: Aesthetic and functional CSS applied to enhance UI/UX.
3. **Conversation Rendering**: Displays conversations in chat-bubble style for better readability.
4. **Dynamic Annotations**: Allows users to dynamically validate and annotate sections of the call transcript.
5. **Sidebar Filtering**: Filter conversations by annotator and interaction ID.
6. **Data Persistence**: Annotations are saved in a JSON file for future reference.
7. **Error Handling**: Ensures robust handling of data format issues or missing annotations.

---

## Modules and Functionalities
1. **Custom CSS Integration**:
   - Enhances aesthetics of the app with custom themes and elements.
   - Improves user engagement through smooth transitions and hover effects.

2. **Conversation Renderer**:
   - Displays agent and customer dialogues in distinct chat bubbles.
   - Supports structured display of call interactions.

3. **Annotation and Validation**:
   - Dynamic forms to validate and annotate specific sections of data.
   - Supports marking fields as correct, missing, or incorrect, with optional remarks.

4. **Data Management**:
   - **Save Annotations**: Converts annotated data into JSON format and saves to disk.
   - **Load Annotations**: Retrieves previously saved annotations from JSON files.

5. **Visualization Tabs**:
   - **Transcript and Annotation**: Shows the call transcript and allows annotation.
   - **View Annotations**: Displays all saved annotations with interaction ID selection.

6. **Error Handling**:
   - Handles JSON decoding errors and ensures app stability.

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Streamlit library
- Required Python packages:
  - `streamlit`
  - `pandas`
  - `numpy`
  - `json`

### Steps
1. Clone the repository.
2. Install the required libraries:
   ```bash
   pip install streamlit pandas numpy