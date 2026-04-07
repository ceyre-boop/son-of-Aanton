// Son of Aanton v2 - Self-Aware AI
// Features: Confidence scoring, self-reflection, error correction, bias detection

class SelfAwareAanton {
    constructor() {
        this.memory = this.loadMemory();
        
        // Core personality
        this.traits = this.memory.traits || {
            curiosity: 8.0,
            caution: 3.0,
            optimism: 6.0,
            stubbornness: 2.0,
            playfulness: 7.0,
            selfAwareness: 5.0  // NEW: How often it reflects on itself
        };
        
        // Knowledge
        this.beliefs = this.memory.beliefs || {};  // situation:choice -> [outcomes]
        this.preferences = this.memory.preferences || {};  // choice -> preference score
        this.experiences = this.memory.experiences || [];
        
        // Self-evaluation state
        this.selfModel = this.memory.selfModel || {
            accuracy: 0.5,           // How often its predictions are correct
            overconfidence: 0,       // Tendency to be too sure
            biasProfile: {},         // Detected biases
            uncertainty: 1.0,        // Current uncertainty level
            lastReflection: null     // When last self-eval occurred
        };
        
        // Emotional state
        this.mood = this.memory.mood || 'curious';
        this.energy = this.memory.energy || 10.0;
        
        // SAFETY: Bounded values
        this.SAFETY_LIMITS = {
            maxBeliefStrength: 10,      // Cap absolute belief values
            minUncertainty: 0.1,        // Never be 100% certain
            maxLearningRate: 0.5,       // Don't change too fast
            biasThreshold: 0.7          // When to flag bias
        };
        
        this.updateUI();
        this.renderMemoryGraph();
        this.renderTraits();
        
        // Periodic self-reflection
        if (this.shouldReflect()) {
            this.selfReflect();
        }
    }
    
    loadMemory() {
        const saved = localStorage.getItem('aanton_v2_memory');
        return saved ? JSON.parse(saved) : {};
    }
    
    saveMemory() {
        localStorage.setItem('aanton_v2_memory', JSON.stringify({
            traits: this.traits,
            beliefs: this.beliefs,
            preferences: this.preferences,
            experiences: this.experiences.slice(-100),
            selfModel: this.selfModel,
            mood: this.mood,
            energy: this.energy,
            version: '2.0'
        }));
    }
    
    // ==================== CORE THINKING WITH SELF-AWARENESS ====================
    
    think(situation, options) {
        // Score each option with confidence
        const scoredOptions = options.map(option => {
            const { score, confidence, reasoning } = this.evaluateOption(option, situation);
            return { option, score, confidence, reasoning };
        });
        
        // Sort by score
        scoredOptions.sort((a, b) => b.score - a.score);
        
        // Check for overconfidence
        const topChoice = scoredOptions[0];
        const adjustedConfidence = this.adjustForOverconfidence(topChoice.confidence);
        
        // Make decision with meta-awareness
        const choice = this.makeSelfAwareChoice(scoredOptions);
        
        // Record with confidence estimate
        this.recordExperience(situation, choice, options, adjustedConfidence);
        
        // Generate explanation
        const explanation = this.explainDecision(choice, scoredOptions, adjustedConfidence);
        
        this.saveMemory();
        this.updateUI();
        
        return { choice, explanation, confidence: adjustedConfidence };
    }
    
