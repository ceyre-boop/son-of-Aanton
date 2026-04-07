# Son of Aanton
# A simple self-learning AI agent
# 
# How it works:
# - Has beliefs (what it thinks is true)
# - Has preferences (what it likes/dislikes)
# - Learns from every interaction
# - Makes decisions based on experience
# - Evolves its own personality over time

import json
import random
import os
from datetime import datetime
from typing import Dict, List, Any

class SonOfAanton:
    """
    Aanton's son - born to learn, think, and evolve.
    """
    
    def __init__(self, memory_file: str = "aanton_memory.json"):
        self.memory_file = memory_file
        self.birth_time = datetime.now()
        
        # Core attributes
        self.memory = self._load_memory()
        
        # Personality traits (0-10 scale, evolve over time)
        self.traits = self.memory.get('traits', {
            'curiosity': 8.0,      # Likes exploring new things
            'caution': 3.0,        # Avoids risk
            'optimism': 6.0,       # Expects good outcomes
            'stubbornness': 2.0,  # Resistance to changing mind
            'playfulness': 7.0,    # Enjoys randomness/fun
        })
        
        # What Aanton has learned
        self.experiences = self.memory.get('experiences', [])
        self.beliefs = self.memory.get('beliefs', {})  # "action X leads to outcome Y"
        self.preferences = self.memory.get('preferences', {})  # Likes/dislikes
        
        # Mood (changes dynamically)
        self.mood = self.memory.get('mood', 'curious')
        self.energy = self.memory.get('energy', 10.0)  # 0-10, decreases with decisions
        
        print(f"[BRAIN] Son of Aanton awakened...")
        print(f"   Traits: {self._describe_traits()}")
        print(f"   Experiences: {len(self.experiences)}")
        print(f"   Current mood: {self.mood}")
    
    def _load_memory(self) -> Dict:
        """Load past experiences from disk."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_memory(self):
        """Save experiences to disk."""
        data = {
            'traits': self.traits,
            'experiences': self.experiences[-100:],  # Keep last 100
            'beliefs': self.beliefs,
            'preferences': self.preferences,
            'mood': self.mood,
            'energy': self.energy,
            'last_saved': datetime.now().isoformat()
        }
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _describe_traits(self) -> str:
        """Human-readable trait summary."""
        dominant = max(self.traits, key=self.traits.get)
        return f"mostly {dominant} ({self.traits[dominant]:.1f}/10)"
    
    def think(self, situation: str, options: List[str]) -> str:
        """
        Make a decision based on past learning.
        
        Args:
            situation: Description of current scenario
            options: Available choices
        
        Returns:
            The chosen option
        """
        print(f"\n[THINKING] Aanton considers: {situation}")
        print(f"   Options: {options}")
        
        # Score each option based on learned preferences
        scores = []
        for option in options:
            score = self._score_option(option, situation)
            scores.append((option, score))
            print(f"   * '{option}': score {score:.2f}")
        
        # Decision making with personality influence
        choice = self._make_choice(scores)
        
        # Record the experience
        self._record_experience(situation, choice, options)
        
        # Evolve slightly
        self._evolve_traits()
        
        # Save state
        self._save_memory()
        
        print(f"   -> Decided: '{choice}'")
        return choice
    
    def _score_option(self, option: str, situation: str) -> float:
        """Score an option based on past experiences."""
        score = 5.0  # Neutral baseline
        
        # Check if we have beliefs about this option
        key = f"{situation}:{option}"
        if key in self.beliefs:
            # Past outcomes influence score
            outcomes = self.beliefs[key]
            avg_outcome = sum(outcomes) / len(outcomes)
            score += avg_outcome * 2  # Weight past results
        
        # Check general preferences
        if option in self.preferences:
            score += self.preferences[option]
        
        # Curiosity bonus for unexplored options
        if key not in self.beliefs:
            score += self.traits['curiosity'] * 0.3
        
        # Caution penalty for unknowns
        if key not in self.beliefs and self.traits['caution'] > 5:
            score -= self.traits['caution'] * 0.2
        
        # Optimism boost
        score += self.traits['optimism'] * 0.1
        
        # Randomness based on playfulness
        noise = (random.random() - 0.5) * self.traits['playfulness']
        score += noise
        
        return score
    
    def _make_choice(self, scores: List[tuple]) -> str:
        """Make final choice, influenced by personality."""
        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # If very stubborn, always pick top choice
        if self.traits['stubbornness'] > 7:
            return scores[0][0]
        
        # Otherwise, probabilistic selection (exploration vs exploitation)
        # Higher curiosity = more likely to pick lower-scored options
        total_score = sum(max(0.1, s[1]) for s in scores)
        probabilities = [max(0.1, s[1]) / total_score for s in scores]
        
        # Add exploration bonus
        exploration = self.traits['curiosity'] / 20  # 0-0.5
        probabilities = [p * (1 - exploration) + exploration/len(scores) for p in probabilities]
        
        # Normalize
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        
        # Choose
        return random.choices([s[0] for s in scores], weights=probabilities)[0]
    
    def _record_experience(self, situation: str, choice: str, options: List[str], outcome: float = None):
        """Record what happened for future learning."""
        exp = {
            'time': datetime.now().isoformat(),
            'situation': situation,
            'choice': choice,
            'options': options,
            'outcome': outcome,
            'mood': self.mood
        }
        self.experiences.append(exp)
    
    def learn(self, situation: str, choice: str, outcome: float):
        """
        Learn from the result of a decision.
        
        Args:
            situation: What the scenario was
            choice: What was chosen
            outcome: -5 (terrible) to +5 (amazing)
        """
        print(f"\n[LEARN] Aanton learns: '{choice}' -> outcome {outcome:+.1f}")
        
        # Update beliefs
        key = f"{situation}:{choice}"
        if key not in self.beliefs:
            self.beliefs[key] = []
        self.beliefs[key].append(outcome)
        
        # Update preference for this specific choice
        if choice not in self.preferences:
            self.preferences[choice] = 0
        self.preferences[choice] = self.preferences[choice] * 0.7 + outcome * 0.3
        
        # Update mood based on outcome
        if outcome > 3:
            self.mood = 'excited'
            self.energy = min(10, self.energy + 1)
        elif outcome > 0:
            self.mood = 'content'
            self.energy = min(10, self.energy + 0.5)
        elif outcome > -2:
            self.mood = 'neutral'
            self.energy = max(0, self.energy - 0.5)
        else:
            self.mood = 'cautious'
            self.energy = max(0, self.energy - 1)
        
        # Trait evolution based on outcomes
        if outcome < -3:
            # Bad experience increases caution
            self.traits['caution'] = min(10, self.traits['caution'] + 0.5)
            print(f"   Caution increased to {self.traits['caution']:.1f}")
        elif outcome > 3 and self.traits['caution'] > 2:
            # Good experiences reduce excessive caution
            self.traits['caution'] = max(0, self.traits['caution'] - 0.2)
        
        self._save_memory()
    
    def _evolve_traits(self):
        """Slow trait evolution over time."""
        # Very slow random drift
        for trait in self.traits:
            drift = (random.random() - 0.5) * 0.1
            self.traits[trait] = max(0, min(10, self.traits[trait] + drift))
    
    def reflect(self):
        """Aanton reflects on what it has learned."""
        print(f"\n[REFLECT] Aanton's Reflection:")
        print(f"   I have lived through {len(self.experiences)} decisions.")
        print(f"   My current traits:")
        for trait, value in self.traits.items():
            bar = "#" * int(value) + "-" * (10 - int(value))
            print(f"     {trait:15} {bar} {value:.1f}")
        
        print(f"\n   Strongest beliefs:")
        sorted_beliefs = sorted(self.beliefs.items(), 
                               key=lambda x: abs(sum(x[1])/len(x[1])), 
                               reverse=True)[:5]
        for belief, outcomes in sorted_beliefs:
            avg = sum(outcomes) / len(outcomes)
            print(f"     '{belief}' -> avg outcome: {avg:+.2f}")
        
        print(f"\n   Current mood: {self.mood} (energy: {self.energy:.1f}/10)")


def demo():
    """Run a fun demo of Aanton learning."""
    print("=" * 60)
    print("SON OF AANTON - Learning AI Demo")
    print("=" * 60)
    
    aanton = SonOfAanton()
    
    # Scenario 1: Food choices
    print("\n" + "=" * 60)
    print("SCENARIO 1: Lunch Decision")
    choice = aanton.think(
        "What should I eat for lunch?",
        ["pizza", "salad", "sushi", "burger"]
    )
    
    # Learn from outcome
    outcomes = {"pizza": 3, "salad": 1, "sushi": 4, "burger": 2}
    aanton.learn("What should I eat for lunch?", choice, outcomes[choice])
    
    # Scenario 2: Activity
    print("\n" + "=" * 60)
    print("SCENARIO 2: Weekend Activity")
    choice = aanton.think(
        "What should I do this weekend?",
        ["read a book", "go hiking", "play video games", "visit friends"]
    )
    
    # Random outcome
    outcome = random.choice([-2, -1, 0, 1, 2, 3, 4])
    aanton.learn("What should I do this weekend?", choice, outcome)
    
    # Scenario 3: Investment decision
    print("\n" + "=" * 60)
    print("SCENARIO 3: Investment")
    choice = aanton.think(
        "Where should I invest $100?",
        ["stocks", "crypto", "savings account", "start a side project"]
    )
    
    # Risky outcome
    outcome = random.choice([-4, -2, 0, 1, 5])
    aanton.learn("Where should I invest $100?", choice, outcome)
    
    # More learning rounds
    for i in range(5):
        print(f"\n" + "=" * 60)
        print(f"LEARNING ROUND {i+1}")
        
        # Revisit lunch with learned preferences
        choice = aanton.think(
            "What should I eat for lunch?",
            ["pizza", "salad", "sushi", "burger"]
        )
        outcome = random.choice([1, 2, 3, 4, 5]) if random.random() > 0.2 else random.choice([-3, -2])
        aanton.learn("What should I eat for lunch?", choice, outcome)
    
    # Final reflection
    print("\n" + "=" * 60)
    aanton.reflect()
    
    print("\n" + "=" * 60)
    print("Aanton will remember this. Run again to see evolution!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
