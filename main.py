import telebot
import requests
import json,time
import re
import random
from telebot import types

# =========================
# إعدادات البوت
# =========================
TOKEN = '7497151281:AAHQLlqAR3dMcosj3uevoK3_E6PdHnM3inw'
bot = telebot.TeleBot(TOKEN)

# =========================
# رسالة الترحيب
# =========================
@bot.message_handler(commands=['start'])
def start_bot(message):
    chat_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name or "Guest"
    user_display = f"@{username}" if username else first_name
    a='''⠀⠀⠀⢠⣶⣿⣿⣿⠟⣴⣾⡿⢷⣾⣿⣿⣿⢯⣫⢶⣩⣾⡷⢿⣾⣿⠇⣿⣿⣿⢶⡇⣈⠖⣿⣶⡄⠀⠀⠀
⠀⠀⣠⣿⣿⣿⣿⣣⣾⣿⣟⣵⣿⣿⡿⣻⣶⢏⣴⣿⣿⢏⣵⣿⣿⢋⢸⣿⣿⢗⣿⢳⢥⣿⡜⢻⣿⣦⠀⠀
⠀⢴⣿⣿⣿⡯⣱⣿⣿⢏⣾⣿⡿⣯⣾⣟⣵⣿⡟⢟⣴⣿⣿⣛⣕⣫⢸⣿⡟⣽⡗⢺⣧⢿⣿⡎⣿⣿⣷⡀
⣸⣿⣿⣿⣛⣲⣿⣿⣡⣿⣿⣟⣵⣿⢭⠾⢋⢀⣴⣿⡿⡿⢩⣢⡯⡝⣿⣿⢳⣿⢐⡺⣿⡾⣿⣿⠼⣿⣿⣗
⣿⣿⣿⢏⣢⣿⠿⣴⣿⡿⢧⣾⡯⠁⠃⢈⣴⣿⣿⡻⡋⣤⣤⣶⣾⢹⣿⢣⣿⢇⢞⡄⣿⣷⢻⣿⡆⣿⣿⡝
⣿⣿⡏⢢⣽⢯⡾⣿⣿⣣⣿⠟⢠⢑⣴⣿⣿⠻⠃⠠⡺⣿⣿⣿⣋⣿⢫⣿⢏⣾⣷⣏⢹⣿⡝⣿⡧⣿⣿⡇
⣿⣟⢎⢑⣵⡿⣼⡳⣳⣿⡟⢐⣔⣿⣟⠟⠅⢰⣆⠀⢉⣄⢝⠿⣼⢫⣿⣏⣾⣿⣿⣿⠊⣿⣯⢻⡇⣿⣿⡷
⢟⣠⡾⢟⡡⣼⠧⣽⣿⡛⣴⣿⠯⢋⢔⣽⣶⣌⠛⣁⡄⣺⡮⡽⣳⣿⢗⣾⡿⣿⣿⣷⣎⠘⣿⣼⠇⣿⣿⣿
⣩⢂⡆⢚⢥⢏⣾⣟⣴⡩⠛⢀⠀⠤⠦⡑⠊⠿⢹⢻⣟⡿⣽⣽⡿⣋⣼⣯⣛⡝⠿⢿⣿⡣⡈⡆⠃⣿⣿⡏
⢳⡫⢍⣳⣴⡿⣩⣾⠅⠀⡠⡲⢜⠢⡂⢌⡣⡃⢈⡁⣕⣽⡿⢟⣑⡿⣿⣏⠋⠉⠙⠃⠪⠓⢎⠷⢹⣿⣿⡇
⡚⠻⡴⣫⡕⣾⣿⡿⣰⣯⢶⡵⢦⡕⣬⢊⡕⣉⢌⣡⣾⡻⠃⢀⠾⡁⠻⣷⡘⠛⢂⣤⡂⠀⠠⠋⣾⣿⣿⡷
⣻⡻⠧⢸⡇⣿⣿⠇⣿⣿⣿⣾⣷⣿⣼⣣⣞⢔⡵⠟⡉⡠⡘⡃⢉⡘⠃⢙⢽⣻⣿⣿⡿⠂⠀⢠⣿⣿⣿⠠
⡥⠙⠷⣾⡇⣿⣿⢧⣿⢹⣿⣿⣿⡿⡿⡹⢕⢩⢴⣎⠶⡱⢎⠕⣡⠆⡐⢌⢄⡡⢨⢣⡴⠁⢀⣼⡗⣿⣏⣆
⠆⡰⢆⣿⠁⣿⣿⢹⣿⣿⣿⢽⣫⣥⣷⠁⠉⡛⠓⠲⠯⣞⡣⣛⢴⡣⢞⠤⠢⢌⢢⠫⠀⠀⣤⣿⢽⣿⢺⣙
⢐⢜⢸⡯⠀⣿⣿⢸⣿⣷⣾⣿⣿⣿⡇⠨⠌⣀⢋⡀⠡⠀⢝⣈⢾⡵⣮⠲⡕⢎⠔⡑⢀⣎⣸⡷⢾⡟⡇⣿
⡩⠂⣿⢇⠂⣿⣿⠈⢻⣿⣿⣿⣿⡿⢇⠐⢆⠶⡀⢈⠃⡱⠀⠤⣼⣿⣷⣟⣜⡧⣚⠈⣼⡇⣿⢳⣟⠻⣼⣿
⠠⣹⡟⠤⣛⢸⣿⢀⠀⠹⣿⠟⠫⣠⣶⣇⡣⣟⠜⡠⣛⠔⢡⢹⣿⣿⣿⣿⣿⣿⠇⢹⣿⢹⣟⣾⡟⣊⢿⣿
⢢⣿⢉⠶⡱⢺⣿⠨⢎⠵⡐⡱⣿⣿⣿⣿⠔⡯⢢⡕⣍⣌⣸⢸⣿⣿⣿⣿⠿⡊⣊⣿⡏⣼⣧⣿⢑⣯⣿⣏
⣿⢣⡧⣛⢜⣹⣿⠰⡣⣛⠄⡠⡈⠻⣻⠟⡊⠶⠱⡪⢪⣾⡌⡏⠿⠟⡛⢡⢪⠑⣸⣟⡁⣿⢸⠧⣼⣼⡏⣆
⢧⣿⡷⣭⢪⣹⡟⢨⡕⢭⢢⡕⢎⠴⡠⠈⢾⠋⠕⠕⡛⢅⡱⢄⠶⠱⠆⠤⡰⠎⣿⠧⢴⡿⢏⢰⣇⡿⢸⡗'''
    z='''⡀⠄⢀                            ⣿⣿⠄⠄⠄⢸⡇⠄⠄
⠄⠄⠄⣾⣿⠿⠿⠶⠿⢿⣿⣿⣿⣿⣦⣤⣄⢀⡅⢠⣾⣛⡉⠄⠄⠄⠸⢀⣿⠄
⠄⠄⢀⡋⣡⣴⣶⣶⡀⠄⠄⠙⢿⣿⣿⣿⣿⣿⣴⣿⣿⣿⢃⣤⣄⣀⣥⣿⣿⠄
⠄⠄⢸⣇⠻⣿⣿⣿⣧⣀⢀⣠⡌⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⣿⣿⣿⠄
⠄⢀⢸⣿⣷⣤⣤⣤⣬⣙⣛⢿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡍⠄⠄⢀⣤⣄⠉⠋⣰
⠄⣼⣖⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⢇⣿⣿⡷⠶⠶⢿⣿⣿⠇⢀⣤
⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣷⣶⣥⣴⣿⡗
⢀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠄
⢸⣿⣦⣌⣛⣻⣿⣿⣧⠙⠛⠛⡭⠅⠒⠦⠭⣭⡻⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠄
⠘⣿⣿⣿⣿⣿⣿⣿⣿⡆⠄⠄⠄⠄⠄⠄⠄⠄⠹⠈⢋⣽⣿⣿⣿⣿⣵⣾⠃⠄
⠄⠘⣿⣿⣿⣿⣿⣿⣿⣿⠄⣴⣿⣶⣄⠄⣴⣶⠄⢀⣾⣿⣿⣿⣿⣿⣿⠃⠄⠄
⠄⠄⠈⠻⣿⣿⣿⣿⣿⣿⡄⢻⣿⣿⣿⠄⣿⣿⡀⣾⣿⣿⣿⣿⣛⠛⠁⠄⠄⠄
⠄⠄⠄⠄⠈⠛⢿⣿⣿⣿⠁⠞⢿⣿⣿⡄⢿⣿⡇⣸⣿⣿⠿⠛⠁⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠄⠉⠻⣿⣿⣾⣦⡙⠻⣷⣾⣿⠃⠿⠋⠁⠄⠄⠄⠄⠄⢀⣠⣴
⣿⣿⣿⣶⣶⣮⣥⣒⠲⢮⣝⡿⣿⣿⡆⣿⡿⠃⠄⠄⠄⠄⠄⠄⠄⣠⣴⣿⣿⣿'''
    x='''⣿⣿⣿⣿⣿⣿⣿⡇⡌⡰⢃⡿⡡⠟⣠⢹⡏⣦⢸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⢰⠋⡿⢋⣐⡈⣽⠟⢀⢻⢸⡂⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣋⠴⢋⡘⢰⣄⣀⣅⣡⠌⠛⠆⣿⡄⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣶⣁⣐⠄⠹⣟⠯⢿⣷⠾⠁⠥⠃⣹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠟⠋⡍⢴⣶⣶⣶⣤⣭⡐⢶⣾⣿⣶⡆⢨⠛⠻⣿⣿⣿
⣿⣿⣿⢏⣘⣚⣣⣾⣿⣿⣿⣿⣿⣿⢈⣿⣿⣿⣧⣘⠶⢂⠹⣿⣿
⣿⣿⠃⣾⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⡀⢿⣿⣿⣿⣿⣿⣿⡇⣿⣿
⣿⣿⡄⣿⣿⣿⣿⣿⣿⡯⠄⠄⠾⠿⠿⢦⣝⠻⣿⣿⣿⣿⠇⣿⣿
⣿⣿⣷⣜⠿⢿⣿⡿⠟⣴⣾⣿⡇⢰⣾⣦⡹⣷⣮⡙⢟⣩⣾⣿⣿
⣿⣿⣿⣿⣿⣆⢶⣶⣦⢻⣿⣿⣷⢸⣿⣿⣷⣌⠻⡷⣺⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡜⢿⣿⡎⢿⣿⣿⡬⣿⣿⣿⡏⢦⣔⠻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠎⠻⣷⡈⢿⣿⡇⢛⣻⣿⣿⢸⣿⣷⠌⡛⢿⣿
⣿⣿⣿⣿⣿⣿⡏⢰⣷⡙⢷⣌⢻⣿⣿⣿⣿⣿⢸⡿⢡⣾⣿⡶⠻
⣿⣿⣿⣿⣿⡟⣰⣶⣭⣙⠊⣿⣷⣬⣛⠻⣿⣿⠈⣴⣿⣿⣿⠃⠄
⣿⣿⣿⣿⡟⠄⠹⢿⣿⣿⣿⣤⠻⠟⠋⠡⠘⠋⢸⣿⣿⡿⠁⠄⠄
⣿⣿⣿⣿⠁⠄⠄⠄⠙⢻⣿⣿⣇⠄⠄⠄⠄⠄⣺⡿⠛⠄⠄⠄⠄
⣿⣿⣿⡏⠄⠄⠄⠄⠄⠄⠄⠉⠻⠷⠄⢠⣄⠄⠋⠄⠄⠄⠄⠄⠄'''
    c='''⣿⣿⣿⣿⠛⠛⠉⠄⠁⠄⠄⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⡟⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿
⣿⣿⡇⠄⠄⠄⠐⠄⠄⠄⠄⠄⠄⠄⠠⣿⣿⣿⣿⣿⣿
⣿⣿⡇⠄⢀⡀⠠⠃⡐⡀⠠⣶⠄⠄⢀⣿⣿⣿⣿⣿⣿
⣿⣿⣶⠄⠰⣤⣕⣿⣾⡇⠄⢛⠃⠄⢈⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡇⢀⣻⠟⣻⣿⡇⠄⠧⠄⢀⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣟⢸⣻⣭⡙⢄⢀⠄⠄⠄⠈⢹⣯⣿⣿⣿⣿⣿
⣿⣿⣿⣭⣿⣿⣿⣧⢸⠄⠄⠄⠄⠄⠈⢸⣿⣿⣿⣿⣿
⣿⣿⣿⣼⣿⣿⣿⣽⠘⡄⠄⠄⠄⠄⢀⠸⣿⣿⣿⣿⣿
⡿⣿⣳⣿⣿⣿⣿⣿⠄⠓⠦⠤⠤⠤⠼⢸⣿⣿⣿⣿⣿
⡞⣸⣿⣿⢏⣼⣶⣶⣶⣶⣤⣶⡤⠐⣿⣿⣿⣿⣿⣿⣿
⣯⣽⣛⠅⣾⣿⣿⣿⣿⣿⡽⣿⣧⡸⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡷⠹⠛⠉⠁⠄⠄⠄⠄⠄⠄⠐⠛⠻⣿⣿⣿⣿
⣿⣿⣿⠃⠄⠄⠄⠄⠄⣠⣤⣤⣤⡄⢤⣤⣤⣤⡘⠻⣿
⣿⣿⡟⠄⠄⣀⣤⣶⣿⣿⣿⣿⣿⣿⣆⢻⣿⣿⣿⡎⠝
⣿⡏⠄⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⠐
⣿⡏⣲⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣿⣿⣿⡟⣼
⣿⡠⠜⣿⣿⣿⣿⣟⡛⠿⠿⠿⠿⠟⠃⠾⠿⢟⡋⢶⣿
⣿⣧⣄⠙⢿⣿⣿⣿⣿⣿⣷⣦⡀⢰⣾⣿⣿⡿⢣⣿⣿
⣿⣿⣿⠂⣷⣶⣬⣭⣭⣭⣭⣵⢰⣴⣤⣤⣶⡾⢐⣿⣿
⣿⣿⣿⣷⡘⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⢃⣼⣿⣿'''
    v='''⣿⣿⣿⣿⣿⣿⠟⠋⠁⣀⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿
⣿⣿⣿⣿⠋⠁⠀⠀⠺⠿⢿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠻⣿
⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⠀⠀⠀⠀⠀⣤⣦⣄⠀⠀
⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⠏⣿⣿⣿⣿⣿⣁⠀⠀⠀⠛⠙⠛⠋⠀⠀
⡿⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⣰⣿⣿⣿⣿⡄⠘⣿⣿⣿⣿⣷⠄⠀⠀⠀⠀⠀⠀⠀⠀
⡇⠀⠀⠀⠀⠀⠀⠀⠸⠇⣼⣿⣿⣿⣿⣿⣷⣄⠘⢿⣿⣿⣿⣅⠀⠀⠀⠀⠀⠀⠀⠀
⠁⠀⠀⠀⣴⣿⠀⣐⣣⣸⣿⣿⣿⣿⣿⠟⠛⠛⠀⠌⠻⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣶⣮⣽⣰⣿⡿⢿⣿⣿⣿⣿⣿⡀⢿⣤⠄⢠⣄⢹⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⡘⣿⣿⣿⣿⣿⣿⠿⣶⣶⣾⣿⣿⡆⢻⣿⣿⠃⢠⠖⠛⣛⣷⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣮⣝⡻⠿⠿⢃⣄⣭⡟⢀⡎⣰⡶⣪⣿⠀
⠀⠀⠘⣿⣿⣿⠟⣛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⡿⢁⣾⣿⢿⣿⣿⠏⠀
⠀⠀⠀⣻⣿⡟⠘⠿⠿⠎⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⣿⣿⠧⣷⠟⠁⠀⠀
⡇⠀⠀⢹⣿⡧⠀⡀⠀⣀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⢰⣿⠀⠀⠀⠀
⡇⠀⠀⠀⢻⢰⣿⣶⣿⡿⠿⢂⣿⣿⣿⣿⣿⣿⣿⢿⣻⣿⣿⣿⡏⠀⠀⠁⠀⠀⠀⠀
⣷⠀⠀⠀⠀⠈⠿⠟⣁⣴⣾⣿⣿⠿⠿⣛⣋⣥⣶⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀ ⣿⡀'''
    b='''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠤⠤⠤⠤⠤⢄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠊⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠢⣀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠏⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡇⠀⣀⠀⢠⠀⡜⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⠇⠀⡃⢀⠀⣴⡇⠀⣸⣿⡅⡀⠀⠀⠀⠀⡆⠀⠀⠀⣿⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⢠⢰⡇⡎⢠⣻⣄⣠⣿⠛⣿⣿⠀⠀⠀⢠⣿⠶⡄⠀⣿⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⢸⣾⣇⣿⣿⠿⣿⣿⡿⠾⢿⣿⢷⡶⢶⡾⣿⣿⣷⣿⣾⣦⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠈⣿⣿⣿⣿⠀⣿⣿⠃⠰⣾⣿⠀⠃⠸⠀⣿⡇⢰⠄⣿⡟⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢀⣿⣿⣿⣿⠀⠻⣿⠀⠰⢿⣿⡇⢰⠀⢰⣿⠇⢸⠀⣿⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢸⣿⣿⣿⠛⠻⡿⠿⠿⠿⠿⠿⠿⠿⠷⠾⠿⣶⣶⣶⣿⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣸⣿⣾⣿⣿⣿⡄⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⢰⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⠀⠀⠈⠹⣿⣷⡀⢸⣄⡀⠀⢠⣤⠄⢀⣤⣾⣿⠀⣜⣀⣀⠀⠀
⠀⠀⠀⠀⠀⠀⡸⠁⠀⣀⡀⠀⠀⡀⠈⢿⣧⠀⣯⠙⠶⢦⣴⣾⣿⠿⢛⡇⢰⠃⠀⠀⠱⡀
⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⣿⠀⠘⣿⣆⣿⢿⣦⣼⡂⠀⣠⠞⢹⣧⡏⠀⠀⠀⠀⢃
⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⢿⡇⠀⢹⣿⣿⠑⠻⣏⠉⠟⠁⠀⣼⣿⣡⣿⠀⠀⠀⡟
⠀⠀⠀⠀⢀⡼⡃⠀⠀⠀⠀⠀⠀⢸⣿⡤⠄⣿⣿⠀⠀⠀⠀⢀⠀⠀⡟⢻⢿⡇⠀⠀⠀⡇
⠀⠀⠀⢀⣾⢿⣷⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⣿⣿⠀⠀⠀⠀⠸⡄⠀⢷⣾⠀⠙⢢⡀⠀⠃
⠀⠀⢠⣾⠏⣾⣿⠀⠀⠀⠀⠀⠀⢹⣿⠀⢀⣿⣿⠀⠀⠀⠀⠀⠈⢆⠘⣿⡆⠀⠀⠙⢴⠀
⠀⢀⡎⠊⣸⣿⣿⡇⠀⠀⠀⠀⠀⢸⣿⠀⣾⣿⠏⠀⠀⠀⠀⠀⠀⠈⢆⢸⡇⠀⠀⠀⠘⡇
⢀⠼⠇⠀⠿⠿⠿⠿⠀⠀⠀⠀⠀⠻⠿⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠼⠎⠁⠀⠀⠀⠠⢷'''
    n='''⣿⣿⣯⠉⠄⠄⠄⠄⠄⠄⡄⠄⠄⠄⠄⠄⠄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡟⠁⠄⠄⠄⠄⠄⢀⢀⠃⠄⠄⠄⠄⠄⠄⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡇⠄⠄⣾⣳⠄⠄⢀⣄⣦⣶⣴⠂⢒⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⡄⠄⠈⠚⡆⠄⢸⣿⣿⣿⣯⠋⡏⠄⠄⢸⣿⣿⣿⠿⠛⠛⠿⣿⣿⣿⣿⣿
⣿⣿⠟⣂⣀⣀⣀⡀⠠⠻⣷⣎⡼⠞⠓⠦⣤⣛⣋⣭⣴⣾⣿⣿⣷⣌⠻⣿⣿⣿
⣿⠋⣼⣿⣿⣿⣿⣿⣷⣦⣍⣙⠻⠳⠄⠄⠈⠙⠿⢿⣿⣿⣿⣿⣿⡟⣰⣿⣿⣿
⡟⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⣀⠄⠄⢀⣤⣤⣭⡛⠛⣩⣴⣿⣿⣿⣿
⣷⠸⠿⠛⠉⠙⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠷⠦⣹⣿⣿⣿⣿
⣿⣧⠄⠄⠄⢀⣴⣷⣶⣦⣬⣭⣉⣙⣛⠛⠿⠿⠿⠟⠁⡀⠄⠄⠄⢁⣿⣿⣿⣿
⣿⣿⡅⠄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣍⠲⣶⣤⣄⡀⠄⣴⣿⣿⣿⣿⣿
⣿⣿⣷⠄⣾⡏⢿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠄⠹⣷⡌⢿⣿⣿⣷⣦⡙⢿⣿⣿⣿
⣿⣿⣿⣷⡌⢷⡘⣿⣿⣿⣿⣿⣿⣧⣀⣀⡀⠄⠈⠹⡈⣿⣿⣿⣿⣿⣦⡙⣿⣿
⣿⣿⣿⣿⣿⣎⢷⡘⢿⣿⣿⣿⣿⣿⣿⣿⠃⠄⣼⣶⡇⣿⣿⣿⣿⣿⣿⠓⠜⣿
⣿⣿⣿⣿⣿⣿⣎⢻⣦⡙⠿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠄⣿⣿⣿⣿⣿⣿⣄⡀⢸
⣿⣿⣿⣿⣿⡿⢃⢼⣿⣿⣷⣤⣍⣉⣙⣛⣛⣉⣥⡄⠄⢿⣿⣿⣿⣿⡿⠟⣥⣿
⣿⣿⣿⡿⢋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⢁⣷⣤⣍⣉⣉⣭⣴⣾⣿⣿'''
    m='''⣿⠟⣽⣿⣿⣿⣿⣿⢣⠟⠋⡜⠄⢸⣿⣿⡟⣬⢁⠠⠁⣤⠄⢰⠄⠇⢻⢸
⢏⣾⣿⣿⣿⠿⣟⢁⡴⡀⡜⣠⣶⢸⣿⣿⢃⡇⠂⢁⣶⣦⣅⠈⠇⠄⢸⢸
⣹⣿⣿⣿⡗⣾⡟⡜⣵⠃⣴⣿⣿⢸⣿⣿⢸⠘⢰⣿⣿⣿⣿⡀⢱⠄⠨⢸
⣿⣿⣿⣿⡇⣿⢁⣾⣿⣾⣿⣿⣿⣿⣸⣿⡎⠐⠒⠚⠛⠛⠿⢧⠄⠄⢠⣼
⣿⣿⣿⣿⠃⠿⢸⡿⠭⠭⢽⣿⣿⣿⢂⣿⠃⣤⠄⠄⠄⠄⠄⠄⠄⠄⣿⡾
⣼⠏⣿⡏⠄⠄⢠⣤⣶⣶⣾⣿⣿⣟⣾⣾⣼⣿⠒⠄⠄⠄⡠⣴⡄⢠⣿⣵
⣳⠄⣿⠄⠄⢣⠸⣹⣿⡟⣻⣿⣿⣿⣿⣿⣿⡿⡻⡖⠦⢤⣔⣯⡅⣼⡿⣹
⡿⣼⢸⠄⠄⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣕⡜⡌⡝⡸⠙⣼⠟⢱⠏
⡇⣿⣧⡰⡄⣿⣿⣿⣿⡿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣋⣪⣥⢠⠏⠄
⣧⢻⣿⣷⣧⢻⣿⣿⣿⡇⠄⢀⣀⣀⡙⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠂⠄⠄
⢹⣼⣿⣿⣿⣧⡻⣿⣿⣇⣴⣿⣿⣿⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿⣰⠄⠄⠄
⣼⡟⡟⣿⢸⣿⣿⣝⢿⣿⣾⣿⣿⣿⢟⣾⣿⣿⣿⣿⣿⣿⣿⣿⠟⠄⡀⡀
⣿⢰⣿⢹⢸⣿⣿⣿⣷⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠉⠄⠄⣸⢰⡇
⣿⣾⣹⣏⢸⣿⣿⣿⣿⣿⣷⣍⡻⣛⣛⣛⡉⠁⠄⠄⠄⠄⠄⠄⢀⢇⡏⠄'''
    r=random.choice([a,x,z,m,c,v,n,b])
    # في دالة start_bot، عدل رسالة الترحيب:
    msg = f"""<b>𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗧𝗵𝗲 𝗖𝗿𝗲𝗱𝗶𝘁 𝗖𝗮𝗿𝗱𝘀 𝗕𝗼𝘁</b>
    <pre>{r}</pre>

<b>𝗖𝗵𝗮𝗻𝗻𝗲𝗹:</b> @A_A_T_T943
<b>𝗢𝘄𝗻𝗲𝗿:</b> @A_A_T_T   |  𝐴𝐻𝑀𝐸𝐷

<b>𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀:</b>

<b>/fake [𝗰𝗼𝘂𝗻𝘁𝗿𝘆]</b> - 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗳𝗮𝗸𝗲 𝗶𝗻𝗳𝗼
<b>/gen [𝗕𝗜𝗡|𝗠𝗼𝗻𝘁𝗵|𝗬𝗲𝗮𝗿|𝗖𝗩𝗩]</b> - 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗰𝗮𝗿𝗱𝘀
<b>/bin [𝗰𝗮𝗿𝗱 𝗻𝘂𝗺𝗯𝗲𝗿]</b> - 𝗖𝗵𝗲𝗰𝗸 𝗕𝗜𝗡 𝗶𝗻𝗳𝗼
<b>/url [𝘄𝗲𝗯𝘀𝗶𝘁𝗲_𝘂𝗿𝗹]</b> - 𝗔𝗻𝗮𝗹𝘆𝘇𝗲 𝘄𝗲𝗯𝘀𝗶𝘁𝗲
<b>/analyze_all</b> - 𝗔𝗻𝗮𝗹𝘆𝘇𝗲 𝗮𝗹𝗹 𝘂𝗿𝗹𝘀 𝗶𝗻 𝗳𝗶𝗹𝗲
<b>/𝗵𝗲𝗹𝗽</b> - 𝗙𝘂𝗹𝗹 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗹𝗶𝘀𝘁

# Upload .txt file with URLs for bulk analysis
#سيتم اضافه بوابات ودوركات وازرار مخصصه لكلشي سيرج مواقع حمايه البوت في مرحله التطوير
"""
    
    bot.send_message(chat_id, msg, parse_mode='HTML')
