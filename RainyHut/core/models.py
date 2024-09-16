from django.db import models


class Dishes(models.Model):
    DishesID = models.AutoField(primary_key=True)
    DishesName = models.CharField(max_length=50, blank=True)
    Description = models.TextField(blank=True)
    DishesPrice = models.DecimalField(max_digits=10, decimal_places=2)
    MeatNeed = models.PositiveIntegerField(default=0)
    VegetableNeed = models.PositiveIntegerField(default=0)
    SeafoodNeed = models.PositiveIntegerField(default=0)
    Pictures = models.ImageField(upload_to="Dishes_Pictures", default="default")
    DishesType_CHOICES = [
        ('light_meal', '简餐'),
        ('desserts', '甜品'),
        ('drinks', '饮品'),
        ('the_rest', '其他'),
    ]
    DishesType = models.CharField(max_length=10, choices=DishesType_CHOICES, default='the_rest')

    @property
    def cookable(self):
        return self.is_cookable()

    def is_cookable(self):
        materials_needed = self.get_materials_need()
        for material_type, amount_needed in materials_needed.items():
            try:
                material = Material.objects.get(MaterialName=material_type)
                if material.Stock < amount_needed:
                    return 'no'
            except Material.DoesNotExist:
                return 'no'
        return 'yes'

    def get_materials_need(self):
        return {
            'Meat': self.MeatNeed,
            'Vegetable': self.VegetableNeed,
            'Seafood': self.SeafoodNeed
        }

    def get_details(self):
        return {
            'DishesID': self.DishesID,
            'DishesName': self.DishesName,
            'DishesPrice': str(self.DishesPrice)
        }

    def __str__(self):
        return f"{self.DishesName}"


class Table(models.Model):
    TableID = models.AutoField(primary_key=True)
    TableNumber = models.CharField(max_length=10)
    STATUS_CHOICES1 = [
        ('in_use', '使用中'),
        ('available', '空闲'),
    ]
    TableStatus = models.CharField(max_length=10, choices=STATUS_CHOICES1, default='available')

    def __str__(self):
        return f"Table {self.TableNumber} - Status: {self.TableStatus}"


class Takeaway(models.Model):
    TakeawayID = models.AutoField(primary_key=True)
    TakeawayAdd = models.TextField(blank=False)

    def __str__(self):
        return f"Takeaway ID {self.TakeawayID} - Address: {self.TakeawayAdd}"


class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    # 外键 Takeaway
    Takeaway = models.ForeignKey(Takeaway, on_delete=models.CASCADE, null=True, blank=True)
    # 外键 Table
    Table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES2 = [
        ('in_progress', '进行中'),
        ('finished', '已完成'),
    ]
    STATUS_CHOICES3 = [
        ('takeaway', '外卖'),
        ('dine_in', '堂食'),
    ]
    OrderStatus = models.CharField(max_length=50, choices=STATUS_CHOICES2, default='in_progress')
    OrderType = models.CharField(max_length=10, choices=STATUS_CHOICES3, blank=True, null=True, default=None)

    def clean(self):
        if bool(self.Takeaway) == bool(self.Table):
            raise ValueError("一个订单只能指向一个外卖或一个堂食")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_order_items(self):
        return OrderItem.objects.filter(Order=self).select_related('Dish')

    def __str__(self):
        table_info = f"Table {self.Table.TableNumber}" if self.Table else "No Table Assigned"
        takeaway_info = f"Takeaway ID {self.Takeaway.TakeawayID}" if self.Takeaway else "No Takeaway Assigned"
        return f"Order ID {self.OrderID} - Total: {self.TotalAmount} - Status: {self.OrderStatus} - {table_info} - {takeaway_info}"


class Material(models.Model):
    MaterialID = models.AutoField(primary_key=True)
    MaterialName = models.CharField(max_length=50, blank=True)
    Stock = models.IntegerField()
    MaterialPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.MaterialName} - Stock: {self.Stock}"


class Expense(models.Model):
    ExpenseID = models.AutoField(primary_key=True)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    EXPENSE_TYPE_CHOICES = [
        ('order', '订单费用'),
        ('other', '其他费用'),
    ]
    ExpenseType = models.CharField(max_length=10, choices=EXPENSE_TYPE_CHOICES)
    ExpenseAmount = models.DecimalField(max_digits=10, decimal_places=2)
    Date = models.DateField()

    def __str__(self):
        order_info = f"Order ID {self.Order.OrderID}" if self.Order else "No Order Associated"
        return f"Expense ID {self.ExpenseID} - Type: {self.ExpenseType} - Amount: {self.ExpenseAmount} - Related to {order_info}"


class OrderItem(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    Dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    Quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('Order', 'Dish')

    def save(self, *args, **kwargs):
        if self.pk is None:
            materials_needed = self.Dish.get_materials_need()
            for material_type, amount_needed in materials_needed.items():
                if amount_needed > 0:
                    material = Material.objects.get(MaterialName=material_type)
                    material.Stock -= amount_needed * self.Quantity
                    material.save()
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.Quantity} x {self.Dish} in Order {self.Order}"


class Cook(models.Model):
    Material = models.ForeignKey(Material, on_delete=models.CASCADE)
    Dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('Material', 'Dish')

    def __str__(self):
        return f"Material {self.Material.MaterialName} for Dish {self.Dish.DishesName}"


class Procure(models.Model):
    Material = models.ForeignKey(Material, on_delete=models.CASCADE)
    Expense = models.ForeignKey(Expense, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('Material', 'Expense')

    def __str__(self):
        return f"Procurement of {self.Material.MaterialName} for Expense ID {self.Expense.ExpenseID}"
