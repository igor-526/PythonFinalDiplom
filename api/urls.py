from django.urls import path
from api.views import PartnerUpdate

apiurlpatterns = [
    path('partner/update/', PartnerUpdate.as_view()),  # импорт товаров
]
