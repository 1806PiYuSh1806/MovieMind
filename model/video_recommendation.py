import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

dataset = pd.read_csv('data.csv')

selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
for feature in selected_features:
    dataset[feature] = dataset[feature].fillna('')

combined_features = (
    dataset['genres'] + ' ' +
    dataset['keywords'] + ' ' +
    dataset['tagline'] + ' ' +
    dataset['cast'] + ' ' +
    dataset['director']
)

vectorizer = TfidfVectorizer()
feature_vector = vectorizer.fit_transform(combined_features)

similarity = cosine_similarity(feature_vector)

def get_recommendations(video_name):
    list_of_all_titles = dataset['title'].tolist()
    find_close_match = difflib.get_close_matches(video_name, list_of_all_titles)
    if not find_close_match:
        return ["No such video, please try again."]

    close_match = find_close_match[0]
    index_of_video = dataset[dataset.title == close_match]['index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_video]))
    sorted_similar_videos = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended_videos = []
    for i, video in enumerate(sorted_similar_videos[:10], 1):
        index = video[0]
        title_from_index = dataset[dataset.index == index]['title'].values[0]
        recommended_videos.append(f"{i}. {title_from_index}")

    return recommended_videos