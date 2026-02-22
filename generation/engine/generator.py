"""Generator module that calls (mock) LLM and returns structured outputs."""
from __future__ import annotations

from typing import Dict


def mock_llm_call(prompt: str, model: str, temperature: float, max_tokens: int) -> Dict[str, str]:
    """Mock LLM function returning structured outputs based on prompt.

    This placeholder simulates a real LLM call and conforms to spec-driven
    parameters.

    Args:
        prompt: The prompt text.
        model: Model identifier.
        temperature: Sampling temperature.
        max_tokens: Token limit.

    Returns:
        Mapping of output type to content.
    """
    # Create deterministic placeholder outputs using prompt summary
    title = "Generated: " + (prompt.splitlines()[0][:60] if prompt else "Untitled")
    medium = f"# {title}\n\nThis is a medium-length article generated with model {model}.\n\n{prompt[:1000]}"
    linkedin_article = f"# {title} - LinkedIn Article\n\nLong-form article.\n\n{prompt[:1500]}"
    linkedin_post = f"{title} — Quick LinkedIn post: concise hook and CTA."
    image_prompts = "\n".join([f"Image prompt {i+1}: scene inspired by the draft." for i in range(6)])
    return {
        "medium.md": medium,
        "linkedin_article.md": linkedin_article,
        "linkedin_post.md": linkedin_post,
        "image_prompts.md": image_prompts,
    }
