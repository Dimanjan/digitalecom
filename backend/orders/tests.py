from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order, OrderItem


class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            total_amount=29.97,
            status="pending"
        )

    def test_order_str(self):
        self.assertIn("Order #", str(self.order))
        self.assertIn("john@example.com", str(self.order))

    def test_order_status(self):
        self.assertEqual(self.order.status, "pending")


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            total_amount=29.97
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product_name="Spotify Premium",
            product_price=9.99,
            quantity=3,
            subtotal=29.97
        )

    def test_order_item_str(self):
        self.assertIn("Spotify Premium", str(self.order_item))
        self.assertIn("x3", str(self.order_item))


class OrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            "customer_name": "Jane Doe",
            "customer_email": "jane@example.com",
            "items": [
                {
                    "product_name": "Spotify Premium",
                    "product_price": "9.99",
                    "quantity": 1
                },
                {
                    "product_name": "ChatGPT Plus",
                    "product_price": "20.00",
                    "quantity": 1
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['customer_email'], "jane@example.com")
        self.assertEqual(float(response.data['total_amount']), 29.99)
        self.assertEqual(len(response.data['items']), 2)

    def test_list_orders(self):
        Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            total_amount=9.99
        )
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_order_detail(self):
        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            total_amount=9.99
        )
        OrderItem.objects.create(
            order=order,
            product_name="Spotify Premium",
            product_price=9.99,
            quantity=1,
            subtotal=9.99
        )
        url = reverse('order-detail', kwargs={'pk': order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_email'], "john@example.com")
        self.assertEqual(len(response.data['items']), 1)