# =========================
# fake command - Fixed
# =========================
# =========================
# Fake Command
# =========================
@bot.message_handler(commands=['fake'])
def fake_command(message):
    try:
        # Check if country code is provided
        if len(message.text.split()) > 1:
            code = message.text.split()[1].upper()
        else:
            code = 'US'  # Default to USA
        
        # Valid country codes
        valid_codes = ['US', 'UK', 'IS', 'JO', 'KSA', 'MO']
        if code not in valid_codes:
            code = 'US'
        
        # Get data from API
        response = requests.get(f'https://randomuser.me/api/?nat={code}', timeout=10)
        
        # Check if request was successful
        if response.status_code != 200:
            bot.reply_to(message, "❌ Could not connect to generation service. Try again.")
            return
        
        data = response.json()
        
        if 'results' not in data or len(data['results']) == 0:
            bot.reply_to(message, "❌ No data found. Try again.")
            return
        
        result = data['results'][0]
        
        # Extract information
        name = f"{result['name']['title']} {result['name']['first']} {result['name']['last']}"
        street = f"{result['location']['street']['number']} {result['location']['street']['name']}"
        city = result['location']['city']
        state = result['location']['state']
        country = result['location']['country']
        postcode = str(result['location']['postcode'])
        phone = result['phone']
        email = result['email']
        
        # Create message
        msg = f"""
📍 𝐅𝐚𝐤𝐞 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧: ✅
━━━━━━━━━━━━━━━━
𝐂𝐨𝐮𝐧𝐭𝐫𝐲:  {country}
𝐍𝐚𝐦𝐞:  {name}
𝐂𝐢𝐭𝐲:  {city}
𝐒𝐭𝐚𝐭𝐞:  {state}
𝐙𝐢𝐩 𝐂𝐨𝐝𝐞:  {postcode}
𝐒𝐭𝐫𝐞𝐞𝐭:  {street}
𝐏𝐡𝐨𝐧𝐞:  {phone}
𝐄𝐦𝐚𝐢𝐥:  {email}
 Generated successfully!
━━━━━━━━━━━━━━━━
"""
        bot.reply_to(message, msg)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# =========================
