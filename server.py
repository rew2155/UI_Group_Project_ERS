from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)
total_questions = 10
correct_counter = [0]

quiz_qs = {
    "1": {
        "id": 1,
        "prompt": "The pile currently looks like this:",
        "situation": "<img class='situation_img' src='https://familymath.stanford.edu/wp-content/uploads/2021/08/playing-cards-e1628288827705.jpg' alt='Situation Image'>",
        "question": "How many extra turns does the following player get?",
        "answer1": "<button id='answer1' class='btn'>1 turn</button>", 
        "answer2": "<button id='answer2' class='btn'>2 turns</button>",
        "answer3": "<button id='answer3' class='btn'>3 turns</button>",
        "answer4": "<button id='answer4' class='btn'>4 turns</button>",
        "correct_answer": "answer4",
        "prev_q": None,
        "next_q": "2",
        "explanation": "An Ace always indicates that a player gets 4 extra turns.",
        "user_answer": None,
    },

    "2":{
        "id": 2,
        "prompt": "The pile currently looks like this 2:",
        "situation": "<img id='situation' class='situation_img' src='https://www.wargamer.com/wp-content/sites/wargamer/2022/04/playing-card-games-kemps.jpg' alt='Situation Image'>", 
        "question": "How many extra turns does the following player get?",
        "answer1": "<button id='answer1' class='btn'>1 turn</button>", 
        "answer2": "<button id='answer2' class='btn'>2 turns</button>",
        "answer3": "<button id='answer3' class='btn'>3 turns</button>",
        "answer4": "<button id='answer4' class='btn'>4 turns</button>",
        "correct_answer": "answer1",
        "prev_q": "1",
        "next_q": "3",
        "explanation": "A Jack always indicates that a player gets 1 extra turn.",
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
        "answer1": "<button id='answer1' class='btn'>Player 2 picks up the pile</button>", 
        "answer2": "<button id='answer2' class='btn'>Player 2 discards a penalty card</button>",
        "answer3": "<button id='answer3' class='btn'>Player 3 picks up the pile</button>",
        "answer4": "<button id='answer4' class='btn'>Player 3 discards a penalty card</button>",
        "correct_answer": "answer1",
        "prev_q": "2",
        "next_q": "4",
        "explanation": "Player 2 appropriately slapped a King-2-King Sandwich, and can pick up the pile.",
        "user_answer": None,
        },

    "4": {
        "id": 4,
        "prompt": "The following list provides the sequence of events in a game with 3 players:",
        "situation": "1. Player 1 plays a 4<br>2. Player 2 plays a Jack<br>3. Player 3 plays a Queen<br>4. Player 1 plays a 2<br>5. Player 1 plays a 3",
        "question": "What happens next?",
        "answer1": "<button id='answer1' class='btn'>Player 1 picks up the pile</button>", 
        "answer2": "<button id='answer2' class='btn'>Player 2 picks up the pile</button>",
        "answer3": "<button id='answer3' class='btn'>Player 3 picks up the pile</button>",
        "answer4": "<button id='answer4' class='btn'>Player 1 discards a penalty card</button>",
        "correct_answer": "answer3",
        "prev_q": "3",
        "next_q": "5",
        "explanation": "Player 3 played a Queen and Player 1 did not play a face card within their two extra turns, so Player 3 gets to pick up the pile.",
        "user_answer": None,
    },

    "5": {
        "id": 5,
        "prompt": "The following list provides the sequence of events in a game with 2 players:",
        "situation": "1. Player 1 plays an 8<br>2. Player 2 plays a 3<br>3. Player 1 plays an 8<br>4. Player 2 plays a 7<br>5. Player 1 slaps the pile",
        "question": "What happens next?",
        "answer1": "<button id='answer1' class='btn'>Player 1 picks up the pile</button>", 
        "answer2": "<button id='answer2' class='btn'>Player 1 discards a penalty card</button>",
        "answer3": "<button id='answer3' class='btn'>Player 2 picks up the pile</button>",
        "answer4": "<button id='answer4' class='btn'>Player 2 discards a penalty card</button>",
        "correct_answer": "answer2",
        "prev_q": "4",
        "next_q": "6",
        "explanation": "Player 1 did not slap the pile at an appropriate moment, so they must discard a penalty card.",
        "user_answer": None,
    },

    "6": {
        "id": 6,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img class='situation_img' src='https://cdn11.bigcommerce.com/s-sjl48p9/images/stencil/500x659/products/493/477/Jumbo_Deck_of_Cards__00402.1355263732.jpg?c=2' alt='Current pile'>",
        "question": "The next card you play is a 7. What do you do next?",
        "answer1": "<button id='answer1' class='btn'>You slap the pile</button>", 
        "answer2": "<button id='answer2' class='btn'>You play another card</button>",
        "answer3": "<button id='answer3' class='btn'>You wait for the next player to go</button>",
        "answer4": "<button id='answer4' class='btn'>You discard a penalty card</button>",
        "correct_answer": "answer2",
        "prev_q": "5",
        "next_q": "7",
        "explanation": "You have only used one out of your three extra turns to play another face card, so you will have to play another card for your second extra turn.",
        "user_answer": None,
    },

    "7": {
        "id": 7,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img class='situation_img' src='https://cdn.shopify.com/s/files/1/1788/4029/files/download_12_large.jpg?v=1566685316' alt='Current pile'>",
        "question": "The next card you play is a Queen. What do you do next?",
        "answer1": "<button id='answer1' class='btn'>You slap the pile</button>", 
        "answer2": "<button id='answer2' class='btn'>You play another card</button>",
        "answer3": "<button id='answer3' class='btn'>You wait for the next player to go</button>",
        "answer4": "<button id='answer4' class='btn'>You discard a penalty card</button>",
        "correct_answer": "answer1",
        "prev_q": "6",
        "next_q": "8",
        "explanation": "You should slap the pile because there is now a Queen-Jack-Queen Sandwich.",
        "user_answer": None,
    },

    "8": {
        "id": 8,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img class='situation_img' src='https://as2.ftcdn.net/v2/jpg/00/80/62/95/1000_F_80629529_zmqcu0Oz8kc0a6PLN97lLexpFWIvG275.jpg' alt='Current pile'>",
        "question": "The next card you play is a Jack. What do you do next?",
        "answer1": "<button id='answer1' class='btn'>You slap the pile</button>", 
        "answer2": "<button id='answer2' class='btn'>You play another card</button>",
        "answer3": "<button id='answer3' class='btn'>You wait for the next player to go</button>",
        "answer4": "<button id='answer4' class='btn'>You discard a penalty card</button>",
        "correct_answer": "answer3",
        "prev_q": "7",
        "next_q": "9",
        "explanation": "You should slap the pile because there is now a Queen-Jack-Queen Sandwich.",
        "user_answer": None,
    },

    "9": {
        "id": 9,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img class='situation_img' src='https://lh3.googleusercontent.com/pw/AP1GczNEqnPt9mhOK38n0I-reh-aftn0RMPkffsRB9vpK-J4fUxWZnOMxJjsotzgWCsn8HfCKnAZvaooqU0IcPMtYlaf8rqQUmWt0fWbl5GvUiqHjM_Fmqo=w2400' alt='Current pile'>",
        "question": "Drag and drop the card that would provide the next player 1 extra turn.",
        "answer1": "<img id='answer1' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/English_pattern_jack_of_spades.svg/1200px-English_pattern_jack_of_spades.svg.png' alt='Option 1'>", 
        "answer2": "<img id='answer2' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/c/ca/English_pattern_queen_of_spades.svg' alt='Option 2'>",
        "answer3": "<img id='answer3' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/1/1c/English_pattern_king_of_diamonds.svg' alt='Option 3'>",
        "answer4": "<img id='answer4' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/English_pattern_ace_of_diamonds.svg/1200px-English_pattern_ace_of_diamonds.svg.png' alt='Option 4'>",
        "correct_answer": "answer1",
        "prev_q": "8",
        "next_q": "10",
        "explanation": "A Jack always indicates that the next player should receive one extra turn.",
        "user_answer": None,
    },
    
    "10": {
        "id": 10,
        "prompt": "It's your turn and the pile currently looks like this:",
        "situation": "<img class='situation_img' src='https://lh3.googleusercontent.com/pw/AP1GczMCiCQm4x2TuVIgJLTjPHO-rAtJXUlovC2GeU9cOSVwfQV2-zEh6qAs4UMOKOYxitg7pkWRUJFTgsmDtMraj58Q1hDRVMW9LT50q2_ellCGAY5CEW8=w2400' alt='Current pile'>",
        "question": "Drag and drop the card that would create the opportunity to slap a Sandwich.",
        "answer1": "<img id='answer1' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/5_of_clubs.svg/1200px-5_of_clubs.svg.png' alt='Option 1'>", 
        "answer2": "<img id='answer2' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/7_of_clubs.svg/1200px-7_of_clubs.svg.png' alt='Option 2'>",
        "answer3": "<img id='answer3' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/English_pattern_ace_of_diamonds.svg/1200px-English_pattern_ace_of_diamonds.svg.png' alt='Option 3'>",
        "answer4": "<img id='answer4' class='drag_card' src='https://upload.wikimedia.org/wikipedia/commons/c/ca/English_pattern_queen_of_spades.svg' alt='Option 4'>",
        "correct_answer": "answer4",
        "prev_q": "9",
        "next_q": "score",
        "explanation": "The last card played was an Ace, and the card played before that was a Queen, so you would want to play a Queen to create a Queen-Ace-Queen Sandwich.",
        "user_answer": None,
    }
}


