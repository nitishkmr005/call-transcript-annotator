# Call Transcript Annotation Tool

A modern Streamlit application for annotating financial advisory call transcripts with detailed metadata, LLM comparison, and analysis capabilities.

## 🌟 Key Features

### 💬 Call Transcript Display
* Real-time transcript visualization with:
  * Color-coded messages (Agent: Light blue, Customer: Light gray)
  * Timestamp tracking for each message
  * Professional message formatting with consistent black text
  * Split-screen interface for efficient annotation

### 📝 Call Annotation System
* Comprehensive form with expandable sections:
  * 📞 Basic Call Information
    - Call ID, Advisor Name, Duration
    - Date, Client ID, Call Type
  * 👤 Client Profile
    - Age, Risk Tolerance
    - Current 401k Balance
    - Years to Retirement
  * 🎯 Retirement Goals
    - Multiple goal selection
    - Monthly income targets
    - Location preferences
    - Lifestyle expectations
  * 💰 Investment Allocation
    - Percentage and amount tracking
    - Multiple investment types (Stocks, Bonds, Cash, etc.)
    - Real-time portfolio breakdown
  * 📋 Interaction Summary
    - Key topics discussed
    - Advisor recommendations
    - Action items tracking
  * 📅 Follow-up Management
    - Required/Not required
    - Priority levels
    - Follow-up type and date
  * 📌 Additional Notes
    - Special considerations
    - Compliance documentation

### 🤖 LLM Evaluation System
* Side-by-side comparison of:
  * Human annotations
  * LLM-generated annotations
  * Detailed metrics analysis
* Performance Metrics:
  * Precision and recall calculations
  * Section-wise comparison
  * Overall performance metrics
* Visual indicators for matches/mismatches

### 💾 Data Management
* Persistent Storage:
  * Parquet file integration
  * Automatic saving of annotations
  * Data loading capabilities
* Export Options:
  * Download as Parquet
  * Download as CSV
* Real-time data visualization

### 🔍 Evaluation Strategy

#### Comparison Framework
* Side-by-side Analysis:
  * Human annotations (left panel)
  * LLM-generated annotations (middle panel)
  * Metrics visualization (right panel)

#### Metric Calculations
* Field-level Comparison:
  * **Text Fields**
    - Direct string matching
    - Binary scoring (1.0 for match, 0.0 for mismatch)
    - Visual indicators: ✅ for match, ❌ for mismatch
  
  * **List Fields** (e.g., Goals, Topics)
    - Set-based comparison
    - Precision = |Common Items| / |LLM Items|
    - Recall = |Common Items| / |Human Items|
    - Visual indicators: 
      * ✅ Perfect match (precision = recall = 1.0)
      * ⚠️ Partial match
      * ❌ No match

  * **Numeric Fields**
    - Exact value matching
    - Future enhancement: tolerance-based matching

#### Performance Metrics
* Section-wise Analysis:
  * Individual metrics for each annotation field
  * Aggregated scores per section
  * Expandable detailed view

* Overall Performance:
  * Average Precision across all fields
  * Average Recall across all fields
  * Summary statistics dashboard

#### Visual Feedback
* Color-coded Indicators:
  * Green (✅): Perfect match
  * Yellow (⚠️): Partial match
  * Red (❌): No match
  * Gray (❓): Unable to compare

#### Use Cases
* Quality Assessment:
  * Evaluate LLM annotation accuracy
  * Identify systematic differences
  * Track performance trends

* Training Feedback:
  * Highlight areas for LLM improvement
  * Identify pattern recognition gaps
  * Guide model fine-tuning

#### Future Enhancements
* Semantic Similarity:
  * Text embedding comparison
  * Fuzzy matching for near-matches
  * Context-aware evaluation

* Advanced Metrics:
  * F1 score calculation
  * Weighted scoring system
  * Custom metric definitions

* Visualization:
  * Trend analysis over time
  * Performance heat maps
  * Interactive metric exploration

## 🚀 Installation & Setup

1. Clone the repository:
