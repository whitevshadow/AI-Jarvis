export class SocketManager {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.onResponse = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    connect() {
        try {
            // Use WebSocket for real-time communication
            this.socket = new WebSocket('ws://localhost:3001');
            
            this.socket.onopen = () => {
                console.log('WebSocket connected');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.updateConnectionStatus();
            };

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };

            this.socket.onclose = () => {
                console.log('WebSocket disconnected');
                this.isConnected = false;
                this.updateConnectionStatus();
                this.attemptReconnect();
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.isConnected = false;
                this.updateConnectionStatus();
            };

        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
            this.isConnected = false;
            this.updateConnectionStatus();
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, 2000 * this.reconnectAttempts);
        }
    }

    updateConnectionStatus() {
        // This could update UI elements to show connection status
        const event = new CustomEvent('connectionStatusChanged', {
            detail: { connected: this.isConnected }
        });
        document.dispatchEvent(event);
    }

    handleMessage(data) {
        switch (data.type) {
            case 'response':
                if (this.onResponse) {
                    this.onResponse(data.payload);
                }
                break;
            case 'system_status':
                this.handleSystemStatus(data.payload);
                break;
            case 'error':
                console.error('Server error:', data.payload);
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }

    handleSystemStatus(status) {
        // Update UI based on system status
        console.log('System status:', status);
    }

    send(data) {
        if (this.isConnected && this.socket) {
            this.socket.send(JSON.stringify(data));
        } else {
            console.warn('WebSocket not connected, cannot send message');
        }
    }

    executeSystemCommand(command) {
        this.send({
            type: 'system_command',
            payload: { command }
        });
    }

    openApplication(app) {
        this.send({
            type: 'open_app',
            payload: { app }
        });
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
            this.isConnected = false;
        }
    }
}