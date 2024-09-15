    
import fitz
import string, random, os, json, requests
from dotenv import load_dotenv

load_dotenv()


sample_urls = [
    "https://collegeessay.org/blog/500-word-essay/500-word-essay-on-environment.pdf",
    "https://watermark.silverchair.com/hcy241.pdf?token=AQECAHi208BE49Ooan9kkhW_Ercy7Dm3ZL_9Cf3qfKAc485ysgAAA1QwggNQBgkqhkiG9w0BBwagggNBMIIDPQIBADCCAzYGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMhRdWAfHMnDxhUFqWAgEQgIIDB4kFLE04NHZb3TEhEZddkWlX83NR29oIs55CDuvdv797SnQZN9QnYJ7lHSGYDa2FtTKfQi_ps4qUmRH0xcLf9zH2p6_l1_hzvxSq3bd9uHIC1C0WI_L_vPlDBzD8n7qMoZtUZjCd95DBHPbehNv55QaF-kx2f8hnEaSBNrTt86WabcaBd-bCdqFrAzXSmaT9BlE_jY56mbtzja_AOBDHgCEljHJxLYfI_fviqsO4UjkW5cPsTKPZLxGNAf7dssrser5csu7YWXlTAOI1RLNulUqNqK6phGjgyXkg8vxzrn86XAHpvleCayLAzo_Doxt3kWCgeuWjKzARQYhsW6yTY6yHJpWCXl2cpJUKPRN0-DraNbsGWKW_pKAsUMA-1cx0rn7Z1x6NkGk-saIQgVqm0NVfYRPPTnvj1j6XOS3Ex7O4VEfFtDPj2zlEP1m-QLi36ut6subyhH1ERcEccMntHxHF7B3d-VSlr-X2bl9P6OaWM72X_GF5hsC4lKCQTVNMBAktsDaXQSbOthv1BHlAx0t9cotQ7iL5Jkx3Q6e0PyurPPHqoNc5W1eklu4dgRFCiBQBrevgcytb7VBfd6L7_ZfO22_JPygclXUUmjZIJRS5zUoy-6PLxOuCmkJqqHaDm5M8AjhD_AXLGVPq1zgN51WiKu9ILw1LHzZoBjDTT5v4PcQWfG66sEOwBEQHZ2ngSuKiFA7X2U6xX7pPW3Wwd6ASAsrx6gJVKQMbKHAqVP5SenekGk3QlYZEyBz5sd5sFGert6h8bcm1Pfd7wVEQCKIuB0OvIQFWqI9SS43yrXWN2JfQ2VbO46FZPHBSpHqyrP48-kh9G9YMZvXHzlJ7139m_6JnPO-JERV-DPzdQEZfW3jdPXsUmekJu9y1XyFEamVoM79zG0S3bjjj4u-aEV_N-itFwVeHUFsMU7J6S4MarBSETDXqV7vkCB7swwrHIXIe1hkcUMy1vV3Nwt_841WQ6lAqED3M5t0a-Yt8aRoi8rW54F-l7GKrFWzzgYPtpYe24obo1SA"
]

def gemini_request( prompt):
    try:
        print("summarizing the text")
        api_key     =os.getenv('GEMINI_API_KEY')        

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 1,
                "topK": 64,
                "topP": 0.95,
                "maxOutputTokens": 8192,
                "responseMimeType": "application/json"
            }

        }

        headers     = {"Content-Type": "application/json"}
        response    = requests.post(url, json=payload, headers=headers)
        response    = response.json()

        data = response.get('candidates')[0].get('content').get('parts')[0].get('text').strip()

        final_response = clean_and_format_response(data) or {}

        return final_response
    except Exception as e:
        print("Exception in geminie:", e ,flush= True)
        return {"error": str(e)}
    

def clean_and_format_response(response):
    try:
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_str = response[json_start:json_end]
        return json.loads(json_str)
    except (json.JSONDecodeError, ValueError) as e:
        print("Error decoding JSON:", e ,flush= True)
        return None



def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str    


def extract_text_from_pdf(url):

    print("Started extracting data from pdf file", flush=True),
    try:
        text        = ""
        response    = requests.get(url)
        path        = f"pdf_file_{get_random_string(10)}.pdf"

        with open(path, "wb") as file:
            file.write(response.content)

        doc = fitz.open(path)
        for page in doc:
            text+=page.get_text()

        print("Data extracted from pdf file successfully", flush=True)
    except Exception as e:
        pass


    try:
        doc.close()
        os.remove(path)
    except Exception as e:
        print(e)
        pass

    return text



ocr_data = extract_text_from_pdf("https://collegeessay.org/blog/500-word-essay/500-word-essay-on-environment.pdf")

print(ocr_data)

print(gemini_request(f"""
    Summarize the text in just 2 paragraphs in easy english , also give me a single line title of the document
    {ocr_data}
    
    """
))