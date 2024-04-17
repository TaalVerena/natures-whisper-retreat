document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    // Fetch booked dates using AJAX from the backend
    fetch('/api/booked-dates/' + window.lodgeId + '/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(bookedDates => {
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                events: '/reservations/events/' + window.lodgeId + '/',
                selectable: true,
                select: function (info) {
                    var startDate = new Date(info.startStr);
                    var endDate = new Date(info.endStr);
                
                    // Check if any of the selected dates are fully booked with confirmed bookings
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
                
                    if (overlapping) {
                        alert('One or more dates in this range are fully booked with confirmed bookings. Please select another date range.');
                        return;
                    }
                
                    // Proceed with selecting the dates
                    document.querySelector('input[name="start_date"]').value = info.startStr;
                    document.querySelector('input[name="end_date"]').value = info.endStr;
                },
                
                eventClick: function (info) {
                    alert('This date is fully booked. Please select another date.');
                }
            });
            calendar.render();
        })
        .catch(error => {
            console.error('Failed to load booked dates:', error);
            alert('Failed to load calendar data!');
        });
});
