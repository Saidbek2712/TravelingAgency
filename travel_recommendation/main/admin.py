"""Django admin for TravelMore."""

from django.contrib import admin
from .models import Category, BudgetCategory, Destination, Hotel, Booking, UserPreference


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BudgetCategory)
class BudgetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('sort_order',)


class HotelInline(admin.TabularInline):
    model = Hotel
    extra = 1


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'budget_category', 'base_price_per_day')
    list_filter = ('budget_category', 'tags')
    search_fields = ('name', 'country')
    filter_horizontal = ('tags',)
    inlines = [HotelInline]
    exclude = ('budget_category_old',)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'rating', 'phone', 'price_modifier')
    list_filter = ('rating', 'destination')
    search_fields = ('name', 'destination__name')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'destination', 'hotel', 'start_date', 'num_days', 'total_price')
    list_filter = ('start_date', 'destination')
    search_fields = ('full_name', 'phone')
    readonly_fields = ('created_at',)


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget', 'created_at')
    list_filter = ('budget',)
    filter_horizontal = ('preferences',)
