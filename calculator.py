#coding: UTF-8
import sys

# 数字を読み込む
def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


# + を読み込む
def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


# - を読み込む
def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


# * を読み込む
def readMultiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


# / を読み込む
def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


# 入力文字列をトークンに分解
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMultiply(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens


# tokensの掛け算と割り算の部分を答えに置き換える
def changeToken(tokens, index, answer):
    newtoken = {'type': 'NUMBER', 'number': answer}
    del tokens[index-2: index+1]
    tokens.insert(index-2, newtoken)

    
# 掛け算と割り算
def evaluateFirst(tokens):
    answer = 0
    index = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLY':
                answer = tokens[index-2]['number'] * tokens[index]['number']
                changeToken(tokens, index, answer)
            elif tokens[index -1]['type'] == 'DIVIDE':
                answer = tokens[index-2]['number'] * 1.0 / tokens[index]['number']
                newtoken = {'type': 'NUMBER', 'number': answer}
                changeToken(tokens, index, answer)
            else:
                index += 1
        else:
            index += 1
    return tokens


# 足し算と引き算
def evaluateSecond(tokens):
    answer = 0
    index = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax'
        index += 1
    return answer


# トークンから計算を実行
def evaluate(firsttokens):
    secondtokens = evaluateFirst(firsttokens)
    answer = evaluateSecond(secondtokens)
    return answer


def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("3*5", 15)
    test("3.0*5", 15.0)
    test("3.0*5.0", 15.0)
    test("3/5", 0.6)
    test("3.0/5", 0.6)
    test("3/5.0", 0.6)
    test("3.0/5.0", 0.6)
    test("3*5-20/4", 10)
    test("3.0*5.0-20.0/4.0", 10)
    test("3*5/2", 7.5)
    test("3.0*5.0/2.0", 7.5)    
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    if line == "end":
        sys.exit()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print "answer = %f\n" % answer   # 計算結果を出力
