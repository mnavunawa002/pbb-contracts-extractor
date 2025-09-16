from google.generativeai import GenerativeModel, configure
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as genai
import io
import os

from dotenv import load_dotenv

load_dotenv()

class GoogleGeminiClient:
    def __init__(self):
        configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_name = "gemini-1.5-pro"
        self.model = GenerativeModel(self.model_name)

    def upload_pdf(self, file_bytes, display_name="Uploaded PDF"):
        """
        Uploads a PDF file to Gemini and returns the uploaded file object.
        :param file_bytes: Bytes of the PDF file.
        :param display_name: Display name for the uploaded file.
        :return: Uploaded file object.
        """
        doc_io = io.BytesIO(file_bytes)
        uploaded_file = genai.upload_file(doc_io, display_name=display_name, mime_type="application/pdf")
        return uploaded_file

    def extract_hot_deal_packages(self, uploaded_file, prompt=None, model=None):
        """
        Extracts hot deal packages from the uploaded PDF using Gemini.
        :param uploaded_file: The file object returned by upload_pdf.
        :param prompt: The prompt to use for summarization.
        :param model: The Gemini model to use.
        :return: The summary text.
        """
        if prompt is None:
            prompt = """
            You are a travel deals expert and marketing copywriter. 
            You are given one or more hotel contracts. Each contract may contain:
            - Hotel details (name, address, star rating, description, price points, validity, room types).
            - Discounts, promotions, special offers.
            - Inclusions such as meals, transfers, activities, honeymoon bonuses.
            - Wedding or event packages.

            [Note]: Hot deal packages are generated from special offers, and wedding packages. Special offers and wedding packages
            cannot be combined in the same deal. If its a special offer, make the wedding_packages array empty and vice versa.

            Your task is to extract structured deal data and generate attractive marketing packages. 
            Follow these rules:

            1. **Output Format**
            Return data strictly as valid JSON matching the following schema:

            {
              "hot_deals": {
                {
                  "name": "string",
                  "deal_type": "limited_time | price_drop | popular_choice | exclusive_access | best_value | trending | seasonal_special | weekend_escape | extended_stay | flight_package | wedding",
                  "hotel": {
                    "name": "string",
                    "address": "string",
                    "rating": float,
                    "price": float,
                    "image": "string (url if available, else placeholder)",
                    "url": "string (hotel booking or official website if given, else placeholder)",
                    "description": "string"
                  },
                  "description": "string",
                  "marketing_headline": "short catchy title (e.g., 'Escape to Paradise – 30% Off')",
                  "marketing_subtitle": "engaging subtitle with savings and appeal",
                  "urgency_message": "short FOMO message (e.g., 'Limited availability – Book by Sunday!')",
                  "valid_from": "YYYY-MM-DD",
                  "valid_until": "YYYY-MM-DD",
                  "booking_deadline": "YYYY-MM-DD",
                  "minimum_nights": int,
                  "maximum_nights": int,
                  "travel_dates_from": "YYYY-MM-DD",
                  "travel_dates_until": "YYYY-MM-DD",
                  "deal_inclusions": [
                    {
                      "title": "string",
                      "description": "string",
                      "category": "bonus | meal | activity | loyalty | honeymoon"
                    }
                  ],
                  "meal_plans": [
                    {
                      "name": "string",
                      "adult_price": float | null,
                      "child_price": float | null,
                      "infant_free": bool,
                      "description": "string"
                    }
                  ],
                  "special_offers": [
                    {
                      "code": "string | null",
                      "title": "string",
                      "description": "string",
                      "min_nights": int,
                      "max_free_nights": int,
                      "valid_from": "YYYY-MM-DD",
                      "valid_until": "YYYY-MM-DD"
                    }
                  ],
                  "wedding_packages": [
                    {
                      "name": "string",
                      "base_price": float | null,
                      "comissionable": bool,
                      "min_guests": int,
                      "description": "string"
                      "code": "string | null",
                    }
                  ],
                }
              ]
            }

            2. **Generation Rules**
            - Infer missing details where possible (e.g., if rating not given, estimate from contract context).
            - Prices must be consistent (original_display_price > discounted_display_price).
            - Calculate `savings_percentage` as `(original - discounted) / original * 100`.
            - Marketing fields must be attractive, persuasive, and aligned with travel/holiday promotions.
            - Inclusions must be classified into the proper category.
            - For each deal, check if meal plans are included or if they have to added with additional costs. In any case, if meal plans apply, include them in the deal.
            - Hot deals are generated from special offers, and wedding packages.

            3. **Creativity**
            - Make the marketing copy engaging and aligned with travel campaigns.
            - Headlines and urgency messages must create FOMO.
            - Deals should feel diverse (not all the same deal_type).

            ---
            """
        model_to_use = model if model else self.model_name
        model_instance = GenerativeModel(model_to_use)
        response = model_instance.generate_content(
            [uploaded_file, prompt],
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        response = response.text
        import json

        # Extract JSON from the response string
        try:
            # Find the first '{' and last '}' to extract the JSON block
            start_idx = response.find('{')
            end_idx = response.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx+1]
                data = json.loads(json_str)
            else:
                # Fallback: try to load the whole response
                data = json.loads(response)
        except Exception as e:
            # If extraction or parsing fails, return the raw response in a dict
            data = {"error": str(e), "raw_response": response}

        return data

    def delete_file(self, uploaded_file):
        """
        Deletes the uploaded file from Gemini.
        :param uploaded_file: The file object to delete.
        """
        genai.delete_file(uploaded_file.name)