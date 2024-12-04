import os
import requests


class SpeechToText:
    def __init__(self, region="eastus"):
        self.api_key = os.getenv("AZURE_SPEECH_API_KEY")
        self.region = region
        self.speech_to_text_url = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"

    def transcribe_audio(self, audio_file_path):
        # Setup request headers
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'audio/wav',
        }

        try:
            # Read audio file in binary mode
            with open(audio_file_path, 'rb') as audio_file:
                # Send POST request to Azure
                response = requests.post(
                    self.speech_to_text_url,
                    headers=headers,
                    data=audio_file,
                    params={
                        'language': 'en-US',
                        'format': 'detailed'
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['DisplayText']
                else:
                    print(f"Error: {response.status_code}")
                    print(response.text)
                    return None
                    
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            return None