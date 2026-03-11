import mss
from PIL import Image
import time
import pyttsx3
import io
import ollama  

# Voice engine initialization
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 

# Captures the screen and resizes the image
def take_screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img.thumbnail((768, 768)) 
        return img

# Sends image to AI and plays the received text as speech
def analyze_speak(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()

    try:
        print("Analyzing screen locally...")
        response = ollama.chat(
            model='moondream',
            messages=[{
                'role': 'user',
                'content': 'What do you see on the screen? Describe it briefly and with a touch of irony.',
                'images': [img_bytes]
            }]
        )
        
        text = response['message']['content']
        print(f"AI: {text}")
        
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"Local analysis error: {e}")

print("Local bot started.")
print("Press Ctrl+C to exit.")

# Main loop: captures screen and calls analysis every 15 seconds
try:
    while True:
        current_img = take_screenshot()
        analyze_speak(current_img)
        print("Waiting 15 seconds before the next snapshot...")
        time.sleep(15)
except KeyboardInterrupt:
    print("\nBot stopped by user.")
