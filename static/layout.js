$(document).ready(function(){
// Get the current question ID
let currentPath = window.location.pathname;
let lesson_id = currentPath.split("/setup/")[1];
lesson_id = parseInt(lesson_id);

// Function to handle navigation to the previous question
$('#prev').click(function() {
    let prevLessonID = lesson_id - 1;
    if (prevLessonID > 0) {
        window.location.href = '/setup/' + prevLessonID;
    } else {
        window.location.href = window.location.href.split('/setup/')[0];
    }
});

// Function to handle navigation to the next question
$('#next').click(function() {
    let nextLessonID = lesson_id + 1;
    if (nextQuestionID <= 23) { // Assuming there are 10 questions in total
        window.location.href = '/setup/' + nextLessonID;
    } 
});
});