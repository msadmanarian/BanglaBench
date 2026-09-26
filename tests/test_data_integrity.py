import pytest
import json
import os

base_dir = os.path.dirname(os.path.dirname(__file__))

def test_annotated_dataset_schema():
    data_path = os.path.join(base_dir, '04_Dataset', 'annotated', 'claims_annotated.json')
    assert os.path.exists(data_path), "Annotated dataset file missing"
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == 60, f"Expected 60 claims, found {len(data)}"
    valid_labels = {"SUPPORTED", "REFUTED", "UNVERIFIABLE", "MISLEADING", "OPINION"}
    valid_domains = {"politics", "health", "finance", "disaster", "sci_tech", "social"}

    for item in data:
        assert item["adjudicated_label"] in valid_labels
        assert item["domain"] in valid_domains
        assert len(item["claim_text_normalized"]) > 0
        assert len(item["evidence_urls"]) > 0

def test_split_leakage_absence():
    splits = [
        ('04_Dataset/train/split_a_train.json', '04_Dataset/test/split_a_test.json'),
        ('04_Dataset/train/split_b_train.json', '04_Dataset/test/split_b_test.json'),
        ('04_Dataset/train/split_c_train.json', '04_Dataset/test/split_c_test.json'),
        ('04_Dataset/temporal/split_d_train_past.json', '04_Dataset/temporal/split_d_test_future.json')
    ]
    for tr_p, te_p in splits:
        with open(os.path.join(base_dir, tr_p), 'r', encoding='utf-8') as f:
            tr = json.load(f)
        with open(os.path.join(base_dir, te_p), 'r', encoding='utf-8') as f:
            te = json.load(f)
        tr_ids = {c["claim_id"] for c in tr}
        te_ids = {c["claim_id"] for c in te}
        assert len(tr_ids.intersection(te_ids)) == 0, f"Leakage detected between {tr_p} and {te_p}"
