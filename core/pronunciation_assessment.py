import azure.cognitiveservices.speech as speechsdk
from config.settings import MICROSOFT_API_KEY, MICROSOFT_REGION, LANGUAGE
from core.scoring import calculate_scores
from utils.preprocess import convert_audio
import json
import time
import wave
import os

def check_audio_format(audio_file):
    with wave.open(audio_file, 'rb') as audio:
        return audio.getnchannels() == 1 and audio.getsampwidth() == 2 and audio.getframerate() == 16000

def run_pronunciation_assessment(audio_file, target_word):
    try:
        # Check if the audio file is in the correct format
        if not check_audio_format(audio_file):
            # Convert the audio file if it's not in the correct format
            converted_file = "converted_audio.wav"
            convert_audio(audio_file, converted_file)
            audio_file = converted_file
        
        speech_config = speechsdk.SpeechConfig(subscription=MICROSOFT_API_KEY, region=MICROSOFT_REGION)
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)

        pronunciation_config = speechsdk.PronunciationAssessmentConfig(
            reference_text=target_word,
            grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
            granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
            enable_miscue=True
        )
        pronunciation_config.enable_prosody_assessment()

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=LANGUAGE, audio_config=audio_config)
        pronunciation_config.apply_to(speech_recognizer)

        recognized_words = []
        fluency_scores = []
        prosody_scores = []
        durations = []

        def recognized(evt):
            print(f"Recognized Text: {evt.result.text}")
            pronunciation_result = speechsdk.PronunciationAssessmentResult(evt.result)
            recognized_words.extend(pronunciation_result.words)
            fluency_scores.append(pronunciation_result.fluency_score)
            prosody_scores.append(pronunciation_result.prosody_score)
            json_result = evt.result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
            jo = json.loads(json_result)
            nb = jo['NBest'][0]
            durations.append(sum([int(w['Duration']) for w in nb['Words']]))


        done = False
        def stop_cb(evt):
            nonlocal done
            done = True

        speech_recognizer.recognized.connect(recognized)
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)
        
        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)
        speech_recognizer.stop_continuous_recognition()

        if not recognized_words:
            raise ValueError("No words recognized")

        return calculate_scores(recognized_words, fluency_scores, durations, prosody_scores)
    except Exception as e:
        print(f"Error in run_pronunciation_assessment: {e}")
        raise