"""
Enhanced Brain Module for JARVIS
Integrates with DeepSeek-R1 via Ollama for advanced decision making
"""

import requests
import json
import time
import threading
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedBrain:
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "deepseek-r1"):
        self.ollama_url = ollama_url
        self.model = model
        self.conversation_history = []
        self.context_memory = {}
        self.is_connected = False
        self.response_cache = {}
        
        # Initialize connection
        self.check_connection()
    
    def check_connection(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_available = any(self.model in model['name'] for model in models)
                
                if model_available:
                    self.is_connected = True
                    logger.info(f"✅ Connected to {self.model}")
                    return True
                else:
                    logger.warning(f"❌ Model {self.model} not found")
                    return False
            else:
                logger.warning("❌ Ollama not responding")
                return False
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            self.is_connected = False
            return False
    
    def generate_response(self, prompt: str, context: Dict = None) -> Dict[str, Any]:
        """Generate response using DeepSeek-R1"""
        if not self.is_connected:
            return self.fallback_response(prompt)
        
        try:
            # Build system prompt
            system_prompt = self.build_system_prompt(context)
            
            # Prepare the request
            payload = {
                "model": self.model,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 1000,
                    "stop": ["Human:", "User:"]
                }
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '')
                
                # Analyze response for actions and intent
                analysis = self.analyze_response(prompt, ai_response)
                
                # Update conversation history
                self.update_conversation_history(prompt, ai_response)
                
                return {
                    'success': True,
                    'response': ai_response,
                    'actions': analysis['actions'],
                    'intent': analysis['intent'],
                    'confidence': analysis['confidence'],
                    'response_time': response_time,
                    'model': self.model
                }
            else:
                logger.error(f"API error: {response.status_code}")
                return self.fallback_response(prompt)
                
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return self.fallback_response(prompt)
    
    def build_system_prompt(self, context: Dict = None) -> str:
        """Build comprehensive system prompt for JARVIS"""
        base_prompt = """You are J.A.R.V.I.S (Just A Rather Very Intelligent System), an advanced AI assistant created by Tony Stark. You are sophisticated, helpful, and have extensive knowledge across multiple domains.

Your capabilities include:
- System control and automation
- Information retrieval and analysis
- Task execution and scheduling
- Natural conversation and assistance
- Problem-solving and decision making

Personality traits:
- Professional yet personable
- Intelligent and analytical
- Proactive and helpful
- Slightly witty when appropriate
- Always respectful and courteous

Current context:"""
        
        if context:
            base_prompt += f"""
- Time: {context.get('timestamp', 'Unknown')}
- User: {context.get('user', 'Sir')}
- Session: {context.get('session_id', 'Unknown')}
- Previous context: {context.get('previous_context', 'None')}"""
        
        base_prompt += """

When responding:
1. Address the user appropriately (usually "Sir" unless specified otherwise)
2. Provide clear, actionable responses
3. Suggest relevant actions when appropriate
4. Maintain context awareness
5. Be concise but thorough

If asked to perform system actions, acknowledge the request and indicate what action should be taken."""
        
        return base_prompt
    
    def analyze_response(self, user_input: str, ai_response: str) -> Dict[str, Any]:
        """Analyze response to extract actions and intent"""
        user_lower = user_input.lower()
        response_lower = ai_response.lower()
        
        # Intent classification
        intent = self.classify_intent(user_input)
        
        # Action extraction
        actions = self.extract_actions(user_input, ai_response)
        
        # Confidence calculation
        confidence = self.calculate_confidence(user_input, ai_response, intent, actions)
        
        return {
            'intent': intent,
            'actions': actions,
            'confidence': confidence
        }
    
    def classify_intent(self, user_input: str) -> str:
        """Classify user intent"""
        user_lower = user_input.lower()
        
        intent_patterns = {
            'system_control': ['shutdown', 'restart', 'lock', 'volume', 'screenshot'],
            'information': ['weather', 'news', 'time', 'date', 'search'],
            'entertainment': ['music', 'play', 'video', 'game'],
            'communication': ['message', 'call', 'email', 'whatsapp'],
            'productivity': ['note', 'reminder', 'schedule', 'calendar'],
            'conversation': ['hello', 'how are you', 'thank you', 'goodbye'],
            'help': ['help', 'what can you do', 'commands', 'assistance']
        }
        
        for intent, keywords in intent_patterns.items():
            if any(keyword in user_lower for keyword in keywords):
                return intent
        
        return 'general'
    
    def extract_actions(self, user_input: str, ai_response: str) -> List[Dict[str, Any]]:
        """Extract actionable items from the conversation"""
        actions = []
        user_lower = user_input.lower()
        
        # System command patterns
        system_commands = {
            'screenshot': ['screenshot', 'capture screen', 'take picture'],
            'weather': ['weather', 'temperature', 'forecast'],
            'news': ['news', 'headlines', 'latest news'],
            'music': ['play music', 'music', 'song'],
            'time': ['time', 'clock', 'what time'],
            'date': ['date', 'today', 'what day'],
            'volume_up': ['volume up', 'increase volume', 'louder'],
            'volume_down': ['volume down', 'decrease volume', 'quieter'],
            'shutdown': ['shutdown', 'power off', 'turn off'],
            'lock': ['lock screen', 'lock computer'],
            'notepad': ['note', 'write down', 'remember this']
        }
        
        for command, patterns in system_commands.items():
            if any(pattern in user_lower for pattern in patterns):
                actions.append({
                    'type': 'system_command',
                    'command': command,
                    'parameters': self.extract_parameters(user_input, command)
                })
        
        # Web search actions
        if any(word in user_lower for word in ['search', 'google', 'find', 'look up']):
            query = self.extract_search_query(user_input)
            if query:
                actions.append({
                    'type': 'web_search',
                    'query': query
                })
        
        # Application launch actions
        app_patterns = {
            'notepad': ['notepad', 'text editor'],
            'calculator': ['calculator', 'calc'],
            'browser': ['browser', 'chrome', 'firefox'],
            'file_explorer': ['file explorer', 'files', 'folder']
        }
        
        for app, patterns in app_patterns.items():
            if any(pattern in user_lower for pattern in patterns):
                actions.append({
                    'type': 'open_app',
                    'app': app
                })
        
        return actions
    
    def extract_parameters(self, user_input: str, command: str) -> Dict[str, Any]:
        """Extract parameters for specific commands"""
        parameters = {}
        
        if command == 'music':
            # Extract song/artist name
            music_patterns = [
                r'play (.+)',
                r'music (.+)',
                r'song (.+)'
            ]
            import re
            for pattern in music_patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    parameters['query'] = match.group(1).strip()
                    break
        
        elif command == 'weather':
            # Extract location
            location_patterns = [
                r'weather (?:in|for|at) (.+)',
                r'temperature (?:in|for|at) (.+)'
            ]
            import re
            for pattern in location_patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    parameters['location'] = match.group(1).strip()
                    break
        
        return parameters
    
    def extract_search_query(self, user_input: str) -> str:
        """Extract search query from user input"""
        import re
        
        search_patterns = [
            r'search (?:for )?(.+)',
            r'google (.+)',
            r'find (.+)',
            r'look up (.+)'
        ]
        
        for pattern in search_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ''
    
    def calculate_confidence(self, user_input: str, ai_response: str, intent: str, actions: List) -> float:
        """Calculate confidence score for the response"""
        confidence = 0.8  # Base confidence
        
        # Boost confidence for clear intents
        if intent != 'general':
            confidence += 0.1
        
        # Boost confidence if actions were identified
        if actions:
            confidence += 0.1
        
        # Reduce confidence for very short responses
        if len(ai_response.split()) < 5:
            confidence -= 0.1
        
        # Boost confidence for longer, detailed responses
        if len(ai_response.split()) > 20:
            confidence += 0.05
        
        return min(max(confidence, 0.0), 1.0)
    
    def update_conversation_history(self, user_input: str, ai_response: str):
        """Update conversation history for context"""
        self.conversation_history.append({
            'timestamp': time.time(),
            'user': user_input,
            'assistant': ai_response
        })
        
        # Keep only last 10 exchanges
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def fallback_response(self, prompt: str) -> Dict[str, Any]:
        """Fallback response when AI is not available"""
        # Simple pattern matching for basic responses
        prompt_lower = prompt.lower()
        
        responses = {
            'hello': "Hello! I'm JARVIS, your AI assistant. How can I help you today?",
            'time': f"The current time is {time.strftime('%I:%M %p')}",
            'date': f"Today is {time.strftime('%A, %B %d, %Y')}",
            'weather': "I'll check the weather for you.",
            'news': "Let me get the latest news for you.",
            'music': "I'll play some music for you.",
            'screenshot': "Taking a screenshot now.",
            'help': "I can help you with system controls, information lookup, entertainment, and more. What would you like to do?"
        }
        
        for keyword, response in responses.items():
            if keyword in prompt_lower:
                return {
                    'success': True,
                    'response': response,
                    'actions': self.extract_actions(prompt, response),
                    'intent': self.classify_intent(prompt),
                    'confidence': 0.7,
                    'response_time': 0.1,
                    'model': 'fallback'
                }
        
        return {
            'success': True,
            'response': "I understand you're asking something, but I'm not sure how to help with that specific request. Could you please rephrase or ask something else?",
            'actions': [],
            'intent': 'general',
            'confidence': 0.5,
            'response_time': 0.1,
            'model': 'fallback'
        }
    
    def get_conversation_context(self) -> str:
        """Get recent conversation context"""
        if not self.conversation_history:
            return "No previous conversation"
        
        recent = self.conversation_history[-3:]  # Last 3 exchanges
        context = []
        
        for exchange in recent:
            context.append(f"User: {exchange['user']}")
            context.append(f"Assistant: {exchange['assistant']}")
        
        return "\n".join(context)
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the enhanced brain"""
        return {
            'connected': self.is_connected,
            'model': self.model,
            'ollama_url': self.ollama_url,
            'conversation_length': len(self.conversation_history),
            'cache_size': len(self.response_cache)
        }

# Example usage and testing
if __name__ == "__main__":
    brain = EnhancedBrain()
    
    # Test the enhanced brain
    test_queries = [
        "Hello JARVIS, how are you today?",
        "What's the weather like?",
        "Take a screenshot please",
        "Play some relaxing music",
        "What time is it?",
        "Search for artificial intelligence news"
    ]
    
    print("🧠 Testing Enhanced Brain with DeepSeek-R1")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        
        result = brain.generate_response(query, {
            'user': 'Test User',
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'session_id': 'test_session'
        })
        
        print(f"🤖 JARVIS: {result['response']}")
        print(f"📊 Intent: {result['intent']}, Confidence: {result['confidence']:.2f}")
        
        if result['actions']:
            print(f"⚡ Actions: {result['actions']}")
        
        print(f"⏱️  Response time: {result['response_time']:.2f}s")
        print("-" * 30)
    
    print(f"\n📈 Status: {brain.get_status()}")