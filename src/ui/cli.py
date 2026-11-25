"""
AI-OS Zengin Terminal Kabuğu (Rich TUI Shell)
Saf konsol/TTY ortamında çalışan veya SSH üzerinden bağlanan
kullanıcılar için etkileşimli yapay zeka arayüzü.
"""

import sys
import os
from src.core.system_controller import SystemController
from src.core.multi_user import MultiUserManager
from src.core.context_manager import ContextManager
from src.core.ai_gateway import AIGateway
from src.core.intent_engine import IntentEngine
from src.core.learning_engine import LearningEngine
from src.core.onboarding import OnboardingWizard
from src.updater.ota_client import OTAUpdater, CURRENT_VERSION

def main():
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        from rich.prompt import Prompt
        console = Console()
        use_rich = True
    except ImportError:
        console = None
        use_rich = False

    sys_ctrl = SystemController()
    user_mgr = MultiUserManager()
    ctx_mgr = ContextManager(sys_ctrl, user_mgr)
    gateway = AIGateway(user_mgr)
    intent_eng = IntentEngine(gateway)
    learning_eng = LearningEngine()
    updater = OTAUpdater()

    if use_rich:
        console.print(Panel.fit(
            f"[bold cyan]AI-OS[/bold cyan] [green]v{CURRENT_VERSION}[/green] - [yellow]Portable Multi-User Live USB[/yellow]\n"
            f"[dim]Kullanıcı:[/dim] [bold]{user_mgr.get_current_user_profile().get('username')}[/bold] | "
            f"[dim]AI Çekirdeği:[/dim] [magenta]Google Gemini 2.0 & Offline SLM[/magenta]",
            border_style="cyan"
        ))
    else:
        print(f"=== AI-OS v{CURRENT_VERSION} Live USB ===")

    while True:
        try:
            if use_rich:
                prompt_text = "[bold cyan]AI-OS ❯[/bold cyan]"
                user_input = Prompt.ask(prompt_text).strip()
            else:
                user_input = input("AI-OS ❯ ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "çık", "kapat"]:
                print("AI-OS oturumu sonlandırıldı.")
                break

            elif user_input.lower() in ["yardım", "help"]:
                if use_rich:
                    table = Table(title="AI-OS Temel Komutları ve Niyetler")
                    table.add_column("Komut / Niyet", style="cyan")
                    table.add_column("Açıklama", style="white")
                    table.add_row("film izlemek istiyorum", "Medya akışını ve oynatıcıyı hazırlar")
                    table.add_row("python öğrenmek istiyorum", "İnteraktif kodlama akademisini başlatır")
                    table.add_row("kurulum / api", "Gemini API ve ilk kurulum sihirbazını açar")
                    table.add_row("durum / telemetri", "Donanım, bellek ve ağ kullanımını gösterir")
                    table.add_row("güncelleme", "Atomik OTA güncelleme kontrolü yapar")
                    console.print(table)
                else:
                    print("Komutlar: 'film izlemek istiyorum', 'python öğrenmek istiyorum', 'kurulum', 'durum', 'çık'")

            elif user_input.lower() in ["kurulum", "api"]:
                wizard = OnboardingWizard(gateway)
                wizard.start_cli_wizard()

            elif user_input.lower() in ["durum", "telemetri", "status"]:
                metrics = sys_ctrl.get_hardware_metrics()
                print(f"CPU: %{metrics['cpu_percent']} | RAM: %{metrics['memory']['used_percent']} ({metrics['memory']['available_mb']} MB Boş)")
                print(f"Platform: {metrics['platform']} | Ağ: {metrics.get('is_online', 'Kontrol ediliyor')}")

            else:
                action = intent_eng.parse_and_execute(user_input)
                if action["type"] == "MEDIA_INTENT":
                    print(f"\n🎬 {action['question']}")
                    for idx, opt in enumerate(action["options"], 1):
                        print(f"  [{idx}] {opt['label']}")
                    choice = input("Seçiminiz (1-3): ").strip()
                    try:
                        chosen = action["options"][int(choice) - 1]
                        print(f"🚀 Başlatılıyor: {chosen['label']} -> {chosen['target']}")
                    except Exception:
                        print("İptal edildi.")
                elif action["type"] == "LEARNING_INTENT":
                    print(f"\n🎓 {action['message']}")
                    # Basit CLI dersi
                    course = learning_eng.get_course("py101")
                    print(f"Müfredat: {course['title']}")
                else:
                    print(f"\n🤖 {action['message']}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nOturum kapatıldı.")
            break

if __name__ == "__main__":
    main()
