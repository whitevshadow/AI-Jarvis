const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const cors = require('cors');
const axios = require('axios');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('dist'));

// Ollama configuration
const OLLAMA_BASE_URL = 'http://localhost:11434';
const MODEL_NAME = 'deepseek-r1';

class AIEngine {
    constructor() {
        this.isOllamaRunning = false;
        this.checkOllamaStatus();
    }

    async checkOllamaStatus() {
        try {
            const response = await axios.get(`${OLLAMA_BASE_URL}/api/tags`);
            this.isOllamaRunning = true;
            console.log('✅ Ollama is running');
            
            // Check if DeepSeek-R1 model is available
            await this.ensureModelAvailable();
        } catch (error) {
            console.log('❌ Ollama is not running. Please start Ollama first.');
            this.isOllamaRunning = false;
        }
    }

    async ensureModelAvailable() {
        try {
            const response = await axios.get(`${OLLAMA_BASE_URL}/api/tags`);
            const models = response.data.models || [];
            
            const hasDeepSeek = models.some(model => 
                model.name.includes('deepseek-r1') || model.name.includes('deepseek')
            );

            if (!hasDeepSeek) {
                console.log('🔄 DeepSeek-R1 model not found. Pulling model...');
                await this.pullModel();
            } else {
                console.log('✅ DeepSeek-R1 model is available');
            }
        } catch (error) {
            console.error('Error checking model availability:', error.message);
        }
    }

    async pullModel() {
        try {
            console.log('📥 Pulling DeepSeek-R1 model from Ollama...');
            
            const response = await axios.post(`${OLLAMA_BASE_URL}/api/pull`, {
                name: MODEL_NAME,
                stream: false
            });

            console.log('✅ DeepSeek-R1 model pulled successfully');
            return true;
        } catch (error) {
            console.error('❌ Failed to pull DeepSeek-R1 model:', error.message);
            return false;
        }
    }

    async generateResponse(message, context = {}) {
        if (!this.isOllamaRunning) {
            throw new Error('Ollama is not running');
        }

        try {
            const systemPrompt = `You are J.A.R.V.I.S, an advanced AI assistant created by Tony Stark. You are helpful, intelligent, and have a sophisticated personality. You can control various system functions and provide information. Always respond in character as J.A.R.V.I.S.

Current context:
- User: ${context.user || 'Sir'}
- Time: ${new Date().toLocaleString()}
- Session: ${context.session_id || 'unknown'}

Respond naturally and helpfully. If the user asks for system commands, suggest appropriate actions.`;

            const response = await axios.post(`${OLLAMA_BASE_URL}/api/generate`, {
                model: MODEL_NAME,
                prompt: message,
                system: systemPrompt,
                stream: false,
                options: {
                    temperature: 0.7,
                    top_p: 0.9,
                    max_tokens: 500
                }
            });

            const aiResponse = response.data.response;
            
            // Analyze response for actions
            const actions = this.extractActions(message, aiResponse);
            
            return {
                response: aiResponse,
                actions: actions,
                confidence: 0.95,
                model: MODEL_NAME,
                timestamp: new Date().toISOString()
            };

        } catch (error) {
            console.error('Error generating AI response:', error.message);
            throw error;
        }
    }

    extractActions(userMessage, aiResponse) {
        const actions = [];
        const lowerMessage = userMessage.toLowerCase();
        const lowerResponse = aiResponse.toLowerCase();

        // System command patterns
        const commandPatterns = {
            'take_screenshot': /screenshot|capture screen/,
            'get_weather': /weather|temperature|forecast/,
            'get_news': /news|headlines|latest news/,
            'play_music': /play music|music|song/,
            'get_time': /time|clock/,
            'get_date': /date|today/,
            'shutdown': /shutdown|power off/,
            'lock_screen': /lock screen|lock computer/,
            'volume_up': /volume up|increase volume/,
            'volume_down': /volume down|decrease volume/,
            'open_notepad': /notepad|take note|write note/
        };

        for (const [command, pattern] of Object.entries(commandPatterns)) {
            if (pattern.test(lowerMessage) || pattern.test(lowerResponse)) {
                actions.push({
                    type: 'system_command',
                    command: command,
                    parameters: this.extractParameters(userMessage, command)
                });
            }
        }

        // Web search pattern
        if (lowerMessage.includes('search') || lowerMessage.includes('google')) {
            const query = userMessage.replace(/search|google|for/gi, '').trim();
            if (query) {
                actions.push({
                    type: 'web_search',
                    query: query
                });
            }
        }

        return actions;
    }

