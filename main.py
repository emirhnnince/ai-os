#!/usr/bin/env python3
"""
AI-OS Ana Çalıştırıcı ve Canlı Ajanik Kabuk (CLI/TUI Simulator)
Bu dosya işletim sisteminin ilk açılışındaki AI arayüzünü simüle eder ve test etmenizi sağlar.
"""

import sys
from src.core.ai_gateway import AIGateway
from src.core.onboarding import OnboardingWizard
from src.core.intent_engine import IntentEngine
from src.core.learning_engine import LearningEngine
from src.updater.ota_client import OTAUpdater, CURRENT_VERSION

def banner():
    print("""
    ======================================================================
      █████╗ ██╗      ██████╗ ███████╗   v{}
     ██╔══██╗██║     ██╔═══██╗██╔════╝   Portable Multi-User Live USB
     ███████║██║     ██║   ██║███████╗   Agentic Operating System
     ██╔══██║██║     ██║   ██║╚════██║   (Dual-Brain: Offline & Gemini)
     ██║  ██║██║     ╚██████╔╝███████║
     ╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝
    ======================================================================
    """.format(CURRENT_VERSION))

def run_learning_session(learning: LearningEngine):
    course = learning.get_course("py101")
    print(f"\n🎓 E-Eğitim Modu Açıldı: {course['title']}")
    step = 0
    while step < len(course["modules"]):
        mod = course["modules"][step]
        print(f"\n--- Adım {mod['step']}: {mod['title']} ---")
        print(f"Ders: {mod['lesson']}")
        print(f"👉 Görev: {mod['task']}")
        try:
            code = input("\nKodunuzu yazın (veya 'çık' yazın): ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if code.lower() == "çık":
            break
        result = learning.evaluate_submission("py101", step, code)
        print(result["message"])
        if result.get("success"):
            step += 1
        elif "hint" in result:
            print(f"💡 İpucu: {result['hint']}")

def main():
    banner()
    gateway = AIGateway()
    intent = IntentEngine(gateway)
    learning = LearningEngine()
    updater = OTAUpdater()

    is_online, status_msg = gateway.network.check_status()
    print(f"[*] Durum: {status_msg}")
    print("[*] 'yardım' veya 'help' yazarak ipuçlarına bakabilir, doğrudan ne yapmak istediğinizi söyleyebilirsiniz.")
    print("[*] Örnek: 'film izlemek istiyorum' veya 'python öğrenmek istiyorum' veya 'güncelleme kontrol et'")
    print("-" * 70)

    while True:
        try:
            user_input = input("\nAI-OS ❯ ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "çık", "kapat"]:
                print("AI-OS oturumu kapatılıyor. İyi çalışmalar!")
                break

            elif user_input.lower() in ["kurulum", "onboarding", "api"]:
                wizard = OnboardingWizard(gateway)
                wizard.start_cli_wizard()

            elif "güncelleme" in user_input.lower() or "update" in user_input.lower():
                print("[*] OTA Güncelleme sunucusu taranıyor...")
                res = updater.check_for_updates()
                if res.get("has_update"):
                    print(f"✨ Yeni Sürüm Bulundu: {res['latest_version']} (Mevcut: {res['current_version']})")
                else:
                    print(f"✅ Sisteminiz en son sürümde ({res['current_version']}).")

            else:
                action = intent.parse_and_execute(user_input)

                # Niyet: Film / Medya
                if action["type"] == "MEDIA_INTENT":
                    print(f"\n🎬 {action['message']}")
                    for idx, opt in enumerate(action["options"], 1):
                        print(f"   [{idx}] {opt['label']}")
                    sub_c = input("\nSeçiminiz: ").strip()
                    try:
                        chosen = action["options"][int(sub_c) - 1]
                        print(f"🚀 Başlatılıyor: {chosen['label']} -> ({chosen.get('target', '')})")
                    except Exception:
                        print("İşlem iptal edildi.")

                # Niyet: E-Eğitim
                elif action["type"] == "LEARNING_INTENT":
                    print(f"\n📚 {action['message']}")
                    run_learning_session(learning)

                # Niyet: Geliştirme Ortamı
                elif action["type"] == "DEV_INTENT":
                    print(f"\n🛠️ {action['message']}")
                    print(f"Hedef Çalışma Alanı: {action['target']}")

                # Genel AI Cevabı
                else:
                    print(f"\n🤖 {action['message']}")

        except (KeyboardInterrupt, EOFError):
            print("\nAI-OS oturumu sonlandırıldı.")
            break
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    main()
