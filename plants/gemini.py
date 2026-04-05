import json
import google.generativeai as genai
from django.conf import settings

PROMPT = """You are a plant expert. Analyze this plant image and return ONLY valid JSON with this exact structure:
{
  "plant_name": "Common name",
  "scientific_name": "Scientific name",
  "health_status": "Healthy|Stressed|Diseased|Unknown",
  "current_condition": "Visible symptoms and observations",
  "care_plan": {
    "light": "Light requirements",
    "water": "Watering frequency and method",
    "soil": "Soil type",
    "temperature": "Temperature range",
    "humidity": "Humidity level"
  },
  "cure_plan": "Cure steps if issues exist, or null if healthy",
  "common_problems": "Common problems for this species"
}
If no plant is visible, set plant_name to "Unknown" and describe what you see."""


def analyze_plant_image(image_bytes: bytes, mime_type: str) -> dict:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-3-flash-preview")

    image_part = {"mime_type": mime_type, "data": image_bytes}

    try:
        response = model.generate_content([PROMPT, image_part])
        text = response.text.strip()
        # Strip markdown code fences if Gemini wraps in ```json ... ```
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return {"error": "Could not parse plant analysis. Please try a clearer image."}
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}
