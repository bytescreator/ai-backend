import os
import tkinter as tk
from tkinter import scrolledtext
import threading
import datetime
import numpy as np
import pygame
import soundfile as sf
import sounddevice as sd
import whisper
from onnxruntime import InferenceSession
import google.generativeai as genai
import gizlidosya

# Google Generative AI yapılandırması
genai.configure(api_key=gizlidosya.api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Piper için ONNX modeli yükleme
PIPER_MODEL_PATH = r"C:\\Users\\melek\\Downloads\\piper_windows_amd64\\piper\\tr_TR-dfki-medium.onnx"
if not os.path.exists(PIPER_MODEL_PATH):
    raise FileNotFoundError(f"Piper model dosyası bulunamadı: {PIPER_MODEL_PATH}")

piper_session = InferenceSession(PIPER_MODEL_PATH)

# Whisper modelini yükleme
whisper_model = whisper.load_model("base")


# Helper functions
def text_to_unicode_ids(text):
    return [max(-256, min(ord(char), 255)) for char in text]


def normalize_audio(audio):
    max_val = np.max(np.abs(audio))
    return audio / max_val if max_val > 0 else audio


def save_audio_to_wav(audio_data, sample_rate, output_file="output.wav"):
    """
    Ses çıktısını WAV formatında kaydet.

    Args:
        audio_data (numpy.ndarray): Normalleştirilmiş ses verisi.
        sample_rate (int): Örnekleme oranı (Hz).
        output_file (str): Kaydedilecek dosya adı.
    """
    sf.write(output_file, audio_data, sample_rate, subtype='PCM_16')
    print(f"Audio saved as {output_file}")

# Piper seslendirme
def piper_speak(text):
    try:
        if not text.strip():
            raise ValueError("Seslendirme için metin boş olamaz.")

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
        audio = normalize_audio(audio)

        # WAV dosyasına kaydetme
        sample_rate = 24000
        save_audio_to_wav(audio, sample_rate,output_file="C:/Users/melek/Downloads/piper_windows_amd64/piper/output.wav")

        # pygame ile ses dosyasını çalma
        pygame.mixer.init(frequency=sample_rate)
        pygame.mixer.music.load("C:/Users/melek/Downloads/piper_windows_amd64/piper/output.wav")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
    except Exception as e:
        print(f"Seslendirme hatası: {e}")


def get_turkish_date():
    now = datetime.datetime.today()
    turkish_months = [
        'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
        'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
    ]
    turkish_weekdays = [
        'Pazar', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'
    ]
    return f"{now.day} {turkish_months[now.month - 1]} {now.year}, {turkish_weekdays[now.weekday()]}"


def generate_response(prompt):
    try:
        if "saat" in prompt.lower():
            now = datetime.datetime.now()
            return f"Şu an saat {now.strftime('%H:%M')}."
        elif "tarih" in prompt.lower():
            return f"Bugünün tarihi: {get_turkish_date()}."
        else:
            return model.generate_content(prompt).text
    except Exception as e:
        return f"Hata oluştu: {e}"


def send_input():
    user_input = user_entry.get("1.0", tk.END).strip()
    if not user_input:
        return
    chat_box.insert(tk.END, f"Siz: {user_input}\n")
    user_entry.delete("1.0", tk.END)
    chat_box.insert(tk.END, "AI düşünüyor...\n")
    threading.Thread(target=process_response, args=(user_input,)).start()


def process_response(user_input):
    response = generate_response(user_input)
    chat_box.insert(tk.END, f"AI: {response}\n")
    piper_speak(response)


def record_and_recognize():
    chat_box.insert(tk.END, "Mikrofon dinleniyor...\n")
    try:
        duration = 5
        sample_rate = 24000
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
        audio = audio.flatten() / np.max(np.abs(audio))

        if audio is None or len(audio) == 0:
            chat_box.insert(tk.END, "Ses kaydı alınamadı.\n")
            return

        result = whisper_model.transcribe(audio, language="tr")
        user_input = result.get('text', '').strip()
        if not user_input:
            chat_box.insert(tk.END, "Anlaşılamayan ses.\n")
            return

        chat_box.insert(tk.END, f"Siz (sesli): {user_input}\n")
        chat_box.insert(tk.END, "AI düşünüyor...\n")
        threading.Thread(target=process_response, args=(user_input,)).start()

    except Exception as e:
        chat_box.insert(tk.END, f"Ses tanıma hatası: {str(e)}\n")


# GUI setup
root = tk.Tk()
root.title("Sesli Asistanım")
root.configure(bg="#f0f0f0")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, font=("Arial", 12), bg="#e0e0e0",
                                     fg="black")
chat_box.pack(padx=10, pady=10)

user_entry = tk.Text(root, height=4, width=40, font=("Arial", 12), bg="#e0e0e0", fg="black")
user_entry.pack(padx=10, pady=5)

send_button = tk.Button(root, text="Gönder", font=("Arial", 12), command=send_input, bg="#4CAF50", fg="white",
                        relief="raised", width=10)
send_button.pack(side=tk.LEFT, padx=20, pady=10)

voice_button = tk.Button(root, text="Sesli Giriş", font=("Arial", 12), command=record_and_recognize, bg="#007BFF",
                         fg="white", relief="raised", width=12)
voice_button.pack(side=tk.LEFT, padx=20, pady=10)

exit_button = tk.Button(root, text="Çıkış", font=("Arial", 12), command=root.quit, bg="#f44336", fg="white",
                        relief="raised", width=10)
exit_button.pack(side=tk.RIGHT, padx=20, pady=10)

root.mainloop()
