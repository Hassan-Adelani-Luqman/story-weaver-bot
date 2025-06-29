import os
import requests
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
import time

# Load environment variables from .env file
load_dotenv()

# Check if AI should be disabled (for testing or memory issues)
USE_AI = os.getenv("USE_AI", "true").lower() == "true"

# Configure the Google Gemini API
if USE_AI:
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # Don't load the model at startup - we'll load it when needed
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        print("Please ensure GOOGLE_API_KEY is set correctly in your .env file.")
        USE_AI = False  # Fallback to non-AI mode

# Get Unsplash Access Key
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
if not UNSPLASH_ACCESS_KEY:
    print("Error: UNSPLASH_ACCESS_KEY not found in .env file.")
    exit(1)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for stories (in production, use a database)
story_archive = []

# Global variable to store the model (lazy loading)
_gemini_model = None

def get_gemini_model():
    """Get or create the Gemini model instance (lazy loading)."""
    global _gemini_model
    if _gemini_model is None:
        try:
            # Get model from environment variable, default to flash for memory efficiency
            model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
            print(f"Loading Gemini model: {model_name}")
            _gemini_model = genai.GenerativeModel(model_name)
            print("Gemini model loaded successfully")
        except Exception as e:
            print(f"Error creating Gemini model: {e}")
            raise
    return _gemini_model

def cleanup_model():
    """Clean up the model to free memory."""
    global _gemini_model
    if _gemini_model is not None:
        _gemini_model = None
        import gc
        gc.collect()
        print("Model cleaned up and memory freed")

def generate_with_gemini(prompt, max_retries=3):
    """Generate content with retry logic and better error handling."""
    for attempt in range(max_retries):
        try:
            model = get_gemini_model()
            response = model.generate_content(prompt)
            result = response.text
            
            # Clean up after each generation to free memory
            cleanup_model()
            
            return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            cleanup_model()  # Clean up on error too
            if attempt == max_retries - 1:
                raise
            # Wait a bit before retrying
            time.sleep(2)  # Increased wait time
    return None

def generate_fallback_story(prompt, mood):
    """Generate a simple fallback story if Gemini fails."""
    fallback_stories = {
        'fantasy': f"Once upon a time, in a realm where magic flowed like rivers, there lived a brave soul who embarked on a quest about {prompt}. Through enchanted forests and mystical mountains, they discovered that the greatest magic was the power of friendship and determination. Their journey taught them that even the smallest acts of courage could change the world forever.",
        'scifi': f"In the year 2157, aboard the starship Nebula, Commander Sarah Chen faced an unprecedented challenge: {prompt}. With advanced AI companions and cutting-edge technology, she navigated through quantum anomalies and discovered that the future of humanity depended on understanding the past. The mission would test not just her skills, but her very understanding of reality itself.",
        'mystery': f"Detective Marcus Blackwood stared at the cryptic message on his desk. The case was unlike any he'd seen before: {prompt}. With his trusty magnifying glass and sharp intuition, he followed the clues through foggy streets and hidden passages. Every shadow held a secret, every whisper a clue. The truth was closer than he imagined.",
        'adventure': f"Deep in the heart of the Amazon rainforest, explorer Dr. Elena Rodriguez discovered something extraordinary: {prompt}. Armed with nothing but her wits and a backpack of supplies, she ventured into uncharted territory. Through raging rivers and ancient ruins, she uncovered secrets that would rewrite history books.",
        'romance': f"In a charming little bookstore on a rainy afternoon, Emma and James found themselves drawn together by a shared love of stories. Their connection deepened as they explored the mystery of {prompt}. Through stolen glances and whispered conversations, they discovered that sometimes the greatest love stories are the ones we write ourselves."
    }
    
    return fallback_stories.get(mood, f"Once upon a time, there was a remarkable story about {prompt}. It was a tale of courage, friendship, and discovery that would be remembered for generations to come.")

# Random prompt suggestions
RANDOM_PROMPTS = [
    "A detective cat solving mysteries in Paris",
    "A journey through time in a pocket watch",
    "A dragon who's afraid of flying",
    "A wizard's apprentice who can only cast spells backwards",
    "A space station where gravity works in reverse",
    "A library where books come alive at midnight",
    "A baker who discovers their sourdough starter is sentient",
    "A lighthouse keeper who receives messages from the future",
    "A garden where each flower holds a different memory",
    "A clockmaker who builds timepieces that show alternate realities",
    "A musician whose melodies can heal broken hearts",
    "A cartographer mapping dreams instead of lands",
    "A seamstress who weaves stories into fabric",
    "A meteorologist who predicts emotions instead of weather",
    "A janitor at a superhero headquarters",
    "A ghost who's terrible at being scary",
    "A robot learning to paint watercolors",
    "A mermaid who collects vintage postcards",
    "A vampire who runs a 24-hour flower shop",
    "A time traveler stuck in a coffee shop loop"
]

