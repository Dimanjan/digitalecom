from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Streaming Services",
            slug="streaming-services",
            description="Music and video streaming platforms"
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Streaming Services")

    def test_category_slug(self):
        self.assertEqual(self.category.slug, "streaming-services")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Streaming Services",
            slug="streaming-services"
        )
        self.product = Product.objects.create(
            name="Spotify Premium",
            slug="spotify-premium",
            description="Premium music streaming service",
            price=9.99,
            category=self.category,
            stock=100
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Spotify Premium")

    def test_product_price(self):
        self.assertEqual(self.product.price, 9.99)

    def test_product_category_relation(self):
        self.assertEqual(self.product.category, self.category)


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Streaming Services",
            slug="streaming-services"
        )
        self.product = Product.objects.create(
            name="Spotify Premium",
            slug="spotify-premium",
            description="Premium music streaming service",
            price=9.99,
            category=self.category,
            stock=100,
            is_active=True
        )

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_product_detail(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Spotify Premium")
        self.assertEqual(float(response.data['price']), 9.99)

    def test_featured_products(self):
        # Create more products
        for i in range(10):
            Product.objects.create(
                name=f"Product {i}",
                slug=f"product-{i}",
                description=f"Description {i}",
                price=10.00 + i,
                category=self.category,
                stock=50,
                is_active=True
            )
        
        url = reverse('product-featured')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data), 8)

    def test_search_products(self):
        url = reverse('product-list')
        response = self.client.get(url, {'search': 'Spotify'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_inactive_product_not_listed(self):
        self.product.is_active = False
        self.product.save()
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Streaming Services",
            slug="streaming-services",
            description="Music and video streaming"
        )

    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_category_detail(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Streaming Services")

