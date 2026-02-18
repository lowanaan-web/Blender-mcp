import webview
import threading
import os
import bpy
from ..core.gemini import GeminiManager
from ..core.engine import AtomicEngine
from ..utils.vision import get_base64_viewport

class UIBridge:
    def __init__(self):
        self.engine = AtomicEngine()
        self.gemini = None
        self._window = None

    def set_window(self, window):
        self._window = window

    def init_gemini(self, api_key, model_name):
        self.gemini = GeminiManager(api_key, model_name)

    def get_settings(self):
        prefs = bpy.context.preferences.addons['blender_mcp'].preferences
        return {
            "api_key": prefs.api_key,
            "model_name": prefs.model_name
        }

    def update_settings(self, api_key, model_name):
        prefs = bpy.context.preferences.addons['blender_mcp'].preferences
        prefs.api_key = api_key
        prefs.model_name = model_name
        # Re-init Gemini with new settings
        self.init_gemini(api_key, model_name)
        return {"status": "success"}

    def fetch_available_models(self, api_key):
        return GeminiManager.list_available_models(api_key)

    def send_to_gemini(self, message):
        if not self.gemini:
            return "Please configure your Gemini API Key in Blender preferences first."

        # Automatically take screenshot on main thread
        import threading
        result = {"image_data": None}
        event = threading.Event()

        def capture_task():
            result["image_data"] = get_base64_viewport()
            event.set()
            return None

        bpy.app.timers.register(capture_task)
        event.wait(timeout=5.0) # Wait for capture

        image_data = result["image_data"]

        # Get response from Gemini
        response_text = self.gemini.send_message(message, image_data)

        # Extract and execute commands
        commands = self.gemini.extract_commands(response_text)
        for cmd in commands:
            # Execute in Blender's main thread?
            # pywebview calls are in a separate thread, so we need to be careful with bpy
            # We'll use a timer or a queue if needed, but for now let's try direct call
            # (In production, use bpy.app.timers to run on main thread)
            self.execute_in_main_thread(cmd)

        return response_text

    def execute_in_main_thread(self, cmd):
        def run():
            self.engine.execute_tool(cmd['tool'], cmd['args'])
            return None # Timers need a return value

        bpy.app.timers.register(run)

    def close(self):
        if self._window:
            self._window.destroy()

def launch():
    bridge = UIBridge()

    # Get API key from preferences
    prefs = bpy.context.preferences.addons['blender_mcp'].preferences
    if prefs.api_key:
        bridge.init_gemini(prefs.api_key, prefs.model_name)

    html_path = os.path.join(os.path.dirname(__file__), "index.html")

    def create_window():
        window = webview.create_window(
            'Blender MCP - Gemini',
            url=html_path,
            width=450,
            height=700,
            transparent=True,
            on_top=True,
            frameless=True,
            js_api=bridge
        )
        bridge.set_window(window)
        webview.start(debug=False)

    threading.Thread(target=create_window, daemon=True).start()
