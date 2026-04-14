/**
 * TravelMore — Main JS
 * Nav toggle, scroll effects, hero carousel, language switcher, modal
 */

console.log('TravelMore Main JS Loaded');

document.addEventListener('DOMContentLoaded', () => {

    /* ─── LANGUAGE SWITCHER ──────────────────────────── */
    window.setLang = function(lang) {
        localStorage.setItem('travelmore_lang', lang);

        // Update DOM elements using data-i18n
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (window.TRAVELMORE_DICTS && window.TRAVELMORE_DICTS[lang] && window.TRAVELMORE_DICTS[lang][key]) {
                if (el.tagName === 'INPUT' && el.type !== 'hidden') {
                    el.placeholder = window.TRAVELMORE_DICTS[lang][key];
                } else {
                    el.textContent = window.TRAVELMORE_DICTS[lang][key];
                }
            }
        });

        // Update active class on buttons
        document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
        const activeBtn = document.getElementById('btn-' + lang);
        if (activeBtn) activeBtn.classList.add('active');
    };

    // Initialize Language
    const savedLang = localStorage.getItem('travelmore_lang') || 'en';
    setLang(savedLang);

    /* ─── FLY ANIMATION ──────────────────────────────── */
    const navLogo = document.querySelector('.nav-logo');
    const logoIcon = document.querySelector('.logo-icon');

    if (navLogo && logoIcon) {
        navLogo.addEventListener('click', (e) => {
            if (window.location.pathname === '/') {
                e.preventDefault();
                logoIcon.classList.remove('fly-animation');
                void logoIcon.offsetWidth; // trigger reflow
                logoIcon.classList.add('fly-animation');
            }
        });
    }

    /* ─── NAV TOGGLE (Mobile) ────────────────────────── */
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    /* ─── NAV SCROLL EFFECT ──────────────────────────── */
    const nav = document.getElementById('main-nav');
    if (nav) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                nav.style.padding = '8px 24px';
            } else {
                nav.style.padding = '12px 24px';
            }
            handleScrollAnimations();
        });
    }

    /* ─── SCROLL ANIMATIONS ──────────────────────────── */
    const animatedElements = document.querySelectorAll('[data-aos]');

    function handleScrollAnimations() {
        animatedElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const isInViewport = (rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.85);
            if (isInViewport) {
                const delay = el.getAttribute('data-delay') || 0;
                setTimeout(() => {
                    el.classList.add('aos-animate');
                }, delay);
            }
        });
    }
    handleScrollAnimations();

    /* ─── HERO CAROUSEL ──────────────────────────────── */
    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.indicator');

    if (slides.length > 0) {
        let currentSlide = 0;
        let slideInterval;

        const goToSlide = (index) => {
            slides[currentSlide].classList.remove('active');
            if (indicators[currentSlide]) indicators[currentSlide].classList.remove('active');
            currentSlide = index;
            slides[currentSlide].classList.add('active');
            if (indicators[currentSlide]) indicators[currentSlide].classList.add('active');
        };

        const nextSlide = () => {
            goToSlide((currentSlide + 1) % slides.length);
        };

        slideInterval = setInterval(nextSlide, 5000);

        indicators.forEach((indicator, idx) => {
            indicator.addEventListener('click', () => {
                clearInterval(slideInterval);
                goToSlide(idx);
                slideInterval = setInterval(nextSlide, 5000);
            });
        });
    }

    /* ─── AUTO-DISMISS ALERTS ────────────────────────── */
    document.querySelectorAll('.glass-message').forEach(msg => {
        setTimeout(() => {
            if (msg && msg.parentElement) {
                msg.style.opacity = '0';
                msg.style.transform = 'translateY(-10px)';
                msg.style.transition = 'all 0.3s ease';
                setTimeout(() => msg.remove(), 300);
            }
        }, 5000);
    });

});

