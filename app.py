# pip3 install virtualenv
# python3 -m venv st 
# source st/bin/activate

# alias python=python3.10  # as env has multiple python versions 3.10 and 3.13
# alias pip=pip3.10

# python3.10 -m pip install torch
# python3.10 -m pip install sentence_transformers
# python3.10 -m pip install streamlit

import streamlit as st
import pandas as pd
import os
from pathlib import Path
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util
import json
import numpy as np

# Custom CSS for better styling
def local_css():
    st.markdown("""
        <style>
        /* Modern Theme Variables */
        :root {
            /* Base colors */
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            
            /* Accent colors */
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-teal: #14b8a6;
            --accent-pink: #ec4899;
            
            /* Gradients */
            --gradient-blue: linear-gradient(135deg, #3b82f6 0%, #2dd4bf 100%);
            --gradient-purple: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
            
            /* Shadows */
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        /* Global Styles */
        .stApp {
            background: var(--bg-primary);
        }

        /* Headers */
        .main-header {
            background: var(--gradient-blue);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            margin-bottom: 2rem !important;
            text-align: center;
        }

        .section-header {
            color: var(--text-primary) !important;
            font-size: 1.8rem !important;
            font-weight: 600 !important;
            margin-bottom: 1.5rem !important;
        }

        /* Message Containers */
        .message-container {
            margin: 15px 0;
            padding: 20px 25px;
            border-radius: 16px;
            box-shadow: var(--shadow-md);
            font-size: 1rem;
            line-height: 1.6;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            max-width: 92%;
        }

        .agent-message {
            background: linear-gradient(145deg, rgba(59, 130, 246, 0.15), rgba(45, 212, 191, 0.1));
            border-left: 4px solid var(--accent-blue);
            margin-right: 8%;
        }

        .customer-message {
            background: linear-gradient(145deg, rgba(139, 92, 246, 0.15), rgba(236, 72, 153, 0.1));
            border-left: 4px solid var(--accent-purple);
            margin-left: 8%;
        }

        .message-container:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
        }

        /* Form Styling */
        .stForm {
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 16px;
            box-shadow: var(--shadow-lg);
        }

        /* Input Fields */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stNumberInput>div>div>input {
            background: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-size: 1rem !important;
            transition: all 0.2s ease;
        }

        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {
            border-color: var(--accent-blue) !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        }

        /* Select Boxes */
        .stSelectbox>div>div>div {
            background: var(--bg-primary) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
        }

        /* Sliders */
        .stSlider>div>div>div {
            background: var(--gradient-blue) !important;
        }

        .stSlider>div>div>div>div {
            background: white !important;
            border: 2px solid var(--accent-blue) !important;
        }

        /* Buttons */
        .stButton>button {
            background: var(--gradient-blue) !important;
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: var(--shadow-sm) !important;
        }

        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-md) !important;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--bg-secondary) !important;
            border-radius: 12px !important;
            padding: 8px !important;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            color: var(--text-secondary) !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: var(--gradient-blue) !important;
            color: white !important;
        }

        /* Dividers */
        hr {
            border-color: rgba(255, 255, 255, 0.1) !important;
            margin: 2rem 0 !important;
        }

        /* Success/Info Messages */
        .stSuccess, .stInfo {
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* DataFrames */
        .dataframe {
            background: var(--bg-secondary) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* Checkbox */
        .stCheckbox {
            color: var(--text-secondary) !important;
        }

        .stCheckbox>div>div>div>div {
            border-color: rgba(255, 255, 255, 0.2) !important;
        }

        /* LLM Evaluation Styles */
        .subsection-header {
            color: var(--text-primary) !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
            padding-bottom: 0.5rem !important;
            border-bottom: 1px solid var(--border-color);
        }
        
        /* Metric cards */
        .metric-card {
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 1px solid var(--border-color);
        }
        
        /* Comparison indicators */
        .match-indicator {
            font-size: 1.2rem;
            margin-left: 0.5rem;
        }
        
        /* Metrics expander styling */
        .metrics-expander {
            background: linear-gradient(145deg, var(--bg-secondary), var(--bg-primary));
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin: 0.5rem 0
        </style>
    """, unsafe_allow_html=True)

