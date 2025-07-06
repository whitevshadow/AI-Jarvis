export class ChatManager {
    constructor() {
        this.messagesContainer = document.getElementById('chatMessages');
        this.messageCount = 0;
    }

    addMessage(sender, content, type = 'user') {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}-message`;
        messageElement.innerHTML = `
            <div class="message-avatar">
                <div class="avatar-icon">${this.getAvatarIcon(sender, type)}</div>
            </div>
            <div class="message-content">
                <p>${this.formatMessage(content)}</p>
            </div>
        `;

        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
        this.messageCount++;

        // Add typing animation for AI responses
        if (type === 'jarvis') {
            this.animateTyping(messageElement.querySelector('.message-content p'));
        }
    }

    getAvatarIcon(sender, type) {
        switch (type) {
            case 'jarvis':
                return 'J';
            case 'user':
                return 'U';
            case 'system':
                return 'S';
            default:
                return sender.charAt(0).toUpperCase();
        }
    }

    formatMessage(content) {
        // Basic formatting for links, code, etc.
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    animateTyping(element) {
        const text = element.textContent;
        element.textContent = '';
        
        let i = 0;
        const typeInterval = setInterval(() => {
            element.textContent += text.charAt(i);
            i++;
            
            if (i >= text.length) {
                clearInterval(typeInterval);
            }
        }, 30);
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    clearMessages() {
        this.messagesContainer.innerHTML = '';
        this.messageCount = 0;
    }

    getMessageCount() {
        return this.messageCount;
    }
}