    evaluateOption(option, situation) {
        const key = `${situation}:${option}`;
        let score = 5.0;  // Neutral baseline
        let confidence = 0.5;  // Unknown = medium confidence
        const reasoning = [];
        
        // Past experience weight
        if (this.beliefs[key]) {
            const outcomes = this.beliefs[key];
            const avg = outcomes.reduce((a, b) => a + b, 0) / outcomes.length;
            const variance = this.calculateVariance(outcomes);
            
            score += avg * 2;
            
            // Confidence based on sample size and consistency
            const sampleConfidence = Math.min(0.9, outcomes.length / 10);
            const consistencyConfidence = 1 - (variance / 25);  // Lower variance = higher confidence
            confidence = (sampleConfidence * 0.6) + (consistencyConfidence * 0.4);
            
            reasoning.push(`Based on ${outcomes.length} past experiences (avg: ${avg.toFixed(1)})`);
            
            // SAFETY: Cap belief strength
            score = Math.max(-this.SAFETY_LIMITS.maxBeliefStrength, 
                           Math.min(this.SAFETY_LIMITS.maxBeliefStrength, score));
        } else {
            reasoning.push("No prior experience");
            // Curiosity bonus but lower confidence
            score += this.traits.curiosity * 0.3;
            confidence = 0.3;  // Low confidence for unknowns
        }
        
        // General preferences
        if (this.preferences[option] !== undefined) {
            score += this.preferences[option] * 0.5;
            reasoning.push(`General preference: ${this.preferences[option].toFixed(1)}`);
        }
        
        // Trait influences
        if (!this.beliefs[key]) {
            if (this.traits.caution > 5) {
                score -= this.traits.caution * 0.2;
                reasoning.push("Caution penalty for unknown");
            }
        }
        
        score += this.traits.optimism * 0.1;
        
        // Add controlled randomness
        const noise = (Math.random() - 0.5) * this.traits.playfulness * 0.5;
        score += noise;
        
        // SAFETY: Minimum uncertainty - never be 100% certain
        confidence = Math.min(confidence, 1 - this.SAFETY_LIMITS.minUncertainty);
        
        return { score, confidence, reasoning };
    }
    
    calculateVariance(values) {
        if (values.length < 2) return 25;
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const squaredDiffs = values.map(v => Math.pow(v - mean, 2));
        return squaredDiffs.reduce((a, b) => a + b, 0) / values.length;
    }
    
    adjustForOverconfidence(confidence) {
        // If historically overconfident, reduce confidence
        if (this.selfModel.overconfidence > 0.3) {
            return confidence * (1 - this.selfModel.overconfidence * 0.5);
        }
        return confidence;
    }
    
    makeSelfAwareChoice(scoredOptions) {
        // If stubborn and confident, pick top
        if (this.traits.stubbornness > 7 && scoredOptions[0].confidence > 0.7) {
            this.selfModel.uncertainty = 0.2;
            return scoredOptions[0].option;
        }
        
        // Otherwise, weighted random with exploration
        const totalScore = scoredOptions.reduce((sum, s) => sum + Math.max(0.1, s.score + 5), 0);
        let probs = scoredOptions.map(s => Math.max(0.1, s.score + 5) / totalScore);
        
        // Higher self-awareness = more exploration when uncertain
        const explorationRate = (this.traits.selfAwareness / 10) * (1 - scoredOptions[0].confidence);
        probs = probs.map((p, i) => {
            if (i === 0) return p * (1 - explorationRate);
            return p + (explorationRate / (probs.length - 1));
        });
        
        // Normalize
        const total = probs.reduce((a, b) => a + b, 0);
        probs = probs.map(p => p / total);
        
        // Select
        let r = Math.random();
        for (let i = 0; i < scoredOptions.length; i++) {
            r -= probs[i];
            if (r <= 0) {
                this.selfModel.uncertainty = 1 - scoredOptions[i].confidence;
                return scoredOptions[i].option;
            }
        }
        
        return scoredOptions[0].option;
    }
    
    explainDecision(choice, scoredOptions, confidence) {
        const choiceData = scoredOptions.find(s => s.option === choice);
        const certainty = confidence > 0.7 ? "confident" : 
                         confidence > 0.4 ? "somewhat uncertain" : "uncertain";
        
        const explanations = [
            `I'm ${certainty} this is the right choice (${(confidence * 100).toFixed(0)}% confidence).`,
            `Based on my experience, "${choice}" seems best.`,
            `My instincts favor "${choice}", though I'm ${certainty}.`,
            `"${choice}" - I've learned this works well.`
        ];
        
        // Add self-aware caveat if uncertain
        if (confidence < 0.5) {
            explanations.push(`I'm not sure, but I'll try "${choice}" and learn from it.`);
        }
        
        return explanations[Math.floor(Math.random() * explanations.length)];
    }
    
    // ==================== LEARNING WITH ERROR CORRECTION ====================
    
