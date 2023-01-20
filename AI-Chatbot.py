import sys
import time
import random
import re
import sqlite3
from string import punctuation
from collections import Counter
from math import sqrt
def next():
        print("\n" * 18)

def slow_type(x):
        typing_speed = 50
        for l in x:
                sys.stdout.write(l)
                sys.stdout.flush()
                time.sleep(random.random() * 10.0/typing_speed)
print("🙂 What's your name ")
L = input("\n\n")
next()
print("\n\n🙂 Hi " + L, end = "")

A = ', how are you '
need_be = 5
count = 1
ae = 0
users_time = 0
emotion_lvl = 0
check = 1
total_time = 0
response_length = 0
analysis = "on"
total_rlen = 0
warning_rlen = 0
warning_low = .2
warning_hi = 1.275
l_wl = .2
Q = ["Why", "What", "How", "When"]
while True:
        if emotion_lvl != check:
                check = emotion_lvl
                dbase = str(emotion_lvl) + ".db"
                connection = sqlite3.connect(dbase)
                cursor = connection.cursor()

                try:

                        cursor.execute('''
                        CREATE TABLE words (word TEXT UNIQUE)''')

                        cursor.execute('''
                        CREATE TABLE sentences (sentence TEXT UNIQUE, used INT NOT NULL DEFAULT 0)''')

                        cursor.execute('''
                        CREATE TABLE associations (word_id INT NOT NULL, sentence_id INT NOT NULL, weight REAL NOT NULL)''')

                except:
                        pass


                def get_id(entityName, text):
                        tableName = entityName + 's'
                        columnName = entityName
                        cursor.execute('SELECT rowid FROM ' + tableName + ' WHERE ' + columnName + ' = ?', (text,))
                        row = cursor.fetchone()
                        if row:
                                return row[0]
                        else:
                                cursor.execute('INSERT INTO ' + tableName + ' (' + columnName + ') VALUES (?)', (text,))
                                return cursor.lastrowid

                def get_words(text):
                        wordsRegexpString = '(?:\w+|[' + re.escape(punctuation) + ']+)'
                        wordsRegexp = re.compile(wordsRegexpString)
                        wordsList = wordsRegexp.findall(text.lower())
                        return Counter(wordsList).items()

        if ae > 0:
                print("\n" * 15)
        name_random = random.randint(1, 5)
        response_wait = random.randint(0, 2)

        total_time += users_time
        avg_time = total_time/count

        total_rlen += response_length
        avg_rlen = int(total_rlen/count)

        if ae <= 1:
                Z = ("")
                id_number = 2
                ae += 1

        if ae >= 2:
                ae += 1
                count += 1
                if avg_time * warning_low >= users_time >= avg_time * warning_hi:
                        if count - 1 > need_be:
                                emotion_lvl = 5
                                # 4s
                                # 1.35 = 5s
                                # * .075 = 1s
                if response_length < avg_rlen * l_wl:
                        if count - 1 > need_be:
                                emotion_lvl = 5

                inB = B.title()
                if "?" in inB:
                        emotion_lvl = 1
                        id_number = 1
                if "!" in inB:
                        emotion_lvl = 2
                        id_number = 1
                if inB == Q:
                        emotion_lvl = 1
                        id_number = 1
                if "Happy" in inB:
                        emotion_lvl = 3
                        id_number = 1
                if "Sad" in inB:
                        emotion_lvl = 4
                        id_number = 1


                inA = A.title()
                if "Happy" in inA:
                        emotion_lvl = 3
                        id_number = 2
                if "Sad" in inA:
                        emotion_lvl = 4
                        id_number = 2
                if "Idk" in inA:
                        emotion_lvl = 5
                        id_number = 2

                if emotion_lvl == 0:
                        Z = ("🙂 ")
                if emotion_lvl == 1:
                        Z = ("🤔 ")
                        response_wait += 1
                if emotion_lvl == 2:
                        Z = ("😃 ")
                        response_wait = 0
                if emotion_lvl == 3:
                        Z = ("😊 ")
                if emotion_lvl == 4:
                        Z = ("😔 ")
                        name_random = random.randint(1,3)
                        response_wait += 3
                if emotion_lvl == 5:
                        Z = ("😕 ")

        reading_time = response_length * .3
        response_final = response_wait + reading_time

        if ae > 1:
                if "on" in analysis:
                        l = L.title()
                        if id_number == 1:
                                user = L
                        if id_number == 2:
                                user = "Computer"
                        if name_random == 1:
                                yes_no = "yes"
                        if name_random > 1:
                                yes_no = "no"
                        prop_check = users_time / avg_time
                        lw_wl = int(avg_rlen * l_wl)
                        print("(Anaylsis:\n")
                        print("Count: ", count - 1, "\n")

                        print("Subject: ", l)
                        print("Avg response time: ", avg_time)
                        print("Last response time: ", users_time)
                        print("Avg word length: ", avg_rlen)
                        print("Last word length: ", response_length, "\n")

                        print("Subject: Computer")
                        print("Reading time:", reading_time)
                        print("Response time selected:", response_wait)
                        print("Final response time: ", response_final)
                        print("Used Subjects Name?: ", yes_no, "(", name_random, ")", "\n")
                        if count - 1 >= need_be:
                                print("(AI)")
                                print("Time proportion check: ", prop_check)
                                print("Count ", count - 1, " warning response word length(L): ", lw_wl, "\n")
                        print("Emotion lvl: ", emotion_lvl, "(", user, ")", ")\n")
                        # Anaylsis ends

        print(Z, end = "")
        time.sleep(response_final)
        if name_random == 1:
                slow_type(A + " " + L + "\n")
        else:
                slow_type(A + "\n")
        start = time.time()
        print("")

        B = input(L + ": ").strip()
        next()
        stop = time.time()
        users_time = stop - start
        response_length = len(B.split())


        words = get_words(A)
        words_length = sum([n * len(word) for word, n in words])
        sentence_id = get_id('sentence', B)
        for word, n in words:
                word_id = get_id('word', word)
                weight = sqrt(n / float(words_length))
                cursor.execute('INSERT INTO associations VALUES (?, ?, ?)', (word_id, sentence_id, weight,))
                connection.commit()

        cursor.execute('CREATE TEMPORARY TABLE results(sentence_id INT, sentence TEXT, weight REAL)')

        words = get_words(B)
        words_length = sum([n * len(word) for word, n in words])
        for word, n in words:
                weight = sqrt(n / float(words_length))
                cursor.execute(
                'INSERT INTO results SELECT associations.sentence_id, sentences.sentence, ?*associations.weight/(4+sentences.used) FROM words INNER JOIN associations ON associations.word_id=words.rowid INNER JOIN sentences ON sentences.rowid=associations.sentence_id WHERE words.word=?',
                (weight, word,))

        cursor.execute(
        'SELECT sentence_id, sentence, SUM(weight) AS sum_weight FROM results GROUP BY sentence_id ORDER BY sum_weight DESC LIMIT  1')
        row = cursor.fetchone()
        cursor.execute('DROP TABLE results')

        if row is None:
                cursor.execute(
                'SELECT rowid, sentence FROM sentences WHERE used = (SELECT MIN(used) FROM sentences) ORDER BY RANDOM() LIMIT 1')
                row = cursor.fetchone()

        A = row[1]
        cursor.execute('UPDATE sentences SET used = used + 1 WHERE rowid = ?', (row[0],))
