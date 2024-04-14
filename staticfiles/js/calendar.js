document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var startInput = document.getElementById('start_date');
    var endInput = document.getElementById('end_date');
    var currentSelection = null;

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        selectable: true,
        dateClick: function(info) {
            console.log("Date clicked: " + info.dateStr);
            if (!currentSelection) {
                startInput.value = info.dateStr;
                currentSelection = info.dateStr;
                endInput.value = '';
            } else {
                if (new Date(info.dateStr) >= new Date(currentSelection)) {
                    endInput.value = info.dateStr;
                } else {
                    startInput.value = info.dateStr;
                    endInput.value = currentSelection;
                }
                currentSelection = null;
            }
        },
        events: '/reservations/events/' + window.lodgeId + '/',
        eventColor: '#378006'
    });

    calendar.render();
});