def load_annotations_from_parquet():
    """Load annotations from parquet file if it exists, otherwise return empty list"""
    file_path = Path("annotations.parquet")
    if file_path.exists():
        return pd.read_parquet(file_path).to_dict('records')
    return []

def save_annotations_to_parquet(annotations):
    """Save annotations to parquet file, appending to existing data"""
    file_path = Path("annotations.parquet")
    new_df = pd.DataFrame(annotations)
    
    if file_path.exists():
        existing_df = pd.read_parquet(file_path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    
    combined_df.to_parquet(file_path, index=False)

def load_dummy_annotation_data():
    """Load dummy LLM annotations for testing - matching human annotation structure"""
    dummy_data = {
        "Call Info": {
            "Call ID": "CALL_001",
            "Advisor": "John Smith",
            "Date": "2024-03-20",
            "Duration": "30 minutes",
            "Type": "Retirement Planning",
            "Client ID": "C12345"
        },
        "Client Profile": {
            "Age": 45,
            "Risk Tolerance": "Moderate",
            "Current Balance": 250000,
            "Years to Retirement": 20
        },
        "Retirement Goals": {
            "Goals List": ["Travel Plans", "Healthcare Coverage", "Legacy Planning"],
            "Monthly Income Target": 5000,
            "Location": "Different State",
            "Lifestyle": "Comfortable"
        },
        "Investment Allocation": {
            "Stocks": {"percentage": 60, "amount": 150000},
            "Bonds": {"percentage": 30, "amount": 75000},
            "Cash": {"percentage": 10, "amount": 25000},
            "Real Estate": {"percentage": 0, "amount": 0},
            "Other": {"percentage": 0, "amount": 0}
        },
        "Interaction Summary": {
            "Topics": ['Investment Options' 'Rebalancing Strategy'],
            "Recommendations": "Increase contribution rate to maximize employer match",
            "Action Items": ["Increase Contributions", "Review Investment Mix"]
        },
        "Follow-up": {
            "Required": True,
            "Date": "2024-04-20",
            "Priority": "High",
            "Type": "Portfolio Review"
        },
        "Notes": {
            "Special Considerations": "Client interested in ESG investments",
            "Compliance Notes": "All disclosures provided"
        }
    }
    return dummy_data

def load_dummy_llm_data():
    """Load dummy LLM annotations for testing - matching human annotation structure"""
    dummy_data = {
        "Call Info": {
            "Call ID": "CALL_001",
            "Advisor": "John Smith",
            "Date": "2024-03-20",
            "Duration": "30 minutes",
            "Type": "Retirement Planning",
            "Client ID": "C12345"
        },
        "Client Profile": {
            "Age": 45,
            "Risk Tolerance": "Moderate",
            "Current Balance": 250000,
            "Years to Retirement": 20
        },
        "Retirement Goals": {
            "Goals List": ["Travel Plans", "Healthcare Coverage", "Legacy Planning"],
            "Monthly Income Target": 5000,
            "Location": "Different State",
            "Lifestyle": "Comfortable"
        },
        "Investment Allocation": {
            "Stocks": {"percentage": 60, "amount": 150000},
            "Bonds": {"percentage": 30, "amount": 75000},
            "Cash": {"percentage": 10, "amount": 25000},
            "Real Estate": {"percentage": 0, "amount": 0},
            "Other": {"percentage": 0, "amount": 0}
        },
        "Interaction Summary": {
            "Topics": ["Contribution Rates", "Investment Options", "Risk Management"],
            "Recommendations": "Increase contribution rate to maximize employer match",
            "Action Items": ["Increase Contributions", "Review Investment Mix"]
        },
        "Follow-up": {
            "Required": True,
            "Date": "2024-04-20",
            "Priority": "High",
            "Type": "Portfolio Review"
        },
        "Notes": {
            "Special Considerations": "Client interested in ESG investments",
            "Compliance Notes": "All disclosures provided"
        }
    }
    return dummy_data

def safely_convert_to_string(value):
    """
    Safely converts a value to a string, handling None and complex types.

    Args:
        value: The value to convert.

    Returns:
        A string representation of the value, or an empty string if value is None.
    """
    if value is None:
        return ''
    try:
        return str(value)
    except:
        return repr(value)

def calculate_semantic_similarity(text1, text2, threshold=0.7):
    """Calculates semantic similarity, ensuring 1.0 for identical strings."""
    text1 = safely_convert_to_string(text1)
    text2 = safely_convert_to_string(text2)

    if not text1.strip() and not text2.strip():
        return 0

    if text1.strip() == text2.strip():  # Explicit check for identical strings
        return 1.0

    try:
        embeddings = model.encode([text1, text2], convert_to_tensor=True)
        cosine_sim = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
        return cosine_sim
    except Exception as e:
        print(f"Semantic similarity calculation error: {e}")
        return 0

def calculate_fuzzy_similarity(str1, str2):
    """
    Calculates the fuzzy partial ratio similarity between two strings.

    Args:
        str1: The first string.
        str2: The second string.

    Returns:
        The fuzzy similarity score (0-1).
    """
    if not str1 or not str2:  # Handle empty strings
        return 0
    return fuzz.partial_ratio(str1, str2) / 100

def calculate_comparison_metrics(human_value, llm_value, threshold=0.7):
    """Calculates comparison metrics based on data types."""
    if human_value is None and llm_value is None:
        return {"match": "N/A", "similarity": "0%", "precision": 0, "recall": 0, "comparison_method": "N/A", "is_populated": False}
    if human_value is None or llm_value is None:
        return {"match": "✗", "similarity": "0%", "precision": 0, "recall": 0, "comparison_method": "N/A", "is_populated": False}

    if isinstance(human_value, list) and isinstance(llm_value, list):
        if all(isinstance(item, dict) for item in human_value) and all(isinstance(item, dict) for item in llm_value):
            return compare_list_of_dictionaries(human_value, llm_value, threshold) # Call for list of dictionaries
        elif all(isinstance(item, str) for item in human_value) and all(isinstance(item, str) for item in llm_value):
            return compare_lists(human_value, llm_value, threshold) # Call for list of strings
        else:
            human_str = safely_convert_to_string(human_value)
            llm_str = safely_convert_to_string(llm_value)
            similarity = calculate_fuzzy_similarity(human_str, llm_str)
            match = similarity >= threshold
            return {"match": "✓" if match else "✗", "similarity": f"{similarity * 100:.2f}%", "precision": similarity, "recall": similarity, "comparison_method": "Fuzzy Matching", "is_populated": True}

    if isinstance(human_value, dict) and isinstance(llm_value, dict):
        return compare_dictionaries_values(human_value, llm_value, threshold)

    if isinstance(human_value, str) and isinstance(llm_value, str):
        similarity = calculate_semantic_similarity(human_value, llm_value, threshold)
        match = similarity >= threshold
        return {"match": "✓" if match else "✗", "similarity": f"{similarity * 100:.2f}%", "precision": similarity, "recall": similarity, "comparison_method": "Semantic Similarity", "is_populated": True}
    
    # Default to fuzzy matching for all other types
    human_str = safely_convert_to_string(human_value)
    llm_str = safely_convert_to_string(llm_value)
    similarity = calculate_fuzzy_similarity(human_str, llm_str)
    match = similarity >= threshold
    return {"match": "✓" if match else "✗", "similarity": f"{similarity * 100:.2f}%", "precision": similarity, "recall": similarity, "comparison_method": "Fuzzy Matching", "is_populated": True}

def compare_lists(human_value, llm_value, threshold=0.7):
    """Compares lists using semantic/fuzzy similarity and calculates precision/recall correctly."""

    print('compare_lists')
    human_value = [safely_convert_to_string(x) for x in human_value]
    llm_value = [safely_convert_to_string(x) for x in llm_value]

    populated_human_count = sum(1 for item in human_value if item.strip())
    populated_llm_count = sum(1 for item in llm_value if item.strip())

    if not populated_human_count:
        return {"match": "✗", "similarity": "0%", "precision": 0, "recall": 0, "comparison_method": "List Comparison", "is_populated": True}

    true_positives = 0
    matched_llm_indices = set()

    for human_item in human_value:
        if not human_item.strip():
            continue

        best_match = 0
        best_match_index = -1

        for j, llm_item in enumerate(llm_value):
            if not llm_item.strip() or j in matched_llm_indices:
                continue

            if isinstance(human_item, str) and isinstance(llm_item, str):
                similarity = calculate_semantic_similarity(human_item, llm_item)
                print('SIMILARITY',similarity)
            else:
                similarity = calculate_fuzzy_similarity(human_item, llm_item)
                print('FUZZY',similarity)

            if similarity > best_match:
                best_match = similarity
                best_match_index = j

        if best_match >= threshold:
            true_positives += 1
            if best_match_index != -1: #check if there is a valid index to add
                matched_llm_indices.add(best_match_index)

    precision = true_positives / populated_llm_count if populated_llm_count > 0 else 0
    recall = true_positives / populated_human_count if populated_human_count > 0 else 0
    avg_similarity = (precision + recall) / 2 if (precision + recall) > 0 else 0
    match = avg_similarity >= threshold
    return {
        "match": "✓" if match else "✗",
        "similarity": f"{avg_similarity * 100:.2f}%",
        "precision": precision,
        "recall": recall,
        "comparison_method": "List Comparison",
        "is_populated": True
    }

def compare_list_of_dictionaries(human_value, llm_value, threshold=0.7):
    """Compares lists of dictionaries and calculates precision/recall as requested."""

    populated_human_count = len(human_value)
    populated_llm_count = len(llm_value)

    if not populated_human_count:
        return {"match": "✗", "similarity": "0%", "precision": 0, "recall": 0, "comparison_method": "List of Dictionaries Comparison", "is_populated": True}

    true_positives = 0
    similarities = []

    for human_dict in human_value:
        best_match_similarity = 0
        for llm_dict in llm_value:
            current_similarity = 0
            compared_items = 0
            for human_key, human_item in human_dict.items():
                if human_key in llm_dict:
                    llm_item = llm_dict[human_key]
                    if isinstance(human_item, str) and isinstance(llm_item, str):
                        similarity = calculate_semantic_similarity(human_item, llm_item)
                    else:
                        human_str = safely_convert_to_string(human_item)
                        llm_str = safely_convert_to_string(llm_item)
                        similarity = calculate_fuzzy_similarity(human_str, llm_str)
                    current_similarity += similarity
                    compared_items += 1
            if compared_items > 0:
                current_similarity /= compared_items
                best_match_similarity = max(best_match_similarity, current_similarity)
        if best_match_similarity >= threshold:
            true_positives += 1
            similarities.append(best_match_similarity)

    precision = true_positives / populated_llm_count if populated_llm_count > 0 else 0
    recall = true_positives / populated_human_count if populated_human_count > 0 else 0
    avg_similarity = np.mean(similarities) if similarities else 0
    match = avg_similarity >= threshold
    return {
        "match": "✓" if match else "✗",
        "similarity": f"{avg_similarity * 100:.2f}%",
        "precision": precision,
        "recall": recall,
        "comparison_method": "List of Dictionaries Comparison",
        "is_populated": True
    }

def compare_dictionaries_values(human_data, llm_data, threshold=0.7):
    """Compares dictionary values using fuzzy matching and returns overall similarity."""
    similarities = []
    for key, human_val in human_data.items():
        if key in llm_data:
            llm_val = llm_data[key]
            human_str = safely_convert_to_string(human_val)
            llm_str = safely_convert_to_string(llm_val)
            similarity = calculate_fuzzy_similarity(human_str, llm_str)
            similarities.append(similarity)
    if similarities:
        avg_similarity = np.mean(similarities)
        match = avg_similarity >= threshold
        return {"match": "✓" if match else "✗", "similarity": f"{avg_similarity * 100:.2f}%", "precision": avg_similarity, "recall": avg_similarity, "comparison_method": "Dictionary Comparison", "is_populated": True}
    else:
        return {"match": "✗", "similarity": "0%", "precision": 0, "recall": 0, "comparison_method": "Dictionary Comparison", "is_populated": True}

def compare_dictionaries(human_data, llm_data, threshold=0.7):
    """
    Compares two dictionaries, using appropriate comparison methods based on data type.

    Args:
        human_data: The human-annotated dictionary.
        llm_data: The LLM-generated dictionary.
        threshold: The similarity threshold for string comparisons.

    Returns:
        A Pandas DataFrame containing comparison metrics for each key, 
        or an empty DataFrame if input is invalid or no comparable data is found.
    """
    metrics_data = []
    overall_precision = 0
    overall_recall = 0
    populated_llm_count = 0
    populated_human_count = 0

    if not isinstance(human_data, dict) or not isinstance(llm_data, dict):
        return pd.DataFrame()  # Return empty DataFrame for invalid input

    for key in human_data.keys():
        human_value = human_data.get(key)
        llm_value = llm_data.get(key)
        try:
            comparison_method = "Fuzzy Matching"  # Default is now fuzzy matching
            if isinstance(human_value, str) and isinstance(llm_value, str):
                metrics = calculate_comparison_metrics(human_value, llm_value, threshold)
                comparison_method = metrics["comparison_method"] # Overide if it is string
            elif isinstance(human_value, list) and isinstance(llm_value, list):
                metrics = calculate_comparison_metrics(human_value, llm_value, threshold)
                comparison_method = "List Comparison"
            elif isinstance(human_value, dict) and isinstance(llm_value, dict):
                inner_metrics_df = compare_dictionaries(human_value, llm_value, threshold)
                if not inner_metrics_df.empty:
                    avg_precision = inner_metrics_df['Precision'].mean()
                    avg_recall = inner_metrics_df['Recall'].mean()
                    avg_similarity = (avg_precision + avg_recall) / 2 if not np.isnan(avg_precision) and not np.isnan(avg_recall) else np.nan #calculate average similarity
                    if not np.isnan(avg_similarity):
                        match = avg_similarity >= threshold
                        metrics = {
                            "match": "✓" if match else "✗",
                            "similarity": f"{avg_similarity * 100:.2f}%",
                            "precision": avg_precision,
                            "recall": avg_recall,
                            "comparison_method": "Dictionary Comparison",
                            "is_populated": True
                        }
                    else:
                        metrics = {
                            "match": "N/A",
                            "similarity": "N/A",
                            "precision": avg_precision,
                            "recall": avg_recall,
                            "comparison_method": "Dictionary Comparison",
                            "is_populated": True
                        }
                else:
                    continue
            else:  # All other types now use fuzzy matching
                metrics = calculate_comparison_metrics(human_value, llm_value, threshold)
                comparison_method = metrics["comparison_method"]

            metrics_data.append({
                "Key": key,
                "Human Value": safely_convert_to_string(human_value),
                "LLM Value": safely_convert_to_string(llm_value),
                "Match": metrics['match'],
                "Similarity": metrics['similarity'],
                "Precision": metrics['precision'],
                "Recall": metrics['recall'],
                "Comparison Method": comparison_method
            })

            if metrics["is_populated"]:
                if llm_value is not None:
                    populated_llm_count += 1
                    overall_precision += metrics["precision"]

                if human_value is not None:
                    populated_human_count += 1
                    overall_recall += metrics["recall"]

        except Exception as e:
            print(f"Error processing key {key}: {e}")
            continue

    metrics_df = pd.DataFrame(metrics_data)
    if populated_llm_count > 0:
        avg_precision = overall_precision / populated_llm_count
    else:
        avg_precision = np.nan

    if populated_human_count > 0:
        avg_recall = overall_recall / populated_human_count
    else:
        avg_recall = np.nan

    # print(f"Average Precision (populated LLM attributes): {avg_precision:.2%}")
    # print(f"Average Recall (populated human attributes): {avg_recall:.2%}")
    # print(f"Total LLM populated attributes: {populated_llm_count}")
    # print(f"Total human annotation populated attributes: {populated_human_count}")

    return metrics_df


def load_transcripts_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        # Ensure 'Call ID' is a string for consistent handling
        df['Call ID'] = df['Call ID'].astype(str)
        return df
    except FileNotFoundError:
        st.error(f"CSV file not found at: {csv_path}")
        return pd.DataFrame() # Return empty DataFrame to prevent errors
    except pd.errors.EmptyDataError:
        st.error(f"CSV file is empty: {csv_path}")
        return pd.DataFrame()
    except pd.errors.ParserError:
        st.error(f"Error parsing CSV file: {csv_path}. Check the format.")
        return pd.DataFrame()

def main():
    st.set_page_config(layout="wide", page_title="Call Transcript Annotation", page_icon="📞")
    local_css()
    global model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    if 'annotations' not in st.session_state:
        st.session_state.annotations = load_annotations_from_parquet()

    csv_path = "transcripts.csv"  # Path to your CSV file
    transcripts_df = load_transcripts_from_csv(csv_path)

    if transcripts_df.empty:
        st.stop() # Stop execution if there's an error with CSV loading

    st.markdown('<h1 class="main-header">📞 Call Transcript Annotation Tool</h1>', unsafe_allow_html=True)

    call_ids = transcripts_df['Call ID'].unique().tolist()
    selected_call_id = st.selectbox("Select Call ID", call_ids)

    selected_transcript = transcripts_df[transcripts_df['Call ID'] == selected_call_id]
    transcript = selected_transcript.to_dict('records')

    tabs = st.tabs(["📝 Transcript & Annotation", "📊 View Annotations", "🤖 LLM Evaluation"])

    with tabs[0]:  # Transcript & Annotation
        col1, col2 = st.columns([0.6, 0.4])

        with col1:
            st.markdown('<h3 class="section-header">Call Transcript</h3>', unsafe_allow_html=True)
            for entry in transcript:
                if entry["speaker"] == "Agent":
                    st.markdown(
                        f'<div class="message-container agent-message">'
                        f'<b>{entry["speaker"]}</b> <small>({entry["time"]})</small><br>'
                        f'{entry["text"]}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="message-container customer-message">'
                        f'<b>{entry["speaker"]}</b> <small>({entry["time"]})</small><br>'
                        f'{entry["text"]}</div>',
                        unsafe_allow_html=True
                    )

        with col2: #Annotation Form
            st.markdown('<h3 class="section-header">Call Annotation</h3>', unsafe_allow_html=True)
            # Prefill Call ID in the form
            with st.form("annotation_form", clear_on_submit=True):
                with st.expander("📞 Basic Call Information", expanded=True):
                    call_id = st.text_input("Call ID", value=selected_call_id, disabled=True) #Prefilled
                    col3, col4 = st.columns(2)
                    with col3:
                        call_id = st.text_input("Call ID")
                        agent_name = st.text_input("Financial Advisor Name")
                        call_duration = st.text_input("Call Duration")
                    with col4:
                        call_date = st.date_input("Call Date")
                        customer_id = st.text_input("Client ID")
                        call_type = st.selectbox("Call Type", 
                            ["Initial Consultation", "Portfolio Review", "Retirement Planning", "Investment Adjustment", "General Inquiry"])

                # Client Profile
                with st.expander("👤 Client Profile", expanded=True):
                    col5, col6 = st.columns(2)
                    with col5:
                        age = st.number_input("Client Age", min_value=18, max_value=100)
                        risk_tolerance = st.select_slider("Risk Tolerance", 
                            options=["Very Conservative", "Conservative", "Moderate", "Aggressive", "Very Aggressive"])
                    with col6:
                        current_401k_balance = st.number_input("Current 401k Balance ($)")
                        years_to_retirement = st.number_input("Years to Retirement", min_value=0, max_value=50)

                # Retirement Goals
                with st.expander("🎯 Retirement Goals", expanded=True):
                    retirement_goals = st.multiselect("Selected Retirement Goals",
                        ["Early Retirement", "Travel Plans", "Healthcare Coverage", 
                         "Legacy Planning", "Debt-Free Retirement", "Part-time Work",
                         "Relocate/Downsize", "Start Business", "Education Funding",
                         "Charitable Giving"])
                    
                    monthly_retirement_income = st.number_input("Desired Monthly Retirement Income ($)")
                    
                    col7, col8 = st.columns(2)
                    with col7:
                        retirement_location = st.selectbox("Planned Retirement Location",
                            ["Current Location", "Different State", "International", "Undecided"])
                    with col8:
                        lifestyle_expectation = st.select_slider("Lifestyle Expectation",
                            options=["Basic", "Comfortable", "Luxurious"])

                # Investment Breakdown
                with st.expander("💰 Investment Allocation", expanded=True):
                    st.markdown("##### Current Portfolio Allocation")
                    
                    investment_types = ["Stocks", "Bonds", "Cash", "Real Estate", "Other"]
                    investment_data = {}
                    
                    for i in range(0, len(investment_types), 2):
                        col9, col10 = st.columns(2)
                        with col9:
                            if i < len(investment_types):
                                investment_data[investment_types[i]] = {
                                    "percentage": st.slider(f"{investment_types[i]} (%)", 0, 100, 0),
                                    "amount": st.number_input(f"{investment_types[i]} Amount ($)", min_value=0.0)
                                }
                        with col10:
                            if i + 1 < len(investment_types):
                                investment_data[investment_types[i + 1]] = {
                                    "percentage": st.slider(f"{investment_types[i + 1]} (%)", 0, 100, 0),
                                    "amount": st.number_input(f"{investment_types[i + 1]} Amount ($)", min_value=0.0)
                                }

                # Interaction Summary
                with st.expander("📝 Interaction Summary", expanded=True):
                    key_topics_discussed = st.multiselect("Key Topics Discussed",
                        ["Contribution Rates", "Investment Options", "Risk Management",
                         "Tax Implications", "Employer Match", "Fund Selection",
                         "Rebalancing Strategy", "Distribution Planning", "Rollover Options",
                         "Social Security Integration"])
                    
                    recommendations = st.text_area("Advisor Recommendations")
                    
                    action_items = st.multiselect("Action Items",
                        ["Increase Contributions", "Rebalance Portfolio", "Update Beneficiaries",
                         "Review Investment Mix", "Schedule Follow-up", "Document Updates",
                         "Risk Assessment", "Create Financial Plan"])

                # Follow-up Details
                with st.expander("📅 Follow-up Details", expanded=True):
                    col11, col12 = st.columns(2)
                    with col11:
                        follow_up_needed = st.checkbox("Follow-up Required")
                        follow_up_date = st.date_input("Follow-up Date") if follow_up_needed else None
                    with col12:
                        priority_level = st.select_slider("Priority Level",
                            options=["Low", "Medium", "High"])
                        follow_up_type = st.selectbox("Follow-up Type",
                            ["Portfolio Review", "Document Collection", "Plan Update",
                             "Investment Changes", "General Check-in"]) if follow_up_needed else None

                # Additional Notes
                with st.expander("📌 Additional Notes", expanded=True):
                    special_considerations = st.text_area("Special Considerations")
                    compliance_notes = st.text_area("Compliance Notes")
                    
                submit_button = st.form_submit_button("Submit Annotation")
                
                if submit_button:
                    attributes = {
                        "Call Info": {
                            "Call ID": call_id,
                            "Advisor": agent_name,
                            "Date": call_date,
                            "Duration": call_duration,
                            "Type": call_type,
                            "Client ID": customer_id
                        },
                        "Client Profile": {
                            "Age": age,
                            "Risk Tolerance": risk_tolerance,
                            "Current Balance": current_401k_balance,
                            "Years to Retirement": years_to_retirement
                        },
                        "Retirement Goals": {
                            "Goals List": retirement_goals,
                            "Monthly Income Target": monthly_retirement_income,
                            "Location": retirement_location,
                            "Lifestyle": lifestyle_expectation
                        },
                        "Investment Allocation": investment_data,
                        "Interaction Summary": {
                            "Topics": key_topics_discussed,
                            "Recommendations": recommendations,
                            "Action Items": action_items
                        },
                        "Follow-up": {
                            "Required": follow_up_needed,
                            "Date": follow_up_date,
                            "Priority": priority_level,
                            "Type": follow_up_type
                        },
                        "Notes": {
                            "Special Considerations": special_considerations,
                            "Compliance Notes": compliance_notes
                        }
                    }
                    st.session_state.annotations.append(attributes)
                    
                    # Save to parquet file
                    try:
                        save_annotations_to_parquet([attributes])
                        st.success("✅ 401k Planning Call Annotation Submitted Successfully and Saved to Database!")
                    except Exception as e:
                        st.error(f"Error saving annotation: {str(e)}")

    with tabs[1]:
        st.markdown('<h3 class="section-header">Submitted Annotations</h3>', unsafe_allow_html=True)
        if st.session_state.annotations:
            df = pd.DataFrame(st.session_state.annotations)
            
            # Add download buttons
            col1, col2 = st.columns(2)
            with col1:
                # Download as Parquet
                if st.button("📥 Download as Parquet"):
                    temp_file = "temp_annotations.parquet"
                    df.to_parquet(temp_file, index=False)
                    with open(temp_file, 'rb') as f:
                        st.download_button(
                            "Click to Download",
                            f,
                            file_name="annotations.parquet",
                            mime="application/octet-stream"
                        )
                    os.remove(temp_file)
            
            with col2:
                # Download as CSV
                if st.button("📥 Download as CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Click to Download",
                        csv,
                        file_name="annotations.csv",
                        mime="text/csv"
                    )
            
            # Display the dataframe
            st.dataframe(df, use_container_width=True)
        else:
            st.info("📝 No annotations submitted yet.")

    with tabs[2]:  # LLM Evaluation (Modified for Dark Theme)
        st.markdown('<h3 class="section-header">LLM Evaluation Comparison</h3>', unsafe_allow_html=True)

        if st.session_state.annotations:
            human_annotation = st.session_state.annotations[-1]
            llm_annotation = load_dummy_llm_data()

            comparison_data = []
            overall_metrics = {"precision": [], "recall": []}

            if llm_annotation:
                    comparison_data = []
                    overall_metrics = {"precision": [], "recall": []}

                    for section, human_data in human_annotation.items():
                        llm_data = llm_annotation.get(section, {})
                        if isinstance(human_data, dict):
                            metrics_df = compare_dictionaries(human_data, llm_data)
                            if not metrics_df.empty:
                                st.write(f"### {section} Metrics")
                                
                                def highlight_matches(val):
                                    color = '#66BB6A' if val == '✓' else '#EF5350' if val == '✗' else ''
                                    return f'color: {color}'

                                def highlight_similarity(val):
                                    try:
                                        similarity_value = float(val[:-1]) / 100
                                        if similarity_value >= 0.8:
                                            background = '#388E3C'
                                            color = 'white'
                                        elif similarity_value >= 0.6:
                                            background = '#F9A825'
                                            color = 'black'
                                        else:
                                            background = '#D32F2F'
                                            color = 'white'
                                        return f'background-color: {background}; color: {color}'
                                    except (ValueError, TypeError):
                                        return ''

                                styled_df = metrics_df.style.applymap(highlight_matches, subset=['Match'])\
                                    .applymap(highlight_similarity, subset=['Similarity'])

                                st.dataframe(styled_df, use_container_width=True)
                                
                                avg_precision = metrics_df['Precision'].mean()
                                avg_recall = metrics_df['Recall'].mean()
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Average Precision", f"{avg_precision:.2%}" if not np.isnan(avg_precision) else "N/A")
                                with col2:
                                    st.metric("Average Recall", f"{avg_recall:.2%}" if not np.isnan(avg_recall) else "N/A")
                            else:
                                st.write(f"No comparable data found in {section}")
                        else:
                            metrics = calculate_comparison_metrics(human_data, llm_data)
                            st.write(f"### {section} Metrics")
                            st.write(f"Match: {metrics['match']}, Similarity: {metrics['similarity']}, Precision: {metrics['precision']:.2%}, Recall: {metrics['recall']:.2%}")
            else:
                    st.info("No matching LLM annotation found for this call ID.")
        else:
            st.info("📝 No annotations available for comparison.")


if __name__ == "__main__":
    main()
