from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Seeds the database with sample products'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories...')
        
        # Create categories
        streaming, _ = Category.objects.get_or_create(
            name="Streaming Services",
            defaults={'slug': 'streaming-services', 'description': 'Music and video streaming platforms'}
        )
        
        ai, _ = Category.objects.get_or_create(
            name="AI Tools",
            defaults={'slug': 'ai-tools', 'description': 'Artificial Intelligence and machine learning tools'}
        )
        
        productivity, _ = Category.objects.get_or_create(
            name="Productivity",
            defaults={'slug': 'productivity', 'description': 'Productivity and business tools'}
        )
        
        self.stdout.write(self.style.SUCCESS('Categories created'))

        # Create products
        products_data = [
            {
                'name': 'Spotify Premium',
                'slug': 'spotify-premium',
                'description': 'Premium music streaming service with ad-free listening, offline downloads, and high-quality audio. Access millions of songs and podcasts.',
                'price': 9.99,
                'category': streaming,
                'stock': 100
            },
            {
                'name': 'ChatGPT Plus',
                'slug': 'chatgpt-plus',
                'description': 'Advanced AI assistant with GPT-4 access, priority support, and faster response times. Perfect for professionals and power users.',
                'price': 20.00,
                'category': ai,
                'stock': 50
            },
            {
                'name': 'Netflix Premium',
                'slug': 'netflix-premium',
                'description': 'Ultra HD streaming on up to 4 devices simultaneously. Watch your favorite shows and movies in the highest quality.',
                'price': 15.99,
                'category': streaming,
                'stock': 75
            },
            {
                'name': 'Adobe Creative Cloud',
                'slug': 'adobe-creative-cloud',
                'description': 'Complete suite of creative tools including Photoshop, Illustrator, Premiere Pro, and more. Perfect for designers and creators.',
                'price': 52.99,
                'category': productivity,
                'stock': 30
            },
            {
                'name': 'YouTube Premium',
                'slug': 'youtube-premium',
                'description': 'Ad-free YouTube experience with background playback, offline downloads, and YouTube Music Premium included.',
                'price': 11.99,
                'category': streaming,
                'stock': 90
            },
            {
                'name': 'Midjourney Subscription',
                'slug': 'midjourney-subscription',
                'description': 'AI-powered image generation tool. Create stunning artwork and images from text descriptions with advanced AI technology.',
                'price': 10.00,
                'category': ai,
                'stock': 40
            },
            {
                'name': 'Notion Pro',
                'slug': 'notion-pro',
                'description': 'All-in-one workspace for notes, docs, databases, and collaboration. Organize your work and life in one place.',
                'price': 8.00,
                'category': productivity,
                'stock': 60
            },
            {
                'name': 'Disney+ Premium',
                'slug': 'disney-plus-premium',
                'description': 'Stream Disney, Pixar, Marvel, Star Wars, and National Geographic content in 4K Ultra HD with HDR.',
                'price': 10.99,
                'category': streaming,
                'stock': 80
            },
        ]

        self.stdout.write('Creating products...')
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Already exists: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

