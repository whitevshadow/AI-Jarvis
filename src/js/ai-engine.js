export class AIEngine {
    constructor() {
        this.baseUrl = 'http://localhost:3001';
        this.model = 'deepseek-r1';
        this.isConnected = false;
        this.responseTime = 0;
        
        this.checkConnection();
    }

    async checkConnection() {
        try {
            const response = await fetch(`${this.baseUrl}/health`);
            this.isConnected = response.ok;
            this.updateConnectionStatus();
        } catch (error) {
            console.error('AI Engine connection failed:', error);
            this.isConnected = false;
            this.updateConnectionStatus();
        }
    }

    updateConnectionStatus() {
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-text');
        const modelStatus = document.querySelector('.model-status');

        if (this.isConnected) {
            statusDot.style.background = 'var(--success-green)';
            statusText.textContent = 'Online';
            if (modelStatus) modelStatus.textContent = 'Connected';
        } else {
            statusDot.style.background = 'var(--error-red)';
            statusText.textContent = 'Offline';
            if (modelStatus) modelStatus.textContent = 'Disconnected';
        }
    }

    async processMessage(message) {
        const startTime = Date.now();
        
        try {
            // If AI engine is not connected, use fallback processing
            if (!this.isConnected) {
                return this.fallbackProcessing(message);
            }

            const response = await fetch(`${this.baseUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    model: this.model,
                    context: this.getContext()
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.responseTime = (Date.now() - startTime) / 1000;

            return {
                text: data.response,
                actions: data.actions || [],
                metrics: {
                    responseTime: this.responseTime,
                    confidence: data.confidence || 0.95
                },
                speak: data.speak !== false
            };

        } catch (error) {
            console.error('AI processing error:', error);
            return this.fallbackProcessing(message);
        }
    }

    fallbackProcessing(message) {
        const lowerMessage = message.toLowerCase();
        
        // Simple pattern matching for common commands
        const patterns = {
            greeting: /^(hi|hello|hey|good morning|good afternoon|good evening)/,
            time: /time|clock/,
            date: /date|today/,
            weather: /weather|temperature|forecast/,
            news: /news|headlines/,
            music: /play|music|song/,
            screenshot: /screenshot|capture/,
            exit: /bye|goodbye|exit|quit/
        };

        let response = "I'm not sure how to help with that. Could you please rephrase your request?";
        let actions = [];
        let speak = true;

        if (patterns.greeting.test(lowerMessage)) {
            response = "Hello! How can I assist you today?";
        } else if (patterns.time.test(lowerMessage)) {
            const now = new Date();
            response = `The current time is ${now.toLocaleTimeString()}.`;
            actions = [{ type: 'system_command', command: 'get_time' }];
        } else if (patterns.date.test(lowerMessage)) {
            const now = new Date();
            response = `Today's date is ${now.toLocaleDateString()}.`;
        } else if (patterns.weather.test(lowerMessage)) {
            response = "Let me check the weather for you.";
            actions = [{ type: 'system_command', command: 'get_weather' }];
        } else if (patterns.news.test(lowerMessage)) {
            response = "Fetching the latest news for you.";
            actions = [{ type: 'system_command', command: 'get_news' }];
        } else if (patterns.music.test(lowerMessage)) {
            response = "Playing music for you.";
            actions = [{ type: 'system_command', command: 'play_music' }];
        } else if (patterns.screenshot.test(lowerMessage)) {
            response = "Taking a screenshot now.";
            actions = [{ type: 'system_command', command: 'take_screenshot' }];
        } else if (patterns.exit.test(lowerMessage)) {
            response = "Goodbye! Have a great day!";
            actions = [{ type: 'system_command', command: 'exit' }];
        }

        return {
            text: response,
            actions: actions,
            metrics: {
                responseTime: 0.1,
                confidence: 0.8
            },
            speak: speak
        };
    }

    getContext() {
        return {
            timestamp: new Date().toISOString(),
            user: 'User',
            session_id: this.generateSessionId()
        };
    }

    generateSessionId() {
        return Math.random().toString(36).substring(2, 15) + 
               Math.random().toString(36).substring(2, 15);
    }

    async trainModel(data) {
        try {
            const response = await fetch(`${this.baseUrl}/api/train`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    training_data: data,
                    model: this.model
                })
            });

            return await response.json();
        } catch (error) {
            console.error('Model training error:', error);
            throw error;
        }
    }

    async getModelInfo() {
        try {
            const response = await fetch(`${this.baseUrl}/api/model/info`);
            return await response.json();
        } catch (error) {
            console.error('Model info error:', error);
            return null;
        }
    }
}