$(document).ready(function() {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        editable: false,
        eventLimit: true,
        events: function(start, end, timezone, callback) {
            $.ajax({
                url: '/reservations/events/' + window.lodgeId + '/',
                dataType: 'json',
                data: {
                },
                success: function(response) {
                    var events = [];
                    response.forEach(function(data) {
                        events.push({
                            title: data.title,
                            start: data.start,
                            end: data.end,
                            rendering: 'background',
                            color: data.color
                        });
                    });
                    callback(events);
                }
            });
        }
    });
});
