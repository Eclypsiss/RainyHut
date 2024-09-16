from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import DishesSerializer
from rest_framework import generics
from rest_framework.response import Response
from .models import Order, Table, OrderItem, Dishes, Takeaway, Expense, Material
from .serializers import OrderSerializer1, OrderSerializer2
from .serializers import TakeawaySerializer
from .serializers import ExpenseSerializer, TableSerializer, MaterialSerializer
from decimal import Decimal
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view


@csrf_exempt
def dishes(request):
    if request.method == 'GET':
        dishes = Dishes.objects.all()
        serializer = DishesSerializer(dishes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DishesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def dishes_detail(request, pk):
    try:
        dish = Dishes.objects.get(pk=pk)
    except Dishes.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DishesSerializer(dish, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        dish.delete()
        return HttpResponse(status=204)


@csrf_exempt
def takeaway(request):
    if request.method == 'GET':
        takeaways = Takeaway.objects.all()
        serializer = TakeawaySerializer(takeaways, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TakeawaySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def takeaway_detail(request, pk):
    try:
        takeaway = Takeaway.objects.get(pk=pk)
    except Takeaway.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TakeawaySerializer(takeaway, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        takeaway.delete()
        return HttpResponse(status=204)


@csrf_exempt
def order(request):

    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer2(orders, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        order_data = {
            "OrderType": data.get("order_type"),
            "TotalAmount": data.get("total_amount"),
            "Takeaway": data.get("takeaway_id"),
            "Table": data.get("table_id")
        }

        serializer = OrderSerializer1(data=order_data)

        if serializer.is_valid():
            order_instance = serializer.save()

            items = data.get("items", [])
            for item in items:
                dish_id = item["id"]
                quantity = item["quantity"]
                OrderItem.objects.create(Order=order_instance, Dish_id=dish_id, Quantity=quantity)

            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = OrderSerializer1(order, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        order.delete()
        return HttpResponse(status=204)


class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer1

    def post(self, request, *args, **kwargs):
        order_type = request.data.get('order_type')
        table_id = request.data.get('table_id')
        takeaway_id = request.data.get('takeaway_id')
        total_amount = request.data.get('total_amount')
        items = request.data.get('items')

        if order_type not in ['takeaway', 'dine_in']:
            return Response({"error": "Invalid order type."}, status=400)

        try:
            takeaway = None
            table = None

            if order_type == 'takeaway':
                takeaway = Takeaway.objects.get(TakeawayID=takeaway_id)

            if order_type == 'dine_in':
                table = Table.objects.get(TableID=table_id)

            order = Order.objects.create(
                Takeaway=takeaway,
                Table=table,
                TotalAmount=Decimal(total_amount),
                OrderType=order_type,
            )

            for item in items:
                dish_id = item.get('id')
                quantity = item.get('quantity', 1)

                dish = Dishes.objects.get(DishesID=dish_id)
                OrderItem.objects.create(Order=order, Dish=dish, Quantity=quantity)

            return Response(OrderSerializer1(order).data, status=201)

        except Takeaway.DoesNotExist:
            return Response({"error": "Takeaway does not exist."}, status=404)
        except Table.DoesNotExist:
            return Response({"error": "Table does not exist."}, status=404)
        except Dishes.DoesNotExist:
            return Response({"error": "Dish does not exist."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TableStatusView(generics.RetrieveUpdateAPIView):
    queryset = Table.objects.all()

    def get(self, request, *args, **kwargs):
        table_id = kwargs.get('pk')
        try:
            table = self.queryset.get(TableID=table_id)
            return Response({"status": table.TableStatus}, status=200)
        except Table.DoesNotExist:
            return Response({"error": "Table does not exist."}, status=404)

    def put(self, request, *args, **kwargs):
        table_id = kwargs.get('pk')
        try:
            table = self.queryset.get(TableID=table_id)
            new_status = request.data.get('TableStatus')
            if new_status in ['in_use', 'available']:
                table.TableStatus = new_status
                table.save()
                return Response({"status": "Table status updated successfully."}, status=200)
            else:
                return Response({"error": "Invalid status."}, status=400)
        except Table.DoesNotExist:
            return Response({"error": "Table does not exist."}, status=404)


class OrderDetailViewSet(viewsets.ViewSet):
    def retrieve(self, request, order_id=None):
        try:
            order = Order.objects.get(OrderID=order_id)
            order_items = order.get_order_items()
            data = {
                'OrderID': order.OrderID,
                'TotalAmount': str(order.TotalAmount),
                'OrderStatus': order.OrderStatus,
                'Dishes': [
                    {
                        'DishID': item.Dish.DishesID,
                        'DishName': item.Dish.DishesName,
                        'Quantity': item.Quantity,
                        'DishPrice': str(item.Dish.DishesPrice),
                    }
                    for item in order_items
                ]
            }
            return Response(data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

    def update(self, request, order_id=None):
        try:
            order = Order.objects.get(OrderID=order_id)
            order.OrderStatus = request.data.get('OrderStatus', order.OrderStatus)
            order.save()
            return Response({"status": "订单状态已更新"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': '订单未找到'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def expense(request):
    if request.method == 'GET':
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ExpenseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def tables(request):
    if request.method == 'GET':
        tables = Table.objects.all()
        serializer = TableSerializer(tables, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def materials(request):
    if request.method == 'GET':
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MaterialSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class TableOrdersView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        table_id = kwargs.get('pk')
        try:
            orders = Order.objects.filter(Table__TableID=table_id, OrderStatus='in_progress')

            order_details = []
            for order in orders:
                order_items = order.get_order_items()
                items_details = []
                for item in order_items:
                    items_details.append({
                        'DishName': item.Dish.DishesName,
                        'Quantity': item.Quantity,
                        'DishPrice': str(item.Dish.DishesPrice),
                    })

                order_details.append({
                    'OrderID': order.OrderID,
                    'TotalAmount': str(order.TotalAmount),
                    'Dishes': items_details
                })

            return Response(order_details, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


@api_view(['PUT'])
def update_material(request, material_id):
    material = get_object_or_404(Material, MaterialID=material_id)
    quantity = request.data.get('quantity')

    if quantity is not None:
        original_stock = material.Stock
        material.Stock += quantity
        material.save()

        return Response({'message': '材料数量更新成功', 'new_stock': material.Stock}, status=status.HTTP_200_OK)
    else:
        return Response({'error': '数量不正确'}, status=status.HTTP_400_BAD_REQUEST)