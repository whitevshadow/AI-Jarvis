# Enhanced JARVIS with Web UI and DeepSeek-R1 Integration

An advanced AI assistant with a modern web interface and enhanced decision-making capabilities powered by DeepSeek-R1 via Ollama.

## 🚀 Features

### Web Interface
- **Modern UI**: Sleek, Iron Man-inspired design with animations
- **Voice Recognition**: Browser-based speech recognition
- **Real-time Chat**: WebSocket-powered communication
- **Voice Synthesis**: Text-to-speech responses
- **Responsive Design**: Works on desktop and mobile devices

### AI Capabilities
- **DeepSeek-R1 Integration**: Advanced reasoning and decision making
- **Context Awareness**: Maintains conversation history
- **Intent Classification**: Understands user intentions
- **Action Extraction**: Identifies actionable commands
- **Fallback System**: Works even when AI is offline

### System Integration
- **Python Backend**: Integrates with existing JARVIS modules
- **System Commands**: Execute OS-level operations
- **Web Search**: Automated search capabilities
- **Application Control**: Launch and manage applications

## 🛠️ Installation

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Ollama (for AI capabilities)

### Quick Setup

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Set up Ollama and DeepSeek-R1**
   ```bash
   # Install Ollama (visit https://ollama.ai for instructions)
   # Then run the setup script
   python ai-integration/ollama-setup.py
   ```

3. **Start the Application**
   ```bash
   npm run dev
   ```

4. **Access the Interface**
   - Web UI: http://localhost:3000
   - API Server: http://localhost:3001

## 🔧 Configuration

### Ollama Setup
The enhanced JARVIS uses Ollama to run the DeepSeek-R1 model locally:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull DeepSeek-R1 model
ollama pull deepseek-r1

# Start Ollama service
ollama serve
```

### Environment Variables
Create a `.env` file in the root directory:

```env
OLLAMA_URL=http://localhost:11434
MODEL_NAME=deepseek-r1
PORT=3001
```

## 🎯 Usage

### Web Interface
1. Open http://localhost:3000 in your browser
2. Use the microphone button for voice input
3. Type commands in the chat interface
4. Use quick action buttons for common tasks

### Voice Commands
- "Take a screenshot"
- "What's the weather like?"
- "Play some music"
- "Get the latest news"
- "What time is it?"
- "Lock the screen"

### System Integration
The web interface communicates with your existing Python JARVIS modules:

```python
# Example: Using the enhanced brain
from ai_integration.enhanced_brain import EnhancedBrain

brain = EnhancedBrain()
response = brain.generate_response("Hello JARVIS")
print(response['response'])
```

## 🏗️ Architecture

### Frontend (Web UI)
- **Vite**: Fast development and building
- **Vanilla JavaScript**: No framework dependencies
- **WebSocket**: Real-time communication
- **Web APIs**: Speech recognition and synthesis

### Backend (Node.js)
- **Express**: Web server and API
- **WebSocket**: Real-time communication
- **Ollama Integration**: AI model communication
- **Python Bridge**: Execute existing JARVIS functions

### AI Engine
- **DeepSeek-R1**: Advanced reasoning model
- **Ollama**: Local model hosting
- **Context Management**: Conversation history
- **Action Extraction**: Command identification

## 📁 Project Structure

```
enhanced-jarvis/
├── src/                    # Frontend source code
│   ├── js/                # JavaScript modules
│   ├── styles/            # CSS styles
│   └── main.js           # Main application
├── ai-integration/        # AI enhancement modules
│   ├── enhanced-brain.py  # Enhanced decision engine
│   └── ollama-setup.py   # Setup automation
├── server.js             # Node.js backend server
├── package.json          # Dependencies and scripts
└── vite.config.js        # Build configuration
```

## 🔌 API Endpoints

### REST API
- `GET /health` - System health check
- `POST /api/chat` - Process chat messages
- `GET /api/model/info` - Model information

### WebSocket Events
- `system_command` - Execute system commands
- `open_app` - Launch applications
- `response` - AI responses

## 🎨 Customization

### Themes
Modify CSS variables in `src/styles/main.css`:

```css
:root {
    --primary-blue: #00d4ff;
    --secondary-blue: #0099cc;
    --accent-gold: #ffd700;
    /* ... */
}
```

### AI Behavior
Customize the AI personality in `ai-integration/enhanced-brain.py`:

```python
def build_system_prompt(self, context: Dict = None) -> str:
    base_prompt = """You are J.A.R.V.I.S..."""
    # Modify the system prompt here
    return base_prompt
```

## 🔍 Troubleshooting

### Common Issues

1. **Ollama not connecting**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Start Ollama if needed
   ollama serve
   ```

2. **Model not found**
   ```bash
   # Pull the DeepSeek-R1 model
   ollama pull deepseek-r1
   ```

3. **Voice recognition not working**
   - Ensure you're using HTTPS or localhost
   - Check browser permissions for microphone access
   - Try a different browser (Chrome recommended)

4. **Python integration issues**
   - Ensure Python path is correct in server.js
   - Check that all Python dependencies are installed
   - Verify file paths for existing JARVIS modules

## 🚀 Performance Optimization

### AI Response Speed
- Use GPU acceleration with Ollama if available
- Adjust model parameters for faster responses
- Implement response caching for common queries

### Web Interface
- Enable gzip compression
- Optimize animations for lower-end devices
- Implement lazy loading for components

## 🔒 Security Considerations

- **Local AI**: DeepSeek-R1 runs locally via Ollama
- **No Data Transmission**: Conversations stay on your device
- **System Access**: Be cautious with system command permissions
- **HTTPS**: Use HTTPS in production environments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original JARVIS Python implementation
- Ollama team for local AI hosting
- DeepSeek for the advanced reasoning model
- Iron Man for the inspiration

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information

---

**Enjoy your enhanced JARVIS experience! 🤖✨**