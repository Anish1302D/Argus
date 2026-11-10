"""
Unit Tests for Official TRL Definitions and Ladder Structure.
"""

import pytest
from trl_core.trl_definitions import TRL_LADDER, get_all_definitions, get_trl_definition


def test_ladder_covers_all_nine_levels():
    assert len(TRL_LADDER) == 9
    for lvl in range(1, 10):
        assert lvl in TRL_LADDER
        definition = TRL_LADDER[lvl]
        assert definition.level == lvl
        assert len(definition.title) > 0
        assert len(definition.summary) > 0
        assert len(definition.required_environment) > 0
        assert len(definition.criteria) > 0
        assert len(definition.typical_evidence) > 0


def test_get_trl_definition_valid():
    trl_4 = get_trl_definition(4)
    assert trl_4.level == 4
    assert "laboratory" in trl_4.title.lower()
    # Ensure mandatory criteria exist
    mandatory_criteria = [c for c in trl_4.criteria if c.is_mandatory]
    assert len(mandatory_criteria) >= 1


def test_get_trl_definition_invalid():
    with pytest.raises(ValueError):
        get_trl_definition(0)

    with pytest.raises(ValueError):
        get_trl_definition(10)


def test_get_all_definitions_sorted():
    defs = get_all_definitions()
    assert len(defs) == 9
    assert [d.level for d in defs] == list(range(1, 10))
