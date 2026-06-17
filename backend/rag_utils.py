import re
from pathlib import Path

from config import RULEBOOKS_DIR

RULES_KEYWORDS = (
    "regras",
    "objetivo",
    "como jogar",
    "como se joga",
    "how to play",
    "rules",
    "rulebook",
    "goal",
    "win",
    "vencer",
    "ganhar",
    "vence",
    "setup",
    "preparar",
    "instru",
    "manual",
)

GAME_ALIASES = {
    "catan": ("catan", "katan", "colonos", "settlers"),
    "pandemic": ("pandemic", "pandemia"),
    "ticket to ride": ("ticket to ride", "ticket ride"),
}


def game_name_from_pdf(path: Path) -> str:
    stem = path.stem.lower()
    for suffix in ("-rules", "_rules", "-rulebook", "_rulebook", "-manual"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    return stem.replace("-", " ").replace("_", " ").strip().title()


def known_rulebook_games() -> dict[str, str]:
    games: dict[str, str] = {}
    if RULEBOOKS_DIR.exists():
        for pdf in RULEBOOKS_DIR.glob("*.pdf"):
            name = game_name_from_pdf(pdf)
            games[name.lower()] = name
            games[pdf.stem.lower()] = name
    return games


def detect_game(question: str) -> str | None:
    q = question.lower()
    for canonical, aliases in GAME_ALIASES.items():
        if any(alias in q for alias in aliases):
            return canonical.title()

    for key, display in known_rulebook_games().items():
        if key in q:
            return display

    return None


def is_rules_question(question: str) -> bool:
    q = question.lower()
    return any(keyword in q for keyword in RULES_KEYWORDS)


def expand_question(question: str, game: str | None) -> str:
    if not game:
        return question
    return f"{question} {game} board game rules rulebook objective players"
