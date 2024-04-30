document.addEventListener('DOMContentLoaded', (event) => {
  const exampleTextElements = document.querySelectorAll('.example-text');

  exampleTextElements.forEach((exampleText) => {
    // Check if the content of the example text is effectively empty
    if (!exampleText.textContent.trim()) {
      // Hide the example text container
      exampleText.style.display = 'none';

      // Also hide the example header if it's empty
      let header = exampleText.previousElementSibling;
      if (header && header.classList.contains('example-header')) {
        header.style.display = 'none';
      }
    }
  });

  $(document).ready(function() {
    let currentPath = window.location.pathname;
    let lesson_id = parseInt(currentPath.split("/setup/")[1], 10);

    // Set the URLs for the Previous and Next buttons
    let prevUrl = (lesson_id > 1) ? '/setup/' + (lesson_id - 1) : '';
    let nextUrl = (lesson_id < 23) ? '/setup/' + (lesson_id + 1) : '';

    // Update the Previous button's properties
    if (lesson_id === 0) {
        $('#prev').hide();
    } else if (lesson_id === 1) {
        prevUrl = '/';
        $('#prev').show().attr('href', prevUrl);
        $('#prev').text('< Home');
    } else if (lesson_id === 6) {
        prevUrl = '/setup/1';
        $('#prev').show().attr('href', prevUrl);
        $('#prev').text('< Back to Setup');
    } else {
        $('#prev').show().attr('href', prevUrl);
        $('#prev').text('< Prev');
    }
    

    // Update the Next button's properties
    if (lesson_id === 5) {
        $('#next').text('Rules >').attr('href', '/setup/6');
    } else if (lesson_id === 23) {
        $('#next').text('Overview >').attr('href', '/quickstart');
    } else if (lesson_id < 23) {
        $('#next').show().text('Next >').attr('href', nextUrl);
    } else {
        $('#next').hide();
    }
});


});

