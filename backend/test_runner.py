"""
Custom test runner to organize and run all tests
"""
import os
import sys
from django.test.utils import get_runner
from django.conf import settings

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ecomdigital.settings'
    import django
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests([
        'products.tests',
        'orders.tests',
        'authentication.tests',
        'reviews.tests',
    ])
    
    if failures:
        sys.exit(bool(failures))

