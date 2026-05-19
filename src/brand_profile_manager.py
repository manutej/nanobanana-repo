import json
from pathlib import Path
from typing import Dict, Optional, List


class BrandProfileManager:
    """Loads and applies named brand profiles to enhanced prompts."""

    def __init__(self, profiles_path: Optional[str] = None):
        if profiles_path is None:
            current_dir = Path(__file__).parent
            profiles_path = current_dir.parent / "templates" / "brand_profiles.json"

        with open(profiles_path, "r") as f:
            self.profiles: Dict = json.load(f)

    def list_profiles(self) -> List[str]:
        return sorted(self.profiles.keys())

    def get_profile(self, name: str) -> Dict:
        if name not in self.profiles:
            raise ValueError(
                f"Unknown brand_profile: {name}. "
                f"Must be one of {self.list_profiles()}"
            )
        return self.profiles[name]

    def apply(self, prompt: str, name: Optional[str]) -> str:
        if not name:
            return prompt

        profile = self.get_profile(name)
        colors = ", ".join(profile.get("colors", []))
        style_rules = ", ".join(profile.get("style_rules", []))
        forbidden_styles = ", ".join(profile.get("forbidden_styles", []))
        tone = profile.get("tone", "")

        additions = []
        if tone:
            additions.append(f"brand tone: {tone}")
        if colors:
            additions.append(f"brand colors: {colors}")
        if style_rules:
            additions.append(f"style rules: {style_rules}")
        if forbidden_styles:
            additions.append(f"avoid: {forbidden_styles}")

        if not additions:
            return prompt

        return f"{prompt}, {', '.join(additions)}"
