import pickle
import gzip

# Load original pickle
with open("artifacts/similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# Save compressed pickle
with gzip.open("artifacts/similarity.pkl.gz", "wb") as f:
    pickle.dump(similarity, f)

print("✅ Compressed similarity.pkl saved as similarity.pkl.gz")
