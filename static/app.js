// Redirect to new JavaScript file
// This file is deprecated. Use /static/js/app.js instead.
console.log('Redirecting to new JavaScript file...');
// The new app.js will be loaded from the new pages
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