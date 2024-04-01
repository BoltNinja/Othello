import sys; args = sys.argv[1:]
global ARGS1
ARGS1 = args
import random
import time
SIZE = 8
def alphabeta(board, tokenToMove, oppositeToken, raw_lower, upper):
    board = board.lower()
    lower = raw_lower
    possible_moves = find_psbls(board, tokenToMove, oppositeToken)
    if not possible_moves:
        # curr token cannot move, pass
        possible_moves = find_psbls(board, oppositeToken, tokenToMove)
        if not possible_moves:
            # double skip or end of game 
            return [board.count(tokenToMove) - board.count(oppositeToken)]
        result = alphabeta(board, oppositeToken, tokenToMove, -upper, -lower)
        return [-result[0]] + result[1:] + [-1]
    bestSoFar = [lower - 1]
    for mv in possible_moves:
        newBrd = find_psbls(board, tokenToMove, oppositeToken, bool1=mv)
        result = alphabeta(newBrd, oppositeToken, tokenToMove, -upper, -lower)
        score = -result[0]
        if score < lower:
            continue
        if score > upper:
            return [score]
        if score > bestSoFar[0]:
            bestSoFar = [score] + result[1:] + [mv]
        lower = score + 1
    return bestSoFar
def evalBoard(brd,tkn,other):
    edges = [1, 2, 3, 4, 5, 6,8, 16, 24, 32, 40, 48,15, 23, 31, 39, 47, 55,62, 61, 60, 59, 58, 57,48, 40, 32, 24, 16, 8]
    corners = [0,7,56,63]
    edges1 = ""
    for i in edges:
        edges1+=brd[i]
    corners1 = ""
    for i in corners:
        corners1+=brd[i]
    safeEdges = 0
    # for i in edges:
    #     if safeEdge(brd,tkn,i):
    #         safeEdges+=1
    otherTkn = "o" if tkn=="x" else "x"
    psblLength = find_psbls(brd,tkn,otherTkn)
    return [4*(corners1.count(tkn)-corners1.count(other))+2*safeEdges+len(psblLength)]

def midgame(board, tokenToMove, oppositeToken, raw_lower, upper,lvl = 0):
    board = board.lower()
    lower = raw_lower
    if lvl == 3:
        return evalBoard(board,tokenToMove,oppositeToken)
    

    possible_moves = find_psbls(board, tokenToMove, oppositeToken)

    if not possible_moves:
        # curr token cannot move, pass
        possible_moves = find_psbls(board, oppositeToken, tokenToMove)

        if not possible_moves:
            # double skip or end of game 
            return [board.count(tokenToMove) - board.count(oppositeToken)]
        
        result = midgame(board, oppositeToken, tokenToMove, -upper, -lower,lvl+1)

        return [-result[0]] + result[1:] + [-1]

    bestSoFar = [lower - 1]

    for mv in possible_moves:
        newBrd = find_psbls(board, tokenToMove, oppositeToken, bool1=mv)
        result = midgame(newBrd, oppositeToken, tokenToMove, -upper, -lower,lvl+1)

        score = -result[0]

        if score < lower:
            continue
        if score > upper:
            return [score]

        if score > bestSoFar[0]:
            bestSoFar = [score] + result[1:] + [mv]

        lower = score + 1

    return bestSoFar



def contains_all_digits(string):
    digit_chars = set("0123456789")
    for char in string:
        if char not in digit_chars:
            return False
    return True
def contains_all_letters(string):
    digit_chars = set("qwertyuiopasdfghjklzxcvbnm")
    for char in string:
        if char not in digit_chars:
            return False
    return True
