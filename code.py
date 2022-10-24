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
        '--': '8'}

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

    move += letters[int(inputcharacter())-1]
    move += inputcharacter()
    move += letters[int(inputcharacter())-1]
    move += inputcharacter()

    print("you input "+move)
    return move

#initialise chess board
import chess
import chess.engine
engine = chess.engine.SimpleEngine.popen_uci(r"/home/pi/Stockfish-sf_15/src/stockfish")
engine.configure({"skill level": 20})
board = chess.Board()

dash()

while not board.is_checkmate() or not board.is_stalemate(): 
    
    while True:
        movetoplay = chess.Move.from_uci(inputmove())
        if movetoplay in board.legal_moves:
            board.push(movetoplay)
            break
        else:
            print("illegal move")
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