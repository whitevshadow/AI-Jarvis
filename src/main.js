import './styles/main.css';
import { VoiceManager } from './js/voice.js';
import { ChatManager } from './js/chat.js';
import { AnimationManager } from './js/animations.js';
import { AIEngine } from './js/ai-engine.js';
import { SocketManager } from './js/socket.js';

class JarvisApp {
    constructor() {
        this.voiceManager = new VoiceManager();
        this.chatManager = new ChatManager();
        this.animationManager = new AnimationManager();
        this.aiEngine = new AIEngine();
        this.socketManager = new SocketManager();
        
        this.isListening = false;
        this.isProcessing = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.animationManager.startBackgroundAnimations();
        this.socketManager.connect();
        this.displayWelcomeMessage();
    }

    setupEventListeners() {
        // Voice button
        const voiceBtn = document.getElementById('voiceBtn');
        voiceBtn.addEventListener('click', () => this.toggleVoiceRecognition());

        // Send button
        const sendBtn = document.getElementById('sendBtn');
        sendBtn.addEventListener('click', () => this.sendMessage());

        // Chat input
        const chatInput = document.getElementById('chatInput');
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Control buttons
        const controlBtns = document.querySelectorAll('.control-btn');
        controlBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.executeQuickAction(action);
            });
        });

        // Voice recognition events
        this.voiceManager.onResult = (transcript) => {
            this.handleVoiceInput(transcript);
        };

        this.voiceManager.onStart = () => {
            this.setListeningState(true);
        };

        this.voiceManager.onEnd = () => {
            this.setListeningState(false);
        };

        // Socket events
        this.socketManager.onResponse = (response) => {
            this.handleAIResponse(response);
        };
    }

    async toggleVoiceRecognition() {
        if (this.isListening) {
            this.voiceManager.stop();
        } else {
            try {
                await this.voiceManager.start();
            } catch (error) {
                console.error('Voice recognition error:', error);
                this.chatManager.addMessage('System', 'Voice recognition not available. Please type your message.', 'system');
            }
        }
    }

    setListeningState(listening) {
        this.isListening = listening;
        const voiceBtn = document.getElementById('voiceBtn');
        const listeningIndicator = document.querySelector('.listening-indicator');
        
        if (listening) {
            voiceBtn.classList.add('listening');
            listeningIndicator.classList.add('active');
            this.animationManager.startVoiceVisualization();
        } else {
            voiceBtn.classList.remove('listening');
            listeningIndicator.classList.remove('active');
            this.animationManager.stopVoiceVisualization();
        }
    }

    handleVoiceInput(transcript) {
        const chatInput = document.getElementById('chatInput');
        chatInput.value = transcript;
        this.sendMessage();
    }

    async sendMessage() {
        const chatInput = document.getElementById('chatInput');
        const message = chatInput.value.trim();
        
        if (!message || this.isProcessing) return;

        // Add user message to chat
        this.chatManager.addMessage('User', message, 'user');
        chatInput.value = '';

        // Show processing state
        this.setProcessingState(true);

        try {
            // Send to AI engine
            const response = await this.aiEngine.processMessage(message);
            this.handleAIResponse(response);
        } catch (error) {
            console.error('AI processing error:', error);
            this.chatManager.addMessage('System', 'Sorry, I encountered an error processing your request.', 'error');
        } finally {
            this.setProcessingState(false);
        }
    }

    setProcessingState(processing) {
        this.isProcessing = processing;
        const loadingOverlay = document.getElementById('loadingOverlay');
        
        if (processing) {
            loadingOverlay.classList.add('active');
            this.animationManager.startProcessingAnimation();
        } else {
            loadingOverlay.classList.remove('active');
            this.animationManager.stopProcessingAnimation();
        }
    }

    handleAIResponse(response) {
        // Add AI response to chat
        this.chatManager.addMessage('J.A.R.V.I.S', response.text, 'jarvis');

        // Update metrics
        this.updateMetrics(response.metrics);

        // Execute any actions
        if (response.actions) {
            this.executeActions(response.actions);
        }

        // Speak response if enabled
        if (response.speak) {
            this.voiceManager.speak(response.text);
        }
    }

    updateMetrics(metrics) {
        if (metrics) {
            const responseTimeEl = document.getElementById('responseTime');
            const confidenceEl = document.getElementById('confidence');
            
            if (metrics.responseTime) {
                responseTimeEl.textContent = `${metrics.responseTime}s`;
            }
            
            if (metrics.confidence) {
                confidenceEl.textContent = `${Math.round(metrics.confidence * 100)}%`;
            }
        }
    }

    executeActions(actions) {
        actions.forEach(action => {
            switch (action.type) {
                case 'system_command':
                    this.socketManager.executeSystemCommand(action.command);
                    break;
                case 'open_app':
                    this.socketManager.openApplication(action.app);
                    break;
                case 'web_search':
                    window.open(`https://www.google.com/search?q=${encodeURIComponent(action.query)}`, '_blank');
                    break;
                default:
                    console.log('Unknown action type:', action.type);
            }
        });
    }

    executeQuickAction(action) {
        const quickCommands = {
            weather: 'What\'s the weather like today?',
            news: 'Give me the latest news',
            music: 'Play some music',
            screenshot: 'Take a screenshot'
        };

        const command = quickCommands[action];
        if (command) {
            const chatInput = document.getElementById('chatInput');
            chatInput.value = command;
            this.sendMessage();
        }
    }

    displayWelcomeMessage() {
        setTimeout(() => {
            this.chatManager.addMessage('J.A.R.V.I.S', 
                'All systems online. Enhanced AI capabilities powered by DeepSeek-R1 are now available. How may I assist you today?', 
                'jarvis'
            );
        }, 1000);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new JarvisApp();
});