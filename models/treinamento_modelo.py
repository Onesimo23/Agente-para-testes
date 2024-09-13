from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def treinar_modelo():
    try:
        data = load_iris()
        X = data.data
        y = data.target

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print('Accuracy:', accuracy)

    except Exception as e:
        print(f"Erro ao treinar o modelo: {e}")

if __name__ == "__main__":
    treinar_modelo()
