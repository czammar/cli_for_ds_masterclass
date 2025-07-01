import spacy
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import numpy as np
import random
from .config import bot_config
from os import path


class PredictBot:

    def __init__(self, config=bot_config):

        self.config = bot_config
        self.nlp = spacy.load('es_core_news_sm')
        # Obtain conversation data
        self.vectorizer = self._get_vectorizer()
        self.le = self._get_label_enconder()
        self.model = self._get_model()
        self.tags_answers = self._get_tags_answers()

    def _get_model(self):
        filename = "./src/bot/data/model.pk"
        with open(filename, "rb") as file:
            model = pickle.load(file)

        return model

    def _get_vectorizer(self):
        filename = "./src/bot/data/vectorizer.pk"
        with open(filename, "rb") as file:
            vectorizer = pickle.load(file)

        return vectorizer

    def _get_label_enconder(self):
        filename = "./src/bot/data/label_encoder.pk"
        with open(filename, "rb") as file:
            label_enconder = pickle.load(file)

        return label_enconder

    def _get_tags_answers(self):
        filename = "./src/bot/data/tags_answers.pk"
        with open(filename, "rb") as file:
            tags_answers = pickle.load(file)

        return tags_answers

    def text_pre_process(self, message: str):
        """
        Procesa el texto del nuevo mensaje
        """
        # Procesa el mensaje con spaCy
        tokens = self.nlp(message)

        # remueve signos de puntuacion y lematiza
        new_tokens = [
            t.orth_ for t in tokens if not t.is_punct
            ]

        # pasa a minusculas
        new_tokens = [t.lower() for t in new_tokens]

        # une los tokens procesados con un espacio
        clean_message = ' '.join(new_tokens)

        return clean_message

    def bow_representation(self, message: str):
        """
        Obtiene la representacion del mensaje en su
        codificacion de la nube de palabras
        """
        bow_message = self.vectorizer.transform(
            [message]
            ).toarray()

        return bow_message

    def get_predicted_label(self, message: str) -> str:
        point = self.bow_representation(
            self.text_pre_process(message)
            )

        probabilities = self.model.predict_proba(point)

        predicted_label = int(
            np.argmax(probabilities)
        )

        return self.le.inverse_transform([predicted_label])[0]

    def predicted_msg(self, message: str) -> str:

        predicted_label = self.get_predicted_label(message)
        possible_answers = self.tags_answers[predicted_label]

        if self.config.DETERMINISTIC_ANS:
            answer = possible_answers[0]
        else:
            answer = random.choice(possible_answers)

        return answer