import os
import requests
from dotenv import load_dotenv
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class ActionWellbeing(Action):
    def name(self) -> str:
        return "action_wellbeing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a mental wellbeing assistant. You give practical, safe, and empathetic tips on stress management, relaxation, and emotional wellbeing."},
                {"role": "user", "content": tracker.latest_message.get("text")}
            ]
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            # ✅ safer parsing
            tips = (
                data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "Sorry, I couldn't fetch tips right now.")
            )

        except Exception as e:
            tips = f"Error fetching tips: {e}"

        dispatcher.utter_message(text=tips)
        return []