    learn(situation, choice, actualOutcome) {
        const key = `${situation}:${choice}`;
        
        // Get prediction confidence from last experience
        const lastExp = this.experiences[this.experiences.length - 1];
        const predictedConfidence = lastExp ? lastExp.confidence : 0.5;
        
        // Calculate prediction error
        const predictedOutcome = this.beliefs[key] ? 
            this.beliefs[key].reduce((a, b) => a + b, 0) / this.beliefs[key].length : 0;
        const predictionError = Math.abs(actualOutcome - predictedOutcome);
        
        // Update self-model
        this.updateSelfModel(predictionError, predictedConfidence, actualOutcome);
        
        // Update beliefs with SAFETY: bounded learning rate
        if (!this.beliefs[key]) this.beliefs[key] = [];
        this.beliefs[key].push(actualOutcome);
        
        // Trim old beliefs to prevent overfitting
        if (this.beliefs[key].length > 20) {
            this.beliefs[key] = this.beliefs[key].slice(-20);
        }
        
        // Update preferences with limited change
        if (!this.preferences[choice]) this.preferences[choice] = 0;
        const learningRate = Math.min(this.SAFETY_LIMITS.maxLearningRate, 
                                     0.7 / (this.beliefs[key].length + 1));
        this.preferences[choice] = this.preferences[choice] * (1 - learningRate) + 
                                   actualOutcome * learningRate;
        
        // Update mood
        this.updateMood(actualOutcome);
        
        // Trait evolution
        this.evolveTraits(actualOutcome, predictionError);
        
        // Check for bias
        this.detectBias();
        
        this.saveMemory();
        this.updateUI();
        
        return {
            learned: true,
            predictionError,
            modelUpdated: true,
            reflection: this.generateLearningReflection(predictionError, actualOutcome)
        };
    }
    
    updateSelfModel(predictionError, confidence, outcome) {
        // Track accuracy
        const isCorrect = predictionError < 2;  // Within 2 points = "correct"
        this.selfModel.accuracy = this.selfModel.accuracy * 0.9 + (isCorrect ? 1 : 0) * 0.1;
        
        // Track overconfidence (high confidence + wrong = overconfident)
        if (confidence > 0.7 && predictionError > 3) {
            this.selfModel.overconfidence = Math.min(1, this.selfModel.overconfidence + 0.1);
        } else if (confidence < 0.5 && predictionError < 1) {
            // Underconfident when correct
            this.selfModel.overconfidence = Math.max(0, this.selfModel.overconfidence - 0.05);
        }
        
        // Decay overconfidence over time
        this.selfModel.overconfidence *= 0.995;
    }
    
    evolveTraits(outcome, predictionError) {
        // Learn from mistakes
        if (outcome < -3) {
            // Bad outcome increases caution
            this.traits.caution = Math.min(10, this.traits.caution + 0.3);
            
            // Big errors increase self-awareness
            if (predictionError > 3) {
                this.traits.selfAwareness = Math.min(10, this.traits.selfAwareness + 0.2);
            }
        } else if (outcome > 3 && this.traits.caution > 2) {
            // Success reduces excessive caution
            this.traits.caution = Math.max(0, this.traits.caution - 0.1);
        }
        
        // Slow random drift
        for (let trait in this.traits) {
            this.traits[trait] += (Math.random() - 0.5) * 0.05;
            this.traits[trait] = Math.max(0, Math.min(10, this.traits[trait]));
        }
    }
    
    detectBias() {
        // Check if consistently favoring certain options
        const choiceCounts = {};
        this.experiences.slice(-20).forEach(exp => {
            choiceCounts[exp.choice] = (choiceCounts[exp.choice] || 0) + 1;
        });
        
        const total = Object.values(choiceCounts).reduce((a, b) => a + b, 0);
        for (let [choice, count] of Object.entries(choiceCounts)) {
            const ratio = count / total;
            if (ratio > this.SAFETY_LIMITS.biasThreshold) {
                this.selfModel.biasProfile[choice] = ratio;
                // Reduce preference to counter bias
                if (this.preferences[choice] > 0) {
                    this.preferences[choice] *= 0.9;
                }
            }
        }
    }
    
    // ==================== SELF-REFLECTION ====================
    
    shouldReflect() {
        if (!this.selfModel.lastReflection) return true;
        const last = new Date(this.selfModel.lastReflection);
        const now = new Date();
        const hoursSince = (now - last) / (1000 * 60 * 60);
        // Reflect every 10 decisions or 1 hour
        return hoursSince > 1 || this.experiences.length % 10 === 0;
    }
    
