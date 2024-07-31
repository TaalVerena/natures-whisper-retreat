// Execute code when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Get the calendar element by ID
    var calendarEl = document.getElementById('calendar');

    // Fetch booked dates for the current lodge from the API
    fetch('/api/booked-dates/' + window.lodgeId + '/')
        .then(response => {
            // Check if the response is successful
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Parse the response as JSON
            return response.json();
        })
        .then(bookedDates => {
            // Create a FullCalendar instance
            var calendar = new FullCalendar.Calendar(calendarEl, {
                // Set initial view to 'dayGridMonth'
                initialView: 'dayGridMonth',
                // Define events endpoint for fetching reservation events
                events: '/reservations/events/' + window.lodgeId + '/',
                // Enable date selection
                selectable: true,
                // Handle date selection
                select: function (info) {
                    var startDate = new Date(info.startStr);
                    var endDate = new Date(info.endStr);

                    // Check if selected dates are in the past
                    var today = new Date();
                    if (startDate < today || endDate < today) {
                        alert('You cannot book past dates. Please select future dates.');
                        return;
                    }

                    // Check for overlapping bookings
                    var overlapping = false;
                    for (var d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
                        var dateString = d.toISOString().split('T')[0];
                        console.log('Checking date:', dateString);
                        var isBooked = bookedDates.some(function (bookedDate) {
                            return dateString === bookedDate.date && bookedDate.status === 'confirmed';
                        });
                        console.log('Is booked:', isBooked);
                        if (isBooked) {
                            overlapping = true;
                            break;
                        }
                    }

                    // Display alert if dates overlap with existing bookings
                    if (overlapping) {
                        alert('One or more dates in this range are fully booked with confirmed bookings. Please select another date range.');
                        return;
                    }

                    // Populate start_date and end_date fields in the form
                    document.querySelector('input[name="start_date"]').value = info.startStr;
                    document.querySelector('input[name="end_date"]').value = info.endStr;
                },
                // Handle click events on booked dates
                eventClick: function (info) {
                    alert('This date is fully booked. Please select another date.');
                }
            });
            // Render the calendar
            calendar.render();
        })
        // Handle errors
        .catch(error => {
            console.error('Failed to load booked dates:', error);
            alert('Failed to load calendar data!');
        });
});
