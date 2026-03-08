function loadTrips() {
    const container = document.getElementById('trips-container');
    if (!container) return;

    container.innerHTML = '<p class="loading">Chargement des trajets...</p>';

    fetch('/trips')
        .then(response => {
            if (!response.ok) throw new Error('Impossible de récupérer les trajets');
            return response.json();
        })
        .then(data => {
            container.innerHTML = '';
            if (!data || data.length === 0) {
                container.innerHTML = '<p class="no-trips">Aucun trajet disponible pour le moment.</p>';
                return;
            }
            data.forEach(trip => {
                const card = document.createElement('div');
                card.className = 'trip-card';
                card.innerHTML = `
                    <div class="trip-header">
                        <h3>Trajet #${trip.id}</h3>
                        <span class="trip-status">Actif</span>
                    </div>
                    <div class="trip-details">
                        <div class="trip-route">
                            <div class="city">
                                <p class="label">Départ</p>
                                <p class="value">${trip.departure_city}</p>
                            </div>
                            <div class="arrow">→</div>
                            <div class="city">
                                <p class="label">Destination</p>
                                <p class="value">${trip.destination_city}</p>
                            </div>
                        </div>
                        <div class="trip-info">
                            <div class="info-item">
                                <span class="label">Chauffeur</span>
                                <span class="value">${trip.driver_name || 'Non disponible'}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Prix</span>
                                <span class="value">€${trip.price.toFixed(2)}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Places disponibles</span>
                                <span class="value">${trip.available_seats}</span>
                            </div>
                        </div>
                    </div>
                    <button class="btn-offer" onclick="makeOffer(${trip.id})">Faire une offre</button>
                `;
                container.appendChild(card);
            });
        })
        .catch(error => {
            console.error('Error loading trips:', error);
            container.innerHTML = `<p class="error">Erreur lors du chargement des trajets : ${error.message}</p>`;
        });
}

function makeOffer(tripId) {
    const newOffer = prompt('Entrez votre prix proposé:');
    if (newOffer !== null) {
        const passengerName = prompt('Entrez votre nom:');
        if (passengerName !== null) {
            fetch('/offers', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    trip_id: tripId,
                    passenger_name: passengerName,
                    proposed_price: parseFloat(newOffer)
                })
            })
            .then(response => {
                if (!response.ok) throw new Error('Échec de la soumission de l\'offre');
                return response.json();
            })
            .then(data => {
                alert('Offre soumise avec succès!');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erreur lors de la soumission de l\'offre: ' + error.message);
            });
        }
    }
}

if (document.getElementById('create-trip-form')) {
    document.getElementById('create-trip-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = {
            driver_id: parseInt(formData.get('driver_id')),
            departure_city: formData.get('departure_city'),
            destination_city: formData.get('destination_city'),
            price: parseFloat(formData.get('price')),
            available_seats: parseInt(formData.get('available_seats'))
        };
        fetch('/trips', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => alert('Trip created!'))
        .catch(error => console.error('Error:', error));
    });
}

if (document.getElementById('make-offer-form')) {
    document.getElementById('make-offer-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = {
            trip_id: parseInt(formData.get('trip_id')),
            passenger_name: formData.get('passenger_name'),
            proposed_price: parseFloat(formData.get('proposed_price'))
        };
        fetch('/offers', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => alert('Offer submitted!'))
        .catch(error => console.error('Error:', error));
    });
}