    extractParameters(message, command) {
        const parameters = {};
        
        switch (command) {
            case 'play_music':
                const musicMatch = message.match(/play (.+)/i);
                if (musicMatch) {
                    parameters.query = musicMatch[1];
                }
                break;
            case 'get_weather':
                const locationMatch = message.match(/weather (?:in|for) (.+)/i);
                if (locationMatch) {
                    parameters.location = locationMatch[1];
                }
                break;
        }

        return parameters;
    }
}

class SystemController {
    constructor() {
        this.pythonPath = 'python'; // Adjust if needed
    }

    async executeCommand(command, parameters = {}) {
        console.log(`Executing command: ${command}`, parameters);

        try {
            switch (command) {
                case 'take_screenshot':
                    return await this.takeScreenshot();
                case 'get_weather':
                    return await this.getWeather(parameters.location);
                case 'get_news':
                    return await this.getNews();
                case 'play_music':
                    return await this.playMusic(parameters.query);
                case 'get_time':
                    return this.getTime();
                case 'get_date':
                    return this.getDate();
                case 'volume_up':
                    return await this.changeVolume(2);
                case 'volume_down':
                    return await this.changeVolume(-2);
                case 'shutdown':
                    return await this.shutdown();
                case 'lock_screen':
                    return await this.lockScreen();
                case 'open_notepad':
                    return await this.openNotepad();
                default:
                    return { success: false, message: 'Unknown command' };
            }
        } catch (error) {
            console.error(`Error executing command ${command}:`, error);
            return { success: false, message: error.message };
        }
    }

    async runPythonScript(scriptPath, args = []) {
        return new Promise((resolve, reject) => {
            const python = spawn(this.pythonPath, [scriptPath, ...args]);
            let output = '';
            let error = '';

            python.stdout.on('data', (data) => {
                output += data.toString();
            });

            python.stderr.on('data', (data) => {
                error += data.toString();
            });

            python.on('close', (code) => {
                if (code === 0) {
                    resolve({ success: true, output: output.trim() });
                } else {
                    reject(new Error(error || `Process exited with code ${code}`));
                }
            });
        });
    }

    async takeScreenshot() {
        try {
            // Use the existing Python screenshot functionality
            const result = await this.runPythonScript('Features/OS/Windows.py', ['screenshot']);
            return { success: true, message: 'Screenshot taken successfully' };
        } catch (error) {
            return { success: false, message: 'Failed to take screenshot' };
        }
    }

    async getWeather(location = '') {
        try {
            const query = location || 'current weather';
            const result = await this.runPythonScript('Features/Web_Scraping/Weather.py', [query]);
            return { success: true, message: 'Weather information retrieved', data: result.output };
        } catch (error) {
            return { success: false, message: 'Failed to get weather information' };
        }
    }

    async getNews() {
        try {
            const result = await this.runPythonScript('Features/Web_Scraping/News.py');
            return { success: true, message: 'Latest news retrieved', data: result.output };
        } catch (error) {
            return { success: false, message: 'Failed to get news' };
        }
    }

    async playMusic(query = '') {
        try {
            const searchQuery = query || 'relaxing music';
            const result = await this.runPythonScript('Features/Task.py', ['music', searchQuery]);
            return { success: true, message: `Playing: ${searchQuery}` };
        } catch (error) {
            return { success: false, message: 'Failed to play music' };
        }
    }

    getTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        return { success: true, message: `Current time is ${timeString}` };
    }

    getDate() {
        const now = new Date();
        const dateString = now.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        return { success: true, message: `Today is ${dateString}` };
    }

    async changeVolume(change) {
        try {
            const result = await this.runPythonScript('Features/OS/Volume_control.py', [change.toString()]);
            const action = change > 0 ? 'increased' : 'decreased';
            return { success: true, message: `Volume ${action}` };
        } catch (error) {
            return { success: false, message: 'Failed to change volume' };
        }
    }

    async shutdown() {
        try {
            const result = await this.runPythonScript('Features/OS/Windows.py', ['shutdown']);
            return { success: true, message: 'System shutdown initiated' };
        } catch (error) {
            return { success: false, message: 'Failed to shutdown system' };
        }
    }

    async lockScreen() {
        try {
            const result = await this.runPythonScript('Features/OS/Windows.py', ['lock']);
            return { success: true, message: 'Screen locked' };
        } catch (error) {
            return { success: false, message: 'Failed to lock screen' };
        }
    }

    async openNotepad() {
        try {
            const result = await this.runPythonScript('Features/OS/Notepad.py');
            return { success: true, message: 'Notepad opened for note taking' };
        } catch (error) {
            return { success: false, message: 'Failed to open notepad' };
        }
    }
}

// Initialize components
const aiEngine = new AIEngine();
const systemController = new SystemController();

// WebSocket handling
wss.on('connection', (ws) => {
    console.log('Client connected');

    ws.on('message', async (message) => {
        try {
            const data = JSON.parse(message);
            
            switch (data.type) {
                case 'system_command':
                    const result = await systemController.executeCommand(
                        data.payload.command, 
                        data.payload.parameters
                    );
                    
                    ws.send(JSON.stringify({
                        type: 'response',
                        payload: {
                            text: result.message,
                            success: result.success,
                            data: result.data
                        }
                    }));
                    break;

                default:
                    console.log('Unknown WebSocket message type:', data.type);
            }
        } catch (error) {
            console.error('WebSocket message error:', error);
            ws.send(JSON.stringify({
                type: 'error',
                payload: { message: error.message }
            }));
        }
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

// REST API endpoints
app.get('/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        ollama: aiEngine.isOllamaRunning,
        timestamp: new Date().toISOString()
    });
});

app.post('/api/chat', async (req, res) => {
    try {
        const { message, context } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        const response = await aiEngine.generateResponse(message, context);
        
        // Execute any system commands
        if (response.actions && response.actions.length > 0) {
            for (const action of response.actions) {
                if (action.type === 'system_command') {
                    const result = await systemController.executeCommand(
                        action.command, 
                        action.parameters
                    );
                    
                    // Append system command result to response
                    if (result.success && result.message) {
                        response.response += `\n\n${result.message}`;
                    }
                }
            }
        }

        res.json(response);
    } catch (error) {
        console.error('Chat API error:', error);
        res.status(500).json({ 
            error: 'Internal server error',
            message: error.message 
        });
    }
});

app.get('/api/model/info', async (req, res) => {
    try {
        if (!aiEngine.isOllamaRunning) {
            return res.status(503).json({ error: 'Ollama is not running' });
        }

        const response = await axios.get(`${OLLAMA_BASE_URL}/api/tags`);
        res.json({
            models: response.data.models,
            current_model: MODEL_NAME,
            ollama_status: 'running'
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Serve the web app
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

const PORT = process.env.PORT || 3001;

server.listen(PORT, () => {
    console.log(`🚀 JARVIS Enhanced Server running on port ${PORT}`);
    console.log(`🌐 Web UI: http://localhost:${PORT}`);
    console.log(`🤖 AI Engine: ${aiEngine.isOllamaRunning ? 'Connected' : 'Disconnected'}`);
    console.log('\n📋 Setup Instructions:');
    console.log('1. Install Ollama: https://ollama.ai/');
    console.log('2. Run: ollama pull deepseek-r1');
    console.log('3. Start Ollama service');
    console.log('4. Access the web interface at the URL above');
});