/* ─── GLOBAL CLICK LISTENER (Event Delegation) ──── */
document.addEventListener('click', (e) => {
    const btn = e.target.closest('.view-details-btn');
    if (btn) {
        console.log('Details button clicked');
        const name = btn.getAttribute('data-name');
        const country = btn.getAttribute('data-country');
        openDetailsModal(name, country);
    }

    const bookBtn = e.target.closest('.open-booking-btn');
    if (bookBtn) {
        console.log('Booking button clicked');
        const id = bookBtn.getAttribute('data-id');
        const name = bookBtn.getAttribute('data-name');
        const baseprice = bookBtn.getAttribute('data-baseprice');
        openBookingModal(id, name, baseprice);
    }
});

/* ════════════════════════════════════════════════════════
   MODAL LOGIC — runs outside DOMContentLoaded so it's
   available to inline onclick handlers too
   ════════════════════════════════════════════════════════ */

function openDetailsModal(name, country) {
    const modal = document.getElementById('details-modal');
    if (!modal) return;

    document.getElementById('modal-dest-name').textContent = name;
    document.getElementById('modal-dest-country').textContent = country;

    // --- Agency contacts (unique per destination) ---
    const agenciesList = document.getElementById('modal-agencies');
    const phoneBase = hashCode(name + country);
    agenciesList.innerHTML = `
        <li>
            <strong>TravelMore Official</strong><br>
            <a href="tel:+1800${pad(phoneBase % 10000)}" class="accent-link">+1 (800) ${pad(phoneBase % 10000).slice(0,3)}-${pad(phoneBase % 10000).slice(3)}</a>
        </li>
        <li>
            <strong>${country} Local Tours</strong><br>
            <a href="tel:+1888${pad((phoneBase+1234) % 10000)}" class="accent-link">+1 (888) ${pad((phoneBase+1234) % 10000).slice(0,3)}-${pad((phoneBase+1234) % 10000).slice(3)}</a>
        </li>
        <li>
            <strong>${name} Resort Agency</strong><br>
            <a href="tel:+1877${pad((phoneBase+5678) % 10000)}" class="accent-link">+1 (877) ${pad((phoneBase+5678) % 10000).slice(0,3)}-${pad((phoneBase+5678) % 10000).slice(3)}</a>
        </li>
    `;

    // --- Hotels with star ratings and map links ---
    const hotelsList = document.getElementById('modal-hotels');
    const hotels = [
        { hotelName: `Grand ${name} Resort & Spa`,   rating: 5 },
        { hotelName: `${name} Boutique Hotel`,        rating: 4 },
        { hotelName: `The ${country} Retreat`,        rating: 5 },
        { hotelName: `${name} Inn`,                   rating: 3 },
    ];

    hotelsList.innerHTML = hotels.map(h => {
        const stars = '★'.repeat(h.rating) + '☆'.repeat(5 - h.rating);
        const mapQ  = encodeURIComponent(`${h.hotelName}, ${name}, ${country}`);
        return `
            <li>
                <div class="hotel-info">
                    <span class="hotel-name">${h.hotelName}</span>
                    <a href="https://www.google.com/maps/search/?api=1&query=${mapQ}" target="_blank" rel="noopener" class="location-pin" title="View on Map">📍</a>
                </div>
                <div class="hotel-stars">${stars}</div>
            </li>
        `;
    }).join('');

    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // prevent scroll behind modal
}

function closeDetailsModal() {
    const modal = document.getElementById('details-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeDetailsModal();
});

/* Helpers */
function hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = ((hash << 5) - hash) + str.charCodeAt(i);
        hash |= 0;
    }
    return Math.abs(hash);
}

function pad(n) {
    return String(n).padStart(4, '0');
}

/* ════════════════════════════════════════════════════════
   BOOKING MODAL LOGIC
   ════════════════════════════════════════════════════════ */

let currentHotelData = {};

