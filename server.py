from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)

quiz_qs = {
    "1":{
        "id": 1,
        "prompt": "The pile currently looks like this:",
        "situation":
        "question": "How many extra turns does the following player get?",
        "answer1": "1",
        "answer2": "2",
        "answer3": "3",
        "answer4": "4",
        "correct_answer": "answer4",
        "next_q": "2",
    },

    "2":{
        "id": 2,
        "prompt": "The pile currently looks like this:",
        "situation": 
        "question": "How many extra turns does the following player get?",
        "answer1": "1",
        "answer2": "2",
        "answer3": "3",
        "answer4": "4",
        "correct_answer": "answer1",
        "next_q": "3",
    },

    "3":{
        "id": 3,
        "prompt": "The following list provides the sequence of events in a game with 4 players:",
        "situation": "1. Player 1 plays a 3 <br> 2. Player 2 plays a King <br> 3. Player 3 plays a 2 <br> 4. Player 3 plays a King <br> 5. Player 2 slaps the pile",
        "question": "What happens next?",
        "answer1": "Player 2 picks up the pile",
        "answer2": "Player 2 discards a penalty card",
        "answer3": "Player 3 picks up the pile",
        "answer4": "Player 3 discards a penalty card",
        "correct_answer": "answer1",
        "next_q": "4",
    },

    "4":{
        "id": 4,
        "prompt": "The following list provides the sequence of events in a game with 3 players:",
        "situation": "1. Player 1 plays a 4 <br> 2. Player 2 plays a Jack <br> 3. Player 3 plays a Queen <br> 4. Player 1 plays a 2 <br> 5. Player 1 plays a 3",
        "question": "What happens next?",
        "answer1": "Player 1 picks up the pile",
        "answer2": "Player 2 picks up the pile",
        "answer3": "Player 3 picks up the pile",
        "answer4": "Player 1 discards a penalty card",
        "correct_answer": "answer3",
        "next_q": "5",
    },

    "5":{
        "id": 5,
        "prompt": "The following list provides the sequence of events in a game with 2 players:",
        "situation": "1. Player 1 plays an 8 <br> 2. Player 2 plays a 3 <br> 3. Player 1 plays an 8 <br> 4. Player 2 plays a 7 <br> 5. Player 1 slaps the pile",
        "question": "What happens next?",
        "answer1": "Player 1 picks up the pile",
        "answer2": "Player 1 discards a penalty card",
        "answer3": "Player 2 picks up the pile",
        "answer4": "Player 2 discards a penalty card",
        "correct_answer": "answer2",
        "next_q": "6",
    },

    "6":{
        "id": 6,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": 
        "question": "The next card you play is a 7. What do you do next?",
        "answer1": "You slap the pile",
        "answer2": "You play another card",
        "answer3": "You wait for the next player to go",
        "answer4": "You discard a penalty card",
        "correct_answer": "answer2",
        "next_q": "7",
    },

    "7":{
        "id": 7,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation":
        "question": "The next card you play is a Queen. What do you do next?",
        "answer1": "You slap the pile",
        "answer2": "You play another card",
        "answer3": "You wait for the next player to go",
        "answer4": "You discard a penalty card",
        "correct_answer": "answer1",
        "next_q": "8",
    },

    "8":{
        "id": 8,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": 
        "question": "The next card you play is a Jack. What do you do next?",
        "answer1": "You slap the pile",
        "answer2": "You play another card",
        "answer3": "You wait for the next player to go",
        "answer4": "You discard a penalty card",
        "correct_answer": "answer3",
        "next_q": "9",
    },

    "9":{
        "id": 9,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": 
        "question": "Drag and drop the card that would provide the next player 1 extra turn.",
        "answer1": 
        "answer2":
        "answer3":
        "answer4":
        "correct_answer": "answer1",
        "next_q": "10",
    },

    "10":{
        "id": 10,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation":
        "question": "Drag and drop the card that would create the opportunity to slap a Sandwich.",
        "answer1":
        "answer2":
        "answer3":
        "answer4":
        "correct_answer": "answer4",
        "next_q": "score",
    }
}

# ROUTES

@app.route('/')
def homepage():
    return render_template('homepage.html')

#TODO: @app.route for learning portion 

@app.route('/quiz/<int:id>')
def quiz(id):
    question = None
    for q in quiz_qs:
        if quiz_qs["id"] == id :
            question = q
            break
    return render_template('quiz.html', question=question)
