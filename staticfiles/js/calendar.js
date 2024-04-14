$(document).ready(function () {
    var startInput = $('#start_date');
    var endInput = $('#end_date');
    var currentSelection = null;

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month'
        },
        editable: false,
        eventLimit: true,
        dateClick: function (info) {
            if (!currentSelection) {
                startInput.val(info.dateStr); 
                currentSelection = info.dateStr; 
                endInput.val(''); 
            } else {
               
                if (new Date(info.dateStr) >= new Date(currentSelection)) {
                    endInput.val(info.dateStr); 
                } else {
                    startInput.val(info.dateStr); 
                    endInput.val(currentSelection); 
                }
                currentSelection = null;
            }
        },

        // Event fetching from backend
        events: function (start, end, timezone, callback) {
            $.ajax({
                url: '/reservations/events/' + window.lodgeId + '/',
                dataType: 'json',
                success: function (response) {
                    var events = [];
                    response.forEach(function (data) {
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
    }).render(); 

});
