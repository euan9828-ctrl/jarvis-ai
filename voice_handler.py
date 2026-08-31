import speech_recognition as sr
import pyttsx3
from config import CONFIG
import logging

logger = logging.getLogger(__name__)

class VoiceHandler:
    def __init__(self):
        """Initialize speech recognition and text-to-speech engines"""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure text-to-speech
        self.engine.setProperty('rate', CONFIG['VOICE_RATE'])
        self.engine.setProperty('volume', CONFIG['VOICE_VOLUME'])
        
        # Set voice (optional: select female or male voice)
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
    
    def listen(self):
        """Listen for voice input from microphone"""
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=CONFIG['LISTENING_TIMEOUT'])
                
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language=CONFIG['LANGUAGE'])
            print(f"✓ You said: {text}")
            return text.lower()
        
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that. Could you repeat?")
            return None
        except sr.RequestError as e:
            self.speak(f"Sorry, there was an error with the speech recognition service: {e}")
            logger.error(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in listen: {e}")
            return None
    
    def speak(self, text):
        """Convert text to speech and play it"""
        try:
            print(f"🤖 JARVIS: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            print(f"Error speaking: {e}")
    
    def wait_for_wake_word(self):
        """Listen for wake word to activate JARVIS"""
        print(f"👂 Waiting for wake word '{CONFIG['WAKE_WORD']}'...")
        while True:
            try:
                heard = self.listen()
                if heard and CONFIG['WAKE_WORD'] in heard:
                    self.speak(f"Yes, I'm here. How can I help?")
                    return True
            except Exception as e:
                logger.error(f"Error waiting for wake word: {e}")
                continue