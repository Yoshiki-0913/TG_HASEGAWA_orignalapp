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
<<<<<<< HEAD
from PSMApp import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('PSMApp.urls')),
=======
from django.urls import path
from PSMApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('confirm', views.ConfirmView.as_view(), name="confirm"),
    path('process_payment/', views.ProcessPaymentView.as_view(), name='process_payment'),  # 決済処理
>>>>>>> f1aba63ceff0ba09c596aca8c57e2105c705a08d
]

# 開発環境でのメディアファイルの配信設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)