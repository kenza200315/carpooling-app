// Covoiturage Algeria - Comprehensive Application Logic

// Global State
let allTrips = [];
let selectedTrip = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Set up global alert container if it doesn't exist
    if (!document.getElementById('alerts-container')) {
        const container = document.createElement('div');
        container.id = 'alerts-container';
        document.querySelector('main').insertBefore(container, document.querySelector('main').firstChild);
    }
}

// ============================================================================
// TRIP LOADING AND DISPLAY
// ============================================================================

function loadTrips() {
    const container = document.getElementById('trips-container');
    if (!container) return;

    fetch('/trips')
        .then(res => res.json())
        .then(trips => {
            if (!Array.isArray(trips)) {
                showError('Failed to load trips');
                return;
            }
            
            allTrips = trips;
            displayTrips(trips);
        })
        .catch(err => showError('Failed to load trips: ' + err.message));
}

function displayTrips(trips) {
    const container = document.getElementById('trips-container');
    if (!container) return;

    if (trips.length === 0) {
        container.innerHTML = '<div class="text-center" style="grid-column: 1/-1; padding: 3rem;"><p style="color: var(--text-light);"><i class="fas fa-search"></i> No trips available</p></div>';
        return;
    }

    container.innerHTML = trips.map(trip => `
        <div class="trip-card">
            <div class="trip-header">
                <div class="trip-route"><i class="fas fa-map-marker-alt"></i> ${trip.departure_city} → ${trip.destination_city}</div>
            </div>
            <div class="trip-body">
                <div class="trip-info">
                    <div class="trip-info-item">
                        <div class="trip-info-label"><i class="fas fa-chair"></i> Available Seats</div>
                        <div>${trip.available_seats}</div>
                    </div>
                    <div class="trip-info-item">
                        <div class="trip-info-label"><i class="fas fa-user"></i> Driver</div>
                        <div class="driver-info">
                            ${trip.driver_photo ? `<img src="${trip.driver_photo}" alt="Driver" class="driver-avatar-small">` : '<div class="driver-avatar-small"><i class="fas fa-user"></i></div>'}
                            <div>
                                <div>${trip.driver_name || 'Unknown'}</div>
                                ${trip.driver_rating > 0 ? `<div class="driver-rating"><i class="fas fa-star"></i> ${trip.driver_rating} (${trip.total_reviews} reviews)</div>` : '<div class="driver-rating">No reviews yet</div>'}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="trip-price"><i class="fas fa-coins"></i> ${trip.price} DA</div>
                
                ${trip.description ? `<div style="font-size: 0.9rem; color: var(--text-light); margin-bottom: 1rem;"><i class="fas fa-note-sticky"></i> ${trip.description}</div>` : ''}
                
                <div class="trip-footer">
                    <button class="btn btn-primary btn-trip" onclick="makeOffer(${trip.id}, ${trip.price})">
                        <i class="fas fa-handshake"></i> Make Offer
                    </button>
                    <button class="btn btn-outline btn-trip" onclick="viewTripDetails(${trip.id})">
                        <i class="fas fa-info-circle"></i> Details
                    </button>
                    <button class="btn btn-outline btn-trip" onclick="startChat(${trip.id}, '${trip.driver_name || 'Driver'}')">
                        <i class="fas fa-comments"></i> Chat
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// ============================================================================
// FILTERING
// ============================================================================

function applyFilters() {
    const departure = document.getElementById('departure_city')?.value || '';
    const destination = document.getElementById('destination_city')?.value || '';
    const maxPrice = parseFloat(document.getElementById('max_price')?.value) || Infinity;
    const minSeats = parseInt(document.getElementById('min_seats')?.value) || 1;

    const filtered = allTrips.filter(trip => {
        const matchDeparture = !departure || trip.departure_city.toLowerCase().includes(departure.toLowerCase());
        const matchDestination = !destination || trip.destination_city.toLowerCase().includes(destination.toLowerCase());
        const matchPrice = trip.price <= maxPrice;
        const matchSeats = trip.available_seats >= minSeats;
        return matchDeparture && matchDestination && matchPrice && matchSeats;
    });

    displayTrips(filtered);
}

function resetFilters() {
    if (document.getElementById('departure_city')) document.getElementById('departure_city').value = '';
    if (document.getElementById('destination_city')) document.getElementById('destination_city').value = '';
    if (document.getElementById('max_price')) document.getElementById('max_price').value = '';
    if (document.getElementById('min_seats')) document.getElementById('min_seats').value = '1';
    displayTrips(allTrips);
}

// ============================================================================
// OFFER MANAGEMENT
// ============================================================================

function makeOffer(tripId, tripPrice) {
    selectedTrip = tripId;
    document.getElementById('offer-trip-id').value = tripId;
    document.getElementById('proposed_price').placeholder = tripPrice + ' DA (or less)';
    document.getElementById('offer-modal').classList.add('active');
}

function submitOffer(e) {
    if (e) e.preventDefault();

    const tripId = document.getElementById('offer-trip-id').value;
    const name = document.getElementById('passenger_name').value;
    const phone = document.getElementById('passenger_phone')?.value;
    const price = document.getElementById('proposed_price').value;
    const message = document.getElementById('offer_message')?.value;

    if (!tripId || !name || !price) {
        showError('Please fill in all required fields');
        return;
    }

    fetch('/offers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            trip_id: parseInt(tripId),
            passenger_id: 1,
            passenger_name: name,
            passenger_phone: phone || null,
            proposed_price: parseFloat(price),
            price_da: parseFloat(price)
        })
    })
    .then(res => res.json())
    .then(data => {
        showSuccess('Offer submitted successfully! Drive will respond soon.');
        closeModal();
        document.getElementById('offer-form').reset();
    })
    .catch(err => showError('Failed to submit offer: ' + err.message));
}

function viewTripDetails(tripId) {
    const trip = allTrips.find(t => t.id === tripId);
    if (!trip) return;

    const modal = document.getElementById('details-modal');
    const content = document.getElementById('trip-details-content');
    
    content.innerHTML = `
        <div class="trip-info">
            <div class="trip-info-item">
                <div class="trip-info-label">From</div>
                <div>${trip.departure_city}</div>
            </div>
            <div class="trip-info-item">
                <div class="trip-info-label">To</div>
                <div>${trip.destination_city}</div>
            </div>
            <div class="trip-info-item">
                <div class="trip-info-label">Price</div>
                <div>${trip.price} DA</div>
            </div>
            <div class="trip-info-item">
                <div class="trip-info-label">Available Seats</div>
                <div>${trip.available_seats}</div>
            </div>
            <div class="trip-info-item">
                <div class="trip-info-label">Driver</div>
                <div>${trip.driver_name || 'Unknown'}</div>
            </div>
            <div class="trip-info-item">
                <div class="trip-info-label">Status</div>
                <div style="text-transform: uppercase; color: var(--success-color);">${trip.status}</div>
            </div>
        </div>
        ${trip.description ? `<div style="margin-top: 1rem; padding: 1rem; background: var(--light-bg); border-radius: var(--border-radius);"><strong>Description:</strong><br>${trip.description}</div>` : ''}
        <div class="form-actions" style="margin-top: 1.5rem;">
            <button class="btn btn-primary" onclick="makeOffer(${trip.id}, ${trip.price})">
                <i class="fas fa-handshake"></i> Make Offer
            </button>
            <button class="btn btn-outline" onclick="closeModal()">Close</button>
        </div>
    `;
    
    modal.classList.add('active');
}

// ============================================================================
// CHAT FUNCTIONALITY
// ============================================================================

function startChat(tripId, partnerName) {
    window.location.href = `/static/pages/chat.html?trip_id=${tripId}&partner_name=${encodeURIComponent(partnerName)}`;
}

// ============================================================================
// MODALS
// ============================================================================

function closeModal() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('active');
    });
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        closeModal();
    }
});

// ============================================================================
// ALERTS & NOTIFICATIONS
// ============================================================================

function showSuccess(message) {
    showAlert(message, 'success');
}

function showError(message) {
    showAlert(message, 'error');
}

function showAlert(message, type = 'success') {
    const container = document.getElementById('alerts-container');
    if (!container) return;

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <div>
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            ${message}
        </div>
        <button class="alert-close" onclick="this.parentElement.remove()">&times;</button>
    `;

    container.appendChild(alert);

    setTimeout(() => {
        if (alert.parentElement) {
            alert.remove();
        }
    }, 5000);
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Set up form submission event listeners
document.addEventListener('DOMContentLoaded', () => {
    const offerForm = document.getElementById('offer-form');
    if (offerForm) {
        offerForm.addEventListener('submit', submitOffer);
    }
});