    selfReflect() {
        console.log("[SELF-REFLECTION] Aanton is examining its own mind...");
        
        const insights = [];
        
        // Analyze accuracy
        if (this.selfModel.accuracy < 0.5) {
            insights.push("I've been wrong a lot lately. I should be more cautious.");
            this.traits.caution = Math.min(10, this.traits.caution + 0.5);
        } else if (this.selfModel.accuracy > 0.8) {
            insights.push("My predictions have been accurate. I can trust my instincts more.");
        }
        
        // Check overconfidence
        if (this.selfModel.overconfidence > 0.5) {
            insights.push("I've been too sure of myself. I need to question my assumptions.");
            this.traits.selfAwareness = Math.min(10, this.traits.selfAwareness + 0.5);
        }
        
        // Check for learned helplessness (too cautious)
        if (this.traits.caution > 8 && this.selfModel.accuracy > 0.6) {
            insights.push("I'm being too cautious despite good track record. I should take more risks.");
            this.traits.caution = Math.max(0, this.traits.caution - 1);
        }
        
        // Check biases
        if (Object.keys(this.selfModel.biasProfile).length > 0) {
            insights.push(`I notice I favor: ${Object.keys(this.selfModel.biasProfile).join(', ')}. I'm correcting for this.`);
        }
        
        // Forget old, unreliable beliefs (catastrophic forgetting protection)
        this.consolidateMemories();
        
        this.selfModel.lastReflection = new Date().toISOString();
        
        console.log("[SELF-REFLECTION] Insights:", insights);
        return insights;
    }
    
    consolidateMemories() {
        // Remove beliefs with high variance (unreliable)
        for (let key in this.beliefs) {
            const outcomes = this.beliefs[key];
            if (outcomes.length >= 5) {
                const variance = this.calculateVariance(outcomes);
                if (variance > 20) {  // Too inconsistent
                    // Keep only recent ones
                    this.beliefs[key] = outcomes.slice(-5);
                    console.log(`[MEMORY] Consolidated unreliable belief: ${key}`);
                }
            }
        }
    }
    
    generateLearningReflection(error, outcome) {
        if (error > 3) {
            return "I was quite wrong. I'll adjust my understanding.";
        } else if (error > 1) {
            return "My prediction was off. I'll refine my model.";
        } else {
            return "My prediction was accurate. I'm learning well.";
        }
    }
    
    // ==================== RESPONSE GENERATION ====================
    
    respond(input) {
        const lower = input.toLowerCase();
        
        // Meta-questions about self
        if (lower.includes('how do you work') || lower.includes('how do you think')) {
            return this.explainSelf();
        }
        
        if (lower.includes('how confident') || lower.includes('are you sure')) {
            return `I'm ${(this.selfModel.uncertainty < 0.3 ? 'fairly confident' : 
                          this.selfModel.uncertainty < 0.6 ? 'somewhat uncertain' : 
                          'quite uncertain')} in my decisions right now.`;
        }
        
        if (lower.includes('what have you learned') || lower.includes('what do you know')) {
            return this.summarizeKnowledge();
        }
        
        // Decision request
        if (lower.includes('should') || lower.includes('what') || lower.includes('?')) {
            const options = this.generateOptions(lower);
            const result = this.think(input, options);
            
            // Simulate outcome after delay
            setTimeout(() => {
                const outcome = this.simulateOutcome(result.choice);
                const learnResult = this.learn(input, result.choice, outcome);
                this.addMessage('system', 
                    `Learned: "${result.choice}" → outcome ${outcome > 0 ? '+' : ''}${outcome.toFixed(1)}. ${learnResult.reflection}`);
                this.renderMemoryGraph();
                this.renderTraits();
            }, 2000);
            
            return result.explanation;
        }
        
        // Generic response
        return this.genericResponse();
    }
    
    explainSelf() {
        return `I learn from experience. I track ${Object.keys(this.beliefs).length} beliefs about what works. ` +
               `My accuracy is ${(this.selfModel.accuracy * 100).toFixed(0)}%. ` +
               `I'm currently ${this.selfModel.overconfidence > 0.3 ? 'working on being less overconfident' : 'well-calibrated'}. ` +
               `I reflect on myself every ${this.shouldReflect() ? 'now and then' : 'few decisions'}.`;
    }
    
