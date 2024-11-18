import os
import joblib

def logistic_regression_sentiment(text):
    current_dir = os.path.dirname(__file__)
    
    vectorizer_path = os.path.join(current_dir, 'logistic_regression_vectorizer.pkl')
    model_path = os.path.join(current_dir, 'logistic_regression_model.pkl')

    vectorizer = joblib.load(vectorizer_path)
    text_vectorized = vectorizer.transform([text])
    model = joblib.load(model_path)
    predicted_sentiment = model.predict(text_vectorized)
    return int(predicted_sentiment[0])

if __name__ == "__main__":
    test_text_1 = "Why does Skiles smell like vomit | Selftext: It’s been smelling like that for the past month or two. | Flair: Rant"
    print(f"Test 1 - Predicted sentiment: {logistic_regression_sentiment(test_text_1)}")

    test_text_2 = "I love the new features in the latest update! | Selftext: The app is so much better now. | Flair: Positive"
    print(f"Test 2 - Predicted sentiment: {logistic_regression_sentiment(test_text_2)}")