import streamlit as st
import pandas as pd
import json
from sentence_transformers import SentenceTransformer, util
from rapidfuzz import fuzz
from typing import Dict, Any, List, Optional


class JSONComparatorApp:
    def __init__(self):
        """Initialize attributes."""
        self.attribute_methods = {}
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Pretrained semantic similarity model

    ###############################################################################
    #                               UTILITY METHODS
    ###############################################################################

    @staticmethod
    def parse_json(json_str: str) -> Optional[Dict[str, Any]]:
        """Safely parse a JSON string into a Python dictionary."""
        if not json_str:
            return None
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None

    @staticmethod
    def is_null(value: Any) -> bool:
        """Determine if a value is considered null."""
        if value is None:
            return True
        if isinstance(value, str) and not value.strip():
            return True
        return False

    def compare_texts_semantic(self, text1: str, text2: str, threshold: float = 0.8) -> bool:
        """Compare two text values using semantic similarity."""
        embeddings1 = self.model.encode(text1, convert_to_tensor=True)
        embeddings2 = self.model.encode(text2, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embeddings1, embeddings2).item()
        return similarity >= threshold

    @staticmethod
    def compare_texts_fuzzy(text1: str, text2: str, threshold: int = 80) -> bool:
        """Compare two text values using fuzzy matching (partial ratio)."""
        similarity = fuzz.partial_ratio(text1, text2)
        return similarity >= threshold

    def compare_items_static(self, item1: Any, item2: Any, method: str = 'semantic') -> bool:
        """
        Compare individual items based on the specified method.
        Supports semantic similarity, fuzzy matching, and exact matching.
        """
        if self.is_null(item1) and self.is_null(item2):
            return True  # Both are null, considered a match
        if self.is_null(item1) or self.is_null(item2):
            return False  # One is null and the other is not

        if isinstance(item1, str) and isinstance(item2, str):
            if method == 'semantic':
                return self.compare_texts_semantic(item1, item2)
            elif method == 'fuzzy':
                return self.compare_texts_fuzzy(item1, item2)
            else:
                return item1.strip().lower() == item2.strip().lower()  # Exact match

        if isinstance(item1, dict) and isinstance(item2, dict):
            return item1 == item2  # Placeholder, adjust for deeper comparison if needed

        # Default to exact match for non-text values
        return item1 == item2

    def compare_list_items(self, gt_list: List[Any], llm_list: List[Any], method: str) -> int:
        """
        Compare items in two lists. Each item in the llm_list is compared against all items in gt_list.
        Once a match is found, the corresponding item in gt_list is marked as used and will not be matched again.
        Returns the number of correct matches.
        """
        gt_matched = [False] * len(gt_list)  # Track which gt_list items have been matched
        correct_matches = 0

        for llm_item in llm_list:
            for idx, gt_item in enumerate(gt_list):
                if not gt_matched[idx] and self.compare_items_static(llm_item, gt_item, method=method):
                    correct_matches += 1
                    gt_matched[idx] = True  # Mark the item as matched
                    break  # Stop checking further items in gt_list for this llm_item

        return correct_matches

    ###############################################################################
    #                           COMPARISON + METRICS
    ###############################################################################

    def calculate_record_metrics(self, attribute_metrics: Dict[str, Dict[str, Optional[float]]]) -> Dict[str, Optional[float]]:
        """
        Calculate record-level precision and recall based on non-null attribute-level metrics.
        Uses the count of non-null precision and recall values as denominators.
        """
        precision_sum = 0
        recall_sum = 0
        non_null_precision_count = 0
        non_null_recall_count = 0

        # Iterate over attribute-level metrics
        for key, metrics in attribute_metrics.items():
            precision = metrics.get("Precision")
            recall = metrics.get("Recall")

            # Only include non-null values in the sums and counts
            if precision is not None:
                precision_sum += precision
                non_null_precision_count += 1
            if recall is not None:
                recall_sum += recall
                non_null_recall_count += 1

        # Calculate record-level precision and recall
        record_precision = precision_sum / non_null_precision_count if non_null_precision_count > 0 else None
        record_recall = recall_sum / non_null_recall_count if non_null_recall_count > 0 else None

        return {"Precision": record_precision, "Recall": record_recall}

    def compare_jsons(self, gt_json: Any, llm_json: Any, attribute_methods: Dict[str, str] = None) -> Dict[str, Dict[str, Optional[float]]]:
        """
        Recursively compare JSON objects and calculate precision/recall.
        Handles dictionaries and lists appropriately to avoid type errors.
        """
        results = {}
        attribute_metrics = {}

        if isinstance(gt_json, dict) and isinstance(llm_json, dict):
            # Compare dictionaries by their keys
            all_keys = set(gt_json.keys()).union(set(llm_json.keys()))
            for key in all_keys:
                method = attribute_methods.get(key, "semantic") if attribute_methods else "semantic"
                gt_value = gt_json.get(key)
                llm_value = llm_json.get(key)

                # Handle null scenarios
                if self.is_null(gt_value) and self.is_null(llm_value):
                    attribute_metrics[key] = {"Precision": None, "Recall": None}
                    continue
                if not self.is_null(gt_value) and self.is_null(llm_value):
                    attribute_metrics[key] = {"Precision": None, "Recall": 0.0}
                    continue

                if isinstance(gt_value, list) and isinstance(llm_value, list):
                    # Compare lists
                    correct_matches = self.compare_list_items(gt_value, llm_value, method)
                    precision = correct_matches / len(llm_value) if llm_value else 0.0
                    recall = correct_matches / len(gt_value) if gt_value else 0.0
                    attribute_metrics[key] = {"Precision": precision, "Recall": recall}

                elif isinstance(gt_value, dict) and isinstance(llm_value, dict):
                    # Nested dictionaries
                    sub_results = self.compare_jsons(gt_value, llm_value, attribute_methods)
                    attribute_metrics.update({f"{key}.{sub_key}": sub_result for sub_key, sub_result in sub_results.items()})

                else:
                    # Single value comparison
                    match = self.compare_items_static(gt_value, llm_value, method)
                    precision = 1.0 if match else 0.0
                    recall = 1.0 if match else 0.0
                    attribute_metrics[key] = {"Precision": precision, "Recall": recall}

        # Calculate record-level metrics using updated logic
        record_metrics = self.calculate_record_metrics(attribute_metrics)

        # Add record-level metrics to the results
        results.update(attribute_metrics)
        results["__RECORD__"] = record_metrics

        return results

    ###############################################################################
    #                            STREAMLIT APP
    ###############################################################################

    def run_app(self):
        """Run the Streamlit app."""
        st.set_page_config(page_title="Precision and Recall App", layout="wide")
        st.title("Precision and Recall Calculation for JSON Comparison")

        # Sidebar
        with st.sidebar:
            st.header("File Upload")
            file_choice = st.radio("Select input type:", ("Two JSON files", "CSV file with JSON columns"))
            gt_file = st.file_uploader("Upload Ground Truth JSON", type=["json"]) if file_choice == "Two JSON files" else None
            llm_file = st.file_uploader("Upload LLM JSON", type=["json"]) if file_choice == "Two JSON files" else None
            csv_file = st.file_uploader("Upload a CSV with 'annotated_json' & 'llm_json'", type=["csv"]) if file_choice == "CSV file with JSON columns" else None

        if file_choice == "Two JSON files" and gt_file and llm_file:
            gt_json = self.parse_json(gt_file.read())
            llm_json = self.parse_json(llm_file.read())
            self.process_json_files(gt_json, llm_json)

        elif file_choice == "CSV file with JSON columns" and csv_file:
            self.process_csv_file(csv_file)

    def process_json_files(self, gt_json, llm_json):
        """Process individual JSON files."""
        st.subheader("Comparison Method Selection")
        all_keys = sorted(set(gt_json.keys()).union(set(llm_json.keys())))
        
        # Allow users to select the comparison method for each key
        for key in all_keys:
            self.attribute_methods[key] = st.selectbox(f"Method for '{key}'", ("semantic", "fuzzy", "exact"))

        if st.button("Compare JSON Files"):
            # Perform comparison
            results = self.compare_jsons(gt_json, llm_json, self.attribute_methods)
            attribute_level_metrics = {key: value for key, value in results.items() if key != "__RECORD__"}
            record_metrics = results.get("__RECORD__", {})

            # Display attribute-level metrics
            st.write("### Attribute-Level Precision and Recall")
            df_results = pd.DataFrame.from_dict(attribute_level_metrics, orient="index")
            st.dataframe(df_results)

            # Display record-level metrics
            st.write("### Record-Level Precision and Recall")
            st.markdown(f"**Precision**: `{record_metrics.get('Precision')}`")
            st.markdown(f"**Recall**: `{record_metrics.get('Recall')}`")

    def calculate_avg(self, values: List[Optional[float]]) -> Optional[float]:
        """
        Calculate the average of a list of numeric values, ignoring None values.
        """
        valid_values = [v for v in values if v is not None]
        return sum(valid_values) / len(valid_values) if valid_values else None

    def calculate_avg_attribute_metrics(self, all_attribute_metrics: List[Dict[str, Dict[str, Optional[float]]]]) -> Dict[str, Dict[str, float]]:
        """
        Calculate the average precision and recall for each attribute across multiple JSON pairs.
        """
        aggregated_metrics = {}
        counts = {}

        for attribute_metrics in all_attribute_metrics:
            for key, metrics in attribute_metrics.items():
                if key not in aggregated_metrics:
                    aggregated_metrics[key] = {"Precision": 0, "Recall": 0}
                    counts[key] = {"Precision": 0, "Recall": 0}

                # Aggregate precision
                if metrics["Precision"] is not None:
                    aggregated_metrics[key]["Precision"] += metrics["Precision"]
                    counts[key]["Precision"] += 1

                # Aggregate recall
                if metrics["Recall"] is not None:
                    aggregated_metrics[key]["Recall"] += metrics["Recall"]
                    counts[key]["Recall"] += 1

        # Calculate averages
        for key in aggregated_metrics:
            aggregated_metrics[key]["Precision"] = (
                aggregated_metrics[key]["Precision"] / counts[key]["Precision"]
                if counts[key]["Precision"] > 0
                else None
            )
            aggregated_metrics[key]["Recall"] = (
                aggregated_metrics[key]["Recall"] / counts[key]["Recall"]
                if counts[key]["Recall"] > 0
                else None
            )

        return aggregated_metrics

    def process_csv_file(self, csv_file):
        """Process a CSV file containing JSON pairs."""
        df = pd.read_csv(csv_file)
        if "annotated_json" not in df.columns or "llm_json" not in df.columns:
            st.error("CSV must contain 'annotated_json' and 'llm_json' columns.")
            return

        # Parse JSON strings into dictionaries
        df["annotated_dict"] = df["annotated_json"].apply(self.parse_json)
        df["llm_dict"] = df["llm_json"].apply(self.parse_json)

        st.write("CSV processed successfully.")
        st.write(df.head())

        # Initialize accumulators for averaging
        all_attribute_metrics = []
        record_precisions = []
        record_recalls = []

        # Process each row (JSON pair)
        for _, row in df.iterrows():
            gt_json = row["annotated_dict"]
            llm_json = row["llm_dict"]

            if not isinstance(gt_json, dict) or not isinstance(llm_json, dict):
                st.warning("Skipping row with invalid JSON data.")
                continue

            # Perform comparison for the current pair
            results = self.compare_jsons(gt_json, llm_json, self.attribute_methods)
            attribute_level_metrics = {key: value for key, value in results.items() if key != "__RECORD__"}
            record_metrics = results.get("__RECORD__", {})

            # Accumulate attribute-level metrics
            all_attribute_metrics.append(attribute_level_metrics)

            # Accumulate record-level metrics
            record_precisions.append(record_metrics.get("Precision"))
            record_recalls.append(record_metrics.get("Recall"))

        # Calculate average attribute-level precision and recall
        avg_attribute_metrics = self.calculate_avg_attribute_metrics(all_attribute_metrics)

        # Calculate average record-level precision and recall
        avg_record_precision = self.calculate_avg(record_precisions)
        avg_record_recall = self.calculate_avg(record_recalls)

        # Display averaged attribute-level metrics
        st.write("### Average Attribute-Level Precision and Recall Across All JSON Pairs")
        df_avg_attributes = pd.DataFrame.from_dict(avg_attribute_metrics, orient="index")
        st.dataframe(df_avg_attributes)

        # Display averaged record-level metrics
        st.write("### Average Record-Level Precision and Recall Across All JSON Pairs")
        st.markdown(f"**Average Precision**: `{avg_record_precision}`")
        st.markdown(f"**Average Recall**: `{avg_record_recall}`")

if __name__ == "__main__":
    app = JSONComparatorApp()
    app.run_app()