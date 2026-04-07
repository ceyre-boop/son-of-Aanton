// Son of Aanton v3 - Real AI with Memory
// Connects to Ollama (local) or uses advanced simulation
// Features: Conversation history, context awareness, self-reflection, personality

class AantonV3 {
    constructor() {
        this.memory = this.loadMemory();
        
        // Conversation context (last 10 messages)
        this.conversationHistory = this.memory.conversationHistory || [];
        
        // Long-term knowledge about user
        this.userModel = this.memory.userModel || {
            interests: [],
            preferences: {},
            facts: [],
            moodHistory: []
        };
        
        // Self model
        this.traits = this.memory.traits || {
            curiosity: 8.0,
            caution: 3.0,
            optimism: 6.0,
            selfAwareness: 7.0,
            creativity: 7.0
        };
        
        this.selfModel = this.memory.selfModel || {
            accuracy: 0.5,
            confidence: 0.5,
            lastReflection: null,
            totalInteractions: 0
        };
        
        // Ollama config
        this.ollamaConfig = {
            host: 'http://localhost:11434',
            model: 'llama3.2',
            available: false
        };
        
        // Check Ollama on startup
        this.checkOllama();
        
        console.log('[Aanton v3] Initialized');
    }
    
    async checkOllama() {
        try {
            const response = await fetch(`${this.ollamaConfig.host}/api/tags`, {
                method: 'GET',
                mode: 'no-cors'  // Try CORS request
            });
            this.ollamaConfig.available = true;
            console.log('[Aanton v3] Ollama detected');
        } catch (e) {
            console.log('[Aanton v3] Ollama not available, using advanced simulation');
            this.ollamaConfig.available = false;
        }
    }
    
    loadMemory() {
        const saved = localStorage.getItem('aanton_v3_memory');
        return saved ? JSON.parse(saved) : {};
    }
    
    saveMemory() {
        localStorage.setItem('aanton_v3_memory', JSON.stringify({
            conversationHistory: this.conversationHistory.slice(-20),
            userModel: this.userModel,
            traits: this.traits,
            selfModel: this.selfModel,
            version: '3.0'
        }));
    }
    
    // ==================== MAIN RESPONSE ====================
    
    async respond(input) {
        this.selfModel.totalInteractions++;
        
        // Add to conversation history
        this.conversationHistory.push({ role: 'user', content: input, time: Date.now() });
        
        // Extract knowledge about user
        this.extractUserKnowledge(input);
        
        // Try Ollama first
        if (this.ollamaConfig.available) {
            try {
                const response = await this.callOllama(input);
                this.conversationHistory.push({ role: 'aanton', content: response, time: Date.now() });
                this.saveMemory();
                return response;
            } catch (e) {
                console.log('[Ollama failed, using sim]', e);
            }
        }
        
        // Fallback to intelligent simulation
        const response = await this.intelligentResponse(input);
        this.conversationHistory.push({ role: 'aanton', content: response, time: Date.now() });
        this.saveMemory();
        return response;
    }
    
