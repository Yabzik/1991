import random

subjects_sets = {
    'програмування': ['👨‍💻', '👩‍💻', '💻', '🖥️'],
    'математика': ['📏', '📐'],
    'мова': ['🌐'],
    'мережі': ['🤖'],
    'психологі': ['🔮', '🧩'],
    'хакатон': ['🤖'],
    'fallback': ['👨‍🏫', '​✍️', '👩‍🏫', '🤯', '👨‍🎓', '👩‍🎓', '​​​​🤓']
}

def choose(text):
    text = text.lower()
    for subject, emojis in subjects_sets.items():
        if subject in text:
            return random.choice(emojis)
    return random.choice(subjects_sets['fallback'])