# Gen Command
# =========================
def get_bin_info(bin_number):
    try:
        response = requests.get(f'https://lookup.binlist.net/{bin_number[:6]}', timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

@bot.message_handler(commands=['gen'])
def generate_card(message):
    try:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "⚠️ Usage: /gen BIN|Month|Year|CVV\nExample: /gen 552742|12|25|123")
            return
        
        input_text = message.text.split('/gen ', 1)[1]
        parts = re.split(r'[|:/]', input_text)
        
        if len(parts) < 1:
            bot.reply_to(message, "❌ Invalid format. Use: BIN|Month|Year|CVV")
            return
        
        bin_part = re.sub(r'[^0-9]', '', parts[0])
        month = re.sub(r'[^0-9]', '', parts[1]) if len(parts) > 1 else None
        year = re.sub(r'[^0-9]', '', parts[2]) if len(parts) > 2 else None
        cvv = re.sub(r'[^0-9]', '', parts[3]) if len(parts) > 3 else None
        
        if len(bin_part) < 6:
            bot.reply_to(message, "❌ BIN must be at least 6 digits")
            return
        
        cards = []
        for i in range(10):
            remaining_digits = 16 - len(bin_part)
            if remaining_digits > 0:
                random_part = ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits)])
                card_number = bin_part + random_part
            else:
                card_number = bin_part[:16]
            
            if month and month.isdigit() and 1 <= int(month) <= 12:
                card_month = month.zfill(2)
            else:
                card_month = str(random.randint(1, 12)).zfill(2)
            
            if year and year.isdigit():
                if len(year) == 2:
                    card_year = year
                elif len(year) == 4:
                    card_year = year[2:]
                else:
                    card_year = str(random.randint(23, 30))
            else:
                card_year = str(random.randint(23, 30))
            
            if cvv and cvv.isdigit() and 3 <= len(cvv) <= 4:
                card_cvv = cvv
            else:
                card_cvv = str(random.randint(100, 999))
            
            cards.append(f"{card_number}|{card_month}|{card_year}|{card_cvv}")
        
        bin_info = get_bin_info(bin_part)
        
        cards_text = '\n'.join(cards)
        
        msg = f"""
💳 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞𝐝 𝐂𝐚𝐫𝐝𝐬:
━━━━━━━━━━━━━━━━
{cards_text}
━━━━━━━━━━━━━━━━
"""
        
        if bin_info:
            bank_name = bin_info.get('bank', {}).get('name', 'Unknown')
            country_name = bin_info.get('country', {}).get('name', 'Unknown')
            card_type = bin_info.get('type', 'Unknown')
            brand = bin_info.get('scheme', 'Unknown')
            
            msg += f"""
📊 𝐁𝐈𝐍 𝐈𝐧𝐟𝐨 ({bin_part[:6]}):
𝐁𝐚𝐧𝐤: {bank_name}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country_name}
𝐓𝐲𝐩𝐞: {card_type}
𝐁𝐫𝐚𝐧𝐝: {brand}
"""
        
        bot.reply_to(message, f"<code>{msg}</code>", parse_mode='HTML')
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}\nUse: /gen 552742|12|25|123")

