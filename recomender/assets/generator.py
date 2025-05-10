import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load data
movies = pd.read_csv('recomender/assets/tmdb_5000_movies.csv')
credits = pd.read_csv('recomender/assets/tmdb_5000_credits.csv')

# Merge
df = movies.merge(credits, on='title')

# Keep relevant columns
df = df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Helper functions
def extract_names(obj):
    try:
        return [item['name'] for item in ast.literal_eval(obj)]
    except:
        return []

def extract_director(obj):
    try:
        for item in ast.literal_eval(obj):
            if item['job'] == 'Director':
                return item['name']
    except:
        return ''
    return ''

# Apply functions
df['genres'] = df['genres'].apply(extract_names)
df['keywords'] = df['keywords'].apply(extract_names)
df['cast'] = df['cast'].apply(lambda x: extract_names(x)[:3])
df['crew'] = df['crew'].apply(extract_director)

# Combine into tags
df['tags'] = df['overview'].fillna('') + ' ' + \
             df['genres'].apply(lambda x: " ".join(x)) + ' ' + \
             df['keywords'].apply(lambda x: " ".join(x)) + ' ' + \
             df['cast'].apply(lambda x: " ".join(x)) + ' ' + \
             df['crew']

# Lowercase
df['tags'] = df['tags'].str.lower()

# Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()

# Cosine similarity
cosine_sim = cosine_similarity(vectors)

# Save final data
final_data = df[['movie_id', 'title']]
with open('recomender/assets/movie_data.pkl', 'wb') as f:
    pickle.dump((final_data, cosine_sim), f)

print("✅ movie_data.pkl generated successfully.")
