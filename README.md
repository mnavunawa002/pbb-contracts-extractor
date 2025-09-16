# Hot Deal Package Extractor

This tool leverages AI to extract hotel rates contracts (uploaded as PDFs) and construct compelling hot deal packages for marketing purposes.

## Features

- **PDF Contract Extraction**: Upload hotel rates contracts as PDF files and automatically extract relevant data using AI.
- **Deal Construction**: Builds structured hot deal packages, including inclusions, meal plans, special offers, and wedding packages.
- **Marketing Ready**: Generates marketing headlines, subtitles, urgency messages, and calculates savings.
- **Flexible Deal Types**: Supports various deal types such as limited time, price drop, exclusive access, trending, and more.
- **Extensible Models**: Built with Pydantic models for easy extension and validation.

## Models

The core models are defined in `src/models.py`:

- `Hotel`: Basic hotel information.
- `HotDeal`: Main deal structure with pricing, validity, and marketing fields.
- `DealInclusion`: Add-ons and bonuses included in the deal.
- `MealPlan`: Meal options and pricing.
- `SpecialOffer`: Special codes, free nights, and combinable offers.
- `WeddingPackage`: Wedding-specific packages and pricing.

## Getting Started

1. **Install dependencies**:

   ```
   pip install -r src/requirements.txt
   ```

2. **Set up environment variables**:

   Create a `.env` file with your configuration (see `.env.example` if available).

3. **Run the tool**:

   ```
   streamlit run src/app.py
   ```

## How it Works

1. **Upload PDF**: Upload your hotel rates contract as a PDF file through the app interface.
2. **AI Extraction**: The tool uses AI to parse and extract rates, inclusions, and other relevant details from the PDF.
3. **Deal Construction**: Extracted data is mapped to the internal models to create hot deal packages.
4. **Review & Export**: Review the generated deals and export or use them for marketing.
