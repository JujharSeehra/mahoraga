import os


def create_ai_provider():
    provider = os.getenv("AI_PROVIDER", "hcai").lower()

    if provider == "hcai":
        from brain.hcai import HCAI
        return HCAI()

    if provider == "gemini":
        from brain.gemini import GeminiBrain
        return GeminiBrain()

    raise ValueError(
        f"Unknown AI_PROVIDER: {provider}"
    )