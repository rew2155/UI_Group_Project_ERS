$(document).ready(function(){
    // Get the current question ID
    let currentPath = window.location.pathname;
    let question_id = currentPath.split("/quiz/")[1];
    question_id = parseInt(question_id);

    let answerDropped = false;

    // Function to handle multiple choice questions
    function handleMultipleChoice() {
        user_answer = null;
        correct_answer = null;

        // Function to handle click event on answer buttons
        $(document).on('click', 'button[id^="answer"]', function() {
            console.log('Button clicked!'); // Debug statement

            // Get the selected answer
            let selectedAnswer = $(this).attr('id');
            user_answer = selectedAnswer;

            console.log('Selected answer:', selectedAnswer); // Debug statement

            // Disable all answer buttons
            $('button[id^="answer"]').prop('disabled', true);

            // Make an AJAX call to submit the answer only if the question number is 8 or less
            if (question_id <= 8) {
                // Retrieve the CSRF token from the page
                let csrfToken = $('meta[name=csrf-token]').attr('content');

                console.log('CSRF Token:', csrfToken); // Debug statement

                $.ajax({
                    url: '/submit-answer/' + question_id,
                    type: 'POST',
                    data: { answer: selectedAnswer, csrf_token: csrfToken }, // Include CSRF token in the request data
                    success: function(response) {
                        // Display the result in the "result" span
                        if (response.is_correct) {
                            $('#result').text('Correct!');
                        } else {
                            $('#result').append('Incorrect!')
                            $('#result').append(response.exp);
                        }

                        correct_answer = response.correct_answer;
                    },
                    error: function(xhr, status, error) {
                        // Handle error
                        console.error(error);
                    }
                });
            }

            $('#next').prop('disabled', false);
        });

        if (correct_answer == user_answer) {
            $('button[id=' + user_answer +']').prop('disabled', false);
            $('button[id=' + user_answer +']').addClass('correct');
        } else {
            $('button[id=' + correct_answer +']').prop('disabled', false);
            $('button[id=' + user_answer +']').addClass('incorrect');
        }
    }

    // Function to handle drag-and-drop questions
    function handleDragAndDrop() {
        // Enable draggable for answer images if no answer has been dropped yet
        if (!answerDropped) {
            $('img[id^="answer"]').draggable({
                revert: 'invalid',
                cursor: 'move',
                opacity: 0.7
            });
        }

        user_answer = null;
        correct_answer = null;

        // Enable droppable for the situation image
        $('#situation').droppable({
            drop: function(event, ui) {
                // Get the dropped answer image ID
                let droppedAnswer = ui.draggable.attr('id');
                user_answer = droppedAnswer;

                console.log('Dropped answer:', droppedAnswer); // Debug statement

                // Set answerDropped flag to true
                answerDropped = true;

                console.log('Answer dropped:', answerDropped); // Debug statement

                // Disable dragging of answer choices
                $('img[id^="answer"]').draggable('disable');

                // Remove the last part of the URL after /quiz/1
                let baseUrl = window.location.href.split('/quiz/')[0];

                $('#next').prop('disabled', false);

                // Make AJAX call to check if dropped answer is correct
                $.ajax({
                    url: baseUrl + '/check-answer/' + question_id, // Pass the current question ID dynamically
                    type: 'POST',
                    data: { answer: droppedAnswer },
                    success: function(response) {
                        // Display result message based on server response
                        if (response.is_correct) {
                            $('#result').append("Correct!");
                        } else {
                            $('#result').append("Inorrect!");
                            $('#result').append(response.exp);
                        }

                        correct_answer = response.correct_answer;
                    },
                    error: function(xhr, status, error) {
                        console.error('AJAX error:', error);
                    }
                });
            }
        });

        if (correct_answer == user_answer) {
            $('button[id=' + user_answer +']').prop('disabled', false);
            $('button[id=' + user_answer +']').addClass('correct');
        } else {
            $('button[id=' + correct_answer +']').prop('disabled', false);
            $('button[id=' + user_answer +']').addClass('incorrect');
        }

    }

    function questionAnswered() {
        let baseUrl = window.location.href.split('/quiz/')[0];
        $.ajax({
            url: baseUrl + '/already-answered/' + question_id,
            type: 'POST',
            success: function(response) {
                if (response.user_answer == null) {
                    console.log("reached");
                    handleQuestionFormat();
                } else {
                    if (response.correct_answer == response.user_answer) {
                        $('button[id^="answer"]').prop('disabled', true);
                        // $('button[id=' + response.user_answer +']').prop('disabled', false);
                        // $('button[id=' + response.user_answer +']').addClass('correct');
                        $('#result').append("Correct!");
                    } else {
                        $('button[id^="answer"]').prop('disabled', true);
                        // ('button[id=' + response.correct_answer +']').prop('disabled', false);
                        // $('button[id=' + response.user_answer +']').addClass('incorrect');
                        $('#result').append("Incorrect!");
                        $('#result').append(response.exp);
                    }
                }
            }
        })
    }

    // Function to handle different question formats based on question ID
    function handleQuestionFormat() {
        $('#next').prop('disabled', true);

        if (question_id < 9) {
            handleMultipleChoice();
        } else {
            // Logic for handling different question format (e.g., drag and drop)
            handleDragAndDrop();
        }
    }

    // Call the function to handle the question format
    questionAnswered();

    // Function to handle navigation to the previous question
    $('#prev').click(function() {
        let prevQuestionID = question_id - 1;
        if (prevQuestionID > 0) {
            window.location.href = '/quiz/' + prevQuestionID;
        } else {
            window.location.href = window.location.href.split('/quiz/')[0] + '/quickstart';
        }
    });

    // Function to handle navigation to the next question
    $('#next').click(function() {
        let nextQuestionID = question_id + 1;
        if (nextQuestionID <= 10) { // Assuming there are 10 questions in total
            window.location.href = '/quiz/' + nextQuestionID;
        } else {
            window.location.href = '/result';
        }
    });
    
});