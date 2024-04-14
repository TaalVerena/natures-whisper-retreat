document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        select: function(info) {
            document.getElementById('start_date').value = info.startStr;
            document.getElementById('end_date').value = info.endStr;
        }
    });
    calendar.render();
});
