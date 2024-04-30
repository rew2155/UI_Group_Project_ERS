$(document).ready(function() {
    let currentPath = window.location.pathname;
    let question_id = parseInt(currentPath.split("/quiz/")[1], 10);

    questionAnswered();

    function questionAnswered() {
        let baseUrl = window.location.href.split('/quiz/')[0];
        $.ajax({
            url: baseUrl + '/already-answered/' + question_id,
            type: 'POST',
            success: function(response) {
                if (response.user_answer == null) {
                    $('#next').prop('disabled', true); // Initially disable the Next button
                    console.log("reached");
                    handleQuestionFormat();
                } else {
                    $('button[id^="answer"]').prop('disabled', true);
                    $('button[id=' + response.user_answer + ']').addClass('selected');
                    //if (response.correct_answer == response.user_answer) {
                        //$('button[id^="answer"]').prop('disabled', true);
                        //$().addClass('selected');
                        // $('button[id=' + response.user_answer +']').prop('disabled', false);
                        // $('button[id=' + response.user_answer +']').addClass('correct');
                        //$('#result').append("Correct!");
                    //} else {
                        //$('button[id^="answer"]').prop('disabled', true);
                        // ('button[id=' + response.correct_answer +']').prop('disabled', false);
                        // $('button[id=' + response.user_answer +']').addClass('incorrect');
                        //$('#result').append("Incorrect!");
                        //$('#result').append(response.exp)
                    //}
                }
            }
        })
    }

    function showResultPopup(message) {
        $('#resultText').text(message);
        $('#resultModal').show();
    }

    $('.close').click(function() {
        $('#resultModal').hide();
    });

    $(window).click(function(event) {
        if ($(event.target).hasClass('modal')) {
            $('#resultModal').hide();
        }
    });

    function handleMultipleChoice() {
        $(document).on('click', 'button[id^="answer"]', function() {
            $('button[id^="answer"]').prop('disabled', true); // Disable all answer buttons
            $(this).prop('disabled', false); // Enable the clicked button
            $('button[id^="answer"]').removeClass('selected'); // Remove selected class from all buttons
            $(this).addClass('selected'); // Add selected class to clicked button

            let selectedAnswer = $(this).attr('id');
            $('#next').prop('disabled', false); // Enable the Next button

            $.ajax({
                url: '/submit-answer/' + question_id,
                type: 'POST',
                data: { answer: selectedAnswer },
                success: function(response) {
                    let message = response.is_correct ? "Correct!" : "Incorrect! " + response.exp;
                    showResultPopup(message);
                },
                error: function(xhr, status, error) {
                    console.error('Error submitting answer:', error);
                }
            });
        });
    }

    function handleDragAndDrop() {
        $('img[id^="answer"]').draggable({
            revert: 'invalid',
            cursor: 'move',
            opacity: 0.7
        });

        $('#situation').droppable({
            drop: function(event, ui) {
                let droppedAnswer = ui.draggable.attr('id');
                $('img[id^="answer"]').draggable('disable');
                $('#next').prop('disabled', false); // Enable the Next button

                $.ajax({
                    url: '/check-answer/' + question_id,
                    type: 'POST',
                    data: { answer: droppedAnswer },
                    success: function(response) {
                        let message = response.is_correct ? "Correct!" : "Incorrect! " + response.exp;
                        showResultPopup(message);
                    },
                    error: function(xhr, status, error) {
                        console.error('AJAX error:', error);
                    }
                });
            }
        });
    }

    function handleQuestionFormat() {
        if (question_id < 9) {
            handleMultipleChoice();
        } else {
            handleDragAndDrop();
        }
    }


    $('#prev').click(function() {
        let prevQuestionID = question_id - 1;
        if (prevQuestionID > 0) {
            window.location.href = '/quiz/' + prevQuestionID;
        } else {
            window.location.href = window.location.href.split('/quiz/')[0] + '/quickstart';
        }
    });

    $('#next').click(function() {
        let nextQuestionID = question_id + 1;
        if (nextQuestionID <= 10) {
            window.location.href = '/quiz/' + nextQuestionID;
        } else {
            window.location.href = '/result';
        }
    });
});
