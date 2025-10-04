from django.core.management.base import BaseCommand
from django.utils.text import slugify
from pcapp.models import Category, Company, Product

class Command(BaseCommand):
    help = 'Fixes empty slugs in the database'

    def handle(self, *args, **options):
        # Fix Category slugs
        categories = Category.objects.filter(slug='')
        for category in categories:
            category.slug = slugify(category.name)
            category.save()
            self.stdout.write(self.style.SUCCESS(f'Fixed slug for category: {category.name}'))

        # Fix Company slugs
        companies = Company.objects.filter(slug='')
        for company in companies:
            company.slug = slugify(company.name)
            company.save()
            self.stdout.write(self.style.SUCCESS(f'Fixed slug for company: {company.name}'))

        # Fix Product slugs
        products = Product.objects.filter(slug='')
        for product in products:
            product.slug = slugify(product.name)
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Fixed slug for product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully fixed all empty slugs')) 