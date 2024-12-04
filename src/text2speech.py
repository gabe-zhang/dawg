import os
import requests


class TextToSpeech:
    def __init__(self, region="eastus"):
        self.api_key = os.getenv("AZURE_SPEECH_API_KEY")
        self.region = region
        self.text_to_speech_url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"

    def convert_to_speech(self, text, voice_name="en-US-GuyNeural", output_file_path="output.wav"):
        # Setup request headers
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm'
        }

        # Construct SSML request body with voice customization
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
            <voice name='{voice_name}'>
                {text}
            </voice>
        </speak>
        """

        try:
            # Send POST request to Azure
            response = requests.post(
                self.text_to_speech_url,
                headers=headers,
                data=ssml.encode('utf-8')
            )

            if response.status_code == 200:
                # Save the audio content to a file
                with open(output_file_path, 'wb') as audio_file:
                    audio_file.write(response.content)
                print(f"Audio file saved as {output_file_path}")
                return output_file_path
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                return False

        except Exception as e:
            print(f"Error during text-to-speech conversion: {str(e)}")

# Example usage
if __name__ == "__main__":
    tts = TextToSpeech()
    text_to_convert = "Sup dawg, I am your AI-powered home buddy. Feel free to ask me about the room lighting, humidity and temperature."
    tts.convert_to_speech(
        text_to_convert,
        voice_name="en-US-GuyNeural",
        output_file_path="data/sup_dawg.wav"
    )