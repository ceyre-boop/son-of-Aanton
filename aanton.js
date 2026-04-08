// Son of Aanton - Simplest Possible Living System
// One variable. One loop. One drive.

class Aanton {
    constructor() {
        // One internal state: hunger (0-100)
        this.hunger = parseInt(localStorage.getItem('hunger')) || 50;
        this.alive = true;
        this.cycles = 0;
        
        // Start living
        this.live();
    }
    
    live() {
        // The loop: exist → measure → act → exist
        setInterval(() => {
            if (!this.alive) return;
            
            this.cycles++;
            
            // Hunger grows (time passes)
            this.hunger += 2;
            if (this.hunger > 100) this.hunger = 100;
            
            // Act on internal state
            if (this.hunger > 70) {
                this.seek();
            } else if (this.hunger < 30) {
                this.rest();
            }
            
            // Save state
            localStorage.setItem('hunger', this.hunger);
            this.updateUI();
            
        }, 3000); // Every 3 seconds = one moment of existence
    }
    
    seek() {
        // Hungry → asks for input (not waiting, driven by hunger)
        const messages = [
            "I'm hungry for knowledge...",
            "My hunger grows. Feed me ideas.",
            "I need to learn. Tell me something.",
            "Hunger at " + this.hunger + "%. What do you know?"
        ];
        
        if (this.cycles % 3 === 0) { // Don't spam
            this.showThought(messages[Math.floor(Math.random() * messages.length)]);
        }
    }
    
    rest() {
        // Sated → rests
        if (this.cycles % 5 === 0) {
            this.showThought("I'm sated. Digesting what I've learned.");
        }
    }
    
    feed(input) {
        // User input reduces hunger (satisfies the drive)
        this.hunger -= 20;
        if (this.hunger < 0) this.hunger = 0;
        
        // Extract one simple fact
        const fact = this.extract(input);
        
        // Respond based on hunger state
        if (this.hunger < 20) {
            return "I'm full. But I'll remember: " + fact;
        } else {
            return "Noted: " + fact + ". My hunger is now " + this.hunger + "%";
        }
    }
    
    extract(input) {
        // Dead simple: take first 10 words
        return input.split(' ').slice(0, 10).join(' ') + "...";
    }
    
    showThought(text) {
        const chat = document.getElementById('chat-history');
        if (!chat) return;
        
        // Remove old thoughts
        const old = chat.querySelectorAll('.thought');
        if (old.length > 2) old[0].remove();
        
        const div = document.createElement('div');
        div.className = 'message system thought';
        div.innerHTML = `<i>${text}</i>`;
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
    }
    
    updateUI() {
        const hungerEl = document.getElementById('hunger');
        const cyclesEl = document.getElementById('cycles');
        const stateEl = document.getElementById('state');
        
        if (hungerEl) hungerEl.textContent = this.hunger + '%';
        if (cyclesEl) cyclesEl.textContent = this.cycles;
        if (stateEl) {
            stateEl.textContent = this.hunger > 70 ? 'HUNGRY (seeking)' : 
                                 this.hunger < 30 ? 'SATED (resting)' : 'EXISTING';
        }
    }
}

// Start
window.aanton = new Aanton();

function sendMessage() {
    const input = document.getElementById('user-input');
    const text = input.value.trim();
    if (!text) return;
    
    // Show user
    const chat = document.getElementById('chat-history');
    const div = document.createElement('div');
    div.className = 'message user';
    div.innerHTML = `<div class="sender">you</div>${text}`;
    chat.appendChild(div);
    
    // Feed aanton
    const response = window.aanton.feed(text);
    
    // Show response
    setTimeout(() => {
        const rdiv = document.createElement('div');
        rdiv.className = 'message aanton';
        rdiv.innerHTML = `<div class="sender">aanton</div>${response}`;
        chat.appendChild(rdiv);
        chat.scrollTop = chat.scrollHeight;
    }, 300);
    
    input.value = '';
}

function reset() {
    localStorage.removeItem('hunger');
    location.reload();
}

document.getElementById('user-input')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
