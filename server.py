from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
total_questions = 10
correct_counter = [0]

quiz_qs = {
    "1": {
        "id": 1,
        "prompt": "The pile currently looks like this:",
        "situation": "<img class='situation_img' src='https://familymath.stanford.edu/wp-content/uploads/2021/08/playing-cards-e1628288827705.jpg' alt='Situation Image'>",
        "question": "How many extra turns does the following player get?",
        "answer1": "<button id='answer1'>1</button>", 
        "answer2": "<button id='answer2'>2</button>",
        "answer3": "<button id='answer3'>3</button>",
        "answer4": "<button id='answer4'>4</button>",
        "correct_answer": "answer4",
        "prev_q": None,
        "next_q": "2"
    },

    "2":{
        "id": 2,
        "prompt": "The pile currently looks like this 2:",
        "situation": "<img id='situation' class='situation_img' src='https://www.wargamer.com/wp-content/sites/wargamer/2022/04/playing-card-games-kemps.jpg' alt='Situation Image'>", 
        "question": "How many extra turns does the following player get?",
        "answer1": "<button id='answer1'>1</button>", 
        "answer2": "<button id='answer2'>2</button>",
        "answer3": "<button id='answer3'>3</button>",
        "answer4": "<button id='answer4'>4</button>",
        "correct_answer": "answer1",
        "prev_q": "1",
        "next_q": "3",
    },

    "3": {
        "id": 3,
        "prompt": "The following list provides the sequence of events in a game with 4 players:",
        "situation": """1. Player 1 plays a 3 <br> 
                        2. Player 2 plays a King <br> 
                        3. Player 3 plays a 2 <br> 
                        4. Player 3 plays a King <br> 
                        5. Player 2 slaps the pile""",  # Formatted as a single string
        "question": "What happens next?",
        "answer1": "<button id='answer1'>Player 2 picks up the pile</button>", 
        "answer2": "<button id='answer2'>Player 2 discards a penalty card</button>",
        "answer3": "<button id='answer3'>Player 3 picks up the pile</button>",
        "answer4": "<button id='answer4'>Player 3 discards a penalty card</button>",
        "correct_answer": "answer1",
        "prev_q": "2",
        "next_q": "4",
        },

    "4": {
        "id": 4,
        "prompt": "The following list provides the sequence of events in a game with 3 players:",
        "situation": "1. Player 1 plays a 4<br>2. Player 2 plays a Jack<br>3. Player 3 plays a Queen<br>4. Player 1 plays a 2<br>5. Player 1 plays a 3",
        "question": "What happens next?",
        "answer1": "<button id='answer1'>Player 1 picks up the pile</button>", 
        "answer2": "<button id='answer2'>Player 2 picks up the pile</button>",
        "answer3": "<button id='answer3'>Player 3 picks up the pile</button>",
        "answer4": "<button id='answer4'>Player 1 discards a penalty card</button>",
        "correct_answer": "answer3",
        "prev_q": "3",
        "next_q": "5",
    },

    "5": {
        "id": 5,
        "prompt": "The following list provides the sequence of events in a game with 2 players:",
        "situation": "1. Player 1 plays an 8<br>2. Player 2 plays a 3<br>3. Player 1 plays an 8<br>4. Player 2 plays a 7<br>5. Player 1 slaps the pile",
        "question": "What happens next?",
        "answer1": "<button id='answer1'>Player 1 picks up the pile</button>", 
        "answer2": "<button id='answer2'>Player 1 discards a penalty card</button>",
        "answer3": "<button id='answer3'>Player 2 picks up the pile</button>",
        "answer4": "<button id='answer4'>Player 2 discards a penalty card</button>",
        "correct_answer": "answer2",
        "prev_q": "4",
        "next_q": "6",
    },

    "6": {
        "id": 6,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img class='situation_img' src='https://cdn11.bigcommerce.com/s-sjl48p9/images/stencil/500x659/products/493/477/Jumbo_Deck_of_Cards__00402.1355263732.jpg?c=2' alt='Current pile'>",
        "question": "The next card you play is a 7. What do you do next?",
        "answer1": "<button id='answer1'>You slap the pile</button>", 
        "answer2": "<button id='answer2'>You play another card</button>",
        "answer3": "<button id='answer3'>You wait for the next player to go</button>",
        "answer4": "<button id='answer4'>You discard a penalty card</button>",
        "correct_answer": "answer2",
        "prev_q": "5",
        "next_q": "7",
    },

    "7": {
        "id": 7,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img class='situation_img' src='https://cdn.shopify.com/s/files/1/1788/4029/files/download_12_large.jpg?v=1566685316' alt='Current pile'>",
        "question": "The next card you play is a Queen. What do you do next?",
        "answer1": "<button id='answer1'>You slap the pile</button>", 
        "answer2": "<button id='answer2'>You play another card</button>",
        "answer3": "<button id='answer3'>You wait for the next player to go</button>",
        "answer4": "<button id='answer4'>You discard a penalty card</button>",
        "correct_answer": "answer1",
        "prev_q": "6",
        "next_q": "8",
    },
    "8": {
        "id": 8,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img class='situation_img' src='https://as2.ftcdn.net/v2/jpg/00/80/62/95/1000_F_80629529_zmqcu0Oz8kc0a6PLN97lLexpFWIvG275.jpg' alt='Current pile'>",
        "question": "The next card you play is a Jack. What do you do next?",
        "answer1": "<button id='answer1'>You slap the pile</button>", 
        "answer2": "<button id='answer2'>You play another card</button>",
        "answer3": "<button id='answer3'>You wait for the next player to go</button>",
        "answer4": "<button id='answer4'>You discard a penalty card</button>",
        "correct_answer": "answer3",
        "prev_q": "7",
        "next_q": "9",
    },
    "9": {
        "id": 9,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img id='situation' src='https://lh3.googleusercontent.com/pw/AP1GczNEqnPt9mhOK38n0I-reh-aftn0RMPkffsRB9vpK-J4fUxWZnOMxJjsotzgWCsn8HfCKnAZvaooqU0IcPMtYlaf8rqQUmWt0fWbl5GvUiqHjM_Fmqo=w2400' alt='Current pile'>",
        "question": "Drag and drop the card that would provide the next player 1 extra turn.",
        "answer1": "<img id='answer1' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/English_pattern_jack_of_spades.svg/1200px-English_pattern_jack_of_spades.svg.png' alt='Option 1'>", 
        "answer2": "<img id='answer2' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/51_Q_di_picche.jpg/800px-51_Q_di_picche.jpg' alt='Option 2'>",
        "answer3": "<img id='answer3' class='drag_card' src='https://m.media-amazon.com/images/I/71EkglvyWjL._AC_UF1000,1000_QL80_.jpg' alt='Option 3'>",
        "answer4": "<img id='answer4' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/English_pattern_ace_of_diamonds.svg/1200px-English_pattern_ace_of_diamonds.svg.png' alt='Option 4'>",
        "correct_answer": "answer1",
        "prev_q": "8",
        "next_q": "10",
    },
    "10": {
        "id": 10,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img id='situation' src='https://lh3.googleusercontent.com/pw/AP1GczMCiCQm4x2TuVIgJLTjPHO-rAtJXUlovC2GeU9cOSVwfQV2-zEh6qAs4UMOKOYxitg7pkWRUJFTgsmDtMraj58Q1hDRVMW9LT50q2_ellCGAY5CEW8=w2400' alt='Current pile'>",
        "question": "Drag and drop the card that would create the opportunity to slap a Sandwich.",
        "answer1": "<img id='answer1' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/5_of_clubs.svg/1200px-5_of_clubs.svg.png' alt='Option 1'>", 
        "answer2": "<img id='answer2' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/7_of_clubs.svg/1200px-7_of_clubs.svg.png' alt='Option 2'>",
        "answer3": "<img id='answer3' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/English_pattern_ace_of_diamonds.svg/1200px-English_pattern_ace_of_diamonds.svg.png' alt='Option 3'>",
        "answer4": "<img id='answer4' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/51_Q_di_picche.jpg/800px-51_Q_di_picche.jpg' alt='Option 4'>",
        "correct_answer": "answer4",
        "prev_q": "9",
        "next_q": "score",
    }
    }

