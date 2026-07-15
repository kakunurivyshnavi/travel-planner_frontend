import os
import requests
import gradio as gr

FASTAPI_URL = "https://travel-planner-backend-1-6p3k.onrender.com"

def get_plan(destination, days, budget, interests):
    try:
        response = requests.get(
            FASTAPI_URL,
            params={
                "destination": destination.strip(),
                "days": int(days),
                "budget": int(budget),
                "interests": interests.strip()
            },
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        return f"""
🌍 Destination: {data.get("destination")}

📅 Days: {data.get("days")}

💰 Budget: ₹{data.get("budget")}

🗓️ Itinerary

{data.get("itinerary")}
"""

    except requests.exceptions.RequestException as e:
        return f"❌ Backend Error:\n{e}"

    except Exception as e:
        return f"❌ Error:\n{e}"


demo = gr.Interface(
    fn=get_plan,
    inputs=[
        gr.Textbox(label="Destination", placeholder="e.g. Goa"),
        gr.Slider(1, 14, value=3, step=1, label="Days"),
        gr.Slider(100, 50000, value=5000, step=100, label="Budget"),
        gr.Textbox(label="Interests", placeholder="Beach, Food, Adventure")
    ],
    outputs=gr.Textbox(label="Travel Plan"),
    title="🌍 AI Travel Planner",
    description="Generate personalized travel itineraries using FastAPI + Gemini."
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )