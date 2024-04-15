document.addEventListener('DOMContentLoaded', function() {
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
                selectOverlap: function(event) {
                    return event.extendedProps.type !== 'booked';
                },
                select: function(info) {
                    var startDate = info.startStr;
                    var endDate = info.endStr;
                    

                    if (bookedDates.includes(startDate)) {
                        alert('Please select another date as this is fully booked.');
                        calendar.unselect();
                    } else {
                        document.querySelector('input[name="start_date"]').value = startDate;
                        document.querySelector('input[name="end_date"]').value = endDate;
                    }
                },
                eventClick: function(info) {
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