lesson_ls = {
    "1": {
        "id": 1,
        "Title": "What You Need",
        "Subtitle": "Standard 52-card deck of playing cards 2-10 players",
        "Picture": "",
        "Category": "Setup & Gameplay",
        "Status": "1 of 5",
    },
    "2":{
        "id": 2,
        "Title": "",
        "Subtitle": "",
        "Picture" : "",
        "Category": "",
        "Status": "",
    },
    "3":{
        "id": 3,
        "Title": "",
        "Subtitle": "",
        "Picture": "",
        "Category": "",
        "Status": "",
    },
    "4":{
        "id": 4,
        "Title": "",
        "Subtitle": "",
        "Picture" : "",
        "Category": "",
        "Status": "",
    },
    "5":{
        "id": 5,
        "Title": "",
        "Subtitle": "",
        "Picture" : "",
        "Category": "",
        "Status": "",
    },
    "6":{
        "id": 6,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "7":{
        "id": 7,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "8":{
        "id": 8,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "9":{
        "id": 9,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "10":{
        "id": 10,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "11":{
        "id": 11,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "12":{
        "id": 12,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "13":{
        "id": 13,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "14":{
        "id": 14,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "15":{
        "id": 15,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "16":{
        "id": 16,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "17":{
        "id": 17,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "18":{
        "id": 18,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "19":{
        "id": 19,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "20":{
        "id": 20,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "21":{
        "id": 21,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "22":{
        "id": 22,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    },
    "23":{
        "id": 23,
        "Title": "",
        "Subtitle":"",
        "Picture":"",
        "Example":"",
        "Category":"",
        "Status":"",
    }
}

# ROUTES

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/quickstart')
def quickstart():
    return render_template('quickstart.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

#TODO: @app.route for learning portion 

@app.route('/setup/<int:lesson_id>')
def setup(lesson_id):
    """Serve a quiz question page."""
    lesson_key = str(lesson_id)
    if lesson_key in lesson_ls:
        lesson = lesson_ls[lesson_key]
        return render_template('learn.html', lesson=lesson)
    else:
        return "Lesson not found", 404

@app.route('/quiz/<int:question_id>')
def quiz(question_id):
    """Serve a quiz question page."""
    question_key = str(question_id)
    if question_key in quiz_qs:
        question = quiz_qs[question_key]
        return render_template('quiz.html', question=question)
    else:
        return "Question not found", 404

@app.route('/submit-answer/<int:question_id>', methods=['POST'])
def submit_answer(question_id):
    """Process user's answer and redirect to next question or results."""
    question_key = str(question_id)
    if question_key in quiz_qs:
        user_answer = request.form.get('answer')
        correct_answer = quiz_qs[question_key]['correct_answer']

        # Check if the user's answer matches the correct answer
        is_correct = (user_answer == correct_answer)

        # Increment correct_counter if the answer is correct
        if is_correct:
            correct_counter[0] += 1

        # Determine the next question ID
        next_question_id = quiz_qs[question_key]['next_q']

        # Redirect to the next question or results page
        if next_question_id == "score":
            return redirect(url_for('result'))
        else:
            return jsonify({'is_correct': is_correct, 'redirect': url_for('quiz', question_id=next_question_id)})
    
    return "Invalid request", 400

@app.route('/check-answer/<int:question_id>', methods=['POST'])
def check_answer(question_id):
    # Retrieve the submitted answer from the AJAX request
    submitted_answer = request.form.get('answer')

    # Retrieve the correct answer for the given question_id
    correct_answer = quiz_qs[str(question_id)]['correct_answer']

    # Check if the submitted answer matches the correct answer
    if submitted_answer == correct_answer:
        return 'Correct!'
    else:
        return 'Incorrect!'

@app.route('/result')
def result():
    return render_template('results.html', correct_count=correct_counter[0], total_questions=total_questions)
if __name__ == '__main__':

    app.run(debug=True)
