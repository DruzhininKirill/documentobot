from telebot import  types

keyboard_1 = types.InlineKeyboardMarkup(row_width= 3)
s1 = types.InlineKeyboardButton (text= "Help", callback_data="help")
s2 = types.InlineKeyboardButton (text= "Start", callback_data="start")

keyboard_1.add(s1, s2)

keyboard_2 = types.InlineKeyboardMarkup(row_width= 3)
a1 = types.InlineKeyboardButton (text= "Text", callback_data="text")
a2 = types.InlineKeyboardButton (text= "Scan", callback_data="scan")

keyboard_2.add(a1, a2)

keyboard_3 = types.InlineKeyboardMarkup(row_width= 3)
b1 = types.InlineKeyboardButton (text= "Yes", callback_data="correct")
b2 = types.InlineKeyboardButton (text= "No", callback_data="ncorrect")

keyboard_3.add(b1, b2)