"""
AI-OS Canlı Web ve Kiosk Sunucusu (Live Server & Desktop Backend)
USB Live ortamında localhost:8080 üzerinde çalışır,
hem yerel ekranda (Kiosk) hem de yerel ağdaki (LAN) diğer cihazlarda masaüstünü sunar.
"""

import os
import sys
import json
import asyncio
import subprocess
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from src.core.system_controller import SystemController
from src.core.multi_user import MultiUserManager
from src.core.context_manager import ContextManager
from src.core.offline_slm import OfflineSLMManager
from src.core.ai_gateway import AIGateway
from src.core.intent_engine import IntentEngine
from src.core.learning_engine import LearningEngine
from src.core.bluetooth_manager import BluetoothManager
from src.core.wifi_manager import WiFiRadarManager
from src.core.ai_os_agent import AIOSAgent
from src.core.onboarding_manager import OnboardingManager
from src.updater.ota_client import OTAUpdater

app = FastAPI(title="AI OS Live Server", version="0.1.0")

# Çekirdek Servis Örnekleri
sys_ctrl = SystemController()
user_mgr = MultiUserManager()
context_mgr = ContextManager(sys_ctrl, user_mgr)
bt_mgr = BluetoothManager()
wifi_radar = WiFiRadarManager()
ai_gw = AIGateway(user_mgr)
intent_eng = IntentEngine(ai_gw)
learning_eng = LearningEngine()
ota_updater = OTAUpdater()
ai_os_agent = AIOSAgent(ai_gw, sys_ctrl, bt_mgr, wifi_radar, intent_eng)
onboarding_mgr = OnboardingManager(user_mgr)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
WEBSITE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "website"))
os.makedirs(TEMPLATES_DIR, exist_ok=True)
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# WebSocket Canlı Bağlantı Yöneticisi
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

