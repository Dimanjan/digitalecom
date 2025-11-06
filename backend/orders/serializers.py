from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_price', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'customer_email',
            'total_amount', 'status', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        total_amount = 0
        for item_data in items_data:
            subtotal = item_data['product_price'] * item_data['quantity']
            total_amount += subtotal
            OrderItem.objects.create(order=order, **item_data, subtotal=subtotal)
        
        order.total_amount = total_amount
        order.save()
        return order

