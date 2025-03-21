import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

SPEECH_KEY = os.getenv("SPEECH_KEY")
SERVICE_REGION = os.getenv("SPEECH_SERVICE_REGION")

def realtime_api_from_mic():
  speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)

  speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="ja-JP")

  print("Say something...")
  result = speech_recognizer.recognize_once()

  if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))


def realtime_api_from_file():
  speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)

  audio_input = speechsdk.AudioConfig(filename="sample.wav")
  speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input, language="ja-JP")

  print("Generating transcript...")
  result = speech_recognizer.recognize_once()

  if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))


def realtime_api_continuos():
  speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)

  speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="ja-JP")

  done = False

  # Define Callbacks
  def recognizing_callback(evt):
    print(f"Recognizing: {evt}")

  def recognized_callback(evt):
    print(f"Recognized: {evt}")

  def session_stopped_callback(evt):
    print(f"Session stopped: {evt}")
    nonlocal done
    done = True

  # Add Callbacks
  speech_recognizer.recognizing.connect(recognizing_callback)
  speech_recognizer.recognized.connect(recognized_callback)
  speech_recognizer.session_stopped.connect(session_stopped_callback)
  speech_recognizer.canceled.connect(session_stopped_callback)

  result = speech_recognizer.start_continuous_recognition_async()

  result.get()
  print('Continuous Recognition is now running, say something.')

  while not done:
    print('type "stop" to exit')
    stop = input()
    if (stop.lower() == "stop"):
      print('Stopping async recognition.')
      speech_recognizer.stop_continuous_recognition_async()
      break
      

if __name__ == "__main__":
  realtime_api_from_mic()
  #realtime_api_from_file()
  #realtime_api_continuos()
  