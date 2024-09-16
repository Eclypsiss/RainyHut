from rest_framework import serializers
from .models import Dishes, Table, Takeaway, Order, Material, Expense, OrderItem, Cook, Procure


class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ['DishesID', 'DishesName', 'Description', 'DishesPrice',
                  'MeatNeed', 'VegetableNeed', 'SeafoodNeed', 'Pictures', 'cookable', 'DishesType']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['TableID', 'TableNumber', 'TableStatus']


class TakeawaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Takeaway
        fields = ['TakeawayID', 'TakeawayAdd']


class OrderSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['OrderID', 'Takeaway', 'Table', 'TotalAmount', 'OrderStatus', 'OrderType']

    def validate(self, attrs):
        takeaway = attrs.get('Takeaway')
        table = attrs.get('Table')

        if takeaway is None and table is None:
            raise serializers.ValidationError("一个订单必须指向外卖或堂食中的一个。")

        if (takeaway is not None) != (table is not None):
            return attrs

        raise serializers.ValidationError("一个订单只能指向一个外卖或一个堂食。")

    def create(self, validated_data):
        order_instance = Order.objects.create(**validated_data)

        if validated_data.get('Takeaway'):
            order_instance.Takeaway = validated_data['Takeaway']

        order_instance.save()

        return order_instance


class OrderSerializer2(serializers.ModelSerializer):
    Takeaway = TakeawaySerializer()

    class Meta:
        model = Order
        fields = ['OrderID', 'Takeaway', 'Table', 'TotalAmount',
                  'OrderStatus', 'OrderType']

    def validate(self, attrs):
        takeaway = attrs.get('Takeaway')
        table = attrs.get('Table')

        if takeaway is None and table is None:
            raise serializers.ValidationError("一个订单必须指向外卖或堂食中的一个。")

        if (takeaway is not None) ^ (table is not None):
            return attrs

        raise serializers.ValidationError("一个订单只能指向一个外卖或一个堂食。")

    def create(self, validated_data):
        takeaway_data = validated_data.pop('Takeaway', None)
        order_instance = Order.objects.create(**validated_data)

        if takeaway_data:
            takeaway_instance = Takeaway.objects.create(**takeaway_data)
            order_instance.Takeaway = takeaway_instance
            order_instance.save()

        return order_instance


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['MaterialID', 'MaterialName', 'Stock', 'MaterialPrice']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['ExpenseID', 'Order', 'ExpenseType', 'ExpenseAmount', 'Date']


class OrderItemSerializer(serializers.ModelSerializer):
    Dish = DishesSerializer()

    class Meta:
        model = OrderItem
        fields = ['Order', 'Dish', 'Quantity']


class CookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cook
        fields = ['Material', 'Dish']


class ProcureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procure
        fields = ['Material', 'Expense']