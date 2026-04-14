"""
Management command to seed the database with categories, budget tiers,
and travel destinations.
Run with: python3 manage.py seed_destinations
"""

from django.core.management.base import BaseCommand
from main.models import Category, BudgetCategory, Destination


# ── Categories ──────────────────────────────────────────────────
CATEGORIES = [
    {'slug': 'mountains', 'name': 'Mountains'},
    {'slug': 'beach',     'name': 'Sea / Ocean / Beach'},
    {'slug': 'nature',    'name': 'Nature / Forest / Green Landscapes'},
    {'slug': 'desert',    'name': 'Desert'},
    {'slug': 'cities',    'name': 'Cities'},
    {'slug': 'landmarks', 'name': 'Famous Landmarks / Architecture'},
    {'slug': 'scenic',    'name': 'Scenic Views'},
]

# ── Budget tiers ────────────────────────────────────────────────
BUDGETS = [
    {'slug': 'low',    'name': '$100 – $300',        'sort_order': 1},
    {'slug': 'medium', 'name': '$500 – $1,000',      'sort_order': 2},
    {'slug': 'high',   'name': '$1,500 – $5,000',    'sort_order': 3},
    {'slug': 'luxury', 'name': '$5,000+ (Luxury)',    'sort_order': 4},
]

# ── Destinations ────────────────────────────────────────────────
DESTINATIONS = [
    # LOW
    {'name': 'Samarkand',         'country': 'Uzbekistan',  'budget': 'low',    'tags': ['landmarks','scenic','cities'],
     'description': 'Ancient Silk Road city with stunning Islamic architecture, mosaic-covered madrasas, and vibrant bazaars.',
     'image_url': 'https://images.unsplash.com/photo-1596484552834-6a58f850e0a1?w=800'},
    {'name': 'Tbilisi',           'country': 'Georgia',     'budget': 'low',    'tags': ['mountains','nature','cities','scenic'],
     'description': 'Charming capital nestled in the Caucasus mountains with colorful old town, hot springs, and incredible cuisine.',
     'image_url': 'https://images.unsplash.com/photo-1565008576549-57569a49371d?w=800'},
    {'name': 'Hanoi',             'country': 'Vietnam',     'budget': 'low',    'tags': ['cities','nature','landmarks'],
     'description': 'A bustling capital with French colonial architecture, ancient temples, serene lakes, and legendary street food.',
     'image_url': 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=800'},
    {'name': 'Kathmandu Valley',  'country': 'Nepal',       'budget': 'low',    'tags': ['mountains','nature','scenic','landmarks'],
     'description': 'Gateway to the Himalayas with UNESCO-listed temples, prayer flags, and breathtaking mountain panoramas.',
     'image_url': 'https://images.unsplash.com/photo-1558799401-1dcba79834c2?w=800'},
    {'name': 'Marrakech',         'country': 'Morocco',     'budget': 'low',    'tags': ['desert','cities','landmarks'],
     'description': 'Vibrant medina with colorful souks, ornate palaces, and the edge of the Sahara Desert nearby.',
     'image_url': 'https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=800'},
    {'name': 'Siem Reap',         'country': 'Cambodia',    'budget': 'low',    'tags': ['landmarks','nature','scenic'],
     'description': 'Home to the legendary Angkor Wat temple complex surrounded by lush tropical forests.',
     'image_url': 'https://images.unsplash.com/photo-1508159452718-d22f29e50617?w=800'},
    {'name': 'La Paz',            'country': 'Bolivia',     'budget': 'low',    'tags': ['mountains','scenic','nature'],
     'description': "The world's highest capital city set amid dramatic Andean landscapes and salt flats.",
     'image_url': 'https://images.unsplash.com/photo-1591397179781-be5ccfb55157?w=800'},

    # MEDIUM
    {'name': 'Antalya',           'country': 'Turkey',      'budget': 'medium', 'tags': ['beach','scenic','landmarks'],
     'description': 'Stunning turquoise coast with ancient ruins, perfect beaches, and warm Mediterranean hospitality.',
     'image_url': 'https://images.unsplash.com/photo-1624367171718-14026220e3a0?w=800'},
    {'name': 'Phuket',            'country': 'Thailand',    'budget': 'medium', 'tags': ['beach','nature','scenic'],
     'description': 'Tropical paradise with crystal-clear waters, limestone cliffs, vibrant nightlife, and Thai temples.',
     'image_url': 'https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=800'},
    {'name': 'Bali',              'country': 'Indonesia',   'budget': 'medium', 'tags': ['beach','nature','mountains','scenic'],
     'description': 'Island of gods with terraced rice fields, ancient temples, volcanic mountains, and surf beaches.',
     'image_url': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800'},
    {'name': 'Lisbon',            'country': 'Portugal',    'budget': 'medium', 'tags': ['cities','beach','landmarks','scenic'],
     'description': 'Pastel-colored hillside capital with historic trams, ocean views, and world-class pastéis de nata.',
     'image_url': 'https://images.unsplash.com/photo-1585208798174-6cedd86e019a?w=800'},
    {'name': 'Cape Town',         'country': 'South Africa','budget': 'medium', 'tags': ['mountains','beach','nature','scenic'],
     'description': 'Where Table Mountain meets the ocean — stunning beaches, vineyards, and diverse wildlife.',
     'image_url': 'https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=800'},
    {'name': 'Petra',             'country': 'Jordan',      'budget': 'medium', 'tags': ['desert','landmarks','scenic'],
     'description': 'Rose-red ancient city carved into desert cliffs — one of the New Seven Wonders of the World.',
     'image_url': 'https://images.unsplash.com/photo-1579606032821-4e6161c81f0c?w=800'},
    {'name': 'Costa Rica Rainforest','country': 'Costa Rica','budget': 'medium','tags': ['nature','beach','mountains','scenic'],
     'description': 'Lush cloud forests, exotic wildlife, volcanic hot springs, and pristine Pacific beaches.',
     'image_url': 'https://images.unsplash.com/photo-1518259102261-b40117eabbc4?w=800'},
    {'name': 'Budapest',          'country': 'Hungary',     'budget': 'medium', 'tags': ['cities','landmarks','scenic'],
     'description': 'The Pearl of the Danube with grand thermal baths, ruin bars, and stunning Gothic and Art Nouveau architecture.',
     'image_url': 'https://images.unsplash.com/photo-1541849546-216549ae216d?w=800'},

    # HIGH
    {'name': 'Santorini',         'country': 'Greece',      'budget': 'high',   'tags': ['beach','scenic','landmarks'],
     'description': 'Iconic white-washed villages perched on volcanic cliffs overlooking the deep blue Aegean Sea.',
     'image_url': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800'},
    {'name': 'Swiss Alps',        'country': 'Switzerland', 'budget': 'high',   'tags': ['mountains','scenic','nature'],
     'description': 'Majestic snow-capped peaks, pristine lakes, luxury chalets, and world-class skiing.',
     'image_url': 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=800'},
    {'name': 'Tokyo',             'country': 'Japan',       'budget': 'high',   'tags': ['cities','landmarks','scenic'],
     'description': 'Ultra-modern metropolis blending ancient temples, neon-lit streets, and Michelin-star cuisine.',
     'image_url': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800'},
    {'name': 'Patagonia',         'country': 'Argentina',   'budget': 'high',   'tags': ['mountains','nature','scenic'],
     'description': 'Dramatic glaciers, towering granite peaks, and pristine wilderness at the edge of the world.',
     'image_url': 'https://images.unsplash.com/photo-1531761535209-180857e963b9?w=800'},
    {'name': 'Iceland Ring Road', 'country': 'Iceland',     'budget': 'high',   'tags': ['nature','scenic','beach'],
     'description': 'Land of fire and ice with geysers, waterfalls, black sand beaches, and the Northern Lights.',
     'image_url': 'https://images.unsplash.com/photo-1504829857797-ddff29c27927?w=800'},
    {'name': 'New Zealand South Island','country': 'New Zealand','budget': 'high','tags': ['mountains','nature','scenic'],
     'description': 'Fjords, glaciers, hobbit villages, and some of the most dramatic scenery on Earth.',
     'image_url': 'https://images.unsplash.com/photo-1507699622108-4be3abd695ad?w=800'},

    # LUXURY
    {'name': 'Maldives',          'country': 'Maldives',    'budget': 'luxury', 'tags': ['beach','scenic'],
     'description': 'Overwater villas on crystal-clear turquoise lagoons — the ultimate tropical luxury escape.',
     'image_url': 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=800'},
    {'name': 'Dubai',             'country': 'UAE',         'budget': 'luxury', 'tags': ['cities','desert','landmarks'],
     'description': "Futuristic skyline, gold souks, desert safaris, and the world's most luxurious hotels.",
     'image_url': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800'},
    {'name': 'Bora Bora',         'country': 'French Polynesia','budget': 'luxury','tags': ['beach','scenic','nature'],
     'description': 'Legendary lagoon surrounded by volcanic peaks and the most exclusive overwater bungalows.',
     'image_url': 'https://images.unsplash.com/photo-1589197331516-4d84b72ebde3?w=800'},
    {'name': 'Swiss Riviera',     'country': 'Switzerland', 'budget': 'luxury', 'tags': ['scenic','mountains','cities'],
     'description': 'Lake Geneva shores with Michelin-star dining, Belle Époque palaces, and Alpine vistas.',
     'image_url': 'https://images.unsplash.com/photo-1527668752968-14dc70a27c95?w=800'},
    {'name': 'Seychelles',        'country': 'Seychelles',  'budget': 'luxury', 'tags': ['beach','nature','scenic'],
     'description': 'Pristine granite-boulder beaches, giant tortoises, and lush tropical forests.',
     'image_url': 'https://images.unsplash.com/photo-1589979481223-deb893043163?w=800'},
    {'name': 'Safari in Serengeti','country': 'Tanzania',   'budget': 'luxury', 'tags': ['nature','scenic','desert'],
     'description': 'Witness the Great Migration across endless golden plains with luxury tented camps.',
     'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800'},
    {'name': 'Monaco',            'country': 'Monaco',      'budget': 'luxury', 'tags': ['cities','beach','landmarks'],
     'description': 'Glamorous Mediterranean principality with casinos, superyachts, and the famous Grand Prix circuit.',
     'image_url': 'https://images.unsplash.com/photo-1530841377377-3ff06c0ca713?w=800'},
]


class Command(BaseCommand):
    help = 'Seed the database with categories, budget tiers, and destinations'

    def handle(self, *args, **options):
        # 1. Create categories
        cat_map = {}
        for c in CATEGORIES:
            obj, _ = Category.objects.get_or_create(slug=c['slug'], defaults={'name': c['name']})
            cat_map[c['slug']] = obj
        self.stdout.write(f'  ✓ {len(cat_map)} categories ready')

        # 2. Create budget tiers
        budget_map = {}
        for b in BUDGETS:
            obj, _ = BudgetCategory.objects.get_or_create(
                slug=b['slug'],
                defaults={'name': b['name'], 'sort_order': b['sort_order']},
            )
            budget_map[b['slug']] = obj
        self.stdout.write(f'  ✓ {len(budget_map)} budget tiers ready')

        # 3. Create destinations
        Destination.objects.all().delete()
        for d in DESTINATIONS:
            dest = Destination.objects.create(
                name=d['name'],
                country=d['country'],
                description=d['description'],
                image_url=d['image_url'],
                budget_category=budget_map[d['budget']],
            )
            tag_objs = [cat_map[t] for t in d['tags']]
            dest.tags.set(tag_objs)

        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Seeded {len(DESTINATIONS)} destinations. Done!'
        ))
