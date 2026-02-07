from dataclasses import dataclass
from typing import List

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool


@dataclass(frozen=True)
class DMDecision:
    verdict: str
    reference: str


@tool
def lookup_dmg(topic: str) -> str:
    """Return a DMG reference for a topic."""
    return f"DMG reference for {topic}"


@tool
def lookup_monster_manual(topic: str) -> str:
    """Return a Monster Manual reference for a topic."""
    return f"Monster Manual reference for {topic}"


@tool
def lookup_player_handbook(topic: str) -> str:
    """Return a Player's Handbook reference for a topic."""
    return f"PHB reference for {topic}"


TOOLS = [lookup_dmg, lookup_monster_manual, lookup_player_handbook]


class LocalDMModel(BaseChatModel):
    """Local reasoning model that routes to reference tools via LangChain."""

    model_name: str = "dmdless-local"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: List[str] | None = None,
        run_manager=None,
        **kwargs,
    ) -> ChatResult:
        user_message = next(
            (msg.content for msg in reversed(messages) if isinstance(msg, HumanMessage)),
            "",
        )
        verdict = "Ask for an appropriate ability check and set a difficulty class."
        reference = lookup_dmg.invoke("Using ability scores")

        lowered = user_message.lower()
        if "hide" in lowered or "stealth" in lowered:
            verdict = (
                "Call for a Dexterity (Stealth) check contested by passive Perception."
            )
            reference = lookup_dmg.invoke("Hiding & Stealth checks")
        elif "jump" in lowered or "chasm" in lowered:
            verdict = (
                "Allow a running long jump equal to Strength score; "
                "require an Athletics check if strained."
            )
            reference = lookup_dmg.invoke("Movement & jumping")
        elif "lore" in lowered or "history" in lowered:
            verdict = "Request an Intelligence (History) check to recall relevant lore."
            reference = lookup_player_handbook.invoke("Ability checks")
        elif "monster" in lowered or "attack" in lowered:
            verdict = "Identify the creature and apply its listed abilities."
            reference = lookup_monster_manual.invoke("Creature traits")

        content = f"Verdict: {verdict} Reference: {reference}"
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

    @property
    def _llm_type(self) -> str:
        return "dmdless-local"


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a dungeon master. Use rules references when making rulings.",
        ),
        ("human", "Scenario: {scenario}\nContext: {context}"),
    ]
)


def get_dm_response(scenario: str, context: str) -> DMDecision:
    chain = PROMPT | LocalDMModel()
    response = chain.invoke({"scenario": scenario, "context": context})
    content = response.content
    verdict = content.split("Verdict:", 1)[-1].split("Reference:")[0].strip()
    reference = content.split("Reference:", 1)[-1].strip()
    return DMDecision(verdict=verdict, reference=reference)


def format_dm_reply(scenario: str, context: str) -> str:
    decision = get_dm_response(scenario, context)
    return (
        "DM: I hear you. Verdict: "
        f"{decision.verdict} Reference: {decision.reference}. "
        f"Context: {context}"
    )