# =========================
# Bin Command
# =========================
# =========================
# Bin Command - Fixed
# =========================
@bot.message_handler(commands=['bin'])
def bin_check(message):
    try:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "⚠️ Usage: /bin BIN_number\nExample: /bin 552742")
            return
        
        bin_number = message.text.split()[1]
        bin_number = re.sub(r'[^0-9]', '', bin_number)
        
        if len(bin_number) < 6:
            bot.reply_to(message, "❌ BIN must be at least 6 digits")
            return
        
        response = requests.get(f'https://lookup.binlist.net/{bin_number[:6]}', timeout=10)
        
        if response.status_code != 200:
            bot.reply_to(message, "❌ Could not find info for this BIN")
            return
        
        data = response.json()
        
        # استخراج المعلومات
        brand = data.get('scheme', 'Unknown').upper()
        card_type = data.get('type', 'Unknown').upper()
        bank_name = data.get('bank', {}).get('name', 'Unknown')
        country_name = data.get('country', {}).get('name', 'Unknown')
        country_code = data.get('country', {}).get('alpha2', 'Unknown')
        country_flag = data.get('country', {}).get('emoji', '🏳️')
        prepaid = str(data.get('prepaid', 'Unknown')).upper()
        
        # الحصول على مستوى البطاقة
        card_level = get_card_level(bin_number[:6])
        card_info = f"{card_type} - {card_level}" if card_level else card_type
        
        # إصلاح معلومات البنك إن كانت فارغة
        if bank_name == 'Unknown' or not bank_name:
            bank_name = get_bank_name(bin_number[:6])
        
        # التنسيق الجميل
        msg = f"""
𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍

𝗕𝗶𝗻 ⇾ {bin_number[:6]}

𝐈𝐧𝐟𝐨 ⇾ {card_info}
𝐁𝐫𝐚𝐧𝐝 ⇾ {brand}
𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank_name}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country_name} {country_flag}
𝐂𝐨𝐝𝐞 ⇾ {country_code}
𝐏𝐫𝐞𝐩𝐚𝐢𝐝 ⇾ {prepaid}

━━━━━━━━━━━━━━━━
Checked by 𝐴𝐻𝑀𝐸𝐷
"""
        bot.reply_to(message, msg)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# =========================
