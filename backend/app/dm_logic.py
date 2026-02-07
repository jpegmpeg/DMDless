from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class DMGDecision:
    scenario: str
    verdict: str
    reference: str


_DECISIONS: List[DMGDecision] = [
    DMGDecision(
        scenario="The rogue wants to hide in dim light behind the pillar.",
        verdict="Call for a Dexterity (Stealth) check contested by passive Perception.",
        reference="DMG: Hiding & Stealth checks",
    ),
    DMGDecision(
        scenario="The fighter wants to jump a 15-foot chasm while running.",
        verdict="Allow a running long jump equal to Strength score; require an Athletics check if strained.",
        reference="DMG: Movement & jumping",
    ),
    DMGDecision(
        scenario="The wizard wants to recall lore about ancient ruins.",
        verdict="Request an Intelligence (History) check to recall relevant lore.",
        reference="DMG: Ability checks",
    ),
]


def available_scenarios() -> List[DMGDecision]:
    return list(_DECISIONS)


def decide_for_scenario(scenario: str) -> DMGDecision:
    normalized = scenario.strip().lower()
    for decision in _DECISIONS:
        if decision.scenario.strip().lower() == normalized:
            return decision
    return DMGDecision(
        scenario=scenario,
        verdict="Ask for an appropriate ability check and set a difficulty class.",
        reference="DMG: Using ability scores",
    )
