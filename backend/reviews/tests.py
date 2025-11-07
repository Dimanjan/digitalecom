from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Category, Product
from .models import Review


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Streaming Services",
            slug="streaming-services"
        )
        self.product = Product.objects.create(
            name="Spotify Premium",
            slug="spotify-premium",
            description="Premium music streaming",
            price=9.99,
            category=self.category,
            stock=100
        )

    def test_create_review(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="Great service!",
            comment="Love this product!"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)

    def test_review_str(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            title="Good",
            comment="Nice"
        )
        self.assertIn("testuser", str(review))
        self.assertIn("Spotify Premium", str(review))

    def test_unique_review_per_user_product(self):
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="First",
            comment="First review"
        )
        # Try to create another review for same user and product
        with self.assertRaises(Exception):
            Review.objects.create(
                product=self.product,
                user=self.user,
                rating=4,
                title="Second",
                comment="Second review"
            )


class ReviewAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Streaming Services",
            slug="streaming-services"
        )
        self.product = Product.objects.create(
            name="Spotify Premium",
            slug="spotify-premium",
            description="Premium music streaming",
            price=9.99,
            category=self.category,
            stock=100
        )

    def test_create_review_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('review-list')
        data = {
            'product': self.product.id,
            'rating': 5,
            'title': 'Excellent!',
            'comment': 'Great product, highly recommend!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)
        self.assertTrue(Review.objects.filter(product=self.product, user=self.user).exists())

    def test_create_review_unauthenticated(self):
        url = reverse('review-list')
        data = {
            'product': self.product.id,
            'rating': 5,
            'title': 'Excellent!',
            'comment': 'Great product!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_product_reviews(self):
        # Create multiple reviews
        user2 = User.objects.create_user(username='user2', password='pass123')
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="Great!",
            comment="Love it"
        )
        Review.objects.create(
            product=self.product,
            user=user2,
            rating=4,
            title="Good",
            comment="Pretty good"
        )
        
        url = reverse('review-product-reviews')
        response = self.client.get(url, {'product_id': self.product.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['reviews']), 2)
        self.assertEqual(response.data['average_rating'], 4.5)
        self.assertEqual(response.data['total_reviews'], 2)

    def test_get_my_reviews(self):
        self.client.force_authenticate(user=self.user)
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="My review",
            comment="My comment"
        )
        
        url = reverse('review-my-reviews')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "My review")

    def test_update_review(self):
        self.client.force_authenticate(user=self.user)
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            title="Old title",
            comment="Old comment"
        )
        
        url = reverse('review-detail', kwargs={'pk': review.pk})
        data = {
            'product': self.product.id,
            'rating': 5,
            'title': 'Updated title',
            'comment': 'Updated comment'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.title, 'Updated title')

    def test_delete_review(self):
        self.client.force_authenticate(user=self.user)
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="To delete",
            comment="Will be deleted"
        )
        
        url = reverse('review-detail', kwargs={'pk': review.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())

    def test_rating_validation(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('review-list')
        data = {
            'product': self.product.id,
            'rating': 6,  # Invalid rating
            'title': 'Test',
            'comment': 'Test comment'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

