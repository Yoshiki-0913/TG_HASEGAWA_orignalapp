# from django.shortcuts import render
# from django.views.generic import ListView
# from .models import ProductInfo
# Create your views here.

from django.views.generic import ListView
from .models import ProductInfo, CategoryInfo
from django.db.models import Q
import uuid
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views import View
from square.client import Client

class ProductListView(ListView):
    model = ProductInfo
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10  # 1ページあたり10件表示

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        category_id = self.request.GET.get('category', '')

        if search_query:
            queryset = queryset.filter(Q(product_name__icontains=search_query))

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryInfo.objects.all()  # カテゴリ一覧を取得
        return context


class ConfirmView(TemplateView):
    template_name = "confirm.html"

class ProcessPaymentView(View):
    def post(self, request, *args, **kwargs):
        # Square Clientの初期化
        client = Client(
            access_token=settings.SQUARE_ACCESS_TOKEN,
            environment='sandbox',  # 本番環境の場合は 'production'
        )
        
        data = json.loads(request.body)
        amount = int(data.get('amount')) * 100  # 金額を整数で処理 (例: 800円 → 80000)
        nonce = data.get('nonce')

        body = {
            "source_id": nonce,
            "amount_money": {
                "amount": amount,
                "currency": "JPY",
            },
            "idempotency_key": str(uuid.uuid4()),  # 冪等性キー
        }

        # 決済リクエスト
        result = client.payments.create_payment(body)
        if result.is_success():
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": result.errors}, status=400)
