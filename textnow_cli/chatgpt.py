import openai
import config

class ChatGPTClient:
    def __init__(self):
        openai.api_key = config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        self.conversation_history = []
        self.current_model = "gpt-4o"
        
    def set_model(self, model):
        """Switch between models"""
        if model in ["gpt-4o", "o3-mini"]:
            self.current_model = model
            return f"✅ Model changed to {model}"
        return "❌ Invalid model. Use 'gpt-4o' or 'o3-mini'"
    
    def new_session(self):
        """Start a new conversation session"""
        self.conversation_history = []
        return "✅ New session started"
    
    def get_response(self, message):
        """Get ChatGPT response"""
        try:
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": message})
            
            # Keep only last 10 messages to avoid token limits
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            response = self.client.chat.completions.create(
                model=self.current_model,
                messages=self.conversation_history,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}" 