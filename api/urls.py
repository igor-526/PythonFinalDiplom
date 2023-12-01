from django.urls import path
from api.views import PartnerUpdate, Shops, Products

apiurlpatterns = [
    path('partner/update/', PartnerUpdate.as_view()),  # импорт товаров
    path('shops/', Shops.as_view()),  # просмотр магазинов
    path('products/', Products.as_view())  # просмотр всех товаров
]
