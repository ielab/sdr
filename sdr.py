import math
from six import iteritems
from six.moves import xrange
from gensim.models import TfidfModel
import numpy
from numpy import dot
from numpy.linalg import norm
import sys
import scipy
# QLM parameters.
Lamda= 0.2

class SDR(object):
    def __init__(self, corpus, query_dictionary):
        self.query_dictionary = query_dictionary
        self.corpus_size = len(corpus)
        self.corpus = corpus
        self.doc_length = []
        self.f = []
        self.df = {}
        self.idf = {}
        self.initialize()

    def initialize(self):
        for document in self.corpus:
            frequencies = {}
            self.doc_length.append(len(document))
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.f.append(frequencies)

            for word in frequencies:
                if word not in self.df:
                    self.df[word] = 0
                self.df[word] += 1
        for word in self.query_dictionary:
            if word not in self.df:
                self.df[word] = 1
            else:
                self.df[word] += 1
        for word, freq in iteritems(self.df):
            self.idf[word] = math.log(1.0 * self.corpus_size+1 / freq, 2)

    def get_score(self, document, index, df_dic, background_s, weight_d):
        score = 0
        for word in document:
            if word not in self.f[index]:
                continue

            mle = df_dic[word] / background_s

            score += weight_d[word] * (self.query_dictionary[word])* math.log(1 + ((1-Lamda) / Lamda * (self.f[index][word] / (self.doc_length[index] * mle))))
        return score

    def get_scores(self, document, df_dic, background_size):
        scores = []
        original_vector = []
        original_word_order = []
        index_vector = {}
        weight_dic = {}
        for word in document:
            original_word_order.append(word)
            original_vector.append(self.idf[word]*self.query_dictionary[word])
            idf = self.idf[word]
            for index in xrange(self.corpus_size):
                if word in self.f[index]:
                    tf_idf = self.f[index][word] * idf
                    if index in index_vector:
                        index_vector[index].append(tf_idf)
                    else:
                        index_vector[index] = [tf_idf]
                else:
                    if index in index_vector:
                        index_vector[index].append(0)
                    else:
                        index_vector[index] = [0]
        original_vector = [original_vector]
        for i in range(0, len(original_vector[0])):
            positive_vectors = []
            negative_vectors = []
            for index in xrange(self.corpus_size):
                if index_vector[index][i] != 0:
                    positive_vector = index_vector[index]
                    positive_vectors.append(positive_vector)
                else:
                    negative_vector = index_vector[index]
                    negative_vectors.append(negative_vector)
            if len(positive_vectors) !=0:
                positive_values = scipy.spatial.distance.cdist(original_vector, positive_vectors, 'cosine')[0]
            else:
                positive_values = [0]
            if len(negative_vectors) !=0:
                negative_values = scipy.spatial.distance.cdist(original_vector, negative_vectors, 'cosine')[0]
            else:
                negative_values = [0]

            positive_value = 1- ((sum(positive_values)) / len(positive_values))
            negative_values = numpy.nan_to_num(negative_values, nan=0.0)
            negative_value = 1- ((sum(negative_values)) / len(negative_values))
            if positive_value !=0:
                if negative_value !=0:
                    weight_dic[original_word_order[i]] = math.log(1 + (positive_value / negative_value))
                    #print(positive_value / negative_value )
                else:
                    print("negative is 0")
                    weight_dic[original_word_order[i]] = math.log(1 + 0.2)
            else:
                print("positive length 0")
                weight_dic[original_word_order[i]] = math.log(1 + 2)

        for index in xrange(self.corpus_size):
            score = self.get_score(document, index, df_dic, background_size, weight_dic)
            scores.append(score)
        return scores


