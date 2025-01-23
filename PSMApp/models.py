from django.db import models
# カテゴリモデル
class CategoryInfo(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name
# 商品モデル
class ProductInfo(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(CategoryInfo, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
# 決済情報モデル
class SettlementInfo(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', '現金決済'),
        ('card', 'カード決済'),
    ]
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey('EmployeeInfo', on_delete=models.CASCADE)
    settlement_date = models.DateField()
    settlement_amount = models.DecimalField(max_digits=15, decimal_places=2)
    settlement_method = models.CharField(
        max_length=255,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',  # デフォルト値を指定
    )
    def __str__(self):
        return f"Settlement {self.id} by {self.employee.name}"
# 決済商品一覧モデル
class SettlementProductList(models.Model):
    id = models.AutoField(primary_key=True)
    settlement = models.ForeignKey(SettlementInfo, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settlement {self.settlement.id} - Product {self.product.product_name}"
# 従業員モデル
class EmployeeInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_privileges = models.BooleanField(default=False)

    def __str__(self):
        return self.name