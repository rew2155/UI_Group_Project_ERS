$(document).ready(function(){
let currentPath = window.location.pathname;
let lesson_id = currentPath.split("/setup/")[1];
lesson_id = parseInt(lesson_id);

$('#prev').click(function() {
    let prevLessonID = lesson_id - 1;
    if (prevLessonID > 0) {
        window.location.href = '/setup/' + prevLessonID;
    } else {
        window.location.href = window.location.href.split('/setup/')[0];
    }
});

$('#next').click(function() {
    let nextLessonID = lesson_id + 1;
    if (nextLessonID == 6) {
        window.location.href = '/setup/' + 7;
    }
    if (nextLessonID <= 23) { 
        window.location.href = '/setup/' + nextLessonID;
    } else if(lesson_id = 23) {
        window.location.href = '/quickstart';
    }
});

$('#no').click(function() {
    let prevLessonID = 5;
    if (prevLessonID > 0) {
        window.location.href = '/setup/' + prevLessonID;
    } else {
        window.location.href = window.location.href.split('/setup/')[0];
    }
});

});