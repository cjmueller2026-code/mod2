from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Test k values from 1 to 30
k_values = range(1, 31)
scores = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    cv_scores = cross_val_score(knn, X, y, cv=5)
    scores.append(cv_scores.mean())

# Find the best k
best_k = k_values[scores.index(max(scores))]
best_score = max(scores)

print("Best k:", best_k)
print("Cross-validation accuracy:", best_score)

# Plot results
plt.plot(k_values, scores, marker='o')
plt.xlabel("Number of Neighbors (k)")
plt.ylabel("Cross-Validation Accuracy")
plt.title("KNN Accuracy for Different k Values")
plt.grid(True)
plt.show()