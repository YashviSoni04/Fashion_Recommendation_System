import google.generativeai as genai
import json
import re
import time
from typing import Dict
import logging
from .config import settings
from .models import FashionRequest

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

class FashionRecommendationService:
    def __init__(self):
        """Initialize the fashion recommendation service"""
        try:
            if not settings.GEMINI_API_KEY:
                raise ValueError("Gemini API key not configured")
            
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
            logger.info("Fashion Recommendation Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize service: {str(e)}")
            raise

    def create_detailed_prompt(self, request: FashionRequest) -> str:
        """Create a comprehensive prompt for Gemini AI"""
        
        prompt = f"""
You are an expert fashion stylist with 15+ years of experience. Provide personalized fashion recommendations.

USER PROFILE:
- Fashion Type: {request.fashion_type}
- Size: {request.size}
- Gender: {request.gender}
- Budget: {request.budget_range}
- Colors: {request.color_preference}
- Body Type: {request.body_type}
- Occasion: {request.occasion_specific}
- Style: {request.style_preference}

REQUIREMENTS:
1. Provide 3 complete outfit recommendations
2. Include specific brands and price ranges
3. Add size-specific styling tips
4. Suggest where to shop
5. Include styling hacks

FORMAT AS JSON:
{{
    "outfit_recommendations": [
        {{
            "outfit_name": "Outfit Name",
            "description": "Brief description",
            "pieces": {{
                "top": "Specific item details",
                "bottom": "Specific item details", 
                "footwear": "Specific item details",
                "accessories": ["item1", "item2"]
            }},
            "total_budget_estimate": "$X - $Y",
            "styling_notes": "Why this works"
        }}
    ],
    "size_specific_tips": [
        "tip1 for size {request.size}",
        "tip2 for size {request.size}"
    ],
    "recommended_stores": [
        {{
            "store_name": "Store Name",
            "type": "online/physical",
            "budget_level": "budget/premium",
            "why_recommended": "reason"
        }}
    ],
    "styling_hacks": [
        "hack1 for {request.fashion_type}",
        "hack2 for {request.fashion_type}"
    ],
    "color_coordination": "Color palette suggestions",
    "final_note": "Confidence-boosting message"
}}

Be specific and actionable. Include real brands and stores.
"""
        return prompt

    async def get_recommendations(self, request: FashionRequest) -> Dict:
        """Get fashion recommendations from Gemini AI"""
        start_time = time.time()
        
        try:
            logger.info(f"Processing recommendation request for {request.fashion_type} - {request.size}")
            
            prompt = self.create_detailed_prompt(request)
            
            # Generate content
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise ValueError("Empty response from Gemini AI")
            
            response_text = response.text
            logger.info("Received response from Gemini AI")
            
            # Parse JSON response
            recommendations = self._parse_response(response_text)
            
            processing_time = time.time() - start_time
            logger.info(f"Request processed successfully in {processing_time:.2f} seconds")
            
            return {
                "status": "success",
                "data": recommendations,
                "processing_time": processing_time
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Error processing request: {str(e)}")
            
            return {
                "status": "error",
                "message": str(e),
                "processing_time": processing_time,
                "details": {
                    "request_params": request.dict(),
                    "error_type": type(e).__name__
                }
            }

    def _parse_response(self, response_text: str) -> Dict:
        """Parse AI response and extract JSON"""
        try:
            # Find JSON in response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # Fallback: structure the text response
                return {
                    "outfit_recommendations": [{
                        "outfit_name": "AI Generated Recommendation",
                        "description": "Custom recommendation based on preferences",
                        "pieces": {"complete_recommendation": response_text[:500]},
                        "styling_notes": "Detailed AI recommendation"
                    }],
                    "additional_advice": response_text,
                    "note": "Text response - JSON parsing unavailable"
                }
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed: {str(e)}")
            return self._create_fallback_response(response_text)

    def _create_fallback_response(self, text: str) -> Dict:
        """Create structured fallback response"""
        return {
            "outfit_recommendations": [{
                "outfit_name": "Custom Recommendation",
                "description": "AI-powered fashion advice",
                "pieces": {"recommendation": text[:300] + "..."},
                "styling_notes": "Complete recommendation provided"
            }],
            "raw_advice": text,
            "parsing_note": "Structured response generated from text"
        }