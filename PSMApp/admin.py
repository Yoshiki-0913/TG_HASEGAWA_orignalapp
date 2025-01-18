from django.contrib import admin
from .models import CategoryInfo, ProductInfo, SettlementInfo, SettlementProductList, EmployeeInfo

class CategoryInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at', 'updated_at')

class ProductInfoAdmin(admin.ModelAdmin):
    # list_display = ('id', 'product_name', 'unit_price', 'category', 'product_image_tag', 'created_at', 'updated_at')
    list_display = ('id', 'product_name', 'unit_price', 'category', 'created_at', 'updated_at')

    # def product_image_tag(self, obj):
    #     if obj.product_image:
    #         return format_html('<img src="{}" width="50" height="50" />', obj.product_image.url)
    #     return 'No Image'

    # product_image_tag.short_description = 'Product Image'
class SettlementInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'settlement_date', 'settlement_amount', 'settlement_method')

class SettlementProductListAdmin(admin.ModelAdmin):
    list_display = ('id', 'settlement', 'product', 'created_at', 'updated_at')

class EmployeeInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'admin_privileges', 'created_at', 'updated_at')

admin.site.register(CategoryInfo, CategoryInfoAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(SettlementInfo, SettlementInfoAdmin)
admin.site.register(SettlementProductList, SettlementProductListAdmin)
admin.site.register(EmployeeInfo, EmployeeInfoAdmin)
