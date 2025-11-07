from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_price', 'quantity', 'subtotal']


class OrderItemCreateSerializer(serializers.Serializer):
    """Serializer for creating order items (without subtotal)"""
    product_name = serializers.CharField(max_length=200)
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)


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
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calculate total amount first
        from decimal import Decimal
        total_amount = Decimal('0.00')
        for item_data in items_data:
            price = Decimal(str(item_data['product_price']))
            subtotal = price * item_data['quantity']
            total_amount += subtotal
        
        # Create order with total_amount
        order = Order.objects.create(
            total_amount=total_amount,
            **validated_data
        )
        
        # Create order items
        for item_data in items_data:
            price = Decimal(str(item_data['product_price']))
            subtotal = price * item_data['quantity']
            OrderItem.objects.create(
                order=order,
                product_name=item_data['product_name'],
                product_price=price,
                quantity=item_data['quantity'],
                subtotal=subtotal
            )
        
        return order

