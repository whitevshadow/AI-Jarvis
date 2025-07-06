export class AnimationManager {
    constructor() {
        this.voiceVisualizationActive = false;
        this.processingAnimationActive = false;
        this.backgroundAnimationActive = false;
    }

    startBackgroundAnimations() {
        this.backgroundAnimationActive = true;
        this.createFloatingParticles();
        this.animateCircuitLines();
    }

    createFloatingParticles() {
        const container = document.querySelector('.floating-particles');
        if (!container) return;

        // Create additional particles dynamically
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: var(--primary-blue);
                border-radius: 50%;
                opacity: 0;
                animation: float ${15 + Math.random() * 10}s infinite linear;
                animation-delay: ${-Math.random() * 15}s;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
            `;
            container.appendChild(particle);
        }
    }

    animateCircuitLines() {
        const circuitLines = document.querySelector('.circuit-lines');
        if (!circuitLines) return;

        // Add dynamic circuit animation
        setInterval(() => {
            if (this.backgroundAnimationActive) {
                circuitLines.style.opacity = 0.1 + Math.random() * 0.1;
            }
        }, 2000);
    }

    startVoiceVisualization() {
        this.voiceVisualizationActive = true;
        const waves = document.querySelectorAll('.wave');
        
        waves.forEach((wave, index) => {
            wave.style.animation = `wave 0.5s ease-in-out infinite`;
            wave.style.animationDelay = `${index * 0.1}s`;
        });

        // Add random height variations
        this.voiceVisualizationInterval = setInterval(() => {
            if (this.voiceVisualizationActive) {
                waves.forEach(wave => {
                    const height = 10 + Math.random() * 50;
                    wave.style.height = `${height}px`;
                });
            }
        }, 100);
    }

    stopVoiceVisualization() {
        this.voiceVisualizationActive = false;
        
        if (this.voiceVisualizationInterval) {
            clearInterval(this.voiceVisualizationInterval);
        }

        const waves = document.querySelectorAll('.wave');
        waves.forEach(wave => {
            wave.style.height = '10px';
            wave.style.animation = 'none';
        });
    }

    startProcessingAnimation() {
        this.processingAnimationActive = true;
        
        // Animate arc reactor during processing
        const core = document.querySelector('.core');
        if (core) {
            core.style.animation = 'pulse 0.5s ease-in-out infinite';
        }

        // Animate rings faster
        const rings = document.querySelectorAll('.ring');
        rings.forEach((ring, index) => {
            ring.style.animationDuration = `${2 + index}s`;
        });
    }

    stopProcessingAnimation() {
        this.processingAnimationActive = false;
        
        // Reset arc reactor animation
        const core = document.querySelector('.core');
        if (core) {
            core.style.animation = 'pulse 2s ease-in-out infinite';
        }

        // Reset ring animations
        const rings = document.querySelectorAll('.ring');
        rings.forEach((ring, index) => {
            const durations = ['10s', '15s', '20s'];
            ring.style.animationDuration = durations[index] || '10s';
        });
    }

    pulseElement(element, duration = 1000) {
        element.style.animation = `pulse 0.3s ease-in-out`;
        
        setTimeout(() => {
            element.style.animation = '';
        }, duration);
    }

    glowEffect(element, color = 'var(--primary-blue)', duration = 2000) {
        element.style.boxShadow = `0 0 20px ${color}`;
        element.style.transition = 'box-shadow 0.3s ease';
        
        setTimeout(() => {
            element.style.boxShadow = '';
        }, duration);
    }

    typewriterEffect(element, text, speed = 50) {
        element.textContent = '';
        let i = 0;
        
        const typeInterval = setInterval(() => {
            element.textContent += text.charAt(i);
            i++;
            
            if (i >= text.length) {
                clearInterval(typeInterval);
            }
        }, speed);
    }

    slideInElement(element, direction = 'left') {
        const directions = {
            left: 'translateX(-100%)',
            right: 'translateX(100%)',
            top: 'translateY(-100%)',
            bottom: 'translateY(100%)'
        };

        element.style.transform = directions[direction];
        element.style.opacity = '0';
        element.style.transition = 'transform 0.5s ease, opacity 0.5s ease';

        setTimeout(() => {
            element.style.transform = 'translate(0, 0)';
            element.style.opacity = '1';
        }, 100);
    }
}