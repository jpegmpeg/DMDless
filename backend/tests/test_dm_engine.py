from app.dm_engine import format_dm_reply, get_dm_response


def test_known_scenario_returns_reference():
    decision = get_dm_response(
        "The rogue wants to hide in dim light behind the pillar.",
        context="",
    )
    assert "Stealth" in decision.verdict
    assert "DMG reference" in decision.reference


def test_unknown_scenario_returns_fallback():
    decision = get_dm_response("A bard wants to impress the crowd.", context="")
    assert "ability check" in decision.verdict.lower()
    assert "DMG reference" in decision.reference


def test_chain_reply_is_not_offline():
    reply = format_dm_reply("The rogue wants to hide in the shadows.", context="")
    assert reply
    assert "DM is offline" not in reply
