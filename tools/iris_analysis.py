import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from matplotlib.colors import ListedColormap
import argparse


def main():
    # Configure argument parser
    parser = argparse.ArgumentParser(description='Iris Classification Visualizer')
    parser.add_argument('--plot', action='store_true', help='Generate classification plot')
    parser.add_argument('--point', nargs=2, type=float, metavar=('PC1', 'PC2'),
                        help='Get approximate features for PCA coordinates')
    args = parser.parse_args()

    # Load and prepare Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    target_names = iris.target_names

    # Perform PCA dimensionality reduction
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    # Shift PCA coordinates to positive values for better visualization
    x_min, y_min = X_pca.min(axis=0)
    X_pca_shifted = X_pca - np.array([x_min, y_min]) + 0.1  # Small offset

    # Train logistic regression model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_pca_shifted, y)

    def pca_to_original(pca_point):
        """Convert shifted PCA coordinates back to approximate original features"""
        # Revert the visualization shift
        original_pca = np.array(pca_point) + np.array([x_min, y_min]) - 0.1
        # Perform inverse PCA transformation
        approx_features = pca.inverse_transform([original_pca])[0]
        # Clip values to original data ranges
        return np.clip(approx_features, iris.data.min(axis=0), iris.data.max(axis=0))

    def find_uncertain_points(model, n_points=3):
        """Find points with highest classification uncertainty"""
        # Generate random points in the visualization area
        test_grid = np.random.uniform(
            low=[0, 0],
            high=[X_pca_shifted[:, 0].max() + 0.5, X_pca_shifted[:, 1].max() + 0.5],
            size=(1000, 2)
        )
        # Calculate class probabilities
        probas = model.predict_proba(test_grid)
        # Measure uncertainty (1 - max probability)
        uncertainty = 1 - np.max(probas, axis=1)
        # Return most uncertain points
        return test_grid[np.argsort(uncertainty)[-n_points:]]

    if args.point:
        # Point analysis mode
        try:
            # Convert PCA coordinates to original features
            features = pca_to_original(args.point)
            print("\nApproximate original features for PCA point", args.point)
            for name, value in zip(iris.feature_names, features):
                print(f"{name:>17}: {value:.2f}")

            # Predict class
            point_shifted = np.array(args.point).reshape(1, -1)
            class_id = model.predict(point_shifted)[0]
            print(f"\nPredicted class: {class_id} ({target_names[class_id]})")

            # Show class probabilities
            proba = model.predict_proba(point_shifted)[0]
            print("\nClass probabilities:")
            for i, (name, p) in enumerate(zip(target_names, proba)):
                print(f"{name:>17}: {p:.1%}")

            # Interpretation guidance
            if np.max(proba) < 0.6:
                print("\nNote: This is a borderline case (uncertain prediction)")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.plot:
        # Visualization mode
        plt.figure(figsize=(10, 8))

        # Create decision boundary grid
        xx, yy = np.meshgrid(
            np.arange(0, X_pca_shifted[:, 0].max() + 0.5, 0.02),
            np.arange(0, X_pca_shifted[:, 1].max() + 0.5, 0.02))

        # Plot decision regions
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        plt.contourf(xx, yy, Z,
                     cmap=ListedColormap(['#FFDDDD', '#DDFFDD', '#DDDDFF']),
                     alpha=0.8)

        # Plot training data
        plt.scatter(X_pca_shifted[:, 0], X_pca_shifted[:, 1], c=y,
                    cmap=ListedColormap(['#FF0000', '#00AA00', '#0000FF']),
                    edgecolor='k', s=60)

        # Mark uncertain points
        uncertain_points = find_uncertain_points(model)
        plt.scatter(uncertain_points[:, 0], uncertain_points[:, 1],
                    c='black', marker='x', s=100, label='Uncertain points')

        # Configure plot appearance
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")
        plt.title("Iris Classification with Decision Boundaries", pad=20)

        # Create legend
        legend_elements = [
                              plt.Line2D([0], [0], marker='o', color='w',
                                         label=target_names[i],
                                         markerfacecolor=['#FF0000', '#00AA00', '#0000FF'][i],
                                         markersize=10) for i in range(3)
                          ] + [
                              plt.Line2D([0], [0], marker='x', color='black',
                                         label='Uncertain points', markersize=10)
                          ]
        plt.legend(handles=legend_elements, loc="lower right")

        # Add variance information
        exp_var = pca.explained_variance_ratio_
        plt.text(0.02, 0.98,
                 f"Explained variance: PC1={exp_var[0]:.1%}, PC2={exp_var[1]:.1%}",
                 transform=plt.gca().transAxes, ha="left", va="top",
                 bbox=dict(facecolor='white', alpha=0.8))

        plt.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.savefig('iris_classification.png', dpi=300, bbox_inches='tight')
        print("Visualization saved as 'iris_classification.png'")
    else:
        print("Usage instructions:")
        print("  Generate plot: python iris_analysis.py --plot")
        print("  Analyze point: python iris_analysis.py --point PC1 PC2")
        print("\nExample uncertain points to try:")
        print("  python iris_analysis.py --point 4.5 1.2")
        print("  python iris_analysis.py --point 5.0 1.8")


if __name__ == "__main__":
    main()
