import streamlit as st
from clients.google_client import GoogleGeminiClient
import pandas as pd
import json

google_client = GoogleGeminiClient()

st.title("Hot Deal Package Extractor")

st.write("Upload a hotel rates contract as a PDF file and automatically extract relevant data using AI.")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    uploaded_file = google_client.upload_pdf(uploaded_file.read())
    st.write("File uploaded successfully")
    st.write(uploaded_file)
    with st.spinner("Extracting hot deal packages..."):
      # Extract hot deals as JSON string
      hot_deals_data = google_client.extract_hot_deal_packages(uploaded_file)

      if hot_deals_data:
          st.subheader("Extracted Hot Deals (Editable)")
          # convert the hot_deals_data to a pandas dataframe
          # hot_deals_data is already a JSON object (dict), so just extract the hot_deals list and convert to DataFrame
          hot_deals_list = hot_deals_data.get("hot_deals", [])
          
          # For each hot deal, display editable fields in an expander
          for idx, hot_deal in enumerate(hot_deals_list):
              with st.expander(f"Hot Deal {idx+1}: {hot_deal.get('name', 'Unnamed Deal')}"):
                  # Editable fields for main hot deal info
                  hot_deal['name'] = st.text_input("Deal Name", value=hot_deal.get('name', ''), key=f"name_{idx}")
                  hot_deal['deal_type'] = st.text_input("Deal Type", value=hot_deal.get('deal_type', ''), key=f"deal_type_{idx}")
                  hot_deal['description'] = st.text_area("Description", value=hot_deal.get('description', ''), key=f"description_{idx}")
                  hot_deal['marketing_headline'] = st.text_input("Marketing Headline", value=hot_deal.get('marketing_headline', ''), key=f"headline_{idx}")
                  hot_deal['marketing_subtitle'] = st.text_input("Marketing Subtitle", value=hot_deal.get('marketing_subtitle', ''), key=f"subtitle_{idx}")
                  hot_deal['urgency_message'] = st.text_input("Urgency Message", value=hot_deal.get('urgency_message', ''), key=f"urgency_{idx}")
                  hot_deal['original_display_price'] = st.number_input("Original Display Price", value=hot_deal.get('original_display_price', 0.0), key=f"orig_price_{idx}")
                  hot_deal['discounted_display_price'] = st.number_input("Discounted Display Price", value=hot_deal.get('discounted_display_price', 0.0), key=f"disc_price_{idx}")
                  hot_deal['savings_percentage'] = st.number_input("Savings Percentage", value=hot_deal.get('savings_percentage', 0.0), key=f"savings_{idx}")
                  hot_deal['valid_from'] = st.text_input("Valid From (YYYY-MM-DD)", value=hot_deal.get('valid_from', ''), key=f"valid_from_{idx}")
                  hot_deal['valid_until'] = st.text_input("Valid Until (YYYY-MM-DD)", value=hot_deal.get('valid_until', ''), key=f"valid_until_{idx}")
                  hot_deal['booking_deadline'] = st.text_input("Booking Deadline (YYYY-MM-DD)", value=hot_deal.get('booking_deadline', ''), key=f"booking_deadline_{idx}")
                  hot_deal['minimum_nights'] = st.number_input("Minimum Nights", value=hot_deal.get('minimum_nights', 1), key=f"min_nights_{idx}", step=1)
                  hot_deal['maximum_nights'] = st.number_input("Maximum Nights", value=hot_deal.get('maximum_nights', 1), key=f"max_nights_{idx}", step=1)
                  hot_deal['travel_dates_from'] = st.text_input("Travel Dates From (YYYY-MM-DD)", value=hot_deal.get('travel_dates_from', ''), key=f"travel_from_{idx}")
                  hot_deal['travel_dates_until'] = st.text_input("Travel Dates Until (YYYY-MM-DD)", value=hot_deal.get('travel_dates_until', ''), key=f"travel_until_{idx}")

                  # Editable hotel info
                  # st.markdown("**Hotel Information**")
                  # hotel = hot_deal.get('hotel', {})
                  # hotel['name'] = st.text_input("Hotel Name", value=hotel.get('name', ''), key=f"hotel_name_{idx}")
                  # hotel['address'] = st.text_input("Hotel Address", value=hotel.get('address', ''), key=f"hotel_address_{idx}")
                  # hotel['rating'] = st.number_input("Hotel Rating", value=hotel.get('rating', 0.0), key=f"hotel_rating_{idx}")
                  # hotel['price'] = st.number_input("Hotel Price", value=hotel.get('price', 0.0), key=f"hotel_price_{idx}")
                  # hotel['image'] = st.text_input("Hotel Image URL", value=hotel.get('image', ''), key=f"hotel_image_{idx}")
                  # hotel['url'] = st.text_input("Hotel URL", value=hotel.get('url', ''), key=f"hotel_url_{idx}")
                  # hotel['description'] = st.text_area("Hotel Description", value=hotel.get('description', ''), key=f"hotel_desc_{idx}")
                  # hot_deal['hotel'] = hotel

                  # Deal Inclusions
                  st.markdown("**Deal Inclusions**")
                  deal_inclusions = hot_deal.get('deal_inclusions', [])
                  for i, inclusion in enumerate(deal_inclusions):
                      st.markdown(f"*Inclusion {i+1}*")
                      inclusion['title'] = st.text_input("Inclusion Title", value=inclusion.get('title', ''), key=f"inc_title_{idx}_{i}")
                      inclusion['description'] = st.text_area("Inclusion Description", value=inclusion.get('description', ''), key=f"inc_desc_{idx}_{i}")
                      inclusion['category'] = st.text_input("Inclusion Category", value=inclusion.get('category', ''), key=f"inc_cat_{idx}_{i}")
                  hot_deal['deal_inclusions'] = deal_inclusions

                  # Meal Plans
                  st.markdown("**Meal Plans**")
                  meal_plans = hot_deal.get('meal_plans', [])
                  if not meal_plans:
                      st.markdown("No meal plans found")
                  else:
                    for i, meal in enumerate(meal_plans):
                        st.markdown(f"*Meal Plan {i+1}*")
                        meal['name'] = st.text_input("Meal Plan Name", value=meal.get('name', ''), key=f"meal_name_{idx}_{i}")
                        meal['adult_price'] = st.number_input("Adult Price", value=meal.get('adult_price', 0.0) if meal.get('adult_price') is not None else 0.0, key=f"meal_adult_{idx}_{i}")
                        meal['child_price'] = st.number_input("Child Price", value=meal.get('child_price', 0.0) if meal.get('child_price') is not None else 0.0, key=f"meal_child_{idx}_{i}")
                        meal['infant_free'] = st.checkbox("Infant Free", value=meal.get('infant_free', False), key=f"meal_infant_{idx}_{i}")
                        meal['description'] = st.text_area("Meal Plan Description", value=meal.get('description', ''), key=f"meal_desc_{idx}_{i}")
                    hot_deal['meal_plans'] = meal_plans

                  # Special Offers
                  st.markdown("**Special Offers**")
                  special_offers = hot_deal.get('special_offers', [])
                  for i, offer in enumerate(special_offers):
                      st.markdown(f"*Special Offer {i+1}*")
                      offer['code'] = st.text_input("Offer Code", value=offer.get('code', ''), key=f"offer_code_{idx}_{i}")
                      offer['title'] = st.text_input("Offer Title", value=offer.get('title', ''), key=f"offer_title_{idx}_{i}")
                      offer['description'] = st.text_area("Offer Description", value=offer.get('description', ''), key=f"offer_desc_{idx}_{i}")
                      offer['min_nights'] = st.number_input("Min Nights", value=offer.get('min_nights', 1), key=f"offer_min_nights_{idx}_{i}", step=1)
                      offer['max_free_nights'] = st.number_input("Max Free Nights", value=offer.get('max_free_nights', 0), key=f"offer_max_free_{idx}_{i}", step=1)
                      offer['valid_from'] = st.text_input("Offer Valid From (YYYY-MM-DD)", value=offer.get('valid_from', ''), key=f"offer_valid_from_{idx}_{i}")
                      offer['valid_until'] = st.text_input("Offer Valid Until (YYYY-MM-DD)", value=offer.get('valid_until', ''), key=f"offer_valid_until_{idx}_{i}")
                  hot_deal['special_offers'] = special_offers

                  # Wedding Packages
                  st.markdown("**Wedding Packages**")
                  wedding_packages = hot_deal.get('wedding_packages', [])
                  for i, wedding in enumerate(wedding_packages):
                      st.markdown(f"*Wedding Package {i+1}*")
                      wedding['name'] = st.text_input("Wedding Package Name", value=wedding.get('name', ''), key=f"wed_name_{idx}_{i}")
                      wedding['base_price'] = st.number_input("Base Price", value=wedding.get('base_price', 0.0) if wedding.get('base_price') is not None else 0.0, key=f"wed_base_{idx}_{i}")
                      wedding['comissionable'] = st.checkbox("Comissionable", value=wedding.get('comissionable', False), key=f"wed_comm_{idx}_{i}")
                      wedding['min_guests'] = st.number_input("Min Guests", value=wedding.get('min_guests', 2), key=f"wed_min_guests_{idx}_{i}", step=1)
                      wedding['description'] = st.text_area("Wedding Description", value=wedding.get('description', ''), key=f"wed_desc_{idx}_{i}")
                      wedding['code'] = st.text_input("Wedding Code", value=wedding.get('code', ''), key=f"wed_code_{idx}_{i}")
                  hot_deal['wedding_packages'] = wedding_packages
          
          st.download_button(
              label="Download as JSON",
              data=json.dumps({"hot_deals": hot_deals_list}, indent=2),
              file_name="hot_deals.json",
              mime="application/json",
              type="primary",  # This makes the button red in Streamlit
          )
