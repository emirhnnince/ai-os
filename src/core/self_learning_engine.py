"""
AI-OS Kendi Kendini Geliştiren Yapay Zeka Motoru (Self-Learning & Evolution Engine)
Kullanıcının tercihlerini, düzeltmelerini, sık kullandığı eylemleri analiz eder,
hafızasına kaydeder ve sistem istemini (System Prompt) dinamik olarak optimize eder.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional

class SelfLearningEngine:
    def __init__(self, memory_dir: str = "data/memory"):
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)
        self.knowledge_file = os.path.join(self.memory_dir, "learned_knowledge.json")
        self.macros_file = os.path.join(self.memory_dir, "neural_macros.json")
        self.knowledge = self._load_knowledge()
        self.macros = self._load_macros()

    def _load_knowledge(self) -> Dict[str, Any]:
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "user_preferences": {
                "preferred_tone": "zarif ve doğrudan",
                "default_movie_platform": "YouTube",
                "coding_language": "Python",
                "preferred_editor": "VSCode",
                "sound_feedback": True
            },
            "learned_rules": [
                "Kullanıcı film istediğinde önce arama terimini doğrula.",
                "Kodlama sorularında doğrudan çözüm yerine pedagojik ipucu sağla.",
                "Sistem kontrollerinde güvenlik teyidi iste."
            ],
            "corrections_log": [],
            "interaction_count": 0,
            "evolution_level": "v1.2 (Öğrenen Çekirdek)"
        }

    def _load_macros(self) -> Dict[str, Any]:
        if os.path.exists(self.macros_file):
            try:
                with open(self.macros_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "gece modu": {"action": "night_mode", "brightness": 25, "volume": 30},
            "çalışma modu": {"action": "dev_mode", "open_editor": True, "open_music": False}
        }

    def save_knowledge(self):
        with open(self.knowledge_file, "w", encoding="utf-8") as f:
            json.dump(self.knowledge, f, indent=4, ensure_ascii=False)

    def record_interaction(self, user_prompt: str, ai_response: str, user_feedback: Optional[str] = None):
        """Kullanıcı etkileşimini kaydeder ve kendi kendine öğrenme döngüsünü tetikler."""
        self.knowledge["interaction_count"] += 1
        
        # Kullanıcı tercihlerini metinden otomatik çıkar
        lower = user_prompt.lower()
        if "netflix" in lower:
            self.knowledge["user_preferences"]["default_movie_platform"] = "Netflix"
        elif "youtube" in lower:
            self.knowledge["user_preferences"]["default_movie_platform"] = "YouTube"

        if "javascript" in lower or "js" in lower:
            self.knowledge["user_preferences"]["coding_language"] = "JavaScript"
        elif "python" in lower:
            self.knowledge["user_preferences"]["coding_language"] = "Python"

        if user_feedback:
            self.knowledge["corrections_log"].append({
                "timestamp": time.time(),
                "prompt": user_prompt,
                "feedback": user_feedback
            })
            self.reflect_and_evolve(user_feedback)

        self.save_knowledge()

    def reflect_and_evolve(self, feedback: str):
        """Yapay zekanın kendini geliştirdiği özdüşünüm (reflection) fonksiyonu."""
        new_rule = f"Kullanıcı geri bildirimiyle öğrenildi: {feedback}"
        if new_rule not in self.knowledge["learned_rules"]:
            self.knowledge["learned_rules"].append(new_rule)
            self.save_knowledge()

    def get_learned_context_prompt(self) -> str:
        """Sistemin öğrendiği kuralları sistem istemine ekler."""
        rules_text = "\n".join([f"- {r}" for r in self.knowledge.get("learned_rules", [])])
        prefs = self.knowledge.get("user_preferences", {})
        return (
            f"\n[KENDİ KENDİNE GELİŞEN HAFIZA (Öğrenilen Bilgiler)]:\n"
            f"Kullanıcı Tercihleri: Favori Kod Dili: {prefs.get('coding_language')}, "
            f"Favori Medya: {prefs.get('default_movie_platform')}\n"
            f"Öğrenilen Özel Kurallar:\n{rules_text}\n"
        )
