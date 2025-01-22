from django.contrib import admin
from .models import SettlementInfo, EmployeeInfo
from django.urls import path
from django.db.models import Sum
from django.utils.timezone import now, timedelta
import plotly.graph_objects as go
from django.shortcuts import render

# --- ここから棒グラフ --- 
class SettlementInfoAdmin(admin.ModelAdmin):
    list_display = ('employee', 'settlement_date', 'settlement_amount', 'settlement_method')
    list_filter = ('settlement_method',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('weekly-stats/', self.admin_site.admin_view(self.weekly_stats_view), name='weekly-stats'),
        ]
        return custom_urls + urls

    def weekly_stats_view(self, request):
        # 過去1週間のデータを取得
        today = now().date()
        one_week_ago = today - timedelta(days=7)
        settlements = SettlementInfo.objects.filter(
            settlement_date__range=(one_week_ago, today),
            settlement_method='card'
        ).values('settlement_date').annotate(total_amount=Sum('settlement_amount'))

        # データを整形
        dates = [one_week_ago + timedelta(days=i) for i in range(7)]
        date_labels = [date.strftime('%Y-%m-%d') for date in dates]
        data_dict = {s['settlement_date']: s['total_amount'] for s in settlements}
        amounts = [data_dict.get(date, 0) for date in dates]

        # Plotlyで棒グラフを作成
        fig = go.Figure(data=[
            go.Bar(x=date_labels, y=amounts, name='Card Payments')
        ])
        fig.update_layout(
            title='Past Week Card Payments',
            xaxis_title='Date',
            yaxis_title='Amount (¥)',
        )
        graph_html = fig.to_html(full_html=False)

        # テンプレートに渡す
        context = {
            'graph': graph_html,
            'opts': self.model._meta,
        }
        return render(request, 'admin/weekly_stats.html', context)
# --- ここまで棒グラフ --- #

class EmployeeInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'name')

admin.site.register(SettlementInfo, SettlementInfoAdmin)
admin.site.register(EmployeeInfo, EmployeeInfoAdmin)