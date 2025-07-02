import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# Load English language model for NLP processing
nlp = spacy.load('en_core_web_sm')

def process_resumes(resume_folder, job_description, algorithm='default'):
    """
    Process resumes using specified algorithm (A*, naive, or default)
    
    Args:
        resume_folder: Path to folder containing resumes
        job_description: Text of the job description
        algorithm: Ranking algorithm to use ('default', 'astar', 'naive')
        
    Returns:
        List of dictionaries containing candidate info and scores
    """
    # Read and parse all resumes
    resumes = []
    filenames = []
    for filename in os.listdir(resume_folder):
        filepath = os.path.join(resume_folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                resumes.append(text)
                filenames.append(filename)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
    
    if not resumes:
        return []

    # Calculate base TF-IDF similarity scores
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([job_description] + resumes)
    base_scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    
    # Process with selected algorithm
    if algorithm == 'astar':
        return astar_ranking(resumes, filenames, job_description, base_scores)
    elif algorithm == 'naive':
        return naive_ranking(resumes, filenames, base_scores)
    else:  # default
        return default_ranking(resumes, filenames, base_scores)

def default_ranking(resumes, filenames, base_scores):
    """
    Default ranking using cosine similarity only
    """
    ranked = list(zip(filenames, base_scores))
    ranked.sort(key=lambda x: x[1], reverse=True)
    return format_results(ranked, resumes, "TF-IDF Score: {score:.2f}")

def astar_ranking(resumes, filenames, job_description, base_scores):
    """
    A* Search inspired algorithm with skill and experience matching
    """
    job_skills = extract_skills(job_description)
    job_exp = extract_experience(job_description)
    
    ranked = []
    for i, (resume, filename) in enumerate(zip(resumes, filenames)):
        # Base similarity score
        g_score = base_scores[i]
        
        # Skill match heuristic
        resume_skills = extract_skills(resume)
        skill_match = len(set(job_skills) & set(resume_skills)) / len(job_skills) if job_skills else 0
        
        # Experience match heuristic
        resume_exp = extract_experience(resume)
        exp_match = 1 if (resume_exp and job_exp and resume_exp >= job_exp) else 0.5
        
        # Combined score
        total_score = g_score + (skill_match * 0.4) + (exp_match * 0.2)
        
        ranked.append((filename, total_score, 
                      f"TF-IDF: {g_score:.2f} | Skills: {skill_match*100:.0f}% | Exp: {'Match' if exp_match == 1 else 'Partial'}"))
    
    ranked.sort(key=lambda x: x[1], reverse=True)
    return format_results(ranked, resumes)

def naive_ranking(resumes, filenames, base_scores):
    """
    Naive ranking algorithm (simple sort)
    """
    ranked = list(zip(filenames, base_scores))
    ranked.sort(key=lambda x: x[1], reverse=True)
    return format_results(ranked, resumes, "Naive score: {score:.2f}")

def format_results(ranked, resumes, details_format=None):
    """
    Format results consistently across all algorithms
    """
    results = []
    for i, item in enumerate(ranked):
        if len(item) == 2:  # (filename, score)
            filename, score = item
            details = details_format.format(score=score) if details_format else ""
        else:  # (filename, score, details)
            filename, score, details = item
            
        results.append({
            'filename': filename,
            'score': score,
            'skills': extract_skills(resumes[i]),
            'details': details
        })
    return results

def extract_skills(text):
    """Extract skills using NLP and keyword matching"""
    doc = nlp(text.lower())
    skills = set()
    
    # Extract noun phrases containing skill indicators
    for chunk in doc.noun_chunks:
        if 'skill' in chunk.text or 'experience' in chunk.text:
            skills.update(t.text for t in chunk if t.pos_ in ('NOUN', 'PROPN'))
    
    # Add common technical skills
    tech_skills = {
        'python', 'java', 'javascript', 'c++', 'sql', 'html', 'css',
        'machine learning', 'data analysis', 'flask', 'django'
    }
    skills.update(s for s in tech_skills if s in text.lower())
    
    return sorted(skills)[:5]  # Return top 5 skills

def extract_experience(text):
    """Extract experience duration in years"""
    doc = nlp(text.lower())
    for ent in doc.ents:
        if ent.label_ == 'DATE' and ('year' in ent.text or 'yr' in ent.text):
            try:
                return int(ent.text.split()[0])  # Return first number found
            except (ValueError, IndexError):
                continue
    return 0