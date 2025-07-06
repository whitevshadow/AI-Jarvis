export class VoiceManager {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.onResult = null;
        this.onStart = null;
        this.onEnd = null;
        this.onError = null;
        this.retryCount = 0;
        this.maxRetries = 3;
        this.retryDelay = 1000; // 1 second
        
        this.initSpeechRecognition();
    }

    initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
        } else if ('SpeechRecognition' in window) {
            this.recognition = new SpeechRecognition();
        }

        if (this.recognition) {
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.recognition.onstart = () => {
                this.isListening = true;
                this.retryCount = 0; // Reset retry count on successful start
                if (this.onStart) this.onStart();
            };

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                if (this.onResult) this.onResult(transcript);
            };

            this.recognition.onend = () => {
                this.isListening = false;
                if (this.onEnd) this.onEnd();
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.isListening = false;
                
                // Handle different types of errors
                this.handleSpeechError(event.error);
                
                if (this.onEnd) this.onEnd();
            };
        }
    }

    handleSpeechError(errorType) {
        let errorMessage = '';
        let shouldRetry = false;

        switch (errorType) {
            case 'network':
                errorMessage = 'Network error: Please check your internet connection and try again.';
                shouldRetry = true;
                break;
            case 'not-allowed':
                errorMessage = 'Microphone access denied. Please allow microphone permissions in your browser settings.';
                break;
            case 'no-speech':
                errorMessage = 'No speech detected. Please try speaking again.';
                shouldRetry = true;
                break;
            case 'audio-capture':
                errorMessage = 'Audio capture failed. Please check your microphone connection.';
                break;
            case 'service-not-allowed':
                errorMessage = 'Speech recognition service not allowed. Please check your browser settings.';
                break;
            default:
                errorMessage = `Speech recognition error: ${errorType}`;
                shouldRetry = true;
        }

        // Notify the application about the error
        if (this.onError) {
            this.onError(errorMessage, errorType);
        } else {
            console.warn(errorMessage);
        }

        // Attempt retry for certain error types
        if (shouldRetry && this.retryCount < this.maxRetries) {
            this.retryCount++;
            console.log(`Retrying speech recognition (attempt ${this.retryCount}/${this.maxRetries})...`);
            
            setTimeout(() => {
                this.start().catch(error => {
                    console.error('Retry failed:', error);
                });
            }, this.retryDelay * this.retryCount); // Exponential backoff
        }
    }

    async start() {
        if (!this.recognition) {
            const error = 'Speech recognition not supported in this browser. Please use Chrome or Edge.';
            if (this.onError) {
                this.onError(error, 'not-supported');
            }
            throw new Error(error);
        }

        if (this.isListening) {
            return;
        }

        // Check for microphone permissions before starting
        try {
            await this.checkMicrophonePermission();
        } catch (error) {
            const errorMsg = 'Microphone permission required. Please allow microphone access and try again.';
            if (this.onError) {
                this.onError(errorMsg, 'permission-denied');
            }
            throw new Error(errorMsg);
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('Error starting speech recognition:', error);
            if (this.onError) {
                this.onError('Failed to start speech recognition. Please try again.', 'start-failed');
            }
            throw error;
        }
    }

    async checkMicrophonePermission() {
        if (navigator.permissions) {
            try {
                const permission = await navigator.permissions.query({ name: 'microphone' });
                if (permission.state === 'denied') {
                    throw new Error('Microphone permission denied');
                }
            } catch (error) {
                // Fallback: try to access microphone directly
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    stream.getTracks().forEach(track => track.stop());
                } catch (micError) {
                    throw new Error('Microphone access failed');
                }
            }
        }
    }

    stop() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }

    speak(text) {
        if (!this.synthesis) {
            console.warn('Speech synthesis not supported');
            return;
        }

        // Cancel any ongoing speech
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 0.8;

        // Try to use a more robotic voice if available
        const voices = this.synthesis.getVoices();
        const preferredVoice = voices.find(voice => 
            voice.name.includes('Google') || 
            voice.name.includes('Microsoft') ||
            voice.name.includes('Alex')
        );

        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        this.synthesis.speak(utterance);
    }

    isSupported() {
        return !!this.recognition && !!this.synthesis;
    }

    // Method to set error callback
    setErrorCallback(callback) {
        this.onError = callback;
    }

    // Method to get detailed browser support info
    getSupportInfo() {
        return {
            speechRecognition: !!this.recognition,
            speechSynthesis: !!this.synthesis,
            userAgent: navigator.userAgent,
            isSecureContext: window.isSecureContext,
            hasMediaDevices: !!navigator.mediaDevices
        };
    }
}