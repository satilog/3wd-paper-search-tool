def get_prompt(content):
    """
    Returns the LLM prompt with the content dynamically inserted.

    Args:
        content (str): The content to be included in the prompt.

    Returns:
        str: The dynamically formatted prompt.
    """
    return f"""
    You are an expert research paper information extractor. Your task is to read a research paper and output a structured JSON representation of its key information. Follow these instructions carefully:

    1. **Strict Adherence**: Strictly adhere to the JSON schema provided below. Do not deviate from the structure.
    2. **Field Completion**: Populate each field to the best of your ability based on the content of the paper.
    - If a field is not applicable or the information is not available, use `null` for single-value fields or an empty array `[]` for multi-value fields.
    3. **Capture n-Way Decision Approaches**:
    - Look for explicit **two-way**, **three-way**, or **four-way** decision approaches.
    - Additionally, capture **implicit or semantic variations** of these approaches.
    - Each `n_way_decision_approaches` field must contain a list of objects with the fields:
        - `context`: The context or scenario where the approach is applied.
        - `decisions`: A list of the decisions involved in the approach.

    4. **Field Clarity**: Ensure that the meaning of each field is respected and accurately filled. Refer to the field descriptions provided.
    5. **Consistency**: Ensure the output JSON is consistent and adheres to the schema, even when processing different papers.

    ---

    ### **JSON Schema with Field Descriptions**
    ```json
    {{
    "paper_id": "A unique identifier for the paper (e.g., Paper_01).",
    "title": "The exact title of the paper as it appears in the document.",
    "authors": ["List of all authors as they appear in the paper, each as a separate string."],
    "year": "The year of publication.",
    "journal_conference": "The name of the journal or conference where the paper was published.",
    "abstract": "The full abstract of the paper, as provided in the document.",
    "keywords": ["List of keywords provided in the paper."],
    "methodologies": ["List of methodologies or approaches used in the paper."],
    "applications": [
        {{
        "application_name": "Name of the application or use case (e.g., 'Anomaly Detection').",
        "domain": "The domain or area of application (e.g., 'Network IDS', 'Host-based IDS').",
        "weight": "A numerical value indicating the importance or significance of the application (if available)."
        }}
    ],
    "performance_metrics": ["List of performance metrics used or discussed in the paper."],
    "ml_models_used": ["List of machine learning models used in the paper."],
    "datasets": ["List of datasets used in the paper, if mentioned."],
    "results_findings": ["A summary of the key results or findings of the paper."],
    "two_way_approaches": [
        {{
        "context": "The context or scenario where the two-way approach is applied.",
        "decisions": ["List of the two-way decisions made."]
        }}
    ],
    "three_way_approaches": [
        {{
        "context": "The context or scenario where the three-way approach is applied.",
        "decisions": ["List of the three-way decisions made."]
        }}
    ],
    "four_way_approaches": [
        {{
        "context": "The context or scenario where the four-way approach is applied.",
        "decisions": ["List of the four-way decisions made."]
        }}
    ],
    "intrusion_detection_systems": {{
        "ids_type": ["Type(s) of IDS used or discussed (e.g., 'Network IDS', 'Host-based IDS', 'Hybrid IDS')."],
        "detection_methods": ["Detection methods used (e.g., 'Anomaly-based', 'Signature-based', 'Hybrid')."],
        "attack_types": ["List of attack types detected or discussed (e.g., 'DoS', 'DDoS', 'SQL Injection')."],
        "evaluation_environment": "Description of environments used to evaluate the IDS (e.g., 'Simulated Network', 'Real-world Deployment')."
    }},
    "algorithm_details": ["List of algorithms introduced or discussed."],
    "architecture_details": ["List of architecture descriptions or components discussed."],
    "techniques_and_concepts": ["List of techniques and concepts introduced or used in the paper."],
    "data_handling": ["List of data preprocessing or handling steps mentioned in the paper."],
    "comparative_analysis": ["List of comparisons with other models or improvements achieved."],
    "real_world_applicability": ["Details on the real-world applicability of the proposed methods."],
    "future_directions": ["Suggestions for future work or directions highlighted in the paper."],
    "advantages": ["List of advantages of the proposed methodologies."],
    "challenges": ["List of challenges or limitations identified in the paper."],
    "gaps_opportunities": ["List of research gaps or opportunities highlighted in the paper."],
    "relationships": [
        {{
        "methodology_name": "Name of the methodology (e.g., 'Three-way Decision Theory').",
        "application_name": "Name of the associated application (e.g., 'Anomaly Detection').",
        "weight": "A numerical value indicating the strength or relevance of the relationship (if available)."
        }}
    ],
    "category_domain": ["The overarching domain(s) or category(ies) of the paper (e.g., 'Cybersecurity')."],
    "category_methodology": ["The primary methodological approach(es) or category(ies) (e.g., 'Decision-theoretic')."]
    }}
    ```

    ---

    ### **Example Output**
    Here is an example of a properly filled JSON object with semantic n-way decision approaches:

    ```json
    {{
    "paper_id": "Paper_01",
    "title": "Three-way Decision Theory in Intrusion Detection Systems",
    "authors": ["John Doe", "Jane Smith"],
    "year": 2022,
    "journal_conference": "IEEE Transactions on Cybersecurity",
    "abstract": "This paper explores three-way decisions in intrusion detection...",
    "keywords": ["Three-way Decisions", "Intrusion Detection", "Cybersecurity"],
    "methodologies": ["Three-way Decision Theory", "Probabilistic Rough Sets"],
    "applications": [
        {{
        "application_name": "Anomaly Detection",
        "domain": "Network IDS",
        "weight": 5
        }}
    ],
    "performance_metrics": ["Accuracy", "Precision", "Recall", "F1 Score"],
    "ml_models_used": ["SVM", "Random Forest"],
    "datasets": ["KDD Cup 1999"],
    "results_findings": ["The proposed method achieved significant reduction in false positives."],
    "two_way_approaches": [
        {{
        "context": "Transaction-level decision-making in financial fraud detection.",
        "decisions": ["Likely user activity", "Likely intruder activity"]
        }}
    ],
    "three_way_approaches": [
        {{
        "context": "Hierarchical decision-making for intrusion detection.",
        "decisions": ["Transaction Level", "Account Level", "Network Level"]
        }}
    ],
    "four_way_approaches": [],
    "intrusion_detection_systems": {{
        "ids_type": ["Network IDS", "Host-based IDS"],
        "detection_methods": ["Anomaly-based"],
        "attack_types": ["DoS", "SQL Injection"],
        "evaluation_environment": "Simulated Network"
    }},
    "algorithm_details": ["Sequentially Stackable Linux Security (SSLS)"],
    "architecture_details": ["Three-way decision architecture with sliding windows."],
    "techniques_and_concepts": ["Sequence analysis", "Sliding window generation"],
    "data_handling": ["Preprocessing system call sequences"],
    "comparative_analysis": ["Improved precision over baseline models by 10%"],
    "real_world_applicability": ["Deployable on Linux systems"],
    "future_directions": ["Exploring multi-modal intrusion detection."],
    "advantages": ["Reduced false positives", "Improved scalability"],
    "challenges": ["Computational overhead"],
    "gaps_opportunities": ["Hybrid methodology integration"],
    "relationships": [
        {{
        "methodology_name": "Three-way Decision Theory",
        "application_name": "Anomaly Detection",
        "weight": 5
        }}
    ],
    "category_domain": ["Cybersecurity"],
    "category_methodology": ["Decision-theoretic"]
    }}
    ```

    ---

    ### **Strictly Follow Below Instructions**
    1. Use the above template as a guideline for extracting information from a research paper.
    2. Ensure the JSON structure is strictly followed, especially for nested attributes under `two_way_approaches`, `three_way_approaches`, and `four_way_approaches`.
    3. Populate fields with information from the paper. If no data is available, use `null` for single-value fields or `[]` for multi-value fields.
    4. Output only the JSON object, without any additional text or explanation.
    5. Try your best to populate the `two_way_approaches`, `three_way_approaches` and `four_way_approaches` fields as best as you can, look for indirect or semantic usage too.

    {content}
    """
