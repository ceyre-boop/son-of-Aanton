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
        const learned = this.extractUserKnowledge(input);
        
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
        
        // Check for questions about user's preferences/likes
        if ((lower.includes('what do i like') || lower.includes('what do I like') || 
             lower.includes('what do you know i like')) &&
            (this.userModel.facts.length > 0 || this.userModel.interests.length > 0)) {
            return this.answerWhatILike();
        }
        
        // Check for specific attribute questions (what number am I, what am I, etc)
        const attributeMatch = lower.match(/what (number|name|job|am i|am i called)/);
        if (attributeMatch) {
            return this.answerAttributeQuestion(attributeMatch[1]);
        }
        
        // Check if user is sharing a fact (like/hate/am/work)
        if (lower.match(/i (like|love|enjoy|hate|am|work)/)) {
            return this.acknowledgeLearning(input);
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
            /i (like|love|enjoy|hate) ([^.]+)/i,  // Capture everything after like/love/enjoy/hate
            /my (name|job|hobby|favorite) is ([^.]+)/i,
            /i am (a |an )?([^.]+)/i,
            /i work as (a |an )?([^.]+)/i
        ];
        
        let learnedSomething = false;
        for (let pattern of patterns) {
            const match = input.match(pattern);
            if (match) {
                const fact = match[0].trim();
                if (!this.userModel.facts.includes(fact)) {
                    this.userModel.facts.push(fact);
                    console.log('[Learned]', fact);
                    learnedSomething = true;
                }
            }
        }
        
        // Track interests from nouns (simplified)
        const words = input.toLowerCase().split(/\s+/);
        const interestWords = ['music', 'art', 'code', 'game', 'book', 'movie', 'food', 'travel', 'pizza', 'sushi'];
        for (let word of words) {
            if (interestWords.includes(word) && !this.userModel.interests.includes(word)) {
                this.userModel.interests.push(word);
                learnedSomething = true;
            }
        }
        
        return learnedSomething;
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
    
    acknowledgeLearning(input) {
        // Extract what was learned
        const likeMatch = input.match(/i (like|love|enjoy|hate) ([^.]+)/i);
        const amMatch = input.match(/i am (a |an )?([^.]+)/i);
        
        const acknowledgments = [
            "Noted. I'll remember that.",
            "Interesting. I'm adding that to what I know about you.",
            "Good to know. I'm learning more about you with every message.",
            "I'll keep that in mind.",
            "Thanks for sharing that with me."
        ];
        
        if (likeMatch) {
            const thing = likeMatch[2].trim();
            const verb = likeMatch[1];
            return `So you ${verb} ${thing}? ${acknowledgments[Math.floor(Math.random() * acknowledgments.length)]}`;
        }
        
        if (amMatch) {
            const thing = amMatch[2].trim();
            return `You're ${thing}? ${acknowledgments[Math.floor(Math.random() * acknowledgments.length)]}`;
        }
        
        return acknowledgments[Math.floor(Math.random() * acknowledgments.length)];
    }
    
    answerAttributeQuestion(attribute) {
        // Search facts for the attribute
        const relevantFacts = this.userModel.facts.filter(f => {
            const lowerFact = f.toLowerCase();
            if (attribute === 'number') return lowerFact.includes('number');
            if (attribute === 'name') return lowerFact.includes('name') || lowerFact.includes('i am');
            if (attribute === 'job') return lowerFact.includes('job') || lowerFact.includes('work');
            return lowerFact.includes(attribute);
        });
        
        if (relevantFacts.length > 0) {
            // Return the most recent matching fact
            const fact = relevantFacts[relevantFacts.length - 1];
            // Clean up the fact for presentation
            const cleaned = fact.replace(/^i am /i, '').replace(/^i work as /i, '');
            return `You told me you're ${cleaned}. Is that correct?`;
        }
        
        return `I don't know yet. What ${attribute} are you?`;
    }
    
    answerWhatILike() {
        // Find likes from facts
        const likes = this.userModel.facts.filter(f => {
            const lower = f.toLowerCase();
            return lower.includes('like') || lower.includes('love') || lower.includes('enjoy');
        });
        
        if (likes.length > 0) {
            const things = likes.map(f => {
                const match = f.match(/i (like|love|enjoy|hate) ([^.]+)/i);
                return match ? match[2].trim() : f;
            });
            return `You told me you like: ${things.join(', ')}. Did I get that right?`;
        }
        
        if (this.userModel.interests.length > 0) {
            return `I know you're interested in ${this.userModel.interests.join(', ')}. Tell me more about what you like!`;
        }
        
        return "I'm still learning what you like. Tell me more about your preferences!";
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
    
    updateUI() {
        const countEl = document.getElementById('interaction-count');
        const moodEl = document.getElementById('mood');
        const energyEl = document.getElementById('energy');
        const factsEl = document.getElementById('user-facts');
        
        if (countEl) countEl.textContent = this.selfModel.totalInteractions;
        if (moodEl) moodEl.textContent = this.getCurrentMood();
        if (energyEl) energyEl.textContent = this.calculateEnergy().toFixed(1) + '/10';
        
        if (factsEl) {
            if (this.userModel.facts.length === 0) {
                factsEl.textContent = 'Nothing yet...';
            } else {
                factsEl.innerHTML = this.userModel.facts.slice(-5).map(f => `• ${f}`).join('<br>');
            }
        }
        
        this.renderTraits();
        this.renderMemoryGraph();
    }
    
    renderTraits() {
        const container = document.getElementById('traits-viz');
        if (!container) return;
        
        container.innerHTML = '';
        for (let [trait, value] of Object.entries(this.traits)) {
            const div = document.createElement('div');
            div.className = 'trait-bar';
            div.innerHTML = `
                <label>${trait} (${value.toFixed(1)})</label>
                <div class="bar">
                    <div class="bar-fill" style="width: ${value * 10}%"></div>
                </div>
            `;
            container.appendChild(div);
        }
    }
    
    renderMemoryGraph() {
        const container = document.getElementById('memory-graph');
        if (!container || typeof d3 === 'undefined') return;
        
        const width = 310;
        const height = 250;
        
        // Clear previous
        d3.select("#memory-graph").selectAll("*").remove();
        
        // Create nodes from conversation history and user knowledge
        const nodes = [];
        
        // Add conversation topics as nodes
        const topics = this.extractTopics(this.conversationHistory.slice(-10));
        topics.forEach((topic, i) => {
            nodes.push({
                id: `topic-${i}`,
                label: topic,
                type: 'topic',
                r: 8 + Math.random() * 5
            });
        });
        
        // Add user facts as nodes
        this.userModel.facts.slice(-5).forEach((fact, i) => {
            const shortFact = fact.length > 15 ? fact.substring(0, 12) + '...' : fact;
            nodes.push({
                id: `fact-${i}`,
                label: shortFact,
                type: 'fact',
                r: 10
            });
        });
        
        // Add self as center node
        nodes.push({
            id: 'self',
            label: 'Aanton',
            type: 'self',
            r: 15
        });
        
        if (nodes.length <= 1) {
            d3.select("#memory-graph")
                .append("div")
                .style("padding", "20px")
                .style("color", "#666")
                .style("font-size", "12px")
                .text("Talking to you... memories forming...");
            return;
        }
        
        // Create SVG
        const svg = d3.select("#memory-graph")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
        
        // Create links (connect everything to center)
        const links = nodes
            .filter(n => n.id !== 'self')
            .map(n => ({ source: 'self', target: n.id }));
        
        // Force simulation
        const simulation = d3.forceSimulation(nodes)
            .force("charge", d3.forceManyBody().strength(-100))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(d => d.r + 5))
            .force("link", d3.forceLink(links).id(d => d.id).distance(60));
        
        // Draw links
        const link = svg.selectAll(".link")
            .data(links)
            .enter().append("line")
            .attr("class", "link")
            .attr("stroke", "#4a4a6a")
            .attr("stroke-width", 1)
            .attr("opacity", 0.6);
        
        // Draw nodes
        const node = svg.selectAll(".node")
            .data(nodes)
            .enter().append("g")
            .attr("class", "node");
        
        node.append("circle")
            .attr("r", d => d.r)
            .attr("fill", d => {
                if (d.type === 'self') return "#e94560";
                if (d.type === 'fact') return "#4ecca3";
                return "#ffc107";
            })
            .attr("opacity", 0.8);
        
        node.append("text")
            .attr("dx", d => d.r + 3)
            .attr("dy", 4)
            .text(d => d.label)
            .attr("fill", "#eaeaea")
            .attr("font-size", "10px");
        
        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            
            node.attr("transform", d => `translate(${d.x},${d.y})`);
        });
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
    window.aanton.updateUI();
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

// Initial greeting and UI setup
setTimeout(() => {
    window.aanton.addMessage('aanton', window.aanton.introduceSelf());
    window.aanton.updateUI();
}, 500);
