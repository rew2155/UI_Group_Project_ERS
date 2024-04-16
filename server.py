from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
total_questions = 10
correct_counter = [0]

quiz_qs = {
    "1": {
        "id": 1,
        "prompt": "The pile currently looks like this:",
        "situation": "<img src='/static/image1.jpg' alt='Situation Image'>",
        "question": "How many extra turns does the following player get?",
        "answers": [1, 2, 3, 4],
        "correct_answer": 4,
        "next_q": "2"
    },

    "2":{
        "id": 2,
        "prompt": "The pile currently looks like this 2:",
        "situation": "<img id='situation' source='' alt='Situation Image'>", 
        "question": "How many extra turns does the following player get?",
        "answers": [1, 2, 3, 4],
        "correct_answer": 1,
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
        "answers": [
            "Player 2 picks up the pile",
            "Player 2 discards a penalty card",
            "Player 3 picks up the pile",
            "Player 3 discards a penalty card"
        ],
        "correct_answer": "Player 2 picks up the pile",
        "next_q": "4",
        },
    "4": {
        "id": 4,
        "prompt": "The following list provides the sequence of events in a game with 3 players:",
        "situation": "1. Player 1 plays a 4<br>2. Player 2 plays a Jack<br>3. Player 3 plays a Queen<br>4. Player 1 plays a 2<br>5. Player 1 plays a 3",
        "question": "What happens next?",
        "answers": [
            "Player 1 picks up the pile",
            "Player 2 picks up the pile",
            "Player 3 picks up the pile",
            "Player 1 discards a penalty card"
        ],
        "correct_answer": "Player 3 picks up the pile",
        "next_q": "5",
    },
    "5": {
        "id": 5,
        "prompt": "The following list provides the sequence of events in a game with 2 players:",
        "situation": "1. Player 1 plays an 8<br>2. Player 2 plays a 3<br>3. Player 1 plays an 8<br>4. Player 2 plays a 7<br>5. Player 1 slaps the pile",
        "question": "What happens next?",
        "answers": [
            "Player 1 picks up the pile",
            "Player 1 discards a penalty card",
            "Player 2 picks up the pile",
            "Player 2 discards a penalty card"
        ],
        "correct_answer": "Player 1 discards a penalty card",
        "next_q": "6",
    },
    "6": {
        "id": 6,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img src='/static/situation6.jpg' alt='Current pile'>",
        "question": "The next card you play is a 7. What do you do next?",
        "answers": [
            "You slap the pile",
            "You play another card",
            "You wait for the next player to go",
            "You discard a penalty card"
        ],
        "correct_answer": "You play another card",
        "next_q": "7",
    },
    "7": {
        "id": 7,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img src='/static/situation7.jpg' alt='Current pile'>",
        "question": "The next card you play is a Queen. What do you do next?",
        "answers": [
            "You slap the pile",
            "You play another card",
            "You wait for the next player to go",
            "You discard a penalty card"
        ],
        "correct_answer": "You slap the pile",
        "next_q": "8",
    },
    "8": {
        "id": 8,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img src='/static/situation8.jpg' alt='Current pile'>",
        "question": "The next card you play is a Jack. What do you do next?",
        "answers": [
            "You slap the pile",
            "You play another card",
            "You wait for the next player to go",
            "You discard a penalty card"
        ],
        "correct_answer": "You wait for the next player to go",
        "next_q": "9",
    },
    "9": {
        "id": 9,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img src='/static/situation9.jpg' alt='Current pile'>",
        "question": "Drag and drop the card that would provide the next player 1 extra turn.",
        "answers": [
            "<img src='/static/option1.jpg' alt='Option 1'>",
            "<img src='/static/option2.jpg' alt='Option 2'>",
            "<img src='/static/option3.jpg' alt='Option 3'>",
            "<img src='/static/option4.jpg' alt='Option 4'>"
        ],
        "correct_answer": "<img src='/static/option1.jpg' alt='Option 1'>",
        "next_q": "10",
    },
    "10": {
        "id": 10,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img src='/static/situation10.jpg' alt='Current pile'>",
        "question": "Drag and drop the card that would create the opportunity to slap a Sandwich.",
        "answers": [
            "<img src='/static/option1.jpg' alt='Option 1'>",
            "<img src='/static/option2.jpg' alt='Option 2'>",
            "<img src='/static/option3.jpg' alt='Option 3'>",
            "<img src='/static/option4.jpg' alt='Option 4'>"
        ],
        "correct_answer": "<img src='/static/option4.jpg' alt='Option 4'>",
        "next_q": "score",
    }
    }

# ROUTES

@app.route('/')
def home():
    return render_template('homepage.html')

#TODO: @app.route for learning portion 

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

        if type(user_answer) == str and type(correct_answer) == int:
            user_answer = int(user_answer)
        
        if user_answer == correct_answer:
            correct_counter[0] += 1
        
        print(correct_counter[0])

        next_question_id = quiz_qs[question_key]['next_q']

        if next_question_id == "score":
            return redirect(url_for('result'))
        
        return redirect(url_for('quiz', question_id=next_question_id))
    
    return "Invalid request", 400


@app.route('/result')
def result():
    return render_template('results.html', correct_count=correct_counter[0], total_questions=total_questions)
if __name__ == '__main__':


    app.run(debug=True)
