from pydantic import BaseModel
from datetime import datetime, timedelta
from datetime import date as date_type

from enum import Enum

class DealType(Enum):
  LIMITED_TIME = 'limited_time'
  PRICE_DROP = 'price_drop'
  POPULAR_CHOICE = 'popular_choice'
  EXCLUSIVE_ACCESS = 'exclusive_access'
  BEST_VALUE = 'best_value'
  TRENDING = 'trending'
  SEASONAL_SPECIAL = 'seasonal_special'
  WEEKEND_ESCAPE = 'weekend_escape'
  EXTENDED_STAY = 'extended_stay'
  FLIGHT_PACKAGE = 'flight_package'


class DealInclusionType(Enum):
  BONUS = 'bonus'
  MEAL = 'meal'
  ACTIVITY = 'activity'
  LOYALTY = 'loyalty'
  HONEYMOON = 'honeymoon'


class Hotel(BaseModel):
  name: str
  address: str
  rating: float
  price: float
  image: str
  url: str
  description: str


class HotDeal(BaseModel):
  name: str
  deal_type: str
  hotel: Hotel
  description: str
  marketing_headline: str
  marketing_subtitle: str
  urgency_message: str
  original_display_price: float
  discounted_display_price: float
  savings_percentage: float
  valid_from: date_type
  valid_until: date_type
  booking_deadline: date_type
  minimum_nights: int
  maximum_nights: int
  travel_dates_from: date_type
  travel_dates_until: date_type


class DealInclusion(BaseModel):
  hot_deal: HotDeal
  title: str
  description: str
  category: DealInclusionType


class MealPlan(BaseModel):
    hot_deal: HotDeal
    name: str
    adult_price: float | None = None
    child_price: float | None = None
    infant_free: bool = False
    description: str | None = None

    def __str__(self):
        return f"{self.hot_deal.name} - {self.name}"


class SpecialOffer(BaseModel):
    hot_deal: HotDeal
    code: str | None = None
    title: str | None = None
    description: str | None = None
    min_nights: int = 1
    max_free_nights: int = 0
    combined_with: list['SpecialOffer'] = []
    valid_from: date_type | None = None
    valid_until: date_type | None = None

    def __str__(self):
        return f"{self.hot_deal.name} - {self.title}"


class WeddingPackage(BaseModel):
    hot_deal: HotDeal
    name: str
    base_price: float | None = None
    comissionable: bool = False
    min_guests: int = 2
    description: str | None = None

    def __str__(self):
        return f"{self.hot_deal.name} - {self.name}"


class HotDealPackage(BaseModel):
  hot_deal: HotDeal
  meal_plans: list[MealPlan] = []
  special_offers: list[SpecialOffer] = []
  wedding_packages: list[WeddingPackage] = []

  def __str__(self):
    return f"Hot Deal Package: {self.hot_deal}"