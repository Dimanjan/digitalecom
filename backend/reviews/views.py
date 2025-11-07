from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from products.models import Product


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('user', 'product')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def create(self, request, *args, **kwargs):
        # Check if review already exists
        product_id = request.data.get('product')
        if product_id:
            existing_review = Review.objects.filter(
                product_id=product_id,
                user=request.user
            ).first()
            if existing_review:
                return Response(
                    {'error': 'You have already reviewed this product. You can update your existing review instead.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            review = serializer.save(user=request.user)
        except Exception as e:
            if 'UNIQUE constraint' in str(e) or 'unique' in str(e).lower():
                return Response(
                    {'error': 'You have already reviewed this product. You can update your existing review instead.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            raise
        
        # Return full review with ReviewSerializer
        output_serializer = ReviewSerializer(review, context={'request': request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def product_reviews(self, request):
        """Get reviews for a specific product"""
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response(
                {'error': 'product_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        reviews = self.queryset.filter(product=product)
        serializer = self.get_serializer(reviews, many=True)
        
        # Calculate average rating
        if reviews.exists():
            avg_rating = sum(r.rating for r in reviews) / reviews.count()
            total_reviews = reviews.count()
        else:
            avg_rating = 0
            total_reviews = 0
        
        return Response({
            'reviews': serializer.data,
            'average_rating': round(avg_rating, 2),
            'total_reviews': total_reviews
        })

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_reviews(self, request):
        """Get current user's reviews"""
        reviews = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

