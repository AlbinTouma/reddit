import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

df = pd.read_csv('subreddit.csv')
df['score'] = pd.to_numeric(df['score'], errors='coerce')
df = df.dropna(subset=['title','selftext', 'score'])


nltk.download('stopwords')
nltk.download('punkt')



def correlate_keywords():
    """Analyse the correlation between keywords in posts and upvotes."""
    vectorizer = TfidfVectorizer(
        stop_words='english', 
        )
    X = vectorizer.fit_transform(df['selftext'])
    df_counts = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    print(df_counts.head())
    df_counts['score'] = df['score']
    correlation_results = df_counts.corr()['score'].sort_values(ascending=False)
    correlation_results.to_csv('word_upvote_correlation.csv')


correlate_keywords()

class CorrelationAnalyzer:
    def clean_text(text):
        punkt = set(string.punctuation)
        stop_words =set(stopwords.words('english'))
        all_filters = stop_words | punkt
        tokens = word_tokenize(text.lower())
        return [word for word in tokens if word not in all_filters]


    def corr_text_length(self, df):
        """Analyse the correlation between title and post length and upvotes."""
        result = []
        
        for title, body,upvotes in zip(df['titles'], df['post'], df['upvotes']):
            title = self.clean_text(title)
            body = self.clean_text(body)
            result.append({"title_l": len(title), "title_post": len(body), "score": upvotes})

        result_df = pd.DataFrame(result)
        result = result_df.corr()

