import googleapiclient.discovery
from google import genai
from google.genai import types

# --- Configuration ---
PROJECT_ID = "your-project-id"
LOCATION = "us-central1"
YOUTUBE_API_KEY = 'your-yt-api-key'
MODEL_ID = "gemini-3.1-pro-preview" # Or gemini-3.1-flash-lite-preview

# Initialize the YouTube Service
service = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Initialize the Gen AI Client for Vertex AI
client = genai.Client(
    vertexai=True, 
    project=PROJECT_ID, 
    location=LOCATION
)

def youtube_search(query):
    # Perform the search
    request = service.search().list(
        q=query,
        relevanceLanguage='en',
        part='snippet',
        maxResults=2, # modify this to get any number of results needeed
        publishedAfter='2024-11-10T00:00:00Z' # this can be used to get only new videos
    )
    return request.execute()

def generate(yt_link):
    # Prompt logic
    prompt_text = """Go through the review and provide a summary and overall sentiment 
    of the product in question in a single phrase, Positive, Negative, Neutral. 
    Identify the product as well. Return these values in json format."""
    
    # Create the video part using the new SDK's Part class
    video_part = types.Part.from_uri(
        file_uri=yt_link,
        mime_type="video/mp4" # Explicitly setting mime_type is recommended
    )

    # Generate content using the 3.1 model
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt_text, video_part],
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            temperature=1.0,
        )
    )

    return response.text