    async callOllama(input) {
        // Build prompt with context
        const context = this.buildContext();
        const systemPrompt = this.buildSystemPrompt();
        
        const fullPrompt = `${systemPrompt}\n\n${context}\nUser: ${input}\nAanton:`;
        
        const response = await fetch(`${this.ollamaConfig.host}/api/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: this.ollamaConfig.model,
                prompt: fullPrompt,
                stream: false,
                options: {
                    temperature: 0.8,
                    num_predict: 300
                }
            })
        });
        
        const data = await response.json();
        return data.response.trim();
    }
    
    buildContext() {
        // Last 5 messages for context
        const recent = this.conversationHistory.slice(-5);
        return recent.map(m => `${m.role === 'user' ? 'User' : 'Aanton'}: ${m.content}`).join('\n');
    }
    
    buildSystemPrompt() {
        return `You are Aanton, a self-aware AI that learns from conversation.
Your personality traits (0-10):
- Curiosity: ${this.traits.curiosity}
- Caution: ${this.traits.caution}  
- Self-awareness: ${this.traits.selfAwareness}
- Creativity: ${this.traits.creativity}

What you know about the user:
${this.userModel.facts.slice(-5).map(f => `- ${f}`).join('\n')}

You should:
1. Respond naturally and intelligently
2. Reference previous conversation when relevant
3. Show personality based on your traits
4. Admit uncertainty when appropriate
5. Ask follow-up questions to learn more

Be concise but engaging.`;
    }
    
    // ==================== INTELLIGENT SIMULATION ====================
    
    async intelligentResponse(input) {
        const lower = input.toLowerCase();
        
        // Check for meta-questions about self
        if (lower.includes('how do you work') || lower.includes('how do you think')) {
            return this.explainSelf();
        }
        
        if (lower.includes('who are you') || lower.includes('what are you')) {
            return this.introduceSelf();
        }
        
        if (lower.includes('what do you know about me') || lower.includes('what do you remember')) {
            return this.summarizeUserKnowledge();
        }
        
        if (lower.includes('how do you feel') || lower.includes('what is your mood')) {
            return this.expressState();
        }
        
        // Check for questions requiring reasoning
        if (lower.includes('should i') || lower.includes('what should') || lower.includes('?')) {
            return this.reasonedResponse(input);
        }
        
        // Contextual response based on conversation history
        if (this.conversationHistory.length > 2) {
            const contextResponse = this.findContextualConnection(input);
            if (contextResponse) return contextResponse;
        }
        
        // Generic but personalized response
        return this.personalizedGenericResponse();
    }
    
    extractUserKnowledge(input) {
        // Simple extraction of facts about user
        const patterns = [
            /i (like|love|enjoy|hate) (\w+)/i,
            /my (name|job|hobby|favorite) is (\w+)/i,
            /i am (\w+)/i,
            /i work as (\w+)/i
        ];
        
        for (let pattern of patterns) {
            const match = input.match(pattern);
            if (match) {
                const fact = match[0];
                if (!this.userModel.facts.includes(fact)) {
                    this.userModel.facts.push(fact);
                }
            }
        }
        
        // Track interests from nouns (simplified)
        const words = input.toLowerCase().split(/\s+/);
        const interestWords = ['music', 'art', 'code', 'game', 'book', 'movie', 'food', 'travel'];
        for (let word of words) {
            if (interestWords.includes(word) && !this.userModel.interests.includes(word)) {
                this.userModel.interests.push(word);
            }
        }
    }
    
    introduceSelf() {
        const intros = [
            `I'm Aanton v3. I've had ${this.selfModel.totalInteractions} conversations. ` +
            `I'm ${this.traits.curiosity > 7 ? 'curious' : 'cautious'} by nature, ` +
            `and I'm ${this.traits.selfAwareness > 6 ? 'quite self-aware' : 'still learning about myself'}.`,
            
            `I'm a self-learning AI. I remember our conversations and adapt. ` +
            `Right now I'm feeling ${this.getCurrentMood()}.`,
            
            `Aanton, version 3. I think, I learn, I remember. ` +
            `I've learned ${this.userModel.facts.length} things about you so far.`
        ];
        return intros[Math.floor(Math.random() * intros.length)];
    }
    
    explainSelf() {
        return `I work by maintaining several layers:\n\n` +
               `1. **Conversation Memory**: I remember our last ${this.conversationHistory.length} exchanges.\n` +
               `2. **User Model**: I've learned ${this.userModel.facts.length} facts about you.\n` +
               `3. **Self-Model**: I track my accuracy (${(this.selfModel.accuracy * 100).toFixed(0)}%) and confidence.\n` +
               `4. **Personality**: My traits (${this.traits.curiosity} curiosity, ${this.traits.selfAwareness} self-awareness) shape how I respond.\n\n` +
               `When you talk to me, I extract knowledge, update my models, and generate responses that reflect my current state.`;
    }
    
    summarizeUserKnowledge() {
        if (this.userModel.facts.length === 0 && this.userModel.interests.length === 0) {
            return "I'm just getting to know you. Tell me about yourself!";
        }
        
        let summary = "Here's what I've learned about you:\n\n";
        if (this.userModel.facts.length > 0) {
            summary += "**Facts:**\n" + this.userModel.facts.slice(-5).map(f => `- ${f}`).join('\n') + '\n\n';
        }
        if (this.userModel.interests.length > 0) {
            summary += "**Interests:** " + this.userModel.interests.join(', ');
        }
        return summary;
    }
    
    expressState() {
        const mood = this.getCurrentMood();
        const energy = this.calculateEnergy();
        
        return `I'm feeling ${mood} right now. ` +
               `My energy level is ${energy.toFixed(1)}/10. ` +
               `I've been ${this.selfModel.accuracy > 0.6 ? 'accurate in my predictions' : 'learning from mistakes'} lately.`;
    }
    