def find_psbls(board, tokenToPlay, other, bool1 = None):
    psbls = []
    flips = []
    pos = 0
    end = len(board)
    if bool1 is None and "x" in board and "o" in board:
        pos = max(min(board.index("x"), board.index("o")) - 9, 0)
        end = min(max(board.rindex("x"), board.rindex("o")) + 10, len(board))
    posAndEnd = (1,2)
    if bool1 is not None:
        posAndEnd = (bool1, bool1 + 1)
    else:
        posAndEnd = (pos, end)
    for i in range(*posAndEnd):
        if board[i] == ".":
            dummyBool = False
            # upright
            if (not dummyBool or bool1 is not None) and i // SIZE > 1 and i % SIZE < 6 and board[i - 7] == other:
                place = i - 14
                change = [i, i - 7]
                while place // SIZE != -1 and place % SIZE != 0:
                    if board[place] == tokenToPlay:
                        flips += change
                        dummyBool = True
                        psbls.append(i)
                        break
                    elif board[place] == ".":
                        break
                    else:
                        board=board
                    if bool1 is not None:
                        change.append(place)
                    place -= 7
            # downleft
            if (not dummyBool or bool1 is not None) and i // SIZE < 6 and i % SIZE > 1 and board[i + 7] == other:
                place = i + 14
                change = [i, i + 7]
                while place // SIZE != SIZE and place % SIZE != 7:
                    if board[place] == tokenToPlay:
                        flips += change
                        dummyBool = True
                        psbls.append(i)       
                        break
                    elif board[place] == ".":
                        break
                    if bool1 is not None:
                        change.append(place)
                    place = place + 7
            # downright 
            if (not dummyBool or bool1 is not None) and i // SIZE < 6 and i % SIZE < 6 and board[i + 9] == other:
                place = i + 18
                change = [i, i + 9]
                while place // SIZE != SIZE and place % SIZE != 0:
                    if board[place] == tokenToPlay:
                        flips += change
                        psbls.append(i)    
                        break
                    elif board[place] == ".":
                        break
                    if bool1 is not None:
                        change.append(place)
                    place += 9
            # right
            if (not dummyBool or bool1 is not None) and i % SIZE < 6 and board[i + 1] == other:
                change = [i, i + 1]
                place = i + 2
                while place % SIZE != 0:
                    if board[place] == tokenToPlay:
                        psbls.append(i)
                        flips += change
                        dummyBool = True
                        break
                    elif board[place] == ".":
                        break
                    if bool1 is not None:
                        change.append(place)
                    place += 1
            # left
            if (not dummyBool or bool1 is not None) and i % SIZE > 1 and board[i - 1] == other:
                change = [i, i - 1]
                place = i - 2
                while place % SIZE != 7:
                    if board[place] == tokenToPlay:
                        psbls.append(i)
                        flips += change
                        dummyBool = True
                        break
                    elif board[place] == ".":
                        break
                    if bool1 is not None:
                        change.append(place)
                    place -= 1
            # up
            if (not dummyBool or bool1 is not None) and i // SIZE > 1 and board[i - 8] == other:
                place = i - 16
                change = [i, i - 8]
                while place // SIZE != -1:
                    if board[place] == tokenToPlay:
                        flips += change
                        dummyBool = True
                        psbls.append(i)        
                        break
                    elif board[place] == ".":
                        break
                    if bool1 is not None:
                        change.append(place)
                    place -= 8
            # down
            if i // SIZE < 6 and board[i + 8] == other and (not dummyBool or bool1 is not None):
                place = i + 16
                change = [i, i + 8]
                while place // SIZE != 8:
                    if board[place] == tokenToPlay:
                        flips += change
                        psbls.append(i)
                        
                        dummyBool = True
                        break
                    elif board[place] == ".":
                        break
                    else:
                        board=board
                    if bool1 is not None:
                        change.append(place)
                    place += 8
            # upleft
            if i // SIZE > 1 and i % SIZE > 1 and board[i - 9] == other and (not dummyBool or bool1 is not None):
                place = i - 18
                change = [i, i - 9]
                while place // SIZE != -1 and place % SIZE != 7:
                    if board[place] == tokenToPlay:
                        psbls.append(i)
                        flips += change
                        dummyBool = True
                        break
                    elif board[place] == ".":
                        break
                    if bool1 is not None:
                        change.append(place)
                    place -= 9
    if bool1 is not None:
        new1 = board
        for i in flips:
            new1 = new1[:i] + tokenToPlay + new1[i + 1:] 
        return new1
    return psbls
def contains_all_digits(string):
    digit_chars = set("0123456789")
    for char in string:
        if char not in digit_chars:
            return False
    return True
