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
        "next_q": "2",
        "user_answer": None,
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
        "user_answer": None,
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
        "user_answer": None,
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
        "user_answer": None,
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
        "user_answer": None,
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
        "user_answer": None,
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
        "user_answer": None,
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
        "user_answer": None,
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
        "user_answer": None,
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
        "user_answer": None,
    }
}


lesson_ls = {
    "1": {
        "id": 1,
        "Title": "What You Need",
        "Subtitle": "Standard 52-card deck of playing cards 2-10 players",
        "Picture": "<img src='https://lh3.googleusercontent.com/pw/AP1GczMisWr5rKr0--1xvH5ilMZyJicP2B93PXoVDXF-UwtiZUhm3-5AyMw9SR3OVNGTGmklR-x__PhhSHT3jc5bdHdiuqRcuSvVMEX6RqNQzR5W4CW4pmc=w406-h195-p-k'>",
        "Category": "Setup & Gameplay",
        "Status": "1 of 5",
        "Time": None,
    },
    "2":{
        "id": 2,
        "Title": "Dealing",
        "Subtitle": "Equally distribute the deck of 52 cards between all players, with the cards face down",
        "Picture" : "<img src='https://lh3.googleusercontent.com/pw/AP1GczMLtTeM6rCr32POizTQWawXzuVt9KJFPlDytetQkn1snSaMI5p43FKSyCH6mXNLB7adnIP7A81H1H5PJ5lQOmY2fKBJl4IkElh5zFQ8fUNXonrIFbc=w2400'>",
        "Category": "Setup & Gameplay",
        "Status": "2 of 5",
    },
    "3":{
        "id": 3,
        "Title": "First Move",
        "Subtitle": "Start by having the player to the left of the dealer reveal the top card from their deck, placing it evenly between all players.",
        "Picture": "<img src= 'https://lh3.googleusercontent.com/pw/AP1GczP-HY87abIoKjF-F8YAy505RhF1GxnJ6oLJoxlYxTZ7AZtH21vAkac7dO5VN-L6GcDRE4uAbir6PmEjup54Y_kKSL7axGJx0iRlwH2XxgqQDcTtwqw=w2400'>",
        "Category": "Setup & Gameplay",
        "Status": "3 of 5",
    },
    "4":{
        "id": 4,
        "Title": "Direction of Gameplay",
        "Subtitle": "Continue in the clockwise direction",
        "Picture" : "<img src='https://lh3.googleusercontent.com/pw/AP1GczPXzAm9oGflZu4_bEfnkTfuQqf64i-rFghXkQSdo3cO8YHwaSme0EsLj-Kw_7izV6-rQWkQ1fmsW22P4b0CAyTSCk4bNzWBIZycg71PXHQGlJrrOK4=s251-p-k'>",
        "Category": "Setup & Gameplay",
        "Status": "4 of 5",
    },
    "5":{
        "id": 5,
        "Title": "Overall Goal",
        "Subtitle": "You want to claim all of the cards",
        "Picture" : "<img src= 'https://lh3.googleusercontent.com/pw/AP1GczOr_R9CM201_5gO1nSMM5zz0KR6MMg5XYMYOlzt8bHZoA5J9ILsxSRrzK2OdTM75xIJUAxebGtHDqYJk3kivj_pImwMvay3Y4t6-CgiIG3habwm0pQ=w2400'>",
        "Category": "Setup & Gameplay",
        "Status": "5 of 5",
    },
    "6":{
        "id": 6,
        "Title": "Slapping Rules",
        "Subtitle":"Cards can be claimed by slapping the pile at appropriate moments. The first person to slap the pile claims it, and adds it to the bottom of their deck.",
        "Picture":"<img src='https://lh3.googleusercontent.com/pw/AP1GczMprywbxxIddLt5exY2L3yLBQptnWQlzIUTgTglP9IybHz-iMkJuDdObUzvSroUY0Y-crRACL8UiYK_LQ9ptlf557VedFoxVH6LotXYlEdg8CkVNGA=w2400'>",
        "Example":"",
        "Category":"Rules",
        "Status":"1 of 18",
    },
    "7":{
        "id": 7,
        "Title": "Slapping Rules: Doubles",
        "Subtitle":"If two consecutive cards with the same value are played, players may slap and claim the pile. ",
        "Picture":"<img src='https://lh3.googleusercontent.com/pw/AP1GczO8Y9NxoKDDN3lEC5AoeD1HMOpQ6ph4WIPZ0yxxbvSnaAntfU48qM4WOE2Q5SerH4eBaQiyCXLWS51aRQuS-Xrl_zb_jqcKfZcEKO_3M8lMcoSkTZs=w2400'>",
        "Example":"Ex. one player plays a 6 and the next player also plays a 6",
        "Category":"Rules",
        "Status":"2 of 18",
    },
    "8":{
        "id": 8,
        "Title": "Slapping Rules: Sandwiches",
        "Subtitle":"Players may slap and claim the pile if two cards of the same value are played with only one card of a different value between them.",
        "Picture":"<img src='https://lh3.googleusercontent.com/pw/AP1GczN2HVAqKC0mfwD7uahUsRVqQ3lwfROHVpkZCJ89OOAEei6rSep4-LPR3d0cwprO1ftUQvZaPF3dcp3WW_2QA2JcxWAyOINaMquRIeiCh55Z0r5EDTA=w2400'>",
        "Example":"Ex. one player plays a 7, the next player plays a 4, and the following player plays a 7",
        "Category":"Rules",
        "Status":"3 of 18",
    },
    "9":{
        "id": 9,
        "Title": "Slapping Rules: Marriages",
        "Subtitle":"Players may slap and claim the pile if a King and Queen are played consecutively, in any order.",
        "Picture":"<img src='https://lh3.googleusercontent.com/pw/AP1GczMZxhaNn_xmPZY-wNQ1QLZ0pNlqa4SbOWtLT08q91DkFFECQtXd6rpkMvpA5udbsqfkic5NKTheOFU9vLJ6Prv64zW68Tzdf5oBIN2siV-wSn4plPI=w2400'>",
        "Example":"Ex. one player plays a Queen and the next player plays a King",
        "Category":"Rules",
        "Status":"4 of 18",
    },
    "10":{
        "id": 10,
        "Title": "Slapping Rules: Sums of 10",
        "Subtitle":"Players may slap and claim the pile if the value of two consecutive cards adds up to 10.",
        "Picture":"<img src='https://lh3.googleusercontent.com/pw/AP1GczNnvjSNhnkPllZ5nt_fVLyTJjAC-zL3XVZUTtctz4n-sdMVnRafN6E4ldI7p9EyHxYy5-nhXMol1W-1Sd9WybWSuazdNhCMqrSFzovBeTzm5wRuk4c=w2400'>",
        "Example":"Ex. one player plays a 3 and the next player plays a 7",
        "Category":"Rules",
        "Status":"5 of 18",
    },
    "11":{
        "id": 11,
        "Title": "Slapping Rules: Blocking",
        "Subtitle":"If any of the previously described slapping situations occurs, the next player can block by playing another card before other players have a chance to slap.",
        "Picture":"<img src='https://lh3.googleusercontent.com/pw/AP1GczPYCiqyohv60uboXe4A7Ua9J1egh0auqU6Ls9PV1mJoANo04bJG11MDktj-KgxFPNQZBmxAmFWf9LK4bj4DT1TwCwPDPUvWaqdfcnN2Bp1fBZr54y0=w2400'>",
        "Example":"Ex. there is a double 7 in the pile, but the following player plays a 2 before anybody can slap",
        "Category":"Rules",
        "Status":"6 of 18",
    },
    "12":{
        "id": 12,
        "Title": "Slapping Rules: Penalty",
        "Subtitle":"If any player falsely slaps, they must discard the top card from their deck and place it at the bottom of the pile, face up.",
        "Picture":"<img src='https://lh3.googleusercontent.com/pw/AP1GczPT-m-gMmccv-5MaP8huDMQhOkWTEcDaIwZIY88xDKxya6R1kKwBvgnOf37vwRYaZq1b00VRd4s71_OnPcfX4FSrjk9DwcAuyedlvUJyIQApk4pPD8=w2400'>",
        "Example":"Ex. a player slaps the pile with an 8 and a 3 at the top",
        "Category":"Rules",
        "Status":"7 of 18",
    },
    "13":{
        "id": 13,
        "Title": "Slapping Rules: Slapped at the Same Time?",
        "Subtitle":"If you cannot determine who slapped first, the person with the most fingers on the pile claims it. ",
        "Picture":"<img src='https://lh3.googleusercontent.com/pw/AP1GczNjEhRKXICb0Da1LSgWZ0EVELxG6Dc_vMUKF4xykFoDp3gEll1pstwzHkRHvxKH9f0gij7Mw5o3uFeIX9zANLV3qiNn446WzzF_F9-UZ6V4pINE7bY=w2400'>",
        "Example":"",
        "Category":"Rules",
        "Status":"8 0f 18",
    },
    "14":{
        "id": 14,
        "Title": "Face Cards and Aces",
        "Subtitle":"Face cards and aces provide players new opportunities to claim cards!",
        "Picture":"<img src='https://lh3.googleusercontent.com/pw/AP1GczMRM9VAw5GUZa9jtyIpeTDSOYdHBJLFLNOMlvuLuAmChwriKzyvwjCI6Ei5VpVci1FGD9Qm3oxFECsYrdpHIurMEbKDBZcnqNAhlywM6d7RK12E70k=w2400'>",
        "Example":"",
        "Category":"Rules",
        "Status":"9 of 18",
    },
    "15":{
        "id": 15,
        "Title": "Face Cards and Aces: Extra Turns",
        "Subtitle":"When face cards and aces are played, each one implies a different number of turns the next player gets to try to play another face card or ace.",
        "Picture":"<img src=''>",
        "Example":"",
        "Category":"Rules",
        "Status":"10 of 18",
    },
    "16":{
        "id": 16,
        "Title": "Face Cards and Aces: Jacks",
        "Subtitle":"When a Jack is played, the next player gets 1 turn to play another face card or ace.",
        "Picture":"<img src=''>",
        "Example":"",
        "Category":"Rules",
        "Status":"11 of 18",
    },
    "17":{
        "id": 17,
        "Title": "Face Cards and Aces: Queens",
        "Subtitle":"When a Queen is played, the next player gets 2 turns to play another face card or ace.",
        "Picture":"<img src=''>",
        "Example":"",
        "Category":"Rules",
        "Status":"12 of 18",
    },
    "18":{
        "id": 18,
        "Title": "Face Cards and Aces: Kings",
        "Subtitle":"When a King is played, the next player gets 3 turns to play another face card or ace,",
        "Picture":"<img src=''>",
        "Example":"",
        "Category":"Rules",
        "Status":"13 of 18",
    },
    "19":{
        "id": 19,
        "Title": "Face Cards and Aces: Aces",
        "Subtitle":"When an Ace is played, the next player gets 4 turns to play another face card or ace.",
        "Picture":"<img src=''>",
        "Example":"",
        "Category":"Rules",
        "Status":"14 of 18",
    },
    "20":{
        "id": 20,
        "Title": "Face Cards and Aces: Turnout",
        "Subtitle":"When a player is unsuccessful at playing another face card or ace within their extra turns, the most recent person to play a face card or ace picks up the pile.",
        "Picture":"<img src=''>",
        "Example":"",
        "Category":"Rules",
        "Status":"15 of 18",
    },
    "21":{
        "id": 21,
        "Title": "Face Cards and Aces: Running Out of Cards",
        "Subtitle":"If a player runs out of cards during their chain of extra turns, the following player picks up where this player left off.",
        "Picture":"<img src=''>",
        "Example":"",
        "Category":"Rules",
        "Status":"16 of 18",
    },
    "22":{
        "id": 22,
        "Title": "Face Cards and Slapping",
        "Subtitle":"If an opportunity to slap arises within a chain of extra turns, players may interrupt the extra turns and slap and claim the pile.",
        "Picture":"<img src=''>",
        "Example":"",
        "Category":"Rules",
        "Status":"17 of 18",
    },
    "23":{
        "id": 23,
        "Title": "Running out of Cards",
        "Subtitle":"If a player runs out of cards, they are not disqualified! They still have the opportunity to slap the pile, claim cards, and return to normal gameplay.",
        "Picture":"<img src=''>",
        "Example":"",
        "Category":"Rules",
        "Status":"18 of 18",
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

@app.route('/setup/<int:lesson_id>')
def setup(lesson_id):
    """Serve a lesson page or redirect based on lesson_id."""
    if lesson_id < 6:
         lesson_key = str(lesson_id)
    else:
        return render_template('overview.html')

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
        quiz_qs['user_answer'] = user_answer

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
