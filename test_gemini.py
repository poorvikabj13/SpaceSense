import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO

# Configure API
API_KEY = "AIzaSyDa4WbSnt3Ji5L_Zznp-gLjqWa5DLGPEhM"
genai.configure(api_key=API_KEY)

# Test with a simple image
print("Testing Gemini API...")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    
    response = model.generate_content(["What color is this image?", img])
    print(f"✅ Success! Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")
