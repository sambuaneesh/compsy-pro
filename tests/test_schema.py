from css.data.schema import validate_pair_record


def test_validate_pair_record_minimal_valid() -> None:
    row = {
        "id": "role_000001",
        "schema_version": "css_pair_v1",
        "phenomenon": "role_reversal",
        "s": "The chef praised the waiter.",
        "s_cf": "The waiter praised the chef.",
        "edit_type": "swap_agent_patient",
        "source": "templated",
        "template_id": "role_active_transitive_v01",
        "split": "train",
        "gold_label": {
            "role_direction_s": "chef_agent_waiter_patient",
            "role_direction_cf": "waiter_agent_chef_patient",
            "negation_s": None,
            "negation_cf": None,
            "attachment_s": None,
            "attachment_cf": None,
        },
        "edited_spans": {
            "s": [{"label": "agent", "text": "chef", "char_start": 4, "char_end": 8}],
            "s_cf": [{"label": "agent", "text": "waiter", "char_start": 4, "char_end": 10}],
        },
        "surface_controls": {
            "token_len_s": 5,
            "token_len_cf": 5,
            "char_len_s": 27,
            "char_len_cf": 27,
            "lexical_jaccard": 1.0,
            "levenshtein_distance": 12,
        },
        "human_change": None,
    }
    assert validate_pair_record(row) == []