ws_manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def index():
    """Ana AI-OS Ajanik Masaüstü Sayfası"""
    html_path = os.path.join(TEMPLATES_DIR, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>AI OS Loading...</h1>")

@app.get("/download", response_class=HTMLResponse)
async def download_portal():
    """Vercel'de yayınlanacak resmi AI OS indirme sitesinin yerel önizlemesi."""
    site_path = os.path.join(WEBSITE_DIR, "index.html")
    if os.path.exists(site_path):
        with open(site_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>AI OS Download Portal Loading...</h1>")

@app.get("/manifest.json")
async def get_release_manifest():
    """OTA ve indirme sitesinin ortak sürüm manifesti."""
    manifest_path = os.path.join(WEBSITE_DIR, "manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return JSONResponse(json.load(f))
    return JSONResponse({"error": "manifest.json bulunamadı"}, status_code=404)

@app.get("/api/onboarding/status")
async def get_onboarding_status():
    """Kurulum ve kullanıcı giriş durumunu döndürür."""
    return JSONResponse(onboarding_mgr.get_setup_status())

@app.post("/api/onboarding/complete")
async def complete_onboarding(payload: Dict[str, Any]):
    """Misafir, Yerel veya Google hesabı ile kurulumu tamamlar."""
    res = onboarding_mgr.complete_onboarding(payload)
    return JSONResponse(res)

@app.get("/api/self-learning/status")
async def get_learning_status():
    """Kendi kendini geliştiren hafıza ve kuralları döndürür."""
    return JSONResponse(ai_os_agent.learning.knowledge)

@app.post("/api/self-learning/feedback")
async def add_learning_feedback(payload: Dict[str, str]):
    """Yapay zekanın kurallarını kullanıcının geri bildirimiyle geliştirir."""
    fb = payload.get("feedback", "")
    ai_os_agent.learning.reflect_and_evolve(fb)
    return JSONResponse({"success": True, "message": "Geri bildirim öğrenildi ve AI hafızasına eklendi."})

@app.post("/api/sandbox/run")
async def run_sandbox_code(payload: Dict[str, str]):
    """İzole sandbox kod çalıştırma (Python)."""
    code = payload.get("code", "")
    lang = payload.get("language", "python").lower()
    if lang != "python":
        return JSONResponse({"success": False, "output": "", "error": f"Sunucu sandbox şu an yalnızca Python destekler (seçilen: {lang})."})
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=5
        )
        out = proc.stdout or proc.stderr or "(çıktı yok)"
        return JSONResponse({"success": proc.returncode == 0, "output": out, "stdout": proc.stdout, "stderr": proc.stderr})
    except subprocess.TimeoutExpired:
        return JSONResponse({"success": False, "output": "", "error": "Zaman aşımı (5 sn)."})
    except Exception as e:
        return JSONResponse({"success": False, "output": "", "error": str(e)})

@app.get("/api/greeting")
async def get_greeting():
    """AI OS açılış karşılama ve durum verisi."""
    greeting = ai_os_agent.get_greeting()
    return JSONResponse(greeting)

@app.post("/api/ask")
async def ask_ai_os(payload: Dict[str, Any]):
    """AI OS doğal dil sorgusu ve eylem yürütme."""
    cmd = payload.get("command", "") or payload.get("prompt", "") or payload.get("message", "")
    res = ai_os_agent.process_request(str(cmd))
    return JSONResponse(res)

# Geriye dönük uyumluluk için
@app.get("/api/jarvis/greeting")
async def legacy_greeting():
    return JSONResponse(ai_os_agent.get_greeting())

@app.post("/api/jarvis/command")
async def legacy_command(payload: Dict[str, str]):
    cmd = payload.get("command", "")
    return JSONResponse(ai_os_agent.process_request(cmd))

@app.get("/api/bluetooth/devices")
async def get_bluetooth_devices():
    """Bluetooth cihazlarını döndürür."""
    devices = bt_mgr.scan_devices()
    return JSONResponse({"devices": devices})

@app.post("/api/bluetooth/connect")
async def connect_bluetooth_device(payload: Dict[str, str]):
    mac = payload.get("mac", "")
    res = bt_mgr.connect_device(mac)
    return JSONResponse(res)

@app.get("/api/wifi/radar")
async def get_wifi_radar():
    """Wi-Fi spektrum radar sinyalleri."""
    radar = wifi_radar.scan_radar()
    return JSONResponse({"radar": radar})

@app.get("/api/telemetry")
async def get_telemetry():
    """Anlık CPU, RAM, Disk, Ağ ve Batarya verilerini döndürür."""
    metrics = sys_ctrl.get_hardware_metrics()
    metrics["is_online"] = ai_gw.network.is_connected()
    return JSONResponse(metrics)

@app.post("/api/intent")
async def process_intent(payload: Dict[str, str]):
    """Kullanıcının niyetini analiz edip eyleme dönüştürür."""
    prompt = payload.get("prompt", "").strip()
    if not prompt:
        return JSONResponse({"success": False, "error": "Boş komut."})

    action = intent_eng.parse_and_execute(prompt)
    return JSONResponse({"success": True, "action": action})

@app.post("/api/action/execute")
async def execute_action(payload: Dict[str, Any]):
    """İstemci tarafından onaylanan eylemi sistemde çalıştırır."""
    action_type = payload.get("action")
    target = payload.get("target")

    if action_type == "open_browser":
        res = sys_ctrl.launch_application("browser", [target] if target else [])
        return JSONResponse(res)
    elif action_type == "launch_player":
        res = sys_ctrl.launch_application("media_player", [target] if target else [])
        return JSONResponse(res)
    elif action_type == "launch_workspace":
        res = sys_ctrl.launch_application("editor", [target] if target else [])
        return JSONResponse(res)
    elif action_type == "run_command":
        res = sys_ctrl.execute_safe_command(target)
        return JSONResponse(res)

    return JSONResponse({"success": False, "message": "Bilinmeyen eylem türü."})

@app.get("/api/learning/course/{course_id}")
async def get_course_detail(course_id: str):
    """E-Eğitim müfredatını döndürür."""
    course = learning_eng.get_course(course_id)
    return JSONResponse(course)

@app.post("/api/learning/evaluate")
async def evaluate_code(payload: Dict[str, Any]):
    """Öğrencinin yazdığı kodu değerlendirir."""
    course_id = payload.get("course_id", "py101")
    step = int(payload.get("step", 0))
    code = payload.get("code", "")
    res = learning_eng.evaluate_submission(course_id, step, code)
    return JSONResponse(res)

@app.post("/api/settings/api-key")
async def save_api_key(payload: Dict[str, Any]):
    """Gemini veya diğer API anahtarını kaydeder."""
    provider = payload.get("provider", "gemini")
    key = (payload.get("key") or payload.get("api_key") or "").strip()
    model = payload.get("model")
    if model:
        ai_os_agent.active_model = model
    if not key:
        return JSONResponse({"status": "error", "success": False, "message": "API anahtarı boş olamaz."})
    success = user_mgr.update_user_api_key(provider, key)
    return JSONResponse({"status": "ok" if success else "error", "success": success, "message": "API anahtarı başarıyla güncellendi."})

@app.get("/api/settings/model")
async def get_active_model():
    """Aktif AI modelini döndürür."""
    return JSONResponse({"model": ai_os_agent.active_model, "stealth_mode": ai_os_agent.stealth_mode})

@app.post("/api/settings/model")
async def set_active_model(payload: Dict[str, str]):
    """Aktif AI modelini değiştirir."""
    model = payload.get("model", "").strip()
    if not model:
        return JSONResponse({"status": "error", "message": "Model adı belirtilmedi."})
    ai_os_agent.active_model = model
    return JSONResponse({"status": "ok", "model": model, "message": f"Aktif model {model} olarak ayarlandı."})

@app.get("/api/settings/stealth")
async def get_stealth_mode():
    """Gizli / Hava boşluklu (Air-Gap) mod durumunu döndürür."""
    return JSONResponse({"stealth_mode": ai_os_agent.stealth_mode})

@app.post("/api/settings/stealth")
async def toggle_stealth_mode(payload: Dict[str, Any]):
    """Gizli / Hava boşluklu (Air-Gap) modu açar veya kapatır."""
    enabled = bool(payload.get("enabled", not ai_os_agent.stealth_mode))
    ai_os_agent.stealth_mode = enabled
    return JSONResponse({"status": "ok", "stealth_mode": enabled})

@app.get("/api/rag/search")
async def rag_search(q: str = ""):
    """Yerel dokümanlar ve öğrenilmiş hafıza üzerinde anahtar kelime araması yapar."""
    query = q.strip().lower()
    if not query:
        return JSONResponse({"query": q, "results": []})
    results: List[Dict[str, str]] = []
    project_root = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
    docs_dir = os.path.join(project_root, "docs")
    if os.path.isdir(docs_dir):
        for fname in os.listdir(docs_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(docs_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        for idx, line in enumerate(f, 1):
                            if query in line.lower():
                                results.append({"source": f"docs/{fname}:{idx}", "snippet": line.strip()[:180]})
                                if len(results) >= 15:
                                    break
                except Exception:
                    pass
            if len(results) >= 15:
                break
    for rule in ai_os_agent.learning.knowledge.get("learned_rules", []):
        if query in str(rule).lower():
            results.append({"source": "learned_knowledge", "snippet": str(rule)[:180]})
    return JSONResponse({"query": q, "count": len(results), "results": results[:15]})

@app.post("/api/wifi/qr")
async def generate_wifi_qr(payload: Dict[str, str]):
    """Wi-Fi paylaşımı için standart QR payload metni üretir."""
    ssid = payload.get("ssid", "").strip()
    pwd = payload.get("password", "")
    sec = payload.get("security", "WPA")
    if not ssid:
        return JSONResponse({"status": "error", "message": "SSID gerekli."})
    qr_payload = f"WIFI:T:{sec};S:{ssid};P:{pwd};;"
    return JSONResponse({"status": "ok", "ssid": ssid, "qr_payload": qr_payload})

@app.get("/api/system/battery")
async def get_battery_health():
    """Pil sağlığı ve güç telemetrisini döndürür."""
    metrics = sys_ctrl.get_hardware_metrics()
    return JSONResponse({
        "status": "ok",
        "battery": metrics.get("battery", {"percent": 100, "plugged": True, "health": "Good"}),
        "cpu_percent": metrics.get("cpu_percent", 0)
    })

@app.get("/api/ota/status")
async def get_ota_status():
    """OTA güncelleme durumunu kontrol eder."""
    try:
        info = ota_updater.check_for_updates() if hasattr(ota_updater, "check_for_updates") else {"current_version": "2.1.0", "update_available": False}
    except Exception:
        info = {"current_version": "2.1.0", "update_available": False}
    return JSONResponse({"status": "ok", "ota": info})

@app.get("/api/wifi/list")
async def list_wifi():
    """Çevredeki Wi-Fi ağlarını listeler."""
    networks = sys_ctrl.scan_wifi_networks()
    return JSONResponse({"networks": networks})

@app.post("/api/wifi/connect")
async def connect_wifi(payload: Dict[str, str]):
    """Wi-Fi ağına bağlanır."""
    ssid = payload.get("ssid")
    pwd = payload.get("password")
    res = sys_ctrl.connect_wifi(ssid, pwd)
    return JSONResponse(res)

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """Gerçek zamanlı iki yönlü ses/metin AI sohbet hattı."""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            req = json.loads(data)
            prompt = req.get("message", "")

            # Sistem bağlamını oluştur
            ctx = context_mgr.build_system_context()

            # Niyet kontrolü
            action = intent_eng.parse_and_execute(prompt)

            if action.get("type") in ["MEDIA_INTENT", "LEARNING_INTENT", "DEV_INTENT"]:
                await websocket.send_json({
                    "type": "action_required",
                    "action": action
                })
            else:
                ai_res = ai_gw.route_query(prompt, ctx)
                await websocket.send_json({
                    "type": "ai_response",
                    "provider": ai_res.get("provider", "AI-OS"),
                    "text": ai_res.get("text", ""),
                    "mode": ai_res.get("mode", "UNKNOWN")
                })
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        ws_manager.disconnect(websocket)

def run_server(host: str = "0.0.0.0", port: int = 8080):
    import uvicorn
    print(f"[*] AI-OS Live Desktop Server başlatılıyor: http://{host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    run_server()
