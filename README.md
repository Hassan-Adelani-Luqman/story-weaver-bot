# Story Weaver ✨ - Enchanted Storytelling Bot

A magical storytelling chatbot that weaves unique tales based on your imagination, featuring an enchanted library dreamscape UI with animated backgrounds, glowing elements, and AI-powered story generation.

## 🌟 Features

### ✨ Core Functionality
- **AI-Powered Story Generation**: Uses Google Gemini API to create unique, engaging stories
- **Visual Companions**: Integrates Unsplash API to find relevant images for your stories
- **Mood-Based Stories**: Choose from Fantasy, Sci-Fi, Mystery, Adventure, or Romance themes
- **Story Archive**: Save and revisit your favorite generated stories
- **Random Prompt Generator**: Get inspired with creative story prompts

### 🎨 Enchanted UI Features
- **Animated Starry Background**: Twinkling stars and shooting stars create a magical atmosphere
- **Floating Magical Elements**: Wizards, crystal balls, scrolls, and candles float across the screen
- **Split-Screen Interface**: Spellbook-style input panel and scroll-style story display
- **Glowing Interactive Elements**: Buttons and inputs glow with magical effects
- **Typewriter Story Display**: Stories appear with a live writing animation
- **Theme Toggle**: Switch between dark starlight and light daydream themes
- **Mobile Responsive**: Optimized for both desktop and mobile devices

### 🔮 Interactive Elements
- **Mood Picker**: Visual genre selection with animated icons
- **Story Actions**: Regenerate stories, get images, and save to archive
- **Sidebar Features**: Quick access to archive and theme settings
- **Keyboard Shortcuts**: Ctrl+Enter to generate stories quickly

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or newer
- Google Gemini API key
- Unsplash API access key

### 1. Get Your API Keys

#### Google Gemini API Key:
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" → "Create API key in new project"
4. Copy your API key

#### Unsplash API Key:
1. Go to [Unsplash Developers](https://unsplash.com/developers)
2. Register/Login to your account
3. Create a "New Application"
4. Accept the API Guidelines
5. Copy your "Access Key"

### 2. Setup the Project

```bash
# Clone or download the project
mkdir story_weaver_bot
cd story_weaver_bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY="your_google_gemini_api_key_here"
UNSPLASH_ACCESS_KEY="your_unsplash_access_key_here"
```

**⚠️ Important**: Never commit your `.env` file to version control!

### 4. Run the Application

```bash
python app.py
```

Open your browser and navigate to: `http://127.0.0.1:5000`

## 🎮 How to Use

### Basic Story Generation
1. **Choose Your Mood**: Select from Fantasy, Sci-Fi, Mystery, Adventure, or Romance
2. **Enter Your Prompt**: Describe what kind of story you want
3. **Click "Weave Story"**: Watch as your tale unfolds with typewriter animation
4. **Get Visual Companion**: Click "Get Image" to find a relevant photo
5. **Save to Archive**: Stories are automatically saved for later viewing

### Advanced Features
- **Random Prompts**: Click the dice button for creative inspiration
- **Story Archive**: Access your collection via the bookshelf icon
- **Theme Toggle**: Switch between dark and light themes
- **Regenerate**: Create variations of the same prompt
- **Keyboard Shortcut**: Use Ctrl+Enter in the text area for quick generation

## 🛠️ Technical Details

### Backend (Flask)
- **Framework**: Flask with CORS support
- **APIs**: Google Gemini Pro for text generation, Unsplash for images
- **Features**: Story archiving, random prompts, mood-based generation
- **Storage**: In-memory (for demo purposes)

### Frontend
- **Pure HTML/CSS/JavaScript**: No frameworks for maximum compatibility
- **Animations**: CSS keyframes and transitions
- **Responsive Design**: Mobile-first approach
- **Typography**: Google Fonts (Cinzel, Dancing Script, Crimson Text)

### Project Structure
```
story_weaver_bot/
├── app.py                 # Flask backend application
├── templates/
│   └── index.html        # Frontend with enchanted UI
├── .env                  # API keys (create this)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🎨 UI Theme Details

The interface evokes an **enchanted library in a dreamscape** with:

- **Color Palette**: Deep purples, midnight blues, gold accents, soft pastels
- **Typography**: Serif fonts for elegance, script fonts for magic
- **Animations**: Floating elements, twinkling stars, glowing effects
- **Layout**: Split-screen spellbook and scroll design
- **Interactions**: Hover effects, smooth transitions, magical feedback

## 🔧 Customization

### Adding New Moods
Edit the `mood_prompts` dictionary in `app.py` and add corresponding UI elements in `index.html`.

### Changing Visual Elements
Modify the `createFloatingElements()` function to add different magical symbols.

### Extending Story Archive
Replace in-memory storage with a database (SQLite, PostgreSQL, etc.) for persistence.

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Production Deployment
Use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Example Prompts

Try these magical prompts:
- "A detective cat solving mysteries in Paris"
- "A journey through time in a pocket watch"
- "A dragon who's afraid of flying"
- "A wizard's apprentice who can only cast spells backwards"
- "A space station where gravity works in reverse"
- "A library where books come alive at midnight"

## 🐛 Troubleshooting

### Common Issues

**API Key Errors**:
- Ensure your `.env` file is in the project root
- Check that API keys are correctly formatted
- Verify API keys are active and have proper permissions

**Import Errors**:
- Activate your virtual environment
- Install all requirements: `pip install -r requirements.txt`

**UI Not Loading**:
- Check browser console for JavaScript errors
- Ensure Flask is running on the correct port
- Try refreshing the page or clearing browser cache

## 🤝 Contributing

This is a demo project for the monthly challenge. Feel free to fork and enhance with:
- Database integration for persistent storage
- User authentication and personal archives
- Advanced story customization options
- Audio narration features
- PDF export functionality

## 📄 License

This project is created for educational and demonstration purposes. Please respect the terms of service for Google Gemini API and Unsplash API when using their services.

## 🎯 Monthly Challenge Submission

**What it does**: Story Weaver is a magical storytelling bot that generates unique stories based on user prompts, with mood selection and visual companions.

**Tech used**: 
- Backend: Python, Flask, Google Gemini API, Unsplash API
- Frontend: HTML, CSS, JavaScript with enchanted library theme
- Features: AI story generation, image integration, story archiving

**Key Features**:
- ✨ AI-powered story generation with mood selection
- 🎨 Enchanted library dreamscape UI with animations
- 📚 Story archive and random prompt generator
- 🖼️ Visual story companions via Unsplash API
- 📱 Fully responsive design

---

*Where your ideas become stories* ✨

