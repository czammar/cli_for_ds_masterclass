import json
import spacy
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import itertools
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
import pickle


class TrainBot:

    def __init__(self, conversations_path: str):
        self.conversations_path = conversations_path
        self.nlp = spacy.load('es_core_news_sm')

        # Obtain conversation data
        self.conversations = self.get_conversations()

        # Obtaing question data
        self.questions = self.get_questions()
        self.question_processed = self.get_processed_questions()

        # Obtaing data for training
        self.x_train, self.y_train = self.get_train_data()

        # Obtaing a dictionary of tags and possible answers
        self.tags_answers = self._get_tags_answers()

    def get_conversations(self) -> dict:
        with open(self.conversations_path) as f:
            conversations = json.load(f)
        return conversations

    def get_questions(self):

        # lista para extraer preguntas
        questions_ = []

        for script in self.conversations:

            # extraemos preguntas
            question = script['patterns']
            questions_.append(question)

        # Consolida todas las preguntas
        questions = list(itertools.chain.from_iterable(questions_))

        return questions

    def get_processed_questions(self):

        # lista para extraer preguntas
        question_processed = []

        for doc in self.questions:
            tokens = self.nlp(doc)
            # remueve signos de puntuacion y lematiza
            new_tokens = [
                t.orth_ for t in tokens if not t.is_punct
                ]

            # pasa a minusculas
            new_tokens = [t.lower() for t in new_tokens]

            # une los tokens procesados en una string con espacios
            question_processed.append(' '.join(new_tokens))

        return question_processed

    def _get_tags_answers(self) -> dict:
        tags_answers = {}

        for conversation in self.conversations:
            tag = conversation["tag"]
            responses = conversation["responses"]
            tags_answers[tag] = responses

        return tags_answers

    def get_train_data(self) -> tuple:
        # instancia el transformador
        self.vectorizer = CountVectorizer()

        # crea la bolsa de palabras con la lista de documentos
        X = self.vectorizer.fit_transform(self.question_processed)

        # Get Bag of Words for questions
        bow = pd.DataFrame(
            X.toarray(),
            columns=self.vectorizer.get_feature_names_out()
            )

        # Extract question tags
        tags = pd.DataFrame(self.conversations).explode(
            ['patterns']
        ).reset_index(drop=True)["tag"]

        processed_data = pd.concat(
            [bow, tags],
            axis=1
        ).sample(
            frac=1, random_state=123
        ).reset_index(drop=True)

        # Bolsa de palabras como arreglo de numpy
        x_train = processed_data._get_numeric_data().to_numpy()

        # Crea version numerica de etiquetas
        self.le = LabelEncoder()
        y_train = self.le.fit_transform(processed_data['tag'])

        return x_train, y_train

    def fit(self):

        self.base_estimator = LogisticRegression(
            solver='liblinear',
            random_state=11
        )

        # Create a OneVsRestClassifier with LogisticRegression
        # as the base estimator
        self.model = OneVsRestClassifier(self.base_estimator)

        # Train the OneVsRestClassifier
        print("Training the model")
        self.model.fit(self.x_train, self.y_train)
        print("Model succesfully trained")

    def save_objects(self):
        """
        Saving model, vectorizer and label encoding
        """
        pickle.dump(self.model, open("model.pk","wb"))
        print("Model saved to model.pk")

        pickle.dump(self.vectorizer, open("vectorizer.pk","wb"))
        print("Vectorizer saved to vectorizer.pk")

        pickle.dump(self.le, open("label_enconder.pk", "wb"))
        print("Label Encoder to label_enconder.pk")

        pickle.dump(self.tags_answers, open("tags_answers.pk", "wb"))
        print("Tags-Answers dictionary saved to tags_answers.pk")
