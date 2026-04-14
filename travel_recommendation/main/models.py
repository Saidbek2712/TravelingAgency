"""
Models for the travel recommendation app.

Category, BudgetCategory, Destination, Hotel, Booking, UserPreference.
"""

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """A travel preference category (e.g. Mountains, Beach, Cities)."""
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class BudgetCategory(models.Model):
    """A price tier for destinations."""
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Budget Categories'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class Destination(models.Model):
    """A travel destination card."""
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(max_length=500)
    budget_category = models.ForeignKey(
        BudgetCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='destinations',
    )
    budget_category_old = models.CharField(max_length=10, blank=True, default='')
    tags = models.ManyToManyField(Category, blank=True, related_name='destinations')
    # Base price per day in USD
    base_price_per_day = models.DecimalField(
        max_digits=8, decimal_places=2, default=50.00,
        help_text="Base price per day in USD"
    )

    class Meta:
        ordering = ['country', 'name']

    def __str__(self):
        return f"{self.name}, {self.country}"

    def get_tags_list(self):
        return list(self.tags.values_list('name', flat=True))

    def get_budget_category_display(self):
        if self.budget_category:
            return self.budget_category.name
        return self.budget_category_old or '—'


class Hotel(models.Model):
    """A hotel at a destination."""
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='hotels'
    )
    name = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(
        default=3, help_text="Star rating 1-5"
    )
    phone = models.CharField(max_length=50, blank=True, default='')
    address = models.CharField(max_length=300, blank=True, default='')
    price_modifier = models.DecimalField(
        max_digits=4, decimal_places=2, default=1.0,
        help_text="Multiplier for destination base price (e.g. 1.5 = 50% more)"
    )

    class Meta:
        ordering = ['-rating', 'name']

    def __str__(self):
        return f"{self.name} ({'★' * self.rating}) – {self.destination.name}"


class Booking(models.Model):
    """A user's booking for a destination."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    num_days = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone = models.CharField(max_length=50, blank=True, default='', help_text="User phone")
    full_name = models.CharField(max_length=200, blank=True, default='', help_text="User full name")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} → {self.destination.name} ({self.start_date})"

    @property
    def end_date(self):
        from datetime import timedelta
        return self.start_date + timedelta(days=self.num_days - 1)


class UserPreference(models.Model):
    """Stores a user's recommendation query."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    budget = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    preferences = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        budget_name = self.budget.name if self.budget else '—'
        return f"{self.user.username} – {budget_name} ({self.created_at:%Y-%m-%d})"
