import telebot
import subprocess
import time
import threading
import os
import sys
import signal

# استخدام متغير بيئة للتوكن (أكثر أماناً)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8102359893:AAEZUgzUtWN4xyjpApOjQ_ZA3Tv9NGssnF0")

bot = telebot.TeleBot(BOT_TOKEN)

# متغيرات لتخزين الروابط
stream_link = None
video_link = None
is_streaming = False
stream_process = None  # لتخزين العملية الحالية


def start_stream(video, rtmp):
    global is_streaming, stream_process
    is_streaming = True

    while is_streaming:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] بدء البث...")
        try:
            stream_process = subprocess.Popen([
                "ffmpeg",
                "-re",
                "-headers", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "-headers", "Accept: */*",
                "-headers", "Connection: keep-alive",
                "-i", video,
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "128k",
                "-f", "flv",
                rtmp
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stream_process.wait()
            
            if not is_streaming:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] تم إيقاف البث")
                break
                
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] انتهى البث – إعادة التشغيل بعد 5 ثوانٍ...")
            time.sleep(5)

        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] خطأ: {e}")
            if is_streaming:
                time.sleep(5)
            else:
                break


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
                 "اهلاً! أرسل:\n\n"
                 "**رابط الفيديو** أولاً ثم **رابط البث RTMP**\n\n"
                 "للإيقاف: /stop")


# استلام رابط الفيديو
@bot.message_handler(func=lambda m: m.text and m.text.startswith("http") and "rtmp" not in m.text.lower())
def get_video(message):
    global video_link
    video_link = message.text.strip()
    bot.reply_to(message, "✅ تم حفظ رابط الفيديو.\nالآن أرسل **رابط البث RTMP**")


# استلام رابط الـ RTMP
@bot.message_handler(func=lambda m: m.text and m.text.startswith("rtmp"))
def get_rtmp(message):
    global stream_link, video_link, is_streaming

    if video_link is None:
        bot.reply_to(message, "⚠️ أرسل أولاً رابط الفيديو!")
        return

    if is_streaming:
        bot.reply_to(message, "⚠️ يوجد بث نشط بالفعل! استخدم /stop لإيقافه أولاً.")
        return

    stream_link = message.text.strip()
    bot.reply_to(message, "✅ تم حفظ الرابطين.\n🔴 جاري بدء البث...")

    # تشغيل البث في Thread حتى لا يتوقف البوت
    threading.Thread(target=start_stream, args=(video_link, stream_link), daemon=True).start()


# إيقاف البث
@bot.message_handler(commands=['stop'])
def stop(message):
    global is_streaming, stream_process
    
    if not is_streaming:
        bot.reply_to(message, "⚠️ لا يوجد بث نشط حالياً!")
        return
    
    is_streaming = False
    
    # إيقاف عملية ffmpeg
    if stream_process:
        try:
            stream_process.terminate()
            stream_process.wait(timeout=5)
        except:
            stream_process.kill()
    
    bot.reply_to(message, "⏹️ تم إيقاف البث بنجاح!")


# للتعامل مع إيقاف البرنامج بشكل صحيح
def signal_handler(sig, frame):
    global is_streaming, stream_process
    print("\n[إيقاف البوت...]")
    is_streaming = False
    if stream_process:
        stream_process.terminate()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


# بدء البوت مع معالجة الأخطاء
if __name__ == "__main__":
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] بدء تشغيل البوت...")
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] خطأ في الاتصال: {e}")
            print("[إعادة المحاولة بعد 5 ثوانٍ...]")
            time.sleep(5)