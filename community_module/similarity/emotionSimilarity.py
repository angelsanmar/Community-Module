# Authors: Guillermo Jimenez-Díaz
#          Jose Luis Jorro-Aragoneses

from itertools import product
import numpy as np

from community_module.similarity.similarity import Similarity

PLUTCHIK_EMOTIONS = ['anger', 'anticipation', 'disgust', 'fear', 'sadness', 'surprise', 'trust'] # Falta incluir 'joy'

class EmotionSimilarity(Similarity):

    def __init__(self, data):
        """Construct of EmotionSimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of emotions and
            values contain number of times that an emotions is in an element.
        """
        
        # Nos quedamos únicamente con las emociones de Plutchik
        self.data = data[PLUTCHIK_EMOTIONS]

    def _dominantEmotion(self, emotions, size=1):
        """Method to obtain dominant emotions of a user.

        Parameters
        ----------
        emotions : pd.Series
            Series that contains the emotions and times of this emotion in dataset.
        size : int, optional
            Number of dominant emotions to recover, by default 1
        """

        return emotions.sort_values(ascending=False).index[:size].values

    def _emotions_distance(self, emotionA, emotionB):
        """Method to calculate the distance between 2 emotions based on PLUTCHKIN emotions.

        Parameters
        ----------
        emotionA : str
            First emotion.
        emotionB : str
            Second emotion.

        Returns
        -------
        double
            Distance value between emotions.
        """

        indexA = PLUTCHIK_EMOTIONS.index(emotionA)
        indexB = PLUTCHIK_EMOTIONS.index(emotionB)

        if indexB > indexA:
            indexA, indexB = indexB, indexA

        return min( (indexA - indexB) / 4, (indexB - indexA + 8) / 4)

    def distance(self, elemA, elemB, numEmotions = 3):
        """Method to obtain the distance between two element based on the array of emotions.

        Parameters
        ----------
        elemA : int
            Id of first element. This id should be in self.data.
        elemB : int
            Id of second element. This id should be in self.data.
        numEmotions : int, optional
            Number of most represented emotions to calculate the distance, by default 3

        Returns
        -------
        double
            Distance between the two elements.
        """

        emotionsA = self._dominantEmotion(self.data.loc[elemA], numEmotions)
        emotionsB = self._dominantEmotion(self.data.loc[elemB], numEmotions)

        distance = 0
        for i in range(numEmotions):
            distance += self._emotions_distance(emotionsA[i], emotionsB[i])

        return distance / numEmotions

    def similarity(self, elemA, elemB, numEmotions = 3):
        """Method to obtain the similarity between two element based on the array of emotions.

        Parameters
        ----------
        elemA : int
            Id of first element. This id should be in self.data.
        elemB : int
            Id of second element. This id should be in self.data.
        numEmotions : int, optional
            Number of most represented emotions to calculate the similarity, by default 3

        Returns
        -------
        double
            Similarity between the two elements.
        """
        return 1 - self.distance(elemA, elemB, numEmotions) # ¿No debería ser 1 / distancia?

    def matrix_distance(self, numEmotions = 3):
        """Method to calculate the matrix of distance between all element included in data.

        Parameters
        ----------
        numEmotions : int, optional
            Number of most represented emotions to calculate the distance, by default 3

        Returns
        -------
        np.array
            Matrix that contains all distance values.
        """

        users = self.data.index
        pairs = product(range(len(users)), repeat=2)

        matrix = np.zeros((len(users), len(users)))
        for p in pairs:
            dist = self.distance(users[p[0]], users[p[1]])
            matrix[p[0], p[1]] = dist

        return matrix

    def matrix_similarity(self, numEmotions = 3):
        """Method to calculate the matrix of similarity between all element included in data.

        Parameters
        ----------
        numEmotions : int, optional
            Number of most represented emotions to calculate the similarity, by default 3

        Returns
        -------
        np.array
            Matrix that contains all similarity values.
        """

        users = self.data.index
        pairs = product(range(len(users)), repeat=2)

        matrix = np.zeros((len(users), len(users)))
        for p in pairs:
            dist = self.similarity(users[p[0]], users[p[1]])
            matrix[p[0], p[1]] = dist

        return matrix