lesson_ls = {
    "1": {
        "id": 1,
        "Title": "What You Need",
        "Subtitle1": "Standard 52-card deck of playing cards. You are allowed 2-10 players.",
        "Picture": "https://lh3.googleusercontent.com/pw/AP1GczNvOZMAFdBRAdjN-Ob2zmBrGdP-J8Kw7ykEFMKL6Yn8X-uZV7T0LE9U2gWwEhrHWrivacdBrPkWC7AxY3vht8voL2xOvMS52tfQokdDIs4Iy7DxwvM=w2400",
        "Category": "Setup & Gameplay",
        "Status": "1 of 5",
        "Time": None,
    },
    "2":{
        "id": 2,
        "Title": "Dealing",
        "Subtitle1": "Equally distribute the deck of 52 cards between all players, with the cards face down",
        "Picture" : "https://lh3.googleusercontent.com/pw/AP1GczOnVvGPe4OpAtdKJXP7NAIz-B2Zjwb7eau9i4P7ZvXVX1rt4div9jKws7c6J_mEu1_q--WrRc_pF81mScIlrF3VtGKitGW7PFA-DDgIJxdXxKux1Ik=w2400",
        "Category": "Setup & Gameplay",
        "Status": "2 of 5",
        "Time": None,
    },
    "3":{
        "id": 3,
        "Title": "First Move",
        "Subtitle1": "Start by having the player to the left of the dealer reveal the top card from their deck, placing it evenly between all players.",
        "Picture": "https://lh3.googleusercontent.com/pw/AP1GczPOg1BmyjSGzXFgP-xwLSgJigTUa5dkfdqvcIaVuD0b6NxF6vkVRqhO9s1vLg9ASp0uOQUTh12gM8dl_uT466EX_PwRedjpS0Mc20qkAXDF2_hvKNs=w2400",
        "Category": "Setup & Gameplay",
        "Status": "3 of 5",
        "Time": None,
    },
    "4":{
        "id": 4,
        "Title": "Direction of Gameplay",
        "Subtitle1": "Continue in the clockwise direction",
        "Picture" : "https://lh3.googleusercontent.com/pw/AP1GczPSrOzl99VfKtI0TxlQltJFuYZCFiWMM81xuhGmodIIyhtoyucQ8Am6LYs46sS7_qwLFf5rSJDyh9hjmFd2gxmB48xyy7lhr8PdhECMNHtMwsv29Uo=s251-p-k",
        "Category": "Setup & Gameplay",
        "Status": "4 of 5",
        "Time": None,
    },
    "5":{
        "id": 5,
        "Title": "Overall Goal",
        "Subtitle1": "You want to claim all of the cards",
        "Picture" : "https://lh3.googleusercontent.com/pw/AP1GczOOKZX7H2o4QjHZEzSgf7G5We0j8wzbgLVsXkjtvr-nRkOnjvN9lLg8RjEMQQbHpJAGKQIePROInCSCxsyguJNPj1_P8H0PEzmZjUf98rkIXvZuDw4=w2400",
        "Category": "Setup & Gameplay",
        "Status": "5 of 5",
        "Time": None,
    },
    "6":{
        "id": 6,
        "Title": "Slapping Rules",
        "Subtitle1":"Cards can be claimed by slapping the pile at appropriate moments. The first person to slap the pile claims it, and adds it to the bottom of their deck.", 
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczOVWv5wIrvFBFiqb2lWS2Cq8M0GAZmyphnGemlAl8SBCR3HaK_DIOd4-dOw-33Z82RQ2rOyPOQ8riUI0MDxJLb9zolPp9VZfulh1OOUlxObMqpNEJI=w2400",
        "Example":"",
        "Category":"Rules",
        "Status":"1 of 18",
        "Time": None,
    },
    "7":{
        "id": 7,
        "Title": "Slapping Rules:",
        "Title2":"Doubles",
        "Subtitle1":"If two consecutive cards with the same value are played, players may slap and claim the pile.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczNp0aahGUf4objn1zwn8LmL_-Zoyp5u06oWG6g8nhWGPrBSm8_Ec7R8XDx4VTRrX5XcggPTNEMNswcRP2nx90y31jfqZbzy1tCBQ8kDgDvTp8KsSPs=w2400",
        "Example":"Ex. one player plays a 6 and the next player also plays a 6",
        "Category":"Rules",
        "Status":"2 of 18",
        "Time": None,
    },
    "8":{
        "id": 8,
        "Title": "Slapping Rules:",
        "Title2": "Sandwiches",
        "Subtitle1":"Players may slap and claim the pile if two cards of the same value are played with only one card of a different value between them.", 
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczOENs8x60JTuVZvbu-2o_Wk4khQF-eNStTDeY3AnGAlGalduY6EB6AUA5DqcyzK2kcoW5I4hjXwux1N05oaCAiaX-EooOJRxs6jTi5VMTiYfwZ82bY=w2400",
        "Example":"Ex. one player plays a 7, the next player plays a 4, and the following player plays a 7",
        "Category":"Rules",
        "Status":"3 of 18",
        "Time": None,
    },
    "9":{
        "id": 9,
        "Title": "Slapping Rules:",
        "Title2": "Marriages",
        "Subtitle1":"Players may slap and claim the pile if a King and Queen are played consecutively, in any order.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczOi9NMD7gSJDc5PonFAR5L2weyEnKXnk5FcuqHU7-jLc8zT7nETl9X14w-PUJtabiQmOY_w9aKdxdTz0XNnmVw-eyw4iK_2FdT73H4ZPnhUsGMsDZ0=w2400",
        "Example":"Ex. one player plays a Queen and the next player plays a King",
        "Category":"Rules",
        "Status":"4 of 18",
        "Time": None,
    },
    "10":{
        "id": 10,
        "Title": "Slapping Rules:",
        "Title2": "Sums of 10",
        "Subtitle1":"Players may slap and claim the pile if the value of two consecutive cards adds up to 10.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczPZn86IiyD0aWncidOChInjGZZsPItXomoC1qSM57T4Tqv2o4K2_AWzdtE4m-MKl--gC1559RO-Vj5AdtInn22U3WnynK7XzRiOU4gtBOWd8Y0j-Hs=w2400",
        "Example":"Ex. one player plays a 3 and the next player plays a 7",
        "Category":"Rules",
        "Status":"5 of 18",
        "Time": None,
    },
    "11":{
        "id": 11,
        "Title": "Slapping Rules:",
        "Title2": "Blocking",
        "Subtitle1":"If any of the previously described slapping situations occurs, the next player can block by playing another card before other players have a chance to slap.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczNrduTlcnTS7rPoOxDjqhDcyVlcKTJhZbfoSR73sjPb_Vz03BKiGOr9J_pVN6Wd0ED2ouiAyHLpaxc8upGiyjR2spYitYh2bwXMrzeT3nfc40QhsDw=w2400",
        "Example":"Ex. there is a double 7 in the pile, but the following player plays a 2 before anybody can slap",
        "Category":"Rules",
        "Status":"6 of 18",
        "Time": None,
    },
    "12":{
        "id": 12,
        "Title": "Slapping Rules:",
        "Title2": "Penalty",
        "Subtitle1":"If any player falsely slaps, they must discard the top card from their deck and place it at the bottom of the pile, face up.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczOzu5wqCXBuqWF4zlEHEDBCtCA6qxVGlRk0TIUVZ4AtIl7oRxCiiFyTcQmjx1hq1uEjDjVuSJuoXx4JBtiPl7eznbR-JtFBPIx73CbHiPHDZPQnRpc=w2400",
        "Example":"Ex. a player slaps the pile with an 8 and a 3 at the top",
        "Category":"Rules",
        "Status":"7 of 18",
        "Time": None,
    },
    "13":{
        "id": 13,
        "Title": "Slapping Rules: Slapped at the Same Time?",
        "Subtitle1":"If you cannot determine who slapped first, the person with the most fingers on the pile claims it.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczOP4zvi_5GURl8Z8cuk8Q4sbWE2ubyRyP2pFbwun5cs10vHTMoUhssbJ60dHQO7zKOn11qumV2_2YqKF13KclGaomj_1cuZO9ZFaBgtvIxj8OZHj7s=w2400",
        "Example":"",
        "Category":"Rules",
        "Status":"8 of 18",
        "Time": None,
    },
    "14":{
        "id": 14,
        "Title": "Face Cards and Aces",
        "Subtitle1":"Face cards and aces provide players new opportunities to claim cards!",
        "Picture": "https://lh3.googleusercontent.com/pw/AP1GczOFINKO3aiJIuDBSuClrYCoB1b8fWVi0wCQXPQJ8hGCCOzpEMzZVRPVl4k-9z4uHJwdRlHn8dPwMYsOmCGy3gxMY-ci3esafgldnCDd0JMYsQ3tF6U=w2400",
        "Example":"",
        "Category":"Rules",
        "Status":"9 of 18",
        "Time": None,
    },
    "15":{
        "id": 15,
        "Title": "Face Cards and Aces:",
        "Title2": "Extra Turns",
        "Subtitle1":"When face cards and aces are played, each one implies a different number of turns the next player gets to try to play another face card or ace.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczNKzrOzJGVxJ-jUw4O6d82sYgn5BXbx0SAIPV1FhJPN-WcXAO85WCZ9Um_OjndoU8M8_1DK0OZFqVmZ7PeuPXRXqukdXwSZFGwO0Q_4i4WTmaZkYB8=w2400",
        "Example":"",
        "Category":"Rules",
        "Status":"10 of 18",
        "Time": None,
    },
    "16":{
        "id": 16,
        "Title": "Face Cards and Aces:",
        "Title2": "Jacks",
        "Subtitle1":"When a Jack is played, the next player gets", 
        "bigNum": 1,
        "Subtitle2": "turn to play another face card or ace.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczP0-gQT71HZEsvDxnvnLedQH4wvZGX8jZ3DMBtY1vknPtY9QlfcIwWNj96REjF502qh59ih8hg7Ex8itxxWhwJJzVKSkQ7jARgq3Ilkv8KahUiwWsI=w2400",
        "Example":"",
        "Category":"Rules",
        "Status":"11 of 18",
        "Time": None,
    },
    "17":{
        "id": 17,
        "Title": "Face Cards and Aces:",
        "Title2": "Queens",
        "Subtitle1":"When a Queen is played, the next player gets", 
        "bigNum": 2, 
        "Subtitle2": "turns to play another face card or ace.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczMic_btP2-Xhen-scCw7D5PFArPKkRxcs0xrESZQDj8PZYp2AmTx63imxEyrwNu4Xy9WEeHjYKMvZ3QDrmpOoQeimlprCiwbJRFOzzGmO5A6BWa49Y=w2400",
        "Example":"",
        "Category":"Rules",
        "Status":"12 of 18",
        "Time": None,
    },
    "18":{
        "id": 18,
        "Title": "Face Cards and Aces:",
        "Title2": "Kings",
        "Subtitle1":"When a King is played, the next player gets",
        "bigNum": 3, 
        "Subtitle2": "turns to play another face card or ace",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczPqbqwgs8KvI4wBltpFU7tBkHUEj--yFZYheqE34GyvPH1Ka1EfiQ-JN7ri5By8_0th3mDnvF_hv-IcmkfbvsGm7qffEJry1QWKcxZgMXbJqEn5N_I=w2400",
        "Example":"",
        "Category":"Rules",
        "Status":"13 of 18",
        "Time": None,
    },
    "19":{
        "id": 19,
        "Title": "Face Cards and Aces:",
        "Title2": "Aces",
        "Subtitle1":"When an Ace is played, the next player gets",
        "bigNum": 4,
        "Subtitle2": "turns to play another face card or ace.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczMbq1aURewjeL5x16cRsaSfT2_p9uvjhIAHlZNF5WT1NOdnHGEmOMB1TpxBR6Y-pAjabq1vkRd4zbSGNX1PZMu9R_Wev1l-aWi9QAi2rjZfIfAwVb8=w2400",
        "Example":"",
        "Category":"Rules",
        "Status":"14 of 18",
        "Time": None,
    },
    "20":{
        "id": 20,
        "Title": "Face Cards and Aces:",
        "Title2": "Turnout",
        "Subtitle1":"When a player is unsuccessful at playing another face card or ace within their extra turns, the most recent person to play a face card or ace picks up the pile.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczP9tbhkboRIGhzrufl51nXLcjqQSqwcClowi-2uSxDLjigqJh-JHp5hbHDRURfytqhPGTnZ-IeUmdGv327J0ALc3qz3BRmSkuesWN67HAua06wRy4o=w2400",
        "Example":"",
        "Category":"Rules",
        "Status":"15 of 18",
        "Time": None,
    },
    "21":{
        "id": 21,
        "Title": "Face Cards and Aces:",
        "Title2": "Running Out of Cards",
        "Subtitle1":"If a player runs out of cards during their chain of extra turns, the following player picks up where this player left off.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczP0qxn6PRrcaMeKoPJV9zoBy5nPkvMv5Kt4LqY6by33-W_Jl8tsV43AJ9r6jjX-9wMYIksITRG0dzEWHU6BRiJqMKGMWow715AP4rxt5QJTEs0xccE=w2400",
        "Category":"Rules",
        "Status":"16 of 18",
        "Time": None,
    },
    "22":{
        "id": 22,
        "Title": "Face Cards and Slapping",
        "Subtitle1":"If an opportunity to slap arises within a chain of extra turns, players may interrupt the extra turns and slap and claim the pile.",
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczPU6MhZhT_FxmM_A-DYf5r9C5utBM05CWSK0s7vCss11D7NtfmXcS8fbw2L0zWE7Ux488VigD0EEnQSOcWqymZB281WIZktkC97fTpZiZZL3KjaPq0=w2400",
        "Category":"Rules",
        "Status":"17 of 18",
        "Time": None,
    },
    "23":{
        "id": 23,
        "Title": "Running out of Cards",
        "Subtitle1":"If a player runs out of cards, they are not disqualified! They still have the opportunity to slap the pile, claim cards, and return to normal gameplay.", 
        "Picture":"https://lh3.googleusercontent.com/pw/AP1GczO7_Cc7_SAEE-f6Cl0FLBdVKkvqG27KAo6aFLhQfAlNv9UzCxadofPbn9zxtawIyIeMg9HZOGCihpLBRCpDEnwrHByI3i8HHZG00iYu1bwSQvnF_Oc=w2400",
        "Example":"",
        "Category":"Rules",
        "Status":"18 of 18",
        "Time": None,
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
    visit_time = datetime.now()
    print(f"Page visited at: {visit_time}")

    return render_template('overview.html')

@app.route('/setup/<int:lesson_id>')
def setup(lesson_id):
    """Serve a lesson page or redirect based on lesson_id."""
    visit_time = datetime.now()
    print(f"Page visited at: {visit_time}")

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
        quiz_qs[question_key]['user_answer'] = user_answer

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
            return jsonify({'is_correct': is_correct, 'exp': quiz_qs[question_key]['explanation'], 'correct_answer': quiz_qs[question_key]['correct_answer'], 'redirect': url_for('quiz', question_id=next_question_id)})
    
    return "Invalid request", 400

@app.route('/already-answered/<int:question_id>', methods=['POST'])
def already_answered(question_id):
    question_key = str(question_id)
    alr_answered = None
    exp = None
    correct_answer = None
    
    if question_key in quiz_qs:
        if quiz_qs[question_key]['user_answer']:
            alr_answered = quiz_qs[question_key]['user_answer']
            correct_answer = quiz_qs[question_key]['correct_answer']
            exp = quiz_qs[question_key]['explanation']
    
    return jsonify({'user_answer': alr_answered, 'exp': exp, 'correct_answer': correct_answer})


@app.route('/check-answer/<int:question_id>', methods=['POST'])
def check_answer(question_id):
    # Retrieve the submitted answer from the AJAX request
    submitted_answer = request.form.get('answer')

    question_key = str(question_id)

    quiz_qs[question_key]['user_answer'] = submitted_answer

    # Retrieve the correct answer for the given question_id
    correct_answer = quiz_qs[str(question_id)]['correct_answer']

    is_correct = (submitted_answer == correct_answer)

    return jsonify({'is_correct': is_correct, 'exp': quiz_qs[question_key]['explanation'], 'correct_answer': quiz_qs[question_key]['correct_answer']})

@app.route('/result')
def result():
    score = 0
    for question_id, question_info in quiz_qs.items():
        if question_info['user_answer'] == question_info['correct_answer']:
            score += 1
        question_info['user_answer'] = None

    return render_template('results.html', correct_count=score, total_questions=total_questions)
if __name__ == '__main__':

    app.run(debug=True)