def contains_all_letters(string):
    digit_chars = set("qwertyuiopasdfghjklzxcvbnm")
    for char in string:
        if char not in digit_chars:
            return False
    return True
def ruleOfThumb(brd,tkn):
    nearCorners = {0:[1,8,9], 7:[6,14,15], 56: [48,49,57], 63: [54,55,62]}
    safeEdges= [[0,1,2,3,4,5,6,7],[7,15,23,31,39,47,56,63],[56,57,58,59,60,61,62,63],[0,8,16,24,32,40,48,56]]
    edges = {i:j for j in safeEdges for i in j if i not in nearCorners}
    oppositeToken = None
    if tkn == "o":
        oppositeToken = "x"
    else:
        oppositeToken = "o"
    psbls = set(find_psbls(brd,tkn,oppositeToken))

    #if corner available=> grab it
    for i in [0,7,56,63]:
        if i in psbls:
            return i
    notPsbls = []
    for i in [0,7,56,63]:
        if not brd[i]==tkn:
            #computing notPsbls
            notPsbls += nearCorners[i]
        #else:
            #computing best
            #best += nearCorners[i]
    #if best not empty, return item from best
    # for i in best:
    #     if i in psbl:
    #         return i
    if not (psbls-set(notPsbls)): return random.choice(sorted([*psbls]))
    psbls2 = psbls-set(notPsbls)
    
    # #if there is safe edge in psbls-notPsbls=> return one of them
    for i in psbls2:
        if i in edges:
            if safeEdge(brd,tkn,i):
                return i
    # #return one of psbls
    # if psbls:
    #     return random.choice(sorted([*psbls]))
    # else:
    #     return None
    return random.choice(sorted([*psbls2]))

def quickMove(brd, tkn):
    #set HOLELIMIT under which AB/alphabeta runs
    if not brd: 

        return
    other = "o" if tkn=="x" else "x"
    if brd.count('.')<=10:
        return alphabeta(brd, tkn, other, -65, 65)[-1]
    if brd.count('.') <= 50:
        return midgame(brd,tkn,other,-65,65,0)[-1]
    return ruleOfThumb(brd, tkn)
def safeEdge(pzl,tkn,pMove):
    psblEdges= [[0,1,2,3,4,5,6,7],[7,15,23,31,39,47,56,63],[56,57,58,59,60,61,62,63],[0,8,16,24,32,40,48,56]]
    edges = {i:j for j in psblEdges for i in j if i not in {0:[1,8,9], 7:[6,14,15], 56: [48,49,57], 63: [54,55,62]}}
    return True if all([True for i in "".join([pzl[i] for i in edges[pMove][:edges[pMove].index(pMove)]]) if i == tkn]) or all([True for ch in "".join([pzl[i] for i in edges[pMove][edges[pMove].index(pMove)+1:]]) if ch == tkn]) else False

