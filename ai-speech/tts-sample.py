import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

SPEECH_KEY = os.getenv("SPEECH_KEY")
SERVICE_REGION = os.getenv("SPEECH_SERVICE_REGION")

def synthesize_to_speaker(text: str):
  speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
  speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

  result = speech_synthesizer.speak_text_async(text).get()
  
  if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized to speaker.")
  else:
    print(f"Speech synthesis canceled: {result.cancellation_details.reason}")


def synthesize_with_voice(text: str, voice: str):
  speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
  speech_config.speech_synthesis_voice_name = voice
  speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

  result = speech_synthesizer.speak_text_async(text).get()
  
  if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print(f"Speech synthesized with voice [{voice}].")
  else:
    print(f"Speech synthesis canceled: {result.cancellation_details.reason}")


def synthesize_with_ssml(ssml: str):    
  speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
  speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
  
  result = speech_synthesizer.speak_ssml_async(ssml).get()
  
  if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized from SSML.")
  else:
    print(f"Speech synthesis canceled: {result.cancellation_details.reason}")


if __name__ == "__main__":
    text = "Hello, this is a sample text to speech conversion."
    ssml = """
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name='en-US-JennyNeural'>
            <prosody rate='-10.00%' pitch='+5.00%'>
                Hello, this is a sample text to speech conversion using SSML.
            </prosody>
        </voice>
    </speak>
    """

    synthesize_to_speaker(text)
    # synthesize_with_voice(text, "en-US-JennyNeural")
    # synthesize_with_ssml(ssml)