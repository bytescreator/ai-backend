import os
import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import gizlidosya  # API anahtarı için
import threading
import datetime
import numpy as np
from onnxruntime import InferenceSession
import pygame
import soundfile as sf
import sounddevice as sd  # Ses kaydetme için
import whisper  # Whisper kütüphanesini import et

# Google Generative AI yapılandırması
genai.configure(api_key=gizlidosya.api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Piper için ONNX modeli yükleme
piper_model_path = r"C:\\Users\\melek\\Downloads\\piper_windows_amd64\\piper\\tr_TR-dfki-medium.onnx"
if not os.path.exists(piper_model_path):
    raise FileNotFoundError(f"Piper model dosyası bulunamadı: {piper_model_path}")

piper_session = InferenceSession(piper_model_path)

# Whisper modelini yükleme
whisper_model = whisper.load_model("base")  # Burada "base" modeli yüklüyoruz

def text_to_unicode_ids(text):
    return [max(-256, min(ord(char), 255)) for char in text]

def piper_speak(text):
    try:
        if not text.strip():
            raise ValueError("Seslendirme için metin boş olamaz.")

        # Metni sınırla (örneğin 200 karakterle)
        text = text[:200]

        input_ids = np.array([text_to_unicode_ids(text)], dtype=np.int64)
        input_lengths = np.array([len(input_ids[0])], dtype=np.int64)
        scales = np.array([1.0, 1.0, 1.0], dtype=np.float32)

        inputs = {
            "input": input_ids,
            "input_lengths": input_lengths,
            "scales": scales,
        }

        outputs = piper_session.run(None, inputs)
        audio = outputs[0].flatten()

        # Ses dosyasını kaydetme
        output_file = "output.wav"
        sf.write(output_file, audio, 16000)  # 16000 örnekleme oranıyla kaydet

        # pygame ile ses dosyasını çalma
        pygame.mixer.init(frequency=16000)  # 16000 örnekleme oranı ile başlatma
        pygame.mixer.music.load(output_file)  # Ses dosyasını yükle
        pygame.mixer.music.play()  # Ses çalmaya başla

        while pygame.mixer.music.get_busy():  # Ses çalmaya devam ederken bekle
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Seslendirme hatası: {e}")

# Türkçe tarih formatı
def get_turkish_date():
    now = datetime.datetime.today()
    turkish_months = [
        'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
        'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
    ]
    turkish_weekdays = [
        'Pazar', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'
    ]

    day = now.day
    month = turkish_months[now.month - 1]
    year = now.year
    weekday = turkish_weekdays[now.weekday()]
    return f"{day} {month} {year}, {weekday}"

# Modelden yanıt oluşturma
def generate_response(prompt):
    try:
        if "saat" in prompt.lower():
            now = datetime.datetime.now()
            return f"Şu an saat {now.strftime('%H:%M')}."
        elif "tarih" in prompt.lower():
            return f"Bugünün tarihi: {get_turkish_date()}."
        else:
            cevap = model.generate_content(prompt)
            return cevap.text
    except Exception as e:
        return f"Hata oluştu: {e}"

# Kullanıcı girdisi gönderme
def send_input():
    user_input = user_entry.get("1.0", tk.END).strip()
    if not user_input:
        return
    chat_box.insert(tk.END, f"Siz: {user_input}\n")
    user_entry.delete("1.0", tk.END)

    chat_box.insert(tk.END, "AI düşünüyor...\n")
    threading.Thread(target=process_response, args=(user_input,)).start()

# Modelden yanıt alıp ekrana ve sese yazdırma
def process_response(user_input):
    response = generate_response(user_input)
    chat_box.insert(tk.END, f"AI: {response}\n")
    piper_speak(response)

# Ses kaydetme ve Whisper ile çözümleme fonksiyonu
def record_and_recognize():
    chat_box.insert(tk.END, "Mikrofon dinleniyor...\n")
    try:
        # Ses kaydetme
        duration = 5  # saniye
        sample_rate = 16000
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Ses kaydının tamamlanmasını bekle
        audio = np.array(audio, dtype=np.float32).flatten()

        # Whisper kullanarak ses tanıma
        result = whisper_model.transcribe(audio)  # Hata olan kısım burada düzeltilmiş oldu
        user_input = result['text']
        chat_box.insert(tk.END, f"Siz (sesli): {user_input}\n")

        chat_box.insert(tk.END, "AI düşünüyor...\n")
        threading.Thread(target=process_response, args=(user_input,)).start()
    except Exception as e:
        chat_box.insert(tk.END, f"Ses tanıma hatası: {e}\n")

# Arayüz oluşturma
root = tk.Tk()
root.title("sesli asistanım")

# Arka planı ve fontu değiştirme
root.configure(bg="#f0f0f0")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, font=("Arial", 12), bg="#e0e0e0", fg="black")
chat_box.pack(padx=10, pady=10)

user_entry = tk.Text(root, height=4, width=40, font=("Arial", 12), bg="#e0e0e0", fg="black")
user_entry.pack(padx=10, pady=5)

# Butonlar
send_button = tk.Button(root, text="Gönder", font=("Arial", 12), command=send_input, bg="#4CAF50", fg="white", relief="raised", width=10)
send_button.pack(side=tk.LEFT, padx=20, pady=10)

voice_button = tk.Button(root, text="Sesli Giriş", font=("Arial", 12), command=record_and_recognize, bg="#007BFF", fg="white", relief="raised", width=12)
voice_button.pack(side=tk.LEFT, padx=20, pady=10)

exit_button = tk.Button(root, text="Çıkış", font=("Arial", 12), command=root.quit, bg="#f44336", fg="white", relief="raised", width=10)
exit_button.pack(side=tk.RIGHT, padx=20, pady=10)

root.mainloop()
