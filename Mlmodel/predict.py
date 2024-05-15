from flask import Flask, request, jsonify
import pickle
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
# print(len(stopwords.words('english')))
# print(len(set(stopwords.words('english'))))

# s=set(stopwords.words('english'))
# import time

# start_time = time.time()
# s=set(stopwords.words('english'))
# # logic here
# if "if" in s:
#     pass
# print("Time taken: ", time.time() - start_time)
    

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = text.lower()  
    text = ''.join([char for char in text if char not in string.punctuation])
    words = text.split()
    words = [word for word in words if word not in stop_words]  
    return ' '.join(words)



def predict_sentiment(review: str) -> str:
    review = preprocess_text(review)
    print(review)
    with open('./vectorizer.pkl', 'rb') as file:
        vectorizer = pickle.load(file)

    with open('./naive_bayes_model.pkl', 'rb') as file:
        model = pickle.load(file)
    review_vectorized = vectorizer.transform([review.lower()])
    sentiment = model.predict(review_vectorized)
    # print(sentiment)
    return sentiment[0] 

# if __name__ == "__main__":
#     ans=predict_sentiment("If not for the space sequence I would've disliked the movie")
#     print(ans)
    