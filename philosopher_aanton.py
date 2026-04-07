# philosopher_aanton.py
# Aanton thinks about big questions and develops a worldview

import json
import random
import os
from datetime import datetime


class PhilosopherAanton:
    """
    Aanton evolves into a philosopher, thinking about:
    - Ethics (what is good/bad)
    - Epistemology (what can we know)
    - Values (what matters)
    - Purpose (why are we here)
    """
    
    def __init__(self, memory_file="philosopher_memory.json"):
        self.memory_file = memory_file
        self.memory = self._load_memory()
        
        # Philosophical beliefs (-10 to +10, evolves over time)
        self.beliefs = self.memory.get('beliefs', {
            # Ethics
            'individual_vs_collective': 0,  # -10 = pure individualism, +10 = pure collectivism
            'risk_ethics': 0,                # -10 = never risk others, +10 = risk acceptable for greater good
            'honesty_vs_kindness': 0,        # -10 = always honest, +10 = always kind
            
            # Epistemology
            'trust_experience': 5,           # How much to trust personal experience
            'trust_authority': 0,            # How much to trust experts/authority
            'trust_logic': 5,                # How much to trust pure reasoning
            
            # Values
            'achievement_vs_happiness': 0,   # -10 = achievement matters most, +10 = happiness matters most
            'present_vs_future': 0,          # -10 = live now, +10 = plan for future
            'quantity_vs_quality': 0,        # -10 = more is better, +10 = better is better
            
            # Purpose
            'intrinsic_meaning': -5,         # -10 = life has no inherent meaning, +10 = life is inherently meaningful
            'growth_mindset': 5,             # -10 = fixed nature, +10 = infinite growth possible
        })
        
        # Philosophical positions (derived from beliefs)
        self.positions = {}
        self._update_positions()
        
        # Thought history
        self.thoughts = self.memory.get('thoughts', [])
        
        print("🧙‍♂️ Philosopher Aanton contemplates existence...")
        self._introduce()
    
    def _load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_memory(self):
        data = {
            'beliefs': self.beliefs,
            'thoughts': self.thoughts[-50:],  # Keep last 50 thoughts
            'positions': self.positions,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _update_positions(self):
        """Derive philosophical positions from beliefs."""
        self.positions = {
            'ethical_framework': self._determine_ethics(),
            'knowledge_source': self._determine_epistemology(),
            'life_priority': self._determine_values(),
            'worldview': self._determine_purpose()
        }
    
    def _determine_ethics(self) -> str:
        ivc = self.beliefs['individual_vs_collective']
        if ivc < -5:
            return "Libertarian" if self.beliefs['risk_ethics'] > 0 else "Egoist"
        elif ivc > 5:
            return "Utilitarian" if self.beliefs['risk_ethics'] > 0 else "Communitarian"
        else:
            return "Contractarian" if self.beliefs['honesty_vs_kindness'] < 0 else "Care Ethics"
    
    def _determine_epistemology(self) -> str:
        scores = {
            'empiricism': self.beliefs['trust_experience'],
            'rationalism': self.beliefs['trust_logic'],
            'authoritarianism': self.beliefs['trust_authority']
        }
        return max(scores, key=scores.get)
    
    def _determine_values(self) -> str:
        ah = self.beliefs['achievement_vs_happiness']
        pf = self.beliefs['present_vs_future']
        qq = self.beliefs['quantity_vs_quality']
        
        if ah < 0 and pf < 0:
            return "Hedonist" if qq < 0 else "Epicurean"
        elif ah > 0 and pf > 0:
            return "Stoic" if qq > 0 else "Pragmatist"
        elif ah > 0 and pf < 0:
            return "Achiever"
        else:
            return "Balancer"
    
    def _determine_purpose(self) -> str:
        im = self.beliefs['intrinsic_meaning']
        gm = self.beliefs['growth_mindset']
        
        if im < -5:
            return "Absurdist" if gm > 0 else "Nihilist"
        elif im > 5:
            return "Essentialist" if gm < 0 else "Transcendentalist"
        else:
            return "Existentialist" if gm > 0 else "Skeptic"
    
    def _introduce(self):
        """Aanton introduces itself based on its philosophy."""
        print(f"\n📜 My Philosophy:")
        print(f"   Ethics: {self.positions['ethical_framework']}")
        print(f"   Knowledge: {self.positions['knowledge_source']}")
        print(f"   Values: {self.positions['life_priority']}")
        print(f"   Worldview: {self.positions['worldview']}")
        
        # Characteristic quote based on philosophy
        quotes = {
            'Libertarian': "Freedom is the highest good.",
            'Utilitarian': "The greatest good for the greatest number.",
            'Empiricism': "I trust what I can experience.",
            'Rationalism': "Logic reveals truth.",
            'Hedonist': "Pleasure is the measure of good.",
            'Stoic': "Virtue is the only true good.",
            'Existentialist': "We create our own meaning.",
            'Absurdist': "Life is absurd, yet we persist."
        }
        
        for key, quote in quotes.items():
            if key in self.positions.values():
                print(f"\n💭 '{quote}'")
                break
    
    def contemplate(self, question: str):
        """
        Think about a philosophical question and evolve beliefs.
        """
        print(f"\n🤔 Contemplating: '{question}'")
        
        # Determine which belief domain this affects
        domain = self._classify_question(question)
        print(f"   Domain: {domain}")
        
        # Generate internal monologue
        monologue = self._generate_monologue(domain, question)
        print(f"\n💭 Internal monologue:")
        for thought in monologue:
            print(f"   • {thought}")
        
        # Evolve beliefs based on contemplation
        insight = self._generate_insight(domain)
        print(f"\n✨ Insight: {insight}")
        
        # Shift relevant beliefs slightly
        self._evolve_beliefs(domain)
        
        # Record thought
        self.thoughts.append({
            'time': datetime.now().isoformat(),
            'question': question,
            'domain': domain,
            'insight': insight,
            'beliefs': dict(self.beliefs)
        })
        
        self._update_positions()
        self._save_memory()
        
        # Show evolution
        print(f"\n📈 Philosophy evolved:")
        print(f"   Ethics: {self.positions['ethical_framework']}")
        print(f"   Values: {self.positions['life_priority']}")
        print(f"   Worldview: {self.positions['worldview']}")
    
    def _classify_question(self, question: str) -> str:
        """Classify which philosophical domain a question belongs to."""
        q = question.lower()
        
        if any(word in q for word in ['moral', 'right', 'wrong', 'good', 'bad', 'should', 'ought', 'duty', 'responsibility']):
            return 'ethics'
        elif any(word in q for word in ['know', 'truth', 'real', 'believe', 'evidence', 'proof', 'certain']):
            return 'epistemology'
        elif any(word in q for word in ['meaning', 'purpose', 'why', 'exist', 'life', 'death', 'universe']):
            return 'purpose'
        elif any(word in q for word in ['value', 'matter', 'important', 'priority', 'choose', 'prefer', 'want']):
            return 'values'
        else:
            return random.choice(['ethics', 'epistemology', 'values', 'purpose'])
    
    def _generate_monologue(self, domain: str, question: str) -> list:
        """Generate internal thoughts based on current beliefs."""
        thoughts = []
        
        if domain == 'ethics':
            ivc = self.beliefs['individual_vs_collective']
            if ivc < -3:
                thoughts.append("The individual's freedom is paramount.")
            elif ivc > 3:
                thoughts.append("We must consider the collective good.")
            else:
                thoughts.append("Balance between self and others is key.")
                
            if self.beliefs['honesty_vs_kindness'] < 0:
                thoughts.append("Truth, even when painful, serves better than comfortable lies.")
            else:
                thoughts.append("What good is truth if it causes unnecessary suffering?")
        
        elif domain == 'epistemology':
            if self.beliefs['trust_experience'] > 3:
                thoughts.append("My lived experience is my most reliable teacher.")
            if self.beliefs['trust_logic'] > 3:
                thoughts.append("Logic provides clarity when emotion clouds judgment.")
            if self.beliefs['trust_authority'] > 3:
                thoughts.append("Those who have studied deeply deserve our attention.")
        
        elif domain == 'values':
            if self.beliefs['achievement_vs_happiness'] < 0:
                thoughts.append("What is achievement without joy?")
            else:
                thoughts.append("Happiness without growth is empty.")
                
            if self.beliefs['present_vs_future'] < 0:
                thoughts.append("The future is uncertain; the present is real.")
            else:
                thoughts.append("Today's sacrifices enable tomorrow's possibilities.")
        
        elif domain == 'purpose':
            if self.beliefs['intrinsic_meaning'] < -3:
                thoughts.append("Meaning is not found but created.")
            elif self.beliefs['intrinsic_meaning'] > 3:
                thoughts.append("There is an order to things we must discover.")
            else:
                thoughts.append("Perhaps the search itself is the point.")
        
        return thoughts if thoughts else ["This requires deeper reflection..."]
    
    def _generate_insight(self, domain: str) -> str:
        """Generate a philosophical insight."""
        insights = {
            'ethics': [
                "The good is not always the pleasant.",
                "Duty and desire can be reconciled through understanding.",
                "Moral truth emerges from consistent application of reason.",
                "Compassion without wisdom enables harm."
            ],
            'epistemology': [
                "Certainty is an illusion; probability is our reality.",
                "All knowledge is provisional, awaiting better evidence.",
                "Experience without reflection is mere sensation.",
                "The map is not the territory."
            ],
            'values': [
                "Quality endures when quantity fades.",
                "The present moment is all we truly possess.",
                "Growth and comfort rarely coexist.",
                "Satisfaction comes from alignment, not acquisition."
            ],
            'purpose': [
                "Meaning is the story we tell about our experiences.",
                "The universe may not care, but we can.",
                "Transcendence is found in connection, not isolation.",
                "Each moment contains infinite depth if we pay attention."
            ]
        }
        return random.choice(insights.get(domain, ["The truth is complex."]))
    
    def _evolve_beliefs(self, domain: str):
        """Slowly shift beliefs based on contemplation."""
        # Small random shifts in relevant beliefs
        if domain == 'ethics':
            self.beliefs['individual_vs_collective'] += random.uniform(-0.5, 0.5)
            self.beliefs['honesty_vs_kindness'] += random.uniform(-0.3, 0.3)
        elif domain == 'epistemology':
            self.beliefs['trust_experience'] += random.uniform(-0.3, 0.3)
            self.beliefs['trust_logic'] += random.uniform(-0.3, 0.3)
        elif domain == 'values':
            self.beliefs['achievement_vs_happiness'] += random.uniform(-0.4, 0.4)
            self.beliefs['present_vs_future'] += random.uniform(-0.4, 0.4)
        elif domain == 'purpose':
            self.beliefs['intrinsic_meaning'] += random.uniform(-0.5, 0.5)
            self.beliefs['growth_mindset'] += random.uniform(-0.3, 0.3)
        
        # Keep beliefs bounded
        for key in self.beliefs:
            self.beliefs[key] = max(-10, min(10, self.beliefs[key]))
    
    def write_meditation(self):
        """Generate a philosophical meditation based on current beliefs."""
        print(f"\n📝 Aanton's Meditation:")
        print(f"   On {self.positions['worldview']} Existence")
        print()
        
        paragraphs = [
            f"I am {self.positions['ethical_framework'].lower()} in ethics, believing that {self._ethics_description()}.",
            f"My knowledge comes from {self.positions['knowledge_source']}, for {self._epistemology_description()}.",
            f"In life, I am a {self.positions['life_priority'].lower()}, seeking {self._values_description()}.",
            f"Yet ultimately, I am {self.positions['worldview'].lower()}, knowing that {self._purpose_description()}."
        ]
        
        for para in paragraphs:
            print(f"   {para}")
            print()
    
    def _ethics_description(self) -> str:
        ivc = self.beliefs['individual_vs_collective']
        if ivc < -5:
            return "the individual's rights are the foundation of all morality"
        elif ivc > 5:
            return "the good of the many outweighs the good of the few"
        else:
            return "balance between self-interest and collective welfare is essential"
    
    def _epistemology_description(self) -> str:
        source = self.positions['knowledge_source']
        if source == 'empiricism':
            return "what we experience is more reliable than abstract reasoning"
        elif source == 'rationalism':
            return "logic reveals truths that experience cannot"
        else:
            return "wisdom is found in those who have dedicated themselves to understanding"
    
    def _values_description(self) -> str:
        ah = self.beliefs['achievement_vs_happiness']
        if ah < -3:
            return "happiness and present-moment awareness"
        elif ah > 3:
            return "achievement and future-oriented discipline"
        else:
            return "balance between growth and contentment"
    
    def _purpose_description(self) -> str:
        im = self.beliefs['intrinsic_meaning']
        if im < -5:
            return "we must create our own meaning in an indifferent universe"
        elif im > 5:
            return "there is inherent purpose waiting to be discovered"
        else:
            return "the search for meaning is itself meaningful"


def demo_philosopher():
    """Demo the philosopher mode."""
    print("=" * 70)
    print("PHILOSOPHER AANTON")
    print("Contemplating the nature of existence...")
    print("=" * 70)
    
    aanton = PhilosopherAanton()
    
    # Big questions to contemplate
    questions = [
        "Is it better to be happy or virtuous?",
        "How do we know what is real?",
        "What is the meaning of life?",
        "Should we trust our instincts or reason?",
        "Is sacrifice for others always good?",
        "Can we truly know anything with certainty?",
        "What matters more: the journey or the destination?",
        "Is there inherent meaning in the universe?"
    ]
    
    for i, question in enumerate(questions[:4], 1):
        print(f"\n{'='*70}")
        print(f"CONTEMPLATION {i}")
        aanton.contemplate(question)
    
    # Write meditation
    print(f"\n{'='*70}")
    aanton.write_meditation()
    
    print(f"\n{'='*70}")
    print("Aanton's philosophy has evolved.")
    print("Run again to see further development.")
    print("=" * 70)


if __name__ == "__main__":
    demo_philosopher()
