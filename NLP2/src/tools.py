from langchain_core.tools import tool
import os
import random

# Define the data path
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "notes.txt")

@tool
def search_music_theory(query: str) -> str:
    """
    Search for information in the local music theory notes.
    Useful for answering questions about scales, chords, intervals, or terminology.
    """
    try:
        if not os.path.exists(DATA_PATH):
            return "Error: Notes file not found."
        
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Simple case-insensitive keyword search
        results = []
        paragraphs = content.split('\n\n')
        for p in paragraphs:
            if query.lower() in p.lower():
                results.append(p)
        
        if not results:
            return "No specific notes found. Check general knowledge."
        
        return "\n---\n".join(results[:3])
    except Exception as e:
        return f"Error searching notes: {str(e)}"

@tool
def suggest_practice_routine(instrument: str, duration_minutes: int) -> str:
    """
    Generates a random practice routine for a given instrument and duration.
    Useful for planning practice sessions.
    """
    warmups = ["Scales", "Finger independence", "Long tones", "Stretching"]
    techniques = ["Arpeggios", "Alternate picking", "Slapping", "Bending", "Chord transitions"]
    songs = ["Learn a new riff", "Practice repertoire", "Improvisation backing track"]
    
    routine = f"Practice Plan for {instrument} ({duration_minutes} mins):\n"
    
    # Simple split
    warmup_time = max(5, int(duration_minutes * 0.2))
    tech_time = max(10, int(duration_minutes * 0.4))
    song_time = duration_minutes - warmup_time - tech_time
    
    routine += f"1. Warm-up ({warmup_time}m): {random.choice(warmups)}\n"
    routine += f"2. Technique ({tech_time}m): {random.choice(techniques)}\n"
    routine += f"3. Repertoire ({song_time}m): {random.choice(songs)}\n"
    
    return routine

@tool
def get_chord_notes(chord: str) -> str:
    """
    Returns the notes of a requested chord.
    Example input: 'C Major', 'A Minor'
    """
    # Mock database
    chords = {
        "c major": "C - E - G",
        "d major": "D - F# - A",
        "g major": "G - B - D",
        "a minor": "A - C - E",
        "e minor": "E - G - B",
        "f major": "F - A - C"
    }
    return chords.get(chord.lower(), "Chord not found in mini-database. Ask generally.")
