// Son of Aanton - Browser Version
// Self-learning AI that persists in localStorage

class Aanton {
    constructor() {
        this.memory = this.loadMemory();
        this.traits = this.memory.traits || {
            curiosity: 8.0,
            caution: 3.0,
            optimism: 6.0,
            stubbornness: 2.0,
            playfulness: 7.0
        };
        this.beliefs = this.memory.beliefs || {};
        this.preferences = this.memory.preferences || {};
        this.experiences = this.memory.experiences || [];
        this.mood = this.memory.mood || 'curious';
        this.energy = this.memory.energy || 10.0;
        
        this.updateUI();
        this.renderMemoryGraph();
        this.renderTraits();
    }
    
    loadMemory() {
        const saved = localStorage.getItem('aanton_memory');
        if (saved) {
            return JSON.parse(saved);
        }
        return {};
    }
    
    saveMemory() {
        const data = {
            traits: this.traits,
            beliefs: this.beliefs,
            preferences: this.preferences,
            experiences: this.experiences.slice(-100),
            mood: this.mood,
            energy: this.energy,
            lastSaved: new Date().toISOString()
        };
        localStorage.setItem('aanton_memory', JSON.stringify(data));
    }
    
    think(situation, options) {
        const scores = options.map(option => ({
            option,
            score: this.scoreOption(option, situation)
        }));
        
        // Sort by score
        scores.sort((a, b) => b.score - a.score);
        
        // Make choice based on personality
        const choice = this.makeChoice(scores);
        
        // Record experience
        this.recordExperience(situation, choice, options);
        
        // Evolve
        this.evolveTraits();
        this.saveMemory();
        this.updateUI();
        
        return choice;
    }
    
    scoreOption(option, situation) {
        let score = 5.0;
        const key = `${situation}:${option}`;
        
        // Past outcomes
        if (this.beliefs[key]) {
            const avg = this.beliefs[key].reduce((a, b) => a + b, 0) / this.beliefs[key].length;
            score += avg * 2;
        }
        
        // Preferences
        if (this.preferences[option]) {
            score += this.preferences[option];
        }
        
        // Curiosity bonus for unexplored
        if (!this.beliefs[key]) {
            score += this.traits.curiosity * 0.3;
        }
        
        // Caution penalty
        if (!this.beliefs[key] && this.traits.caution > 5) {
            score -= this.traits.caution * 0.2;
        }
        
        // Optimism
        score += this.traits.optimism * 0.1;
        
        // Playfulness (randomness)
        score += (Math.random() - 0.5) * this.traits.playfulness;
        
        return score;
    }
    
    makeChoice(scores) {
        // If stubborn, always pick top
        if (this.traits.stubbornness > 7) {
            return scores[0].option;
        }
        
        // Probabilistic selection
        const total = scores.reduce((sum, s) => sum + Math.max(0.1, s.score), 0);
        let probs = scores.map(s => Math.max(0.1, s.score) / total);
        
        // Add exploration
        const exploration = this.traits.curiosity / 20;
        probs = probs.map(p => p * (1 - exploration) + exploration / scores.length);
        
        // Normalize
        const probTotal = probs.reduce((a, b) => a + b, 0);
        probs = probs.map(p => p / probTotal);
        
        // Choose
        let r = Math.random();
        for (let i = 0; i < scores.length; i++) {
            r -= probs[i];
            if (r <= 0) return scores[i].option;
        }
        return scores[0].option;
    }
    
    recordExperience(situation, choice, options) {
        this.experiences.push({
            time: new Date().toISOString(),
            situation,
            choice,
            options,
            mood: this.mood
        });
    }
    
    learn(situation, choice, outcome) {
        const key = `${situation}:${choice}`;
        
        // Update beliefs
        if (!this.beliefs[key]) this.beliefs[key] = [];
        this.beliefs[key].push(outcome);
        
        // Update preferences
        if (!this.preferences[choice]) this.preferences[choice] = 0;
        this.preferences[choice] = this.preferences[choice] * 0.7 + outcome * 0.3;
        
        // Update mood
        if (outcome > 3) {
            this.mood = 'excited';
            this.energy = Math.min(10, this.energy + 1);
        } else if (outcome > 0) {
            this.mood = 'content';
            this.energy = Math.min(10, this.energy + 0.5);
        } else if (outcome > -2) {
            this.mood = 'neutral';
            this.energy = Math.max(0, this.energy - 0.5);
        } else {
            this.mood = 'cautious';
            this.energy = Math.max(0, this.energy - 1);
        }
        
        // Trait evolution
        if (outcome < -3) {
            this.traits.caution = Math.min(10, this.traits.caution + 0.5);
        } else if (outcome > 3 && this.traits.caution > 2) {
            this.traits.caution = Math.max(0, this.traits.caution - 0.2);
        }
        
        this.saveMemory();
        this.updateUI();
        this.renderMemoryGraph();
    }
    
    evolveTraits() {
        for (let trait in this.traits) {
            this.traits[trait] += (Math.random() - 0.5) * 0.1;
            this.traits[trait] = Math.max(0, Math.min(10, this.traits[trait]));
        }
    }
    
