# Project Requirement Document: JSON Precision and Recall Comparator

---

## Objective

Develop a Streamlit-based application to compare JSON objects and calculate **precision** and **recall** metrics. The tool supports:
1. **Single JSON Pair Comparison**: Compare two individual JSON files.
2. **Batch Processing via CSV**: Process a CSV containing multiple JSON pairs (annotated and generated JSONs).

The application handles complex structures (lists, dictionaries) and provides semantic and fuzzy matching for string attributes.

---

## Features

### 1. **Comparison Methods**
- **Semantic Similarity**: Uses Sentence Transformers to compute similarity between text fields.
- **Fuzzy Matching**: Uses partial ratio-based matching for approximate string comparison.
- **Exact Match**: Compares attributes for equality.

### 2. **Precision and Recall Metrics**
- **Attribute-Level**:
  - Computes precision and recall for each attribute in a JSON pair.
- **Record-Level**:
  - Aggregates precision and recall across attributes for a single JSON pair.
- **Batch-Level**:
  - Averages record-level precision and recall across all JSON pairs in the batch.

### 3. **Streamlit UI**
- **File Upload Options**:
  - Compare two individual JSON files.
  - Process a CSV containing `annotated_json` and `llm_json` columns.
- **Comparison Method Selection**:
  - Users can choose comparison methods for each attribute (semantic, fuzzy, or exact).
- **Metrics Display**:
  - Attribute-level precision and recall for individual JSON pairs.
  - Record-level precision and recall for each JSON pair.
  - Average attribute-level metrics across all pairs in a batch.
  - Average record-level metrics across the batch.

### 4. **Data Structure Handling**
- **Text Fields**:
  - Semantic or fuzzy matching with user-defined thresholds.
- **Lists**:
  - Compares list items and calculates precision and recall based on the number of matched items.
- **Dictionaries**:
  - Supports recursive comparison of nested dictionaries.

---

## Implementation Logic

### 1. **Utility Functions**
- **`parse_json`**:
  - Safely parses JSON strings into Python dictionaries.
- **`is_null`**:
  - Identifies null or empty values in JSON attributes.
- **`compare_texts_semantic`**:
  - Computes semantic similarity between text fields using Sentence Transformers.
- **`compare_texts_fuzzy`**:
  - Compares text fields using fuzzy matching with partial ratio.

### 2. **Comparison Functions**
- **`compare_items_static`**:
  - Compares individual items using the selected method (semantic, fuzzy, or exact).
- **`compare_list_items`**:
  - Matches list items between ground truth and generated JSON, considering each item only once.
- **`compare_jsons`**:
  - Recursively compares JSON structures (dictionaries, lists) and computes precision and recall.

### 3. **Metric Calculation**
- **Attribute-Level Metrics**:
  - Precision = Correct matches / Total items in generated JSON attribute.
  - Recall = Correct matches / Total items in annotated JSON attribute.
- **Record-Level Metrics**:
  - Aggregates attribute-level metrics, considering only non-null precision and recall values.
- **Batch-Level Metrics**:
  - Averages record-level precision and recall across all JSON pairs in the batch.

### 4. **Streamlit UI Integration**
- **Single JSON Pair Processing**:
  - Upload two JSON files, select comparison methods for attributes, and display metrics.
- **Batch Processing via CSV**:
  - Process multiple JSON pairs in a CSV file and display average metrics.

---

## User Workflow

### **Single JSON Pair Comparison**
1. Upload two JSON files (annotated and generated).
2. Select comparison methods for attributes.
3. Click "Compare JSON Files" to calculate metrics.
4. View:
   - Attribute-level precision and recall.
   - Record-level precision and recall.

### **Batch Processing via CSV**
1. Upload a CSV file with columns `annotated_json` and `llm_json`.
2. Application processes each JSON pair in the CSV.
3. View:
   - Average attribute-level metrics across all pairs.
   - Average record-level precision and recall across all pairs.

---

## Data Type Matching Approaches

| **Data Type**       | **Matching Method**                          |
|----------------------|----------------------------------------------|
| **Text Fields**      | Semantic similarity or fuzzy matching.       |
| **Lists**            | Matches list items one-to-one.               |
| **Dictionaries**     | Recursively compares key-value pairs.        |
| **Nested Structures**| Handles multi-level lists and dictionaries.  |

---

## Test Scenarios

### **Single JSON Pair**
1. JSON files with matching attributes and values.
2. JSON files with mismatched attributes or values.
3. JSON files containing null values.

### **Batch Processing**
1. CSV file with valid JSON pairs.
2. CSV file with invalid JSON entries.
3. Large CSV file with multiple JSON pairs.

### **Complex Structures**
1. Nested dictionaries with varying levels of depth.
2. Lists containing dictionaries or complex objects.

---

## Expected Outputs

### **Single JSON Pair**
1. Attribute-Level Metrics (Table):
   - Precision and recall for each attribute.
2. Record-Level Metrics (Text):
   - Precision and recall for the JSON pair.

### **Batch Processing**
1. Average Attribute-Level Metrics (Table):
   - Precision and recall averaged across all JSON pairs for each attribute.
2. Average Record-Level Metrics (Text):
   - Precision and recall averaged across all JSON pairs.

---

## Notes

1. **Null Handling**:
   - Both values null → No contribution to precision/recall.
   - Annotated value null, generated value present → Precision: None, Recall: 0.
2. **Error Handling**:
   - Invalid JSON strings are skipped with a warning.
   - Empty or malformed CSV files are flagged with errors.
3. **Thresholds**:
   - Semantic similarity threshold: 0.8.
   - Fuzzy matching threshold: 80%.

---

## Future Enhancements

1. Support for additional comparison methods (e.g., numeric tolerances).
2. Visualization improvements (e.g., bar charts for metrics).
3. Enhanced performance for large datasets with multi-threading or batch processing.

---

## Technology Stack

| **Component**        | **Technology**                                |
|-----------------------|-----------------------------------------------|
| **Frontend**          | Streamlit                                    |
| **Semantic Matching** | Sentence Transformers (`all-MiniLM-L6-v2`)   |
| **Fuzzy Matching**    | RapidFuzz                                    |
| **Backend**           | Python                                       |
| **Data Processing**   | Pandas                                       |

---

## File Requirements

1. **Two JSON Files**:
   - Individual JSON files for annotated and generated data.
2. **CSV File**:
   - Contains columns `annotated_json` and `llm_json` with valid JSON strings.

---

## Summary

The **JSON Precision and Recall Comparator** is a robust application for evaluating the accuracy of JSON objects generated by LLMs. Its flexible design supports both single-pair and batch processing, with advanced comparison methods and an intuitive UI.