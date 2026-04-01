import httpx
from app.db.repositories import image_repo
from app.config import settings
from google import genai
from PIL import Image
import io
from urllib.parse import quote

client = genai.Client(api_key=settings.gemini_api_key)

def generate_image(project_id: str, prompt: str) -> dict:
    """Generate an image from a text prompt and save it to the project"""
    # Properly encode the prompt for URL
    encoded_prompt = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"

    image = image_repo.save_image(project_id=project_id, prompt=prompt, url=url)
    if image:
        return {
            "success": True,
            "image_id": image["id"],
            "url": url,
            "prompt": prompt
        }
    return {"success": False, "error": "Failed to save image"}

def analyze_image(image_id: str, question: str = "Describe this image in detail") -> dict:
    """Analyze an image using Gemini Vision and return the analysis"""
    image_record = image_repo.get_image(image_id)
    if not image_record:
        return {"error": "Image not found"}
    try:
        response = httpx.get(image_record["url"], timeout=30)
        image_data = Image.open(io.BytesIO(response.content))
        result = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[question, image_data]
        )
        analysis = result.text
        image_repo.update_image_analysis(image_id, analysis)
        return {"success": True, "image_id": image_id, "analysis": analysis}
    except Exception as e:
        return {"error": str(e)}