def get_unsplash_image(query):
    """Fetches a relevant image from Unsplash based on a query."""
    unsplash_api_url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": UNSPLASH_ACCESS_KEY,
        "per_page": 1,
        "orientation": "landscape"
    }
    try:
        response = requests.get(unsplash_api_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data and data['results']:
            return {
                'url': data['results'][0]['urls']['regular'],
                'alt': data['results'][0]['alt_description'] or 'Story illustration',
                'photographer': data['results'][0]['user']['name'],
                'photographer_url': data['results'][0]['user']['links']['html']
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from Unsplash: {e}")
        return None

def extract_story_keywords(story_text):
    """Extract keywords from the story for image search."""
    # Simple keyword extraction - take first sentence and remove common words
    first_sentence = story_text.split('.')[0].strip()
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
    words = [word.lower().strip('.,!?;:"()[]') for word in first_sentence.split()]
    keywords = [word for word in words if word not in common_words and len(word) > 2]
    return ' '.join(keywords[:3])  # Use top 3 keywords

@app.route('/')
def index():
    """Serves the main HTML page for the chatbot."""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'stories_count': len(story_archive)
    })

@app.route('/generate_story', methods=['POST'])
def generate_story():
    """Handles the story generation request from the frontend."""
    data = request.json
    user_prompt = data.get('prompt')
    mood = data.get('mood', 'fantasy')  # Default to fantasy

    if not user_prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        # Enhance prompt based on mood
        mood_prompts = {
            'fantasy': f"Write a magical fantasy story about: {user_prompt}. Include enchanting elements, mystical creatures, or magical powers.",
            'scifi': f"Write a science fiction story about: {user_prompt}. Include futuristic technology, space exploration, or scientific concepts.",
            'mystery': f"Write a mystery story about: {user_prompt}. Include suspense, clues, and an intriguing puzzle to solve.",
            'adventure': f"Write an adventure story about: {user_prompt}. Include exciting journeys, challenges, and discoveries.",
            'romance': f"Write a romantic story about: {user_prompt}. Include emotional connections, relationships, and heartwarming moments."
        }
        
        enhanced_prompt = mood_prompts.get(mood, f"Write an engaging story about: {user_prompt}")
        enhanced_prompt += " Keep the story between 200-400 words, with vivid descriptions and engaging characters."

        # Try to generate content using the Gemini model
        if USE_AI:
            try:
                generated_text = generate_with_gemini(enhanced_prompt)
                if not generated_text:
                    raise Exception("No response from Gemini")
            except Exception as gemini_error:
                print(f"Gemini failed, using fallback: {gemini_error}")
                generated_text = generate_fallback_story(user_prompt, mood)
        else:
            # Use fallback stories when AI is disabled
            generated_text = generate_fallback_story(user_prompt, mood)

        # Generate a title for the story
        if USE_AI:
            try:
                title_prompt = f"Generate a creative, engaging title for this story in 5 words or less: {generated_text[:100]}..."
                story_title = generate_with_gemini(title_prompt)
                if story_title:
                    story_title = story_title.strip().strip('"\'')
                else:
                    story_title = "Untitled Story"
            except Exception as title_error:
                print(f"Title generation failed: {title_error}")
                story_title = f"{mood.title()} Adventure"
        else:
            # Use simple title when AI is disabled
            story_title = f"{mood.title()} Adventure"

        # Create story object
        story_data = {
            'id': len(story_archive) + 1,
            'title': story_title,
            'content': generated_text,
            'prompt': user_prompt,
            'mood': mood,
            'timestamp': datetime.now().isoformat(),
            'image': None
        }

        # Add to archive
        story_archive.append(story_data)

        return jsonify({
            'story': generated_text,
            'title': story_title,
            'story_id': story_data['id']
        })

    except Exception as e:
        print(f"Error generating story: {e}")
        return jsonify({'error': 'Failed to generate story. Please try again.'}), 500

@app.route('/get_image/<int:story_id>', methods=['POST'])
def get_story_image(story_id):
    """Fetches an image for a specific story."""
    try:
        # Find the story
        story = next((s for s in story_archive if s['id'] == story_id), None)
        if not story:
            return jsonify({'error': 'Story not found'}), 404

        # Extract keywords for image search
        image_query = extract_story_keywords(story['content'])
        if not image_query:
            image_query = story['prompt'][:50]

        image_data = get_unsplash_image(image_query)
        
        if image_data:
            # Update story with image data
            story['image'] = image_data
            return jsonify({'image': image_data})
        else:
            return jsonify({'error': 'No suitable image found'}), 404

    except Exception as e:
        print(f"Error fetching image: {e}")
        return jsonify({'error': 'Failed to fetch image. Please try again.'}), 500

@app.route('/random_prompt', methods=['GET'])
def get_random_prompt():
    """Returns a random story prompt."""
    prompt = random.choice(RANDOM_PROMPTS)
    return jsonify({'prompt': prompt})

@app.route('/story_archive', methods=['GET'])
def get_story_archive():
    """Returns the story archive."""
    # Return stories in reverse chronological order (newest first)
    return jsonify({'stories': list(reversed(story_archive))})

@app.route('/story/<int:story_id>', methods=['GET'])
def get_story(story_id):
    """Returns a specific story by ID."""
    story = next((s for s in story_archive if s['id'] == story_id), None)
    if story:
        return jsonify({'story': story})
    else:
        return jsonify({'error': 'Story not found'}), 404

if __name__ == '__main__':
    # Configure for production deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)