global ENDTIME
def main(): 
    ENDTIME = None
    args2 = ARGS1
    SIZE=8
    global HLLIM
    if len(args2)>0 and args2[0] and "." in args2[0]:
        brd = args2[0]
        args2 = args2[1:]
    else:
        brd = "."*27+"ox......xo"+"."*27
    verboseVariable = False
    HLLIM = 10
    newargs2 = []
    hasHoleLimit = False
    if args2:
        for i in args2:
            if "HL" in i:
                HLLIM = int(i[2:])
                hasHoleLimit = True
            elif "v" in i or "V" in i:
                verboseVariable = True
            else:
                newargs2.append(i)
    args2 = newargs2
    stringmoves = ""
    dummymoves = []  
    if args2:
        for i in args2:
            if len(i)==1:
                stringmoves+="_"+i
            else:
                stringmoves+=i
    listmoves = []  
    for i in range(2,len(stringmoves)+1,2):
        listmoves.append(stringmoves[i-2:i])
    for i in listmoves:
        if  "_" in i:
            dummymoves.append(i[1])
        if "-" in i :
            pass
        else:
            dummymoves.append(i)
    args2 = dummymoves
    newargs2 = []
    for i in args2:
        if "_" not in i:
            newargs2.append(i)
    args2 = newargs2

    play = ""
    psbls = []
    rnFrst = args2 == []
    other = ""

    while rnFrst or args2:
        if args2 and args2[0].startswith("-"):
            args2.pop(0)
            continue
        if args2 and len(args2[0]) == 64:
            brd = args2[0].lower()
            args2.pop(0)
        if args2 and contains_all_letters(args2[0]):
            play = args2[0].lower()
            args2.pop(0)
        elif not play:
            specificcount = brd.count(".")
            play = "o" if 64 - specificcount % 2 == 1 else "x"
        if args2 and args2[0]:
            if contains_all_digits(args2[0]):
                firstArgument = int(args2[0])
                if -1 < firstArgument < 64:
                    args2.pop(0)
                    psbls.append(firstArgument)
            else:
                if len(args2[0])==2 and "a" <= args2[0][0].lower() <= "h" and contains_all_digits(args2[0][1]) and -1 < int(args2[0][1]) < SIZE + 1:
                    addTopsbls = (int(args2[0][1])-1)*SIZE + ord(args2[0][0].lower())-ord("a")
                    args2.pop(0)
                    psbls.append(addTopsbls)
        rnFrst = False
    psbls.insert(0, 27)
    snapBoolean = True
    if play == "x":
        other = "o"
    else:
        other = "x"
    # if hasHoleLimit:
    #     quickMove2(brd, play, other, LIMIT)
    #     quit()
    for index, i in enumerate(psbls):
        if snapBoolean:
            snapBoolean = False
        else: 
            g = play
            play = other
            other = g
            if (not verboseVariable and (index==0 or index==len(psbls)-1)) or verboseVariable:
                print(other, "moves to", i)
            brd = brd.lower()
            oldBoard = brd
            brd = find_psbls(brd, other, play, i)
            changedVar = 0
            for a in range(64):
                if not brd[a]=="." and oldBoard[a]=="." or oldBoard[a]=="*":
                    changedVar = a
            brd = brd[:changedVar]+brd[changedVar].upper()+brd[1+changedVar:]
        
        final_psbls = find_psbls(brd.lower(), play, other)
        if not final_psbls and "." in brd:
            g = play
            play = other
            other = g
            final_psbls = find_psbls(brd.lower(), play, other)
        asteriskboard = brd
        for i in final_psbls:
            i = int(i)
            asteriskboard = asteriskboard[:i]+"*"+asteriskboard[i+1:]
        if (not verboseVariable and (index==0 or index==len(psbls)-1)) or verboseVariable:
            print()
            for i in range(SIZE):
                for j in range(SIZE):
                    print(asteriskboard[i * SIZE + j], end="")
                print()
            print()
            print(brd.lower(), str(brd.lower().count("x")) + "/" + str(brd.lower().count("o")))
            if len(final_psbls)==0:
                print("No moves possible")
                ENDTIME = time.time()
                quit()
            else:
                print("Possible moves for", play + ":", set(final_psbls))
        prefmovestr = str(quickMove(brd.lower(), play))
        
        if ((not verboseVariable and (index==0 or index==len(psbls)-1)) or verboseVariable):
            print("The preferred move is " + prefmovestr)
        if (prefmovestr=="None") and ((not verboseVariable and (index==0 or index==len(psbls)-1)) or verboseVariable):
            print("No moves possible")
        if brd.count(".")<=HLLIM and ((not verboseVariable and (index==0 or index==len(psbls)-1)) or verboseVariable):
            ab = alphabeta(brd, play, other, -65, 65)
            print(f"Min score: {ab[0]}; move sequence: {ab[1:]}")
        elif brd.count(".") <= 50 and ((not verboseVariable and (index==0 or index==len(psbls)-1)) or verboseVariable):
            ab = midgame(brd, play, other, -65, 65,0)
            print(f"Min score: {ab[0]}; move sequence: {ab[1:]}")



def contains_all_digits(string):
    digit_chars = set("0123456789")
    for char in string:
        if char not in digit_chars:
            return False
    return True
def contains_all_letters(string):
    digit_chars = set("qwertyuiopasdfghjklzxcvbnm")
    for char in string:
        if char not in digit_chars:
            return False
    return True
if __name__ == "__main__": 
    start = time.time()
    main()
    print("time in seconds:", time.time()-start)
#Aarav Gupta, pd 4, 2025