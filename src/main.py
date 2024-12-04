import argparse
from .speech2text import SpeechToText
from .text2speech import TextToSpeech
from .keyword_search import KeywordSearch
from .utils import get_response


def main():
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='Process audio file for speech recognition and response.')
    parser.add_argument('audio_file', type=str, help='Path to the input audio file (WAV format)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize components
    stt = SpeechToText()
    tts = TextToSpeech()
    keyword_search = KeywordSearch()

    try:
        # Speech to text
        transcription = stt.transcribe_audio(args.audio_file)
        
        if transcription:
            print("\nTranscription:", transcription)
            
            # Analyze the transcribed text
            intent = keyword_search.search(transcription)
            print("\nDetected Categories:", intent['categories'])
            print("Confidence Scores:", [f"{score:.2f}" for score in intent['confidences']])

            # Generate response
            response_text = get_response(intent)
            print("\nResponse:", response_text)
            
            # Convert response to speech
            response_audio = tts.convert_to_speech(response_text)
            if response_audio:
                print(f"\nResponse audio saved to: {response_audio}")
            else:
                print("\nFailed to generate speech response")
        else:
            print("\nTranscription failed")
            
    except FileNotFoundError:
        print(f"\nError: Audio file '{args.audio_file}' not found")
    except Exception as e:
        print(f"\nError processing audio: {str(e)}")

if __name__ == "__main__":
    main()