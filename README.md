# chesscheatshoes
Communicate with a chess engine with one button and a vibration motor

Designed to be used with a raspberry Pi, button and vibration motor to subtley communicate with a chess engine concealed in your shoe. 


# sending moves 
At the start send -- to play as white. The default first move for white is e2e4. The input the opponent black's move and keep playing the game. Enter anything other than -- to play as black and skip the first e2e4 move.
Send opponent moves to the engine by sending coordinates. For example an opening move of e2 to e4 would be 5254. 
To send coordinates press the button in different patterns:

1 = . 

2 = .. 

3 = ...

4 = -

5 = -.

6 = -..

7 = -... 

8 = --


Wait until there is a confirmation buzz before submitting the next number. If there is an unrecognised input, there will be 2 longer buzzes. If after all 4 numbers are entered there is an illegal move entered, there will be a series of short buzzes before allowing you to reenter the opponent move. 

# playing moves
After a move is successfully entered, the vibration motor will reply with a move to play in the same 4 number format. To replay the last move, enter --- instead of the first number for your next move