# دالة للحصول على مستوى البطاقة
# =========================
def get_card_level(bin_number):
    """الحصول على مستوى البطاقة"""
    try:
        first_digit = bin_number[0]
        second_digit = bin_number[1]
        
        # قواعد تحديد المستوى
        if first_digit == '4':
            return "CLASSIC"
        elif first_digit == '5':
            if second_digit in ['1', '2', '3', '4', '5']:
                return "GOLD"
            else:
                return "STANDARD"
        elif first_digit == '3':
            return "PLATINUM"
        elif first_digit == '6':
            return "WORLD"
        else:
            return "STANDARD"
    except:
        return ""

# =========================
# دالة للحصول على اسم البنك
# =========================
def get_bank_name(bin_number):
    """الحصول على اسم البنك من رقم BIN"""
    try:
        # قاعدة بيانات بسيطة للبنوك المشهورة
        bank_bins = {
            '4': 'VISA BANK',
            '5': 'MASTERCARD BANK',
            '3': 'AMERICAN EXPRESS',
            '6': 'DISCOVER BANK'
        }
        
        first_digit = bin_number[0]
        return bank_bins.get(first_digit, "UNKNOWN BANK")
    except:
        return "UNKNOWN BANK"

# =========================
# Website Analysis Functions
# =========================

