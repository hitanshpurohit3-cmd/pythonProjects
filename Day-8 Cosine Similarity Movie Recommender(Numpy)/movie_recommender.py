import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Step 1: Define Movies and Feature Vectors ---

movies = [
    "The Dark Knight",
    "The Hangover",
    "Interstellar",
    "Mean Girls",
    "Mad Max: Fury Road",
    "Inception",
    "The Notebook",
    "John Wick",
    "Forrest Gump",
    "Avengers: Endgame"
]

# Columns represent genres:
# [Action, Comedy, Drama, Romance, Sci-Fi, Thriller]
# Each value is 1 (genre applies) or 0 (it doesn't)
# Some movies get 0.5 for partial genre presence

features = np.array([
    [1, 0, 1, 0, 0, 1],   # The Dark Knight
    [0, 1, 0, 0, 0, 0],   # The Hangover
    [0, 0, 1, 0, 1, 1],   # Interstellar
    [0, 1, 1, 1, 0, 0],   # Mean Girls
    [1, 0, 0, 0, 1, 0],   # Mad Max: Fury Road
    [1, 0, 1, 0, 1, 1],   # Inception
    [0, 0, 1, 1, 0, 0],   # The Notebook
    [1, 0, 0, 0, 0, 1],   # John Wick
    [0, 1, 1, 1, 0, 0],   # Forrest Gump
    [1, 0, 1, 0, 1, 0],   # Avengers: Endgame
], dtype=float)

# --- Step 2: Compute Cosine Similarity ---

def cosine_similarity_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Compute the cosine similarity between every pair of row vectors.

    Cosine similarity = (A · B) / (||A|| * ||B||)

    Args:
        matrix: A 2D NumPy array where each row is a feature vector.

    Returns:
        A square similarity matrix of shape (n, n).
    """
    # Compute the L2 norm (magnitude) of each row vector
    # keepdims=True preserves shape so broadcasting works correctly
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)

    # Avoid division by zero for any zero vectors
    norms = np.where(norms == 0, 1e-10, norms)

    # Normalize each row so every vector has magnitude 1
    normalized = matrix / norms

    # Dot product of normalized vectors = cosine similarity
    # normalized @ normalized.T means: each row dot producted with every other row
    similarity = normalized @ normalized.T

    return similarity


similarity_matrix = cosine_similarity_matrix(features)

# --- Step 3: Recommendation Function ---

def recommend(title: str, top_n: int = 3) -> list:
    """
    Given a movie title, return the top_n most similar movies.

    Args:
        title (str): Name of the movie to base recommendations on.
        top_n (int): Number of recommendations to return. Default is 3.

    Returns:
        list: List of (movie_name, similarity_score) tuples.

    Raises:
        ValueError: If the title is not found in the movie list.
    """
    if title not in movies:
        raise ValueError(f"'{title}' not found. Available: {movies}")

    idx = movies.index(title)            # Get the row index of this movie
    scores = similarity_matrix[idx]      # That row = similarity to all others

    # argsort returns indices that would sort the array (ascending)
    # [::-1] reverses it to descending (most similar first)
    sorted_indices = np.argsort(scores)[::-1]

    results = []
    for i in sorted_indices:
        if movies[i] == title:           # Skip the movie itself (always score 1.0)
            continue
        results.append((movies[i], round(scores[i], 4)))
        if len(results) == top_n:
            break

    return results


# --- Step 4: Display Recommendations ---

query = "Inception"
recs = recommend(query)

print(f"\nTop 3 movies similar to '{query}':")
for rank, (movie, score) in enumerate(recs, start=1):
    print(f"  {rank}. {movie}  (similarity: {score})")

# --- Step 5: Similarity Heatmap ---

plt.figure(figsize=(10, 8))

sns.heatmap(
    similarity_matrix,
    xticklabels=movies,
    yticklabels=movies,
    annot=True,           # Show the numbers inside each cell
    fmt=".2f",            # Format numbers to 2 decimal places
    cmap="YlOrRd",        # Yellow-to-Red color scale
    linewidths=0.5        # Thin lines separating cells
)

plt.title("Movie Cosine Similarity Matrix", fontsize=14, fontweight="bold")
plt.xticks(rotation=45, ha="right")   # Rotate x-axis labels for readability
plt.tight_layout()                     # Prevent label cutoff
plt.savefig("similarity_heatmap.png", dpi=150)
plt.show()
print("Heatmap saved as similarity_heatmap.png")