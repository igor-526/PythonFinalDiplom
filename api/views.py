from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from api.tasks import partner_update
from api.models import Shop, ProductInfo
from api.serializers import ShopSerializer, ProductInfoSerializer


class PartnerUpdate(APIView):
    """
    View для импорта товаров
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': "Пользователь не авторизован"})
        elif request.user.type == "buyer":
            return JsonResponse({"status": "Ошибка: функция доступна только для магазинов"})
        elif not request.FILES.get("update"):
            return JsonResponse({"status": "Ошибка: файл не получен. Отправить файл можно используя form-data "
                                           "под названием 'update'"})
        else:
            status = partner_update(request.FILES.get("update"), request.user)
            return JsonResponse(status)


class Shops(ListAPIView):
    """
    View для росмотра магазинов
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ShopSerializer(queryset, many=True)
        return Response(serializer.data)


class Products(ListAPIView):
    """
    View для просмтора списка товаров
    """
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductInfoSerializer(queryset, many=True)
        return Response(serializer.data)