def analyze_site(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    result = {
        'url': url, 'payment_gateways': [], 'captcha': False, 
        'cloudflare': False, 'graphql': False, 'platform': None, 
        'http_status': None, 'content_type': None, 'cookies': {}, 
        'error': None, 'country': None
    }

    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        headers = response.headers
        content_type = headers.get('Content-Type', '')
        response_text = response.text
        cookies = response.cookies.get_dict()
        country = headers.get('CF-IPCountry', 'Unknown')

        http_version = 'HTTP/1.1' if response.raw.version == 11 else 'HTTP/1.0'
        status_code = response.status_code
        reason_phrase = response.reason
        http_status = f"{http_version} {status_code} {reason_phrase}"

        result.update({
            'payment_gateways': check_for_payment_gateways(headers, response_text, cookies),
            'cloudflare': check_for_cloudflare(response_text),
            'captcha': check_for_captcha(response_text),
            'graphql': check_for_graphql(response_text),
            'platform': check_for_platform(response_text),
            'http_status': http_status,
            'content_type': content_type,
            'cookies': cookies,
            'country': country
        })

    except requests.Timeout:
        result['error'] = '⏰ Timeout error'
    except Exception as e:
        result['error'] = f'❌ Error: {str(e)}'
    
    return result

def check_for_payment_gateways(headers, response_text, cookies):
    gateway_keywords = [
        'stripe', 'paypal', 'square', 'venmo', 'bitcoin', 'braintree', 'amazon-pay',
        'adyen', '2checkout', 'skrill', 'authorize.net', 'worldpay', 'payu', 'paytm',
        'afterpay', 'alipay', 'klarna', 'affirm', 'bluesnap', 'checkout.com', 'dwolla',
        'paddle', 'payoneer', 'sagepay', 'wechat pay', 'yandex.money', 'zelle',
        'shopify', 'buy now', 'add to cart', 'store', 'checkout', 'cart', 'shop now',
        'card', 'payment', 'gateway', 'checkout button', 'pay with'
    ]

    combined_text = response_text.lower() + str(headers).lower() + str(cookies).lower()
    detected_gateways = [keyword.capitalize() for keyword in gateway_keywords if keyword in combined_text]

    return list(set(detected_gateways))

def check_for_cloudflare(response_text):
    cloudflare_markers = ['checking your browser', 'cf-ray', 'cloudflare']
    return any(marker in response_text.lower() for marker in cloudflare_markers)

def check_for_captcha(response_text):
    captcha_markers = ['recaptcha', 'g-recaptcha']
    return any(marker in response_text.lower() for marker in captcha_markers)

def check_for_graphql(response_text):
    graphql_markers = ['graphql', 'application/graphql']
    return any(marker in response_text.lower() for marker in graphql_markers)

def check_for_platform(response_text):
    platform_markers = {
        'woocommerce': ['woocommerce', 'wc-cart', 'wc-ajax'],
        'magento': ['magento', 'mageplaza'],
        'shopify': ['shopify', 'myshopify'],
        'prestashop': ['prestashop', 'addons.prestashop'],
        'opencart': ['opencart', 'route=common/home'],
        'bigcommerce': ['bigcommerce', 'stencil'],
        'wordpress': ['wordpress', 'wp-content'],
        'drupal': ['drupal', 'sites/all'],
        'joomla': ['joomla', 'index.php?option=com_']
    }

    for platform, markers in platform_markers.items():
        if any(marker in response_text.lower() for marker in markers):
            return platform.capitalize()

    return None

def format_analysis_results(results):
    analysis = (
        f"🔍 𝗦𝗜𝗧𝗘 𝗔𝗡𝗔𝗟𝗬𝗦𝗜𝗦 𝗥𝗘𝗦𝗨𝗟𝗧𝗦:\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"𝗨𝗥𝗟 ➜ {results['url']}\n"
        f"𝗣𝗔𝗬𝗠𝗘𝗡𝗧 𝗚𝗔𝗧𝗘𝗪𝗔𝗬𝗦 ➜ {', '.join(results['payment_gateways']) if results['payment_gateways'] else 'None'}\n"
        f"𝗖𝗔𝗣𝗧𝗖𝗛𝗔 ➜ {'✅ Yes' if results['captcha'] else '❌ No'}\n"
        f"𝗖𝗟𝗢𝗨𝗗𝗙𝗟𝗔𝗥𝗘 ➜ {'✅ Yes' if results['cloudflare'] else '❌ No'}\n"
        f"𝗚𝗥𝗔𝗣𝗛𝗤𝗟 𝗗𝗘𝗧𝗘𝗖𝗧𝗘𝗗 ➜ {'✅ Yes' if results['graphql'] else '❌ No'}\n"
        f"𝗣𝗟𝗔𝗧𝗙𝗢𝗥𝗠 ➜ {results['platform'] or 'Unknown'}\n"
        f"𝗛𝗧𝗧𝗣 𝗦𝗧𝗔𝗧𝗨𝗦 ➜ {results['http_status']}\n"
        f"𝗖𝗢𝗨𝗡𝗧𝗥𝗬 ➜ {results['country']}\n"
        f"𝗘𝗥𝗥𝗢𝗥 ➜ {results['error'] or 'None'}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"⚡ Analysis completed successfully!"
    )
    return analysis

# =========================
# URL Analysis Command
# =========================
@bot.message_handler(commands=['url'])
def url_analysis(message):
    try:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "⚠️ Usage: /url <website_url>\nExample: /url https://example.com")
            return
        
        url = message.text.split('/url ', 1)[1].strip()
        
        wait_msg = bot.reply_to(message, " Please wait...")
        
        result = analyze_site(url)
        analysis = format_analysis_results(result)
        
        bot.delete_message(message.chat.id, wait_msg.message_id)
        bot.reply_to(message, analysis)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error analyzing website: {str(e)}")

