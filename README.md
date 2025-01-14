# Streamlit Tools for Transcript Annotation and JSON Comparison

## Overview
This repository contains two Streamlit-based applications designed for interactive data annotation, validation, and comparison:
1. **Call Transcript Annotation Tool**: A tool to annotate and validate call transcripts dynamically.
2. **Precision and Recall Calculation for JSON Comparison**: A tool to compare JSON objects, calculate precision and recall, and analyze attribute-level and record-level metrics.

---

## Features

### Call Transcript Annotation Tool
1. **Wide Layout**: Optimized layout for better visualization.
2. **Custom Styling**: Aesthetic UI with CSS for enhanced user experience.
3. **Conversation Rendering**: Displays call transcripts in chat-bubble style.
4. **Dynamic Annotations**: Enables annotators to validate and annotate transcript sections dynamically.
5. **Sidebar Filtering**: Filters conversations by annotator and interaction ID.
6. **Data Persistence**: Saves annotations to JSON for future access.
7. **Error Handling**: Robust handling of invalid or missing data.

### Precision and Recall Calculation for JSON Comparison
1. **JSON Parsing and Comparison**:
   - Recursive comparison of JSON objects.
   - Precision and recall calculation for attributes and records.
2. **Comparison Methods**:
   - **Semantic Similarity**: Advanced text comparison using SentenceTransformer.
   - **Fuzzy Matching**: Partial ratio-based comparison using RapidFuzz.
   - **Exact Matching**: Case-insensitive exact matching.
3. **File Input Options**:
   - Upload Ground Truth (GT) and LLM JSON files.
   - Process CSV files with JSON columns for batch operations.
4. **Dynamic Attribute Method Selection**:
   - Allows selection of semantic, fuzzy, or exact matching for each attribute.
5. **Metrics Calculation**:
   - Attribute-level and record-level precision and recall.
   - Average metrics across multiple JSON pairs.
6. **Streamlit Interface**:
   - Sidebar for file uploads and method selection.
   - Metrics displayed in detailed and aggregated tables.
7. **Batch Processing**: Processes multiple JSON pairs and displays average metrics.

---

## Modules and Functionalities

### Call Transcript Annotation Tool
1. **Custom CSS Integration**:
   - Enhances aesthetics with custom themes and styles.
2. **Conversation Renderer**:
   - Displays agent and customer dialogues in structured chat bubbles.
3. **Annotation and Validation**:
   - Supports marking fields as correct, missing, or incorrect with optional remarks.
4. **Data Management**:
   - Save and load annotations to/from JSON files.
5. **Visualization Tabs**:
   - Separate tabs for annotating transcripts and viewing saved annotations.

### Precision and Recall Calculation for JSON Comparison
1. **JSON Parsing**:
   - Safely parses JSON strings into dictionaries.
   - Identifies null or empty values.
2. **Comparison Methods**:
   - Semantic, fuzzy, and exact matching for text values.
   - Recursive comparison of dictionaries and lists.
3. **Metrics Calculation**:
   - Computes precision and recall for attributes and records.
   - Aggregates metrics across multiple JSON pairs.
4. **Streamlit Interface**:
   - Interactive sidebar for file uploads and method selection.
   - Detailed tables for attribute-level and record-level metrics.
5. **Batch Processing**:
   - Processes multiple JSON pairs from CSV files.

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Required Python packages:
  - `streamlit`
  - `pandas`
  - `numpy`
  - `json`
  - `sentence-transformers`
  - `rapidfuzz`

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/nitishkmr005/call-transcript-annotator.git
   cd your-repo