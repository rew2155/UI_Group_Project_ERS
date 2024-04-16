from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)

quiz_qs = {
    "1":{
        "id": 1,
        "prompt": "The pile currently looks like this:",
        "situation": "<img id='situation' source='https://live.staticflickr.com/4053/4616131778_4e21a66456_w.jpg'>" #add classes to format image
        "question": "How many extra turns does the following player get?",
        "answer1": "<button id='option1'> 1 </div>",
        "answer2": "<button id='option2'> 2 </div>",
        "answer3": "<button id='option3'> 3 </div>",
        "answer4": "<button id='option4'> 4 </div>",
        "correct_answer": "answer4",
        "next_q": "2",
    },

    "2":{
        "id": 2,
        "prompt": "The pile currently looks like this:",
        "situation": "<img id='situation' source=''>" #add image file
        "question": "How many extra turns does the following player get?",
        "answer1": "<button id='option1'> 1 </div>",
        "answer2": "<button id='option2'> 2 </div>",
        "answer3": "<button id='option3'> 3 </div>",
        "answer4": "<button id='option4'> 4 </div>",
        "correct_answer": "answer1",
        "next_q": "3",
    },

    "3":{
        "id": 3,
        "prompt": "The following list provides the sequence of events in a game with 4 players:",
        "situation": "1. Player 1 plays a 3 <br> 2. Player 2 plays a King <br> 3. Player 3 plays a 2 <br> 4. Player 3 plays a King <br> 5. Player 2 slaps the pile", #maybe make this its own div with a border around it
        "question": "What happens next?",
        "answer1": "<button id='option1'> Player 2 picks up the pile </div>",
        "answer2": "<button id='option2'> Player 2 discards a penalty card </div>",
        "answer3": "<button id='option3'> Player 3 picks up the pile </div>",
        "answer4": "<button id='option4'> Player 3 discards a penalty card </div>",
        "correct_answer": "answer1",
        "next_q": "4",
    },

    "4":{
        "id": 4,
        "prompt": "The following list provides the sequence of events in a game with 3 players:",
        "situation": "1. Player 1 plays a 4 <br> 2. Player 2 plays a Jack <br> 3. Player 3 plays a Queen <br> 4. Player 1 plays a 2 <br> 5. Player 1 plays a 3", #maybe make this its own div with a border around it
        "question": "What happens next?",
        "answer1": "<button id='option1'> Player 1 picks up the pile </div>",
        "answer2": "<button id='option2'> Player 2 picks up the pile </div>",
        "answer3": "<button id='option3'> Player 3 picks up the pile </div>",
        "answer4": "<button id='option4'> Player 1 discards a penalty card </div>",
        "correct_answer": "answer3",
        "next_q": "5",
    },

    "5":{
        "id": 5,
        "prompt": "The following list provides the sequence of events in a game with 2 players:",
        "situation": "1. Player 1 plays an 8 <br> 2. Player 2 plays a 3 <br> 3. Player 1 plays an 8 <br> 4. Player 2 plays a 7 <br> 5. Player 1 slaps the pile", #maybe make this its own div with a border around it
        "question": "What happens next?",
        "answer1": "<button id='option1'> Player 1 picks up the pile </div>",
        "answer2": "<button id='option2'> Player 1 discards a penalty card </div>",
        "answer3": "<button id='option3'> Player 2 picks up the pile </div>",
        "answer4": "<button id='option4'> Player 2 discards a penalty card </div>",
        "correct_answer": "answer2",
        "next_q": "6",
    },

    "6":{
        "id": 6,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img id='situation' source=''>" #add image file
        "question": "The next card you play is a 7. What do you do next?",
        "answer1": "<button id='option1'> You slap the pile </div>",
        "answer2": "<button id='option2'> You play another card </div>",
        "answer3": "<button id='option3'> You wait for the next player to go </div>",
        "answer4": "<button id='option4'> You discard a penalty card </div>",
        "correct_answer": "answer2",
        "next_q": "7",
    },

    "7":{
        "id": 7,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img id='situation' source=''>" #add image file
        "question": "The next card you play is a Queen. What do you do next?",
        "answer1": "<button id='option1'> You slap the pile </div>",
        "answer2": "<button id='option2'> You play another card </div>",
        "answer3": "<button id='option3'> You wait for the next player to go </div>",
        "answer4": "<button id='option4'> You discard a penalty card </div>",
        "correct_answer": "answer1",
        "next_q": "8",
    },

    "8":{
        "id": 8,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img id='situation' source=''>" #add image file
        "question": "The next card you play is a Jack. What do you do next?",
        "answer1": "<button id='option1'> You slap the pile </div>",
        "answer2": "<button id='option2'> You play another card </div>",
        "answer3": "<button id='option3'> You wait for the next player to go </div>",
        "answer4": "<button id='option4'> You discard a penalty card </div>,
        "correct_answer": "answer3",
        "next_q": "9",
    },

    "9":{
        "id": 9,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img id='situation' source='https://photos.app.goo.gl/NsvNfDmdoTh6VskK8'>" #check if this link works and add formatting options
        "question": "Drag and drop the card that would provide the next player 1 extra turn.",
        "answer1": "<img id='option1' source='https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.m.wikipedia.org%2Fwiki%2FFile%3AEnglish_pattern_jack_of_hearts.svg&psig=AOvVaw3f3NWx_1v2ad-ewWqizg8U&ust=1713358629566000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCJj30LbkxoUDFQAAAAAdAAAAABAE'>" #add formatting options
        "answer2": "<img id='option2' source='https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/51_Q_di_picche.jpg/800px-51_Q_di_picche.jpg'>" #add formatting options
        "answer3": "<img id='option3' source='https://static.wikia.nocookie.net/aliceinborderland/images/1/16/King_of_Clubs.png/revision/latest?cb=20221106041043'>" #add formatting options
        "answer4": "<img id='option4' source='https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/01_of_spades_A.svg/1200px-01_of_spades_A.svg.png'>" #add formatting options
        "correct_answer": "answer1",
        "next_q": "10",
    },

    "10":{
        "id": 10,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img id='situation' source='https://photos.app.goo.gl/81rT9RTwFGeauvpi9'>" #check if this link works and add formatting options
        "question": "Drag and drop the card that would create the opportunity to slap a Sandwich.",
        "answer1": "<img id='option1' source='https://static.wikia.nocookie.net/aliceinborderland/images/3/3f/Three_of_Clubs.png/revision/latest?cb=20221106040648'>" #add formatting options
        "answer2": "<img id='option2' source='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/839f488c-d377-4eeb-999f-6bcace090bb4/d3kgfp4-4f84f045-9bd5-41b6-a725-49d6ffe02db7.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzgzOWY0ODhjLWQzNzctNGVlYi05OTlmLTZiY2FjZTA5MGJiNFwvZDNrZ2ZwNC00Zjg0ZjA0NS05YmQ1LTQxYjYtYTcyNS00OWQ2ZmZlMDJkYjcucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.G2m-VwK3lNCoL64myCu1MOGlgmqqrLARfmRXFL9YW_s'>" #add formatting options
        "answer4": "<img id='option4' source='https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/51_Q_di_picche.jpg/800px-51_Q_di_picche.jpg'>" #add formatting options
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
