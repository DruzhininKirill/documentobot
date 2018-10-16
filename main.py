import telebot
import cv_alg
import keyboards
import cv2
import spellchecker
import json

bot = telebot.TeleBot ("640168332:AAEW5HUrEwnvqrn8Aftsevv0ihOVcOANSOE")
jsoncorrect = json
jsonlist = []


@bot.message_handler (content_types = ["text"])
def first(message):
    if message.text == "/start":
        bot.send_message( message.chat.id,
                          "This bot is made to convert docs into text", reply_markup=keyboards.keyboard_1)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline (call):

    if call.data == "start":
        bot.send_message(call.message.chat.id,
                         "Convert into text or simply scan", reply_markup=keyboards.keyboard_2)

    if call.data == "help":
        bot.send_message(call.message.chat.id,
                         "Documentbot is a simple bot that does scan images from"
                         "simple photos or docs. Spell checking with correcting is also "
                         "provided, but recommended only with texts contain 10% of mistakes."
                         "Have fun:)")

    if (call.data == "scan") or (call.data == "text"):
        if call.data == "scan":
            key = 1
        if call.data == "text":
            key = 2
        bot.send_message(call.message.chat.id,
            "OK. Send me a photo of a document. N/B! It has to be with sheet edges.")

    if call.data == "ncorrect":
        data = json.load(open("data.json", encoding="utf8"))
        for connect in data:
            if connect["id"] == call.message.chat.id:
                data.remove(connect)
                output = open("data.json", "w")
                json.dump(data, output)
                output.close()


    if call.data == "correct":
        bot.send_message(call.message.chat.id, "processing")
        spell = spellchecker.SpellChecker()
        word = ""
        words = []
        data = json.load(open("data.json"))
        for connect in data:
            if connect["id"] == call.message.chat.id:
                text = connect["text"] + " "
                print ("TEXTTT \n" + text)
                for char in text:
                    if (char != " ") and (char != "!") and (char != "?") and (char != ".") and (char != ",") and (char != "\n"):
                        word = word + char
                        #print(word)
                    if char == " " or char == "\n" and word != '':

                        words.append(word)
                        word = ""

                print("all words" + str(words))
                wrong = spell.unknown(words)
                print("wrong words: " + str(wrong))
                for w in wrong:
                    low = w.lower()
                    print(low)
                    rep = spell.correction(low)
                    if (rep != low):
                        while text.find(w) > 0:
                            i = text.find(w)
                            text = text[:i] + rep + " " + text[i + len(w):]
                print("Corrected \n" + text)
                bot.send_message(call.message.chat.id, "corrected text: \n" + text)

                data.remove(connect)
                output = open("data.json", "w")
                json.dump(data, output)
                output.close()




@bot.message_handler (content_types = ["photo"])

def proccesing(message):
    print ('message.photo =', message.document)
    fileID = message.photo[-1].file_id
    print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path )

    with open("image.png", 'wb') as new_file:
        new_file.write(downloaded_file)

    image = cv2.imread("image.png")
    bot.send_message(message.chat.id,"processing")
    res = cv_alg.proccesing(image)

    bot.send_message(message.chat.id,
                     "DONE. YOUR TEXT: \n  " + res)
    bot.send_message(message.chat.id,
                     "Some words might be incorrectly spelled. Try to correct them?", reply_markup=keyboards.keyboard_3)
    connect = {'id': message.chat.id ,"text": res}
    jsonlist.append(connect)
    output = open("data.json", "w")
    json.dump(jsonlist, output)
    output.close()

@bot.message_handler (content_types = ["document"])

def proccesing(message):

    fileID = message.document.file_id
    print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path )

    with open("doc.png", 'wb') as new_file:
        new_file.write(downloaded_file)

    image = cv2.imread("image.png")
    bot.send_message(message.chat.id,"processing")
    res = cv_alg.proccesing(image)

    bot.send_message(message.chat.id,
                     "DONE. YOUR TEXT: \n  " + res)
    bot.send_message(message.chat.id,
                     "Some words might be incorrectly spelled. Try to correct them?", reply_markup=keyboards.keyboard_3)
    connect = {'id': message.chat.id ,"text": res}
    jsonlist.append(connect)
    output = open("data.json", "w")
    json.dump(jsonlist, output)
    output.close()

if __name__ == '__main__':
    bot.polling(none_stop=True)