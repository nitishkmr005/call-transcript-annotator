# Project Requirement Document: Call Transcript Annotation and Evaluation Tool

---

## Objective

Develop a **Streamlit-based web application** for annotating, managing, and evaluating financial call transcripts. The tool allows financial advisors to:
1. Annotate call transcripts with structured details.
2. Save annotations to a database for further processing.
3. Compare annotations with LLM-generated outputs and calculate precision, recall, and similarity metrics.

---

## Features

### 1. **Call Transcript Annotation**
- Annotate financial call transcripts using a structured, user-friendly form.
- Store details such as:
  - Call Information (e.g., Call ID, Date, Advisor, Duration).
  - Client Profile (e.g., Age, Risk Tolerance, Balance).
  - Retirement Goals (e.g., Desired Income, Location, Lifestyle).
  - Investment Allocation (e.g., Stocks, Bonds, Cash).
  - Interaction Summary (e.g., Topics Discussed, Recommendations, Action Items).
  - Follow-up Details (e.g., Date, Priority, Type).
  - Notes (e.g., Special Considerations, Compliance Notes).

### 2. **Annotation Management**
- **Save Annotations**:
  - Save annotations in **Parquet** format for efficient storage.
- **View and Export**:
  - Display submitted annotations in a tabular format.
  - Export annotations as **Parquet** or **CSV** files.

### 3. **LLM Annotation Evaluation**
- **Comparison with LLM Annotations**:
  - Load LLM-generated annotations for comparison.
  - Compare annotated and LLM data section-wise.
- **Metrics Calculation**:
  - Attribute-Level: Precision, Recall, and Similarity for individual fields.
  - Section-Level: Average Precision and Recall for each section.
  - Overall Metrics: Aggregated Precision and Recall across all sections.
- **Comparison Methods**:
  - **Semantic Similarity** (via Sentence Transformers).
  - **Fuzzy Matching** (via RapidFuzz).
  - **Date Comparison** with tolerances.

### 4. **Dark-Themed Modern UI**
- Styled using custom CSS for a modern and responsive appearance.
- Dynamic, interactive components for easy navigation and operation.

---

## Implementation Logic

### 1. **Data Management**
- **Loading and Saving Annotations**:
  - Load annotations from **Parquet** files.
  - Save new annotations by appending to the existing dataset.
- **Handling Call Transcripts**:
  - Load call transcripts from **CSV** files.

### 2. **Annotation Process**
- **Form Components**:
  - Dynamic forms with structured sections for annotation.
  - Prefilled fields (e.g., Call ID) for convenience.
- **Validation**:
  - Ensure valid input for key fields (e.g., Age, Balance, Goals).

### 3. **Comparison Logic**
- **Field-Level Matching**:
  - String Fields: Compare using semantic similarity or fuzzy matching.
  - Numeric Fields: Direct comparison with tolerance.
  - Lists: Order-independent comparison with similarity scoring.
  - Dictionaries: Nested comparison of key-value pairs.
- **Precision and Recall**:
  - **Precision**: Correct matches / Total LLM-predicted values.
  - **Recall**: Correct matches / Total annotated values.

### 4. **Metrics Calculation**
- **Attribute-Level**:
  - Compute precision, recall, and similarity for individual attributes.
- **Section-Level**:
  - Aggregate attribute-level metrics within each section.
- **Overall Metrics**:
  - Average section-level precision and recall across all sections.

---

## User Workflow

### **Annotation Process**
1. Load call transcripts from a CSV file.
2. Select a **Call ID** to annotate.
3. Fill out the annotation form with structured details.
4. Submit the annotation to save it to the database.

### **Annotation Management**
1. View all submitted annotations in a table.
2. Export annotations as **Parquet** or **CSV** files.

### **LLM Evaluation**
1. Load LLM-generated annotations for the selected **Call ID**.
2. Compare annotations with LLM outputs section-wise.
3. View metrics (precision, recall, similarity) for:
   - Individual fields.
   - Each section.
   - Overall performance.

---

## Key Components

### **Call Transcript Annotation**
- Form sections:
  - Call Info, Client Profile, Retirement Goals, Investment Allocation, Interaction Summary, Follow-up Details, Notes.
- Input fields:
  - Text boxes, number inputs, sliders, date pickers, multi-select, and dropdowns.

### **LLM Annotation Evaluation**
- Section-wise metrics:
  - Precision, Recall, and Similarity displayed in a styled DataFrame.
- Overall metrics:
  - Displayed as percentages with calculation steps.

---

## Technology Stack

| **Component**         | **Technology**                               |
|------------------------|-----------------------------------------------|
| **Frontend**           | Streamlit                                   |
| **Styling**            | Custom CSS                                  |
| **Semantic Similarity**| Sentence Transformers (`all-MiniLM-L6-v2`)  |
| **Fuzzy Matching**     | RapidFuzz                                   |
| **Backend**            | Python                                      |
| **Data Storage**       | Parquet, CSV                                |

---

## Test Scenarios

### **Annotation**
1. Save annotations to the database.
2. Validate required fields.
3. Ensure exported files match saved annotations.

### **LLM Evaluation**
1. Compare complete annotations with LLM data.
2. Handle missing or invalid sections in LLM data.
3. Calculate metrics for complex structures (e.g., nested dictionaries, lists).

### **UI Functionality**
1. Test responsiveness across devices.
2. Validate file upload functionality.

---

## Expected Outputs

### **Annotation**
- **Parquet/CSV File**:
  - Structured data for each call.
- **Annotation Table**:
  - View submitted annotations.

### **LLM Evaluation**
- **Section-Level Metrics**:
  - Precision, Recall, and Similarity for each section.
- **Overall Metrics**:
  - Aggregated Precision and Recall across all sections.

---

## Future Enhancements
1. Add multi-threading for faster processing of large datasets.
2. Introduce visualizations (e.g., bar charts for section-wise metrics).
3. Allow user-defined thresholds for similarity matching.
4. Extend support for additional data types (e.g., image annotations).