async function openBookingModal(destId, destName, basePrice) {
    const modal = document.getElementById('booking-modal');
    if (!modal) return;

    // Reset properties
    document.getElementById('booking-dest-id').value = destId;
    document.getElementById('booking-dest-name').textContent = destName;
    document.getElementById('booking-base-price').value = basePrice;
    
    // Set default date to relative tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.getElementById('booking-start').value = tomorrow.toISOString().split('T')[0];
    
    // Reset inputs
    document.getElementById('booking-days').value = '5';
    document.getElementById('booking-days-custom').style.display = 'none';
    document.getElementById('booking-days-custom').value = '';
    
    // Hide UI
    document.getElementById('booking-hotels-loading').style.display = 'block';
    document.getElementById('booking-hotel').style.display = 'none';
    document.getElementById('booking-hotel-info').style.display = 'none';
    
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Fetch hotels
    try {
        const res = await fetch(`/api/hotels/${destId}/`);
        const data = await res.json();
        
        const select = document.getElementById('booking-hotel');
        select.innerHTML = '<option value="">No hotel selected (Base package)</option>';
        currentHotelData = {};
        
        data.hotels.forEach(h => {
            currentHotelData[h.id] = h;
            const stars = '★'.repeat(h.rating) + '☆'.repeat(5 - h.rating);
            const opt = document.createElement('option');
            opt.value = h.id;
            opt.textContent = `${h.name} ${stars} (x${h.price_modifier})`;
            select.appendChild(opt);
        });
        
        document.getElementById('booking-hotels-loading').style.display = 'none';
        select.style.display = 'block';
        updateBookingPrice(); // initial price calculation

    } catch (e) {
        document.getElementById('booking-hotels-loading').textContent = 'Failed to load hotels.';
        console.error(e);
    }
}

function closeBookingModal() {
    const modal = document.getElementById('booking-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

function updateBookingPrice() {
    let basePriceStr = document.getElementById('booking-base-price').value;
    // Replace comma with dot for locales like RU (e.g. 50,00 -> 50.00)
    basePriceStr = basePriceStr.replace(',', '.');
    const basePrice = parseFloat(basePriceStr) || 0;
    
    let daysStr = document.getElementById('booking-days').value;
    let days = parseInt(daysStr);
    const customDaysInput = document.getElementById('booking-days-custom');
    
    if (daysStr === 'custom') {
        customDaysInput.style.display = 'block';
        days = parseInt(customDaysInput.value) || 0;
    } else {
        customDaysInput.style.display = 'none';
    }

    if (days < 1) days = 0;

    const hotelId = document.getElementById('booking-hotel').value;
    let modifier = 1.0;
    
    const infoDiv = document.getElementById('booking-hotel-info');
    if (hotelId && currentHotelData[hotelId]) {
        const h = currentHotelData[hotelId];
        modifier = parseFloat(h.price_modifier);
        
        // Show address and map pin
        document.getElementById('booking-hotel-address').textContent = '📌 ' + (h.address || 'Address not available');
        infoDiv.style.display = 'flex';
        
        const q = encodeURIComponent(`${h.name}, ${h.address}`);
        document.getElementById('booking-hotel-map').href = `https://www.google.com/maps/search/?api=1&query=${q}`;
    } else {
        infoDiv.style.display = 'none';
    }
    
    const total = basePrice * modifier * days;
    document.getElementById('booking-total-price').textContent = `$${total.toFixed(2)} USD`;
}

async function submitBooking(e) {
    e.preventDefault();
    
    const btn = document.getElementById('booking-submit-btn');
    btn.textContent = 'Processing...';
    btn.disabled = true;

    // CSRF token from cookies
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
    
    let daysStr = document.getElementById('booking-days').value;
    let days = parseInt(daysStr);
    if (daysStr === 'custom') {
        days = parseInt(document.getElementById('booking-days-custom').value) || 1;
    }

    const payload = {
        dest_id: document.getElementById('booking-dest-id').value,
        hotel_id: document.getElementById('booking-hotel').value || null,
        full_name: document.getElementById('booking-fullname').value,
        phone: document.getElementById('booking-phone').value,
        start_date: document.getElementById('booking-start').value,
        num_days: days
    };

    try {
        const res = await fetch('/api/book/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.ok) {
            window.location.href = '/my-bookings/';
        } else {
            alert('Failed to book: ' + (data.error || 'Unknown error'));
            btn.textContent = 'Confirm Booking';
            btn.disabled = false;
        }
    } catch (err) {
        alert('Network error. Please try again.');
        console.error(err);
        btn.textContent = 'Confirm Booking';
        btn.disabled = false;
    }
}