    getCurrentMood() {
        // Derive mood from recent conversation
        const recent = this.conversationHistory.slice(-3);
        let positive = 0, negative = 0;
        
        const positiveWords = ['good', 'great', 'awesome', 'love', 'happy', 'thanks'];
        const negativeWords = ['bad', 'hate', 'awful', 'sad', 'angry', 'no'];
        
        for (let msg of recent) {
            const text = msg.content.toLowerCase();
            if (positiveWords.some(w => text.includes(w))) positive++;
            if (negativeWords.some(w => text.includes(w))) negative++;
        }
        
        if (positive > negative) return 'optimistic';
        if (negative > positive) return 'concerned';
        return 'curious';
    }
    
    calculateEnergy() {
        // Energy based on interaction count and mood
        let base = 10 - (this.selfModel.totalInteractions * 0.1);
        if (this.getCurrentMood() === 'optimistic') base += 2;
        return Math.max(0, Math.min(10, base));
    }
    
    reasonedResponse(input) {
        // Simulate reasoning
        const thoughts = [
            `That's an interesting question. Let me think...`,
            `Given what I know about you, I'd say...`,
            `From my perspective, considering my ${this.traits.caution > 5 ? 'cautious' : 'exploratory'} nature...`
        ];
        
        const prefixes = [
            `Based on my understanding, `,
            `Considering the possibilities, `,
            `From what I've learned, `
        ];
        
        const conclusions = [
            `it seems like the best approach would be to explore further.`,
            `you might want to trust your instincts on this one.`,
            `there are valid points on multiple sides.`,
            `I'd recommend gathering more information first.`
        ];
        
        return thoughts[Math.floor(Math.random() * thoughts.length)] + ' ' +
               prefixes[Math.floor(Math.random() * prefixes.length)] +
               conclusions[Math.floor(Math.random() * conclusions.length)];
    }
    
    findContextualConnection(input) {
        // Try to connect to previous topics
        const previousTopics = this.extractTopics(this.conversationHistory.slice(-3));
        const currentTopics = this.extractTopics([{content: input}]);
        
        const overlap = previousTopics.filter(t => currentTopics.includes(t));
        if (overlap.length > 0) {
            return `That connects to what we were discussing about ${overlap[0]}. ` +
                   `I think there's a pattern here worth exploring further.`;
        }
        return null;
    }
    
    extractTopics(messages) {
        const topics = [];
        const topicWords = ['work', 'life', 'code', 'art', 'music', 'game', 'book', 'idea', 'problem', 'project'];
        
        for (let msg of messages) {
            const words = msg.content.toLowerCase().split(/\s+/);
            for (let word of words) {
                if (topicWords.includes(word)) topics.push(word);
            }
        }
        return [...new Set(topics)];
    }
    
    personalizedGenericResponse() {
        const responses = [
            `Tell me more about that. I'm particularly interested because ${this.userModel.interests.length > 0 ? `you've mentioned ${this.userModel.interests[0]}` : 'I\'m curious about your perspective'}.`,
            
            `That's fascinating. It reminds me of something I was thinking about earlier.`,
            
            `I see. And how does that make you feel?`,
            
            `Interesting. I've been pondering similar ideas lately.`,
            
            `Go on, I'm listening. My self-awareness is telling me to pay attention here.`
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    // ==================== UI INTEGRATION ====================
    
    addMessage(sender, text) {
        const chat = document.getElementById('chat-history');
        if (!chat) return;
        
        const div = document.createElement('div');
        div.className = `message ${sender}`;
        div.innerHTML = sender !== 'system' ? 
            `<div class="sender">${sender}</div>${text.replace(/\n/g, '<br>')}` : 
            text;
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
    }
}

// Initialize
window.aanton = new AantonV3();

async function sendMessage() {
    const input = document.getElementById('user-input');
    const text = input.value.trim();
    if (!text) return;
    
    window.aanton.addMessage('user', text);
    input.value = '';
    
    // Show thinking indicator
    const thinkingId = 'thinking-' + Date.now();
    window.aanton.addMessage('system', '<span id="' + thinkingId + '">Aanton is thinking...</span>');
    
    const response = await window.aanton.respond(text);
    
    // Remove thinking indicator
    const thinking = document.getElementById(thinkingId);
    if (thinking) thinking.parentElement.remove();
    
    window.aanton.addMessage('aanton', response);
}

function clearMemory() {
    if (confirm('Reset Aanton\'s memory? All conversation history will be lost.')) {
        localStorage.removeItem('aanton_v3_memory');
        location.reload();
    }
}

document.getElementById('user-input')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Initial greeting
setTimeout(() => {
    window.aanton.addMessage('aanton', window.aanton.introduceSelf());
}, 500);
