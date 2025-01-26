"""
URL configuration for orignalapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PSMApp import views 
from django.conf import settings
from django.conf.urls.static import static
from PSMApp.views import handle_cash_settlement

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('confirm/', views.ConfirmView.as_view(), name="confirm"),
    path('process_payment/', views.ProcessPaymentView.as_view(), name='process_payment'),  # 決済処理
    path('handle_cash_settlement/', handle_cash_settlement, name='handle_cash_settlement'),
]

# 開発環境でのメディアファイルの配信設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)