# =========================
# File Analysis Command
# =========================
@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        wait_msg = bot.reply_to(message, "📁 **Processing file... Please wait...** ⏳")
        
        urls = []
        try:
            content = downloaded_file.decode('utf-8')
            urls = [line.strip() for line in content.splitlines() if line.strip()]
        except:
            try:
                content = downloaded_file.decode('latin-1')
                urls = [line.strip() for line in content.splitlines() if line.strip()]
            except:
                bot.delete_message(message.chat.id, wait_msg.message_id)
                bot.reply_to(message, "❌ Cannot decode file.")
                return
        
        if not urls:
            bot.delete_message(message.chat.id, wait_msg.message_id)
            bot.reply_to(message, "❌ No valid URLs found in the file.")
            return
        
        bot.delete_message(message.chat.id, wait_msg.message_id)
        bot.reply_to(message, f"File processed successfully!\nFound URLs: {len(urls)}\n\nSend /analyze_all to start analysis.")
        
        # تخزين مؤقت
        bot.user_data = getattr(bot, 'user_data', {})
        bot.user_data[message.chat.id] = {'urls': urls}
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error processing file: {str(e)}")

# =========================
# Analyze All Command
# =========================
@bot.message_handler(commands=['analyze_all'])
def analyze_all_urls(message):
    try:
        chat_id = message.chat.id
        bot.user_data = getattr(bot, 'user_data', {})
        
        if chat_id not in bot.user_data or 'urls' not in bot.user_data[chat_id]:
            bot.reply_to(message, "❌ No URLs found. Send a .txt file first.")
            return
        
        urls = bot.user_data[chat_id]['urls']
        
        if not urls:
            bot.reply_to(message, "❌ No URLs to analyze.")
            return
        
        progress_msg = bot.reply_to(message, f"Starting analysis of {len(urls)} URLs...**\n\n Analyzing: 0/{len(urls)}")
        
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls):
            try:
                # تحديث رسالة التقدم
                if i % 5 == 0:  # تحديث كل 5 مواقع
                    bot.edit_message_text(
                        f"Analyzing...\n\n Completed: {i}/{len(urls)}\n✅ Successful: {successful}\n❌ Failed: {failed}\n\nCurrent: {url[:30]}...",
                        chat_id,
                        progress_msg.message_id
                    )
                
                # تحليل الموقع
                result = analyze_site(url)
                analysis = format_analysis_results(result)
                
                # إرسال النتائج إذا كان هناك بوابات دفع
                if result['payment_gateways']:
                    bot.send_message(chat_id, analysis)
                    successful += 1
                else:
                    failed += 1
                    
                time.sleep(1)  # تجنب الحظر
                
            except Exception as e:
                failed += 1
                continue
        
        # النتيجة النهائية
        bot.edit_message_text(
            f"✅ **Analysis Completed!**\n\n📊 Results:\n✅ Successful: {successful}\n❌ Failed: {failed}\n📝 Total: {len(urls)}\n\n⚡ Process finished!",
            chat_id,
            progress_msg.message_id
        )
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error in bulk analysis: {str(e)}")

# =========================
# Unknown Command Handler
# =========================
@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    if message.text.startswith('/'):
        bot.reply_to(message, "❌ Unknown command.\n\nAvailable commands:\n/start - Start\n/fake - Fake info\n/gen - Generate cards\n/bin - Check BIN\n/url - Analyze website\n/analyze_all - Analyze all URLs from file")

# =========================
# Run Bot
# =========================
print("✅ Bot is running...")
print("📱 Go to Telegram and search for the bot")
print("⚡ Use /start to begin")

while True:
    try:
        bot.polling(none_stop=True, timeout=30)
    except Exception as e:
        print(f"⚠️ Error: {e}")
        time.sleep(5)