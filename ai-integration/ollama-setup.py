#!/usr/bin/env python3
"""
Ollama Setup and Integration Script for JARVIS
This script helps set up Ollama with DeepSeek-R1 model for enhanced AI capabilities
"""

import subprocess
import sys
import requests
import json
import time
import os
from pathlib import Path

class OllamaSetup:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.model_name = "deepseek-r1"
        
    def check_ollama_installed(self):
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Ollama is installed")
                return True
            else:
                print("❌ Ollama is not installed")
                return False
        except FileNotFoundError:
            print("❌ Ollama is not installed")
            return False
    
    def check_ollama_running(self):
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama service is running")
                return True
            else:
                print("❌ Ollama service is not responding")
                return False
        except requests.exceptions.RequestException:
            print("❌ Ollama service is not running")
            return False
    
    def start_ollama_service(self):
        """Start Ollama service"""
        print("🔄 Starting Ollama service...")
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(['ollama', 'serve'], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:  # Linux/Mac
                subprocess.Popen(['ollama', 'serve'])
            
            # Wait for service to start
            for i in range(10):
                time.sleep(2)
                if self.check_ollama_running():
                    return True
                print(f"⏳ Waiting for Ollama to start... ({i+1}/10)")
            
            print("❌ Failed to start Ollama service")
            return False
        except Exception as e:
            print(f"❌ Error starting Ollama: {e}")
            return False
    
    def check_model_available(self):
        """Check if DeepSeek-R1 model is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                for model in models:
                    if 'deepseek' in model['name'].lower():
                        print(f"✅ DeepSeek model found: {model['name']}")
                        return True
                print("❌ DeepSeek model not found")
                return False
            else:
                print("❌ Failed to check available models")
                return False
        except Exception as e:
            print(f"❌ Error checking models: {e}")
            return False
    
    def pull_model(self):
        """Pull DeepSeek-R1 model"""
        print(f"📥 Pulling {self.model_name} model...")
        print("⚠️  This may take several minutes depending on your internet connection")
        
        try:
            # Use subprocess for better control
            process = subprocess.Popen(
                ['ollama', 'pull', self.model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor the process
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(f"📥 {output.strip()}")
            
            if process.returncode == 0:
                print(f"✅ {self.model_name} model pulled successfully")
                return True
            else:
                error = process.stderr.read()
                print(f"❌ Failed to pull model: {error}")
                return False
                
        except Exception as e:
            print(f"❌ Error pulling model: {e}")
            return False
    
    def test_model(self):
        """Test the model with a simple query"""
        print("🧪 Testing model...")
        
        try:
            payload = {
                "model": self.model_name,
                "prompt": "Hello, I am JARVIS. Please respond as an AI assistant.",
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Model test successful")
                print(f"🤖 Response: {result.get('response', 'No response')[:100]}...")
                return True
            else:
                print(f"❌ Model test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing model: {e}")
            return False
    
    def setup(self):
        """Complete setup process"""
        print("🚀 Setting up Ollama with DeepSeek-R1 for JARVIS")
        print("=" * 50)
        
        # Check if Ollama is installed
        if not self.check_ollama_installed():
            print("\n📋 Please install Ollama first:")
            print("🌐 Visit: https://ollama.ai/")
            print("💻 Or run: curl -fsSL https://ollama.ai/install.sh | sh")
            return False
        
        # Check if service is running
        if not self.check_ollama_running():
            if not self.start_ollama_service():
                print("\n📋 Please start Ollama manually:")
                print("💻 Run: ollama serve")
                return False
        
        # Check if model is available
        if not self.check_model_available():
            if not self.pull_model():
                return False
        
        # Test the model
        if not self.test_model():
            return False
        
        print("\n🎉 Setup completed successfully!")
        print("🤖 DeepSeek-R1 is ready for JARVIS")
        print("\n📋 Next steps:")
        print("1. Start the JARVIS web server: npm run dev")
        print("2. Open http://localhost:3000 in your browser")
        print("3. Enjoy enhanced AI capabilities!")
        
        return True

def main():
    setup = OllamaSetup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'check':
            setup.check_ollama_installed()
            setup.check_ollama_running()
            setup.check_model_available()
        elif command == 'pull':
            setup.pull_model()
        elif command == 'test':
            setup.test_model()
        elif command == 'start':
            setup.start_ollama_service()
        else:
            print("Usage: python ollama-setup.py [check|pull|test|start]")
    else:
        setup.setup()

if __name__ == "__main__":
    main()