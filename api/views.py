from django.http import JsonResponse
from rest_framework.views import APIView
from api.tasks import partner_update


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
