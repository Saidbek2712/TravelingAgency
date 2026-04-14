"""
Views for TravelMore.
"""

import json
from decimal import Decimal
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationForm, LoginForm, RecommendationForm
from .models import Destination, UserPreference, Hotel, Booking


def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect(request.GET.get('next', 'home'))
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def recommendations_view(request):
    results = None
    form = RecommendationForm()
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            budget_cat = form.cleaned_data['budget']
            pref_cats  = form.cleaned_data['preferences']
            up = UserPreference.objects.create(user=request.user, budget=budget_cat)
            up.preferences.set(pref_cats)
            results = list(
                Destination.objects
                .filter(budget_category=budget_cat, tags__in=pref_cats)
                .distinct()
            )
            if not results:
                results = list(Destination.objects.filter(budget_category=budget_cat))
    return render(request, 'recommendations.html', {'form': form, 'results': results})


# ─── Booking API ────────────────────────────────────────────────

def api_hotels(request, dest_id):
    """Return hotels for a destination as JSON."""
    hotels = Hotel.objects.filter(destination_id=dest_id).values(
        'id', 'name', 'rating', 'phone', 'address', 'price_modifier'
    )
    return JsonResponse({'hotels': list(hotels)})


@login_required
@require_POST
def api_book(request):
    """Create a Booking from a JSON POST."""
    try:
        data = json.loads(request.body)
        dest = get_object_or_404(Destination, pk=data['dest_id'])
        hotel = get_object_or_404(Hotel, pk=data['hotel_id']) if data.get('hotel_id') else None

        num_days   = int(data['num_days'])
        base_price = dest.base_price_per_day
        modifier   = hotel.price_modifier if hotel else Decimal('1.0')
        total      = base_price * modifier * num_days

        booking = Booking.objects.create(
            user=request.user,
            destination=dest,
            hotel=hotel,
            start_date=data['start_date'],
            num_days=num_days,
            total_price=total,
            phone=data.get('phone', ''),
            full_name=data.get('full_name', request.user.get_full_name() or request.user.username),
        )
        return JsonResponse({
            'ok': True,
            'booking_id': booking.id,
            'total_price': float(total),
        })
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).select_related('destination', 'hotel')
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def booking_pdf(request, booking_id):
    """Generate and return a professional PDF booking confirmation using reportlab."""
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
 
    hotel_name    = booking.hotel.name    if booking.hotel else 'N/A'
    hotel_phone   = booking.hotel.phone   if booking.hotel else 'N/A'
    hotel_address = booking.hotel.address if booking.hotel else 'N/A'
    resort_name   = f"{booking.destination.name}, {booking.destination.country}"
    
    # Try to use reportlab for high-quality PDF
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor, white
        import io

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Colors and Styles
        primary_color = HexColor('#0066ff')
        text_color = HexColor('#1a1a1e')
        muted_color = HexColor('#909099')

        # Header
        c.setFillColor(primary_color)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(width/2, height - 3*cm, "TravelMore")
        
        c.setFont("Helvetica-Oblique", 11)
        c.setFillColor(muted_color)
        c.drawCentredString(width/2, height - 3.7*cm, "Official Booking Confirmation")
        
        c.setStrokeColor(primary_color)
        c.setLineWidth(2)
        c.line(1.5*cm, height - 4.2*cm, width - 1.5*cm, height - 4.2*cm)

        # Content rendering helper
        y = height - 5.5*cm
        def add_section(title):
            nonlocal y
            y -= 0.5*cm
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(primary_color)
            c.drawString(1.5*cm, y, title)
            y -= 0.6*cm
            c.setStrokeColor(HexColor('#eeeeee'))
            c.setLineWidth(0.5)
            c.line(1.5*cm, y, width - 1.5*cm, y)
            y -= 0.8*cm

        def add_row(label, value):
            nonlocal y
            c.setFont("Helvetica", 12)
            c.setFillColor(muted_color)
            c.drawString(1.5*cm, y, label)
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(text_color)
            c.drawString(6*cm, y, str(value))
            y -= 0.8*cm

        # 1. Traveller Information
        add_section("Traveller Information")
        add_row("Full Name:", booking.full_name)
        add_row("Phone:", booking.phone or 'N/A')
        y -= 0.5*cm

        # 2. Trip Details
        add_section("Trip Details")
        add_row("Resort / Dest:", resort_name)
        add_row("Start Date:", booking.start_date.strftime('%d %B %Y'))
        add_row("Duration:", f"{booking.num_days} days")
        add_row("Ends on:", booking.end_date.strftime('%d %B %Y'))
        y -= 0.5*cm

        # 3. Accommodation
        add_section("Accommodation")
        add_row("Hotel:", hotel_name)
        add_row("Hotel Phone:", hotel_phone)
        addr = hotel_address[:55] + ('...' if len(hotel_address) > 55 else '')
        add_row("Address:", addr)
        y -= 0.5*cm

        # 4. Total Summary
        y -= 1*cm
        c.setFillColor(primary_color)
        c.rect(1.5*cm, y - 0.5*cm, width - 3*cm, 1.2*cm, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 15)
        c.drawCentredString(width/2, y, f"TOTAL PAID:  ${booking.total_price:.2f} USD")

        # Footer
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(muted_color)
        c.drawCentredString(width/2, 2*cm, f"Booking ID: #{booking.id} | Issued on {booking.created_at.strftime('%d %B %Y')}")
        c.drawCentredString(width/2, 1.5*cm, "Thank you for choosing TravelMore — Discover the world, one trip at a time.")

        c.showPage()
        c.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="TravelMore_Booking_{booking.id}.pdf"'
        return response

    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)
