import RPi.GPIO as GPIO
from gpiozero import Button
import time

#setup
Pin=17
button = Button(27)  # GPIO Pin 40

GPIO.setmode(GPIO.BCM)
GPIO.setup(Pin,GPIO.OUT)
GPIO.setwarnings(False)

#input settings 
dot_timeout = 0.3
dash_timeout = 0.8
current_letter = ""


#morse code dictionary 
morse = {' ': ' ',
        ".": '1',
        '..': '2',
        '...': '3',
        '-': '4',
        '-.': '5',
        '-..': '6',
        '-...': '7',
        '--': '8',
        '---': 'replay',}

morsereversed = {' ': ' ',
        "1": '.',
        '2': '..',
        '3': '...',
        '4': '-',
        '5': '-.',
        '6': '-..',
        '7': '-...',
        '8': '--'}


#full code to send moves
def dot():
    GPIO.output(Pin,1)
    time.sleep(0.15)
    GPIO.output(Pin,0)
    time.sleep(0.2)
def dash():
    GPIO.output(Pin,1)
    time.sleep(0.6)
    GPIO.output(Pin,0)
    time.sleep(0.2)


def outputmove(movecords):
    print("outputting move")
    #send the move to output
    movecordsstring = str(movecords)
    for letter in movecordsstring:
        for symbol in morsereversed[letter.upper()]:
            if symbol == '-':
                dash()
            elif symbol == '.':
                dot()
        time.sleep(1)

def inputcharacter():
    current_letter  = ""
    while True:
        # Wait for a keypress or until a letter has been completed
        button.wait_for_press(dash_timeout)  # type: ignore

        # If we've timed out and there's been previous keypresses, show the letter
        if button.is_pressed is False and len(current_letter) > 0:  # type: ignore
            if current_letter in morse:
                dot()
                return morse[current_letter]
            else:
                print("Not recognised")
                
                #restart input 
                dash() # signal error with -- 
                dash() # signal error with -- 
                current_letter = ""
        
        elif button.is_pressed:  # type: ignore

            # The key has been pressed, work out if it's a dot or a dash
            button_down_time = time.time()
            button.wait_for_release()  # type: ignore
            button_up_time = time.time()
            button_down_length = button_up_time - button_down_time

            # Was it a dot or dash?
            if button_down_length > dot_timeout:
                current_letter += '-'
            else:
                current_letter += '.'



#chess here 
def inputmove():
    letters = ["a","b","c","d","e","f","g","h"]
    move = ""
    input1 = inputcharacter()
    if input1 != "replay":
        move += letters[int(input1)-1]
        move += inputcharacter()
        move += letters[int(inputcharacter())-1]
        move += inputcharacter()
    else:
        move = "replay"
    print("you input "+move)
    return move

#initialise chess board
import chess
import chess.engine
engine = chess.engine.SimpleEngine.popen_uci(r"/home/pi/Stockfish-sf_15/src/stockfish")
engine.configure({"skill level": 20})
board = chess.Board()

dash()

moveinnumbers = ""

#is white or black 
print("is white or black")
if(inputcharacter() == "8"):
    print("white")
    movetoplay = chess.Move.from_uci("e2e4")
    board.push(movetoplay)
    dash()
else: 
    print("playing black skipping first")
    dot()
while not board.is_checkmate() or not board.is_stalemate(): 
    
    while True:
        movetoplaystring = inputmove()
        movetoplaystring1 = movetoplaystring[0]+movetoplaystring[1]
        movetoplaystring2 = movetoplaystring[2]+movetoplaystring[3]
        if movetoplaystring != "replay" and movetoplaystring1 != movetoplaystring2:
            movetoplay = chess.Move.from_uci(movetoplaystring)

        if movetoplaystring == "replay":
            outputmove(moveinnumbers)
            continue
        elif movetoplay in board.legal_moves and movetoplaystring1 != movetoplaystring2:
            board.push(movetoplay)
            break
        else:
            print("illegal/invalid move")
            dot()
            dot()
            dot()
            dot()
            dot()


    bestmove = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(bestmove.move)  # type: ignore
    print(board)
    print("################################")

    thebestmove = str(bestmove.move)
    moveinnumbers = ""
    for character in thebestmove:
        numbers = ["0","1","2","3","4","5","6","7","8"]
        letters = ["a","b","c","d","e","f","g","h"]

        if character not in numbers:
            moveinnumbers += str(letters.index(character)+1)
        else:
            moveinnumbers += character

    print(moveinnumbers)
    outputmove(moveinnumbers)