from app import dm_logic


def test_known_scenario_returns_reference():
    decision = dm_logic.decide_for_scenario(
        "The rogue wants to hide in dim light behind the pillar."
    )
    assert "Stealth" in decision.verdict
    assert decision.reference.startswith("DMG")


def test_unknown_scenario_returns_fallback():
    decision = dm_logic.decide_for_scenario("A bard wants to impress the crowd.")
    assert "ability check" in decision.verdict.lower()
    assert decision.reference == "DMG: Using ability scores"
