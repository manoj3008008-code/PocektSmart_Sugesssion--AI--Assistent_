import json
from typing import Optional
from app.core.config import settings
from app.services.recommender import mock_home, mock_party, mock_jewelry

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key) if genai and settings.gemini_api_key else None

    def _call(self, prompt: str, image_bytes: Optional[bytes] = None, mime_type: Optional[str] = None):
        if not self.client:
            return None
        contents = [prompt]
        if image_bytes and mime_type:
            contents.insert(0, types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=3000,
                response_mime_type="application/json",
            ),
        )
        return response.text

    def _parse(self, text):
        if not text:
            return None
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]
        return json.loads(cleaned)

    def generate_home(self, data):
        if settings.use_mock_ai or not self.client:
            return mock_home(data)
        prompt = f"""
You are PocketSmart AI, a budget recommendation assistant.
Create practical home interior recommendations from this JSON:
{json.dumps(data)}
Return ONLY valid JSON with keys:
planner, summary, budget, allocated_total, items, tips, disclaimer, ai_source.
items must be an array of objects with name, category, estimated_price, platform, reason, search_url.
Use platforms such as Amazon, Flipkart, and IKEA only as recommendation/search destinations.
Do not claim live availability. Keep allocated_total <= budget.
"""
        try:
            result = self._parse(self._call(prompt))
            result["planner"]="home"; result["ai_source"]="gemini"
            return result
        except Exception:
            return mock_home(data)

    def generate_party(self, data):
        if settings.use_mock_ai or not self.client:
            return mock_party(data)
        prompt = f"""
You are PocketSmart AI. Plan a party within a strict budget.
Input:
{json.dumps(data)}
Return ONLY JSON with planner, summary, budget, allocated_total, items, tips, disclaimer, ai_source.
Recommend categories food, venue and decoration. Platforms may include Swiggy, Zomato, OYO and general shopping platforms.
Do not claim live availability or exact current vendor pricing. Keep allocated_total <= budget.
"""
        try:
            result = self._parse(self._call(prompt))
            result["planner"]="party"; result["ai_source"]="gemini"
            return result
        except Exception:
            return mock_party(data)

    def generate_jewelry(self, data, image_bytes=None, mime_type=None):
        if settings.use_mock_ai or not self.client:
            return mock_jewelry(data)
        prompt = f"""
You are PocketSmart AI, a jewelry recommendation assistant.
Analyze the optional outfit image if provided and the user input:
{json.dumps(data)}
Return ONLY JSON with planner, summary, budget, allocated_total, items, tips, disclaimer, ai_source.
Items must contain name, category, estimated_price, platform, reason, search_url.
Suggest jewelry based on occasion, style, color and visible outfit characteristics.
Do not identify the person in the image. Do not claim live prices or availability.
Keep allocated_total <= budget.
"""
        try:
            result = self._parse(self._call(prompt, image_bytes, mime_type))
            result["planner"]="jewelry"; result["ai_source"]="gemini"
            return result
        except Exception:
            return mock_jewelry(data)

gemini_service = GeminiService()
