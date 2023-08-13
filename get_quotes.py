# # from nltk.corpus import stopwords
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.feature_extraction.text import CountVectorizer
# # from nltk.tokenize import word_tokenize
import requests
# import nltk
# from nltk.tag import pos_tag
# from nltk.chunk import ne_chunk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('stopwords')
# stopwords


class QUOTE:
    def __init__(self):
        self.api = "https://api.themotivate365.com/stoic-quote"

    def get_quote(self):
        response = requests.get(self.api).json()
        return response

    # def get_quote_sentment(self, quote):
    #     # tokens = word_tokenize(quote)
    #     # pos_tags = pos_tag(tokens)

    #     # ner_trace = ne_chunk(pos_tags)

    #     # keywords = [word for word, tag in pos_tags if tag.startswith(
    #     #     'NN') or tag.startswith('JJ')]
    #     # for subtree in ner_trace:
    #     #     if hasattr(subtree, 'label') and subtree.label() in ['PERSON', 'ORGANIZATION']:
    #     #         keywords.append(
    #     #             ' '.join([word for word, tag in subtree.leaves()]))

    #     # if keywords:
    #     #     return keywords[0]
    #     # else:
    #     #     return "NOT_FOUND"
    #     tokens = word_tokenize(quote)

    #     stop_words = set(stopwords.words('english'))
    #     print()
    #     print(stop_words)
    #     print()
    #     filtered_tokens = [
    #         word for word in tokens if word.lower() not in stop_words]

    #     # Convert the list of tokens to a single string
    #     text = ' '.join(tokens)

    #     # Use TF-IDF to extract keywords
    #     vectorizer = CountVectorizer()
    #     transformer = TfidfTransformer()
    #     tfidf = transformer.fit_transform(vectorizer.fit_transform([text]))
    #     feature_names = vectorizer.get_feature_names_out()

    #     # Get the index of the most significant keyword
    #     most_significant_index = tfidf.sum(axis=0).argmax()

    #     # Get the most significant keyword
    #     summary_word = feature_names[most_significant_index]

    #     return summary_word

# quo=QUOTE()
# print(quo.get_quote())
