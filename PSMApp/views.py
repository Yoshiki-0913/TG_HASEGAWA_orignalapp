# from django.shortcuts import render
# from django.views.generic import ListView
# from .models import ProductInfo
# Create your views here.

from django.views.generic import ListView
from django.shortcuts import render
from .models import ProductInfo, CategoryInfo, SettlementInfo,SettlementProductList
from django.db.models import Q
import uuid
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views import View
from square.client import Client
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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

        return queryset.order_by('created_at')  # 並び替えを追加
    
    '''
    def settlement_selection_view(request):
        payment_methods = SettlementInfo.PAYMENT_METHOD_CHOICES  # 選択肢を取得
        context = {
            'payment_methods': payment_methods,  # テンプレートに渡す
        }
        return render(request, 'product_list.html', context)
    '''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = CategoryInfo.objects.all()  # カテゴリ一覧を取得
        context['payment_methods'] = SettlementInfo.PAYMENT_METHOD_CHOICES
        return context
    
class ConfirmView(TemplateView):
    template_name = "confirm.html"

    def post(self, request, *args, **kwargs):
        settlement_method = request.POST.get('settlement', '')

        context = self.get_context_data()
        context['method'] = 'カード決済' if settlement_method == 'card' else '現金決済' if settlement_method == 'cash' else '未選択'
        return render(request, self.template_name, context)

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
        
@method_decorator(csrf_exempt, name='dispatch')  # AJAXリクエスト用にCSRFを無効化
def handle_cash_settlement(request):
    if request.method == 'POST':
        try:
            # POSTデータの読み込み
            body = json.loads(request.body)
            employee_id = body.get('employee')
            settlement_amount = body.get('settlement_amount')
            settlement_method = body.get('settlement_method')
            selected_products = body.get('selected_products', [])

            # 合計金額を取得し数値型に変換
            settlement_amount = float(settlement_amount) if settlement_amount else 0  # 数値に変換


            # エラー処理: 金額が無効の場合
            if settlement_amount <= 0:
                return JsonResponse({'status': 'error', 'message': settlement_amount })
            if not settlement_method:
                return JsonResponse({'status': 'error', 'message': '決済方法を選択してください。'})
            
            # SettlementInfoの作成
            settlement = SettlementInfo.objects.create(
                employee_id=employee_id,
                settlement_amount=settlement_amount,
                settlement_method=settlement_method
            )

            # 選択された商品をSettlementProductListに登録
            for product_id, quantity in selected_products:
                product = ProductInfo.objects.get(id=product_id)
                SettlementProductList.objects.create(
                    settlement=settlement,
                    product=product,
                    quantity=quantity
                )

            # # その他の処理
            # selected_products = body.get('selected_products', [])

            # settlement = SettlementInfo.objects.create(
            #     employee=request.user,
            #     settlement_amount=settlement_amount,
            #     settlement_method='cash'
            # )

            # for product_id, quantity in selected_products:
            #     product = ProductInfo.objects.get(id=product_id)
            #     SettlementProductList.objects.create(
            #         settlement=settlement,
            #         product=product,
            #         quantity=quantity
            #     )

            return JsonResponse({'status': 'success', 'message': '現金決済が完了しました！'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': '無効なリクエストです。'})
