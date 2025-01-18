# from django.shortcuts import render
# from django.views.generic import ListView
# from .models import ProductInfo
# Create your views here.

from django.views.generic import ListView
from .models import ProductInfo, CategoryInfo
from django.db.models import Q

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
