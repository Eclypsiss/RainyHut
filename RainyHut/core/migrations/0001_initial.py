# Generated by Django 5.0.7 on 2024-08-05 13:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dishes",
            fields=[
                ("DishesID", models.AutoField(primary_key=True, serialize=False)),
                ("DishesName", models.CharField(blank=True, max_length=50)),
                ("Description", models.TextField(blank=True)),
                ("DishesPrice", models.DecimalField(decimal_places=2, max_digits=10)),
                ("MeatNeed", models.PositiveIntegerField(default=0)),
                ("VegetableNeed", models.PositiveIntegerField(default=0)),
                ("SeafoodNeed", models.PositiveIntegerField(default=0)),
                (
                    "Pictures",
                    models.ImageField(default="default", upload_to="Dishes_Pictures"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Material",
            fields=[
                ("MaterialID", models.AutoField(primary_key=True, serialize=False)),
                ("MaterialName", models.CharField(blank=True, max_length=50)),
                ("Stock", models.IntegerField()),
                ("MaterialPrice", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("OrderID", models.AutoField(primary_key=True, serialize=False)),
                ("TotalAmount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "OrderStatus",
                    models.CharField(
                        choices=[("in_progress", "进行中"), ("finished", "已完成")],
                        default="in_progress",
                        max_length=50,
                    ),
                ),
                (
                    "OrderType",
                    models.CharField(
                        blank=True,
                        choices=[("takeaway", "外卖"), ("dine_in", "堂食")],
                        default=None,
                        max_length=10,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Table",
            fields=[
                ("TableID", models.AutoField(primary_key=True, serialize=False)),
                ("TableNumber", models.CharField(max_length=10)),
                (
                    "TableStatus",
                    models.CharField(
                        choices=[("in_use", "使用中"), ("available", "空闲")],
                        default="available",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Takeaway",
            fields=[
                ("TakeawayID", models.AutoField(primary_key=True, serialize=False)),
                ("TakeawayAdd", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("ExpenseID", models.AutoField(primary_key=True, serialize=False)),
                (
                    "ExpenseType",
                    models.CharField(
                        choices=[("order", "订单费用"), ("other", "其他费用")], max_length=10
                    ),
                ),
                ("ExpenseAmount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("Date", models.DateField()),
                (
                    "Order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.order",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="Table",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.table",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="Takeaway",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.takeaway",
            ),
        ),
        migrations.CreateModel(
            name="Cook",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "Dish",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.dishes"
                    ),
                ),
                (
                    "Material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.material"
                    ),
                ),
            ],
            options={
                "unique_together": {("Material", "Dish")},
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Quantity", models.PositiveIntegerField()),
                (
                    "Dish",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.dishes"
                    ),
                ),
                (
                    "Order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.order"
                    ),
                ),
            ],
            options={
                "unique_together": {("Order", "Dish")},
            },
        ),
        migrations.CreateModel(
            name="Procure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "Expense",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.expense"
                    ),
                ),
                (
                    "Material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.material"
                    ),
                ),
            ],
            options={
                "unique_together": {("Material", "Expense")},
            },
        ),
    ]
