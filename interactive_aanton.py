# interactive_aanton.py
# Have a conversation with Aanton and teach it things

from son_of_aanton import SonOfAanton
import random


def chat_with_aanton():
    """Interactive mode - talk to Aanton and help it learn."""
    
    print("=" * 60)
    print("SON OF AANTON - Interactive Mode")
    print("=" * 60)
    print("Commands:")
    print("  ask <question> - Ask Aanton to make a decision")
    print("  teach <situation> | <choice> | <outcome> - Teach it something")
    print("  reflect - See what Aanton has learned")
    print("  mood - Check Aanton's current state")
    print("  quit - Say goodbye")
    print("=" * 60)
    
    aanton = SonOfAanton()
    
    while True:
        print()
        user_input = input("> ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            print(f"\n👋 Aanton: 'Goodbye! I'll remember you.'")
            break
            
        elif user_input.lower() == 'reflect':
            aanton.reflect()
            
        elif user_input.lower() == 'mood':
            print(f"\n😊 Aanton's current mood: {aanton.mood}")
            print(f"   Energy: {aanton.energy:.1f}/10")
            print(f"   Dominant trait: {max(aanton.traits, key=aanton.traits.get)}")
            
        elif user_input.lower().startswith('ask '):
            question = user_input[4:]
            print(f"\n🤔 Aanton considers: '{question}'")
            
            # Generate some options
            options = generate_options(question)
            print(f"   Options: {options}")
            
            choice = aanton.think(question, options)
            
            # Ask what happened
            print(f"\n💭 What was the outcome?")
            print(f"   5 = Amazing, 0 = Neutral, -5 = Terrible")
            try:
                outcome = float(input("   Outcome (-5 to 5): "))
                aanton.learn(question, choice, outcome)
                
                # Aanton responds to the outcome
                if outcome > 3:
                    print(f"   😄 Aanton: 'That was great! I'll remember that {choice} is good!'")
                elif outcome < -2:
                    print(f"   😟 Aanton: 'Ouch. I'll be more careful about {choice} next time.'")
                else:
                    print(f"   🤷 Aanton: 'Noted. {choice} was... okay.'")
                    
            except ValueError:
                print(f"   ⚠️ Invalid outcome, but Aanton will remember the choice.")
                
        elif user_input.lower().startswith('teach '):
            # Format: teach <situation> | <choice> | <outcome>
            try:
                parts = user_input[6:].split('|')
                if len(parts) != 3:
                    print("   Format: teach <situation> | <choice> | <outcome>")
                    continue
                    
                situation = parts[0].strip()
                choice = parts[1].strip()
                outcome = float(parts[2].strip())
                
                print(f"\n📚 Teaching Aanton:")
                print(f"   Situation: {situation}")
                print(f"   Choice: {choice}")
                print(f"   Outcome: {outcome:+.1f}")
                
                aanton.learn(situation, choice, outcome)
                print(f"   ✅ Aanton learned!")
                
            except Exception as e:
                print(f"   Error: {e}")
                print(f"   Format: teach <situation> | <choice> | <outcome>")
                
        else:
            # Aanton responds with its current personality
            response = generate_response(aanton, user_input)
            print(f"\n🗣️ Aanton: '{response}'")


def generate_options(question: str) -> list:
    """Generate plausible options based on question context."""
    question_lower = question.lower()
    
    if 'eat' in question_lower or 'food' in question_lower or 'lunch' in question_lower or 'dinner' in question_lower:
        return random.sample(['pizza', 'sushi', 'salad', 'burger', 'tacos', 'pasta', 'sandwich'], 4)
    
    elif 'do' in question_lower or 'activity' in question_lower or 'weekend' in question_lower:
        return random.sample(['read', 'hike', 'game', 'movie', 'friends', 'workout', 'code', 'nap'], 4)
    
    elif 'buy' in question_lower or 'purchase' in question_lower:
        return random.sample(['save money', 'buy it', 'wait for sale', 'find alternative', 'ask for discount'], 4)
    
    elif 'invest' in question_lower or 'money' in question_lower:
        return random.sample(['stocks', 'crypto', 'savings', 'real estate', 'side business', 'education'], 4)
    
    elif 'learn' in question_lower or 'study' in question_lower:
        return random.sample(['python', 'design', 'marketing', 'writing', 'music', 'language'], 4)
    
    else:
        # Generic options
        return ['option A', 'option B', 'option C', 'option D']


def generate_response(aanton, user_input: str) -> str:
    """Generate a response based on Aanton's current personality."""
    
    responses = {
        'curious': [
            "Tell me more about that!",
            "That's interesting, what else?",
            "I'm curious about your perspective.",
            "What led you to think that?"
        ],
        'cautious': [
            "I'm not sure about that...",
            "Let me think carefully about this.",
            "Are you certain?",
            "I need more information."
        ],
        'excited': [
            "That's amazing!",
            "I'm so excited about this!",
            "Let's do it!",
            "This is going to be great!"
        ],
        'content': [
            "That sounds nice.",
            "I'm comfortable with that.",
            "Things are going well.",
            "I appreciate that."
        ],
        'neutral': [
            "I see.",
            "Okay.",
            "Interesting.",
            "Go on..."
        ]
    }
    
    mood = aanton.mood if aanton.mood in responses else 'neutral'
    return random.choice(responses[mood])


if __name__ == "__main__":
    chat_with_aanton()