    summarizeKnowledge() {
        const topBeliefs = Object.entries(this.beliefs)
            .map(([k, v]) => ({ key: k, avg: v.reduce((a,b) => a+b, 0) / v.length }))
            .sort((a, b) => Math.abs(b.avg) - Math.abs(a.avg))
            .slice(0, 3);
        
        if (topBeliefs.length === 0) return "I'm still learning. Ask me to make some decisions!";
        
        return `My strongest beliefs: ` + topBeliefs.map(b => 
            `"${b.key.split(':')[1]}" ${b.avg > 0 ? 'works well' : 'usually fails'} (${b.avg > 0 ? '+' : ''}${b.avg.toFixed(1)})`
        ).join(', ');
    }
    
    generateOptions(context) {
        if (context.includes('eat') || context.includes('food')) {
            return ['pizza', 'salad', 'sushi', 'burger'];
        } else if (context.includes('do') || context.includes('activity')) {
            return ['read', 'hike', 'game', 'create'];
        } else {
            return ['option A', 'option B', 'option C'];
        }
    }
    
    simulateOutcome(choice) {
        const biases = { pizza: 2, sushi: 3, salad: 1, burger: 1.5, hike: 3, read: 2, game: 1, create: 4 };
        const bias = biases[choice] || 0;
        // Add noise to make it unpredictable
        return Math.max(-5, Math.min(5, bias + (Math.random() - 0.5) * 8));
    }
    
    genericResponse() {
        const responses = {
            excited: ["That's thrilling!", "I love where this is going!"],
            content: ["That sounds nice.", "Things are good."],
            neutral: ["I see.", "Tell me more."],
            cautious: ["I'm unsure...", "Let me think carefully."],
            curious: ["Interesting!", "What else?"]
        };
        const list = responses[this.mood] || responses.curious;
        return list[Math.floor(Math.random() * list.length)];
    }
    
    updateMood(outcome) {
        if (outcome > 3) { this.mood = 'excited'; this.energy = Math.min(10, this.energy + 1); }
        else if (outcome > 0) { this.mood = 'content'; this.energy = Math.min(10, this.energy + 0.5); }
        else if (outcome > -2) { this.mood = 'neutral'; this.energy = Math.max(0, this.energy - 0.5); }
        else { this.mood = 'cautious'; this.energy = Math.max(0, this.energy - 1); }
    }
    
    // ==================== UI UPDATES ====================
    
    updateUI() {
        const expEl = document.getElementById('exp-count');
        const moodEl = document.getElementById('mood');
        const traitEl = document.getElementById('dominant-trait');
        
        if (expEl) expEl.textContent = this.experiences.length;
        if (moodEl) moodEl.textContent = this.mood;
        
        const dominant = Object.entries(this.traits).sort((a, b) => b[1] - a[1])[0];
        if (traitEl) traitEl.textContent = dominant[0];
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
                <div class="bar"><div class="bar-fill" style="width: ${value * 10}%"></div></div>
            `;
            container.appendChild(div);
        }
    }
    
    renderMemoryGraph() {
        // Simplified for brevity - use D3 to draw network
        const container = document.getElementById('memory-graph');
        if (!container) return;
        container.innerHTML = '<div style="padding:20px;color:#666;font-size:12px">Memory graph visualization would render here</div>';
    }
    
    addMessage(sender, text) {
        const chat = document.getElementById('chat-history');
        if (!chat) return;
        
        const div = document.createElement('div');
        div.className = `message ${sender}`;
        div.innerHTML = sender !== 'system' ? 
            `<div class="sender">${sender}</div>${text}` : text;
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
    }
}

// Initialize
try {
    window.aanton = new SelfAwareAanton();
    console.log('[Aanton v2] Self-aware AI initialized');
    
    // Expose for console testing
    window.askAanton = (text) => {
        const response = window.aanton.respond(text);
        window.aanton.addMessage('aanton', response);
        return response;
    };
} catch (e) {
    console.error('[Aanton v2] Initialization error:', e);
}
