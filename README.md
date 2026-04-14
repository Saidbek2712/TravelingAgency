# TravelMore ✈️

TravelMore is a modern, responsive travel recommendation and booking platform built with Django. It features a sleek "liquid glass" (glassmorphism) user interface, dynamic trip recommendations based on user budget and preferences, and a fully functional booking system that generates professional PDF confirmations.

## Features

* **Smart Recommendations**: Users can input their budget tier and preferred vacation types (e.g., Mountains, Beach, Cities) to get curated travel destinations.
* **Modern UI/UX**: The application uses a custom-built, responsive "Glassmorphism" design system with fluid animations and a modern color palette.
* **End-to-End Booking Flow**: 
  * Select a destination and view available hotels.
  * Dynamic price calculation based on base price, hotel modifiers, and duration of stay.
  * Dedicated "My Bookings" dashboard for managing reservations.
* **PDF Confirmations**: Secure, zero-dependency PDF generation (using `reportlab`) that produces professional booking receipts including traveller details, hotel information, and total costs.
* **User Authentication**: Secure registration, login, and session management system.
* **Localization Ready**: Built-in UI language switcher (EN/RU) for the main navigation elements.

## Tech Stack

* **Backend**: Python 3, Django 6.x
* **Database**: SQLite3 (default, configurable to PostgreSQL/MySQL)
* **Frontend**: HTML5, Vanilla CSS3 (Custom Design System), Vanilla JavaScript
* **PDF Generation**: `reportlab`

## Prerequisites

* Python 3.8 or higher
* `pip` (Python package installer)

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/TravelMore.git
   cd TravelMore
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django reportlab
   ```

4. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed the database with sample data**
   *(Note: Ensure you have your `seed_destinations.py` script ready, or add data manually via the admin panel).*
   ```bash
   python manage.py seed_destinations
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Project Structure

```
TravelMore/
├── manage.py
├── travel_recommendation/        # Main Django project settings
└── main/                         # Core application
    ├── migrations/
    ├── static/
    │   ├── css/style.css         # Liquid Glass Design System
    │   └── js/main.js            # Interactive logic & Booking integration
    ├── templates/
    │   ├── base.html             # Base layout & Navigation
    │   ├── home.html             # Landing page
    │   ├── recommendations.html  # Explore & Booking flow
    │   ├── my_bookings.html      # Bookings dashboard
    │   ├── login.html
    │   └── register.html
    ├── models.py                 # DB Schema (Destination, Hotel, Booking, etc.)
    ├── views.py                  # App logic & PDF Generation
    └── urls.py                   # Route definitions
```

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/TravelMore/issues).

