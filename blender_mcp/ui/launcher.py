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
            return {"text": "Please configure your Gemini API Key in Blender preferences first.", "feedback_loop": False}

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
        feedback_requested = False
        feedback_message = ""

        for cmd in commands:
            # Execute and check for feedback request
            # Since we execute in main thread via timer, we need a way to get results back
            # For feedback loop, we'll assume the engine returns it
            # Actually, execute_tool returns the dict. Let's make execute_in_main_thread return it or handle it.

            # For simplicity, we'll check if any command is request_feedback
            if cmd['tool'] == 'request_feedback':
                feedback_requested = True
                feedback_message = cmd['args'].get('message', 'Result of previous action.')

            self.execute_in_main_thread(cmd)

        return {
            "text": response_text,
            "feedback_loop": feedback_requested,
            "feedback_message": feedback_message
        }

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