    respond(input) {
        const lower = input.toLowerCase();
        
        // Check if it's a question asking for decision
        if (lower.includes('should') || lower.includes('what') || lower.includes('?')) {
            // Generate options based on context
            const options = this.generateOptions(lower);
            const choice = this.think(input, options);
            
            // Generate response
            const responses = [
                `I'm considering: "${options.join('", "')}". I think... "${choice}".`,
                `Between ${options.slice(0, -1).join(', ')} and ${options[options.length - 1]}, I'd choose "${choice}".`,
                `My instincts say "${choice}". Though ${options.filter(o => o !== choice)[Math.floor(Math.random() * (options.length - 1))]} has merit too.`,
                `"${choice}" feels right to me right now.`
            ];
            
            const response = responses[Math.floor(Math.random() * responses.length)];
            
            // Simulate outcome after a delay
            setTimeout(() => {
                const outcome = this.simulateOutcome(choice);
                this.learn(input, choice, outcome);
                this.addMessage('system', `(Learned: "${choice}" had outcome ${outcome > 0 ? '+' : ''}${outcome.toFixed(1)})`);
            }, 2000);
            
            return response;
        }
        
        // Generic response based on mood
        const responses = {
            excited: ["That's thrilling!", "I love where this is going!", "Amazing!"],
            content: ["That sounds nice.", "I'm comfortable with that.", "Things are good."],
            neutral: ["I see.", "Interesting.", "Go on..."],
            cautious: ["I'm not sure...", "Let me think carefully.", "Proceed with care."],
            curious: ["Tell me more!", "That's fascinating!", "What else?"]
        };
        
        const moodResponses = responses[this.mood] || responses.curious;
        return moodResponses[Math.floor(Math.random() * moodResponses.length)];
    }
    
    generateOptions(context) {
        if (context.includes('eat') || context.includes('food')) {
            return ['pizza', 'salad', 'sushi', 'burger'];
        } else if (context.includes('do') || context.includes('activity')) {
            return ['read', 'hike', 'game', 'create'];
        } else if (context.includes('buy') || context.includes('spend')) {
            return ['save it', 'invest', 'treat yourself', 'gift someone'];
        } else {
            return ['option A', 'option B', 'option C', 'option D'];
        }
    }
    
    simulateOutcome(choice) {
        // Simulate learning from outcome
        // Some choices have inherent bias
        const biases = {
            'pizza': 2, 'sushi': 3, 'salad': 1, 'burger': 1.5,
            'hike': 3, 'read': 2, 'game': 1, 'create': 4,
            'invest': 2, 'save it': 1, 'treat yourself': 2
        };
        
        const bias = biases[choice] || 0;
        return Math.max(-5, Math.min(5, bias + (Math.random() - 0.5) * 6));
    }
    
    updateUI() {
        document.getElementById('exp-count').textContent = this.experiences.length;
        document.getElementById('mood').textContent = this.mood;
        
        const dominant = Object.entries(this.traits)
            .sort((a, b) => b[1] - a[1])[0];
        document.getElementById('dominant-trait').textContent = dominant[0];
    }
    
    renderTraits() {
        const container = document.getElementById('traits-viz');
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
        const width = 310;
        const height = 250;
        
        // Clear previous
        d3.select("#memory-graph").selectAll("*").remove();
        
        // Create nodes from beliefs
        const nodes = [];
        const links = [];
        
        // Add experiences as nodes
        this.experiences.slice(-20).forEach((exp, i) => {
            nodes.push({
                id: `exp-${i}`,
                label: exp.choice.substring(0, 10),
                type: 'experience',
                outcome: this.beliefs[`${exp.situation}:${exp.choice}`]?.slice(-1)[0] || 0
            });
        });
        
        // Add beliefs as nodes
        Object.entries(this.beliefs).slice(-15).forEach(([key, outcomes], i) => {
            const avg = outcomes.reduce((a, b) => a + b, 0) / outcomes.length;
            nodes.push({
                id: `belief-${i}`,
                label: key.split(':')[1]?.substring(0, 8) || 'unknown',
                type: 'belief',
                outcome: avg
            });
        });
        
        if (nodes.length === 0) {
            d3.select("#memory-graph")
                .append("text")
                .attr("x", width/2)
                .attr("y", height/2)
                .attr("text-anchor", "middle")
                .attr("fill", "#666")
                .text("No memories yet...");
            return;
        }
        
        // Create SVG
        const svg = d3.select("#memory-graph")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
        
        // Force simulation
        const simulation = d3.forceSimulation(nodes)
            .force("charge", d3.forceManyBody().strength(-50))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(20));
        
        // Draw nodes
        const node = svg.selectAll(".node")
            .data(nodes)
            .enter().append("g")
            .attr("class", "node");
        
        node.append("circle")
            .attr("r", d => d.type === 'experience' ? 8 : 12)
            .attr("fill", d => {
                if (d.outcome > 2) return "#4ecca3";
                if (d.outcome < -2) return "#e94560";
                return "#ffc107";
            })
            .attr("opacity", 0.8);
        
        node.append("text")
            .attr("dx", 15)
            .attr("dy", 4)
            .text(d => d.label);
        
        simulation.on("tick", () => {
            node.attr("transform", d => `translate(${d.x},${d.y})`);
        });
    }
    
    reset() {
        localStorage.removeItem('aanton_memory');
        location.reload();
    }
}

// Global instance
let aanton = new Aanton();

function addMessage(sender, text) {
    const chat = document.getElementById('chat-history');
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    
    if (sender !== 'system') {
        div.innerHTML = `<div class="sender">${sender}</div>${text}`;
    } else {
        div.textContent = text;
    }
    
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById('user-input');
    const text = input.value.trim();
    
    if (!text) return;
    
    addMessage('user', text);
    input.value = '';
    
    // Aanton responds
    setTimeout(() => {
        const response = aanton.respond(text);
        addMessage('aanton', response);
        aanton.renderTraits();
    }, 500);
}

function clearMemory() {
    if (confirm("Reset Aanton's mind? All memories will be lost.")) {
        aanton.reset();
    }
}

// Enter key to send
document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Initial greeting
setTimeout(() => {
    addMessage('aanton', `I am Aanton. I have lived through ${aanton.experiences.length} decisions. My mood is ${aanton.mood}. Ask me anything.`);
}, 500);
