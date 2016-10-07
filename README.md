# japanese_sentiment
It's a sentiment analysis system for Japanese customer reviews.

#1	Introduction

The popularity and convenience of Internet accelerate the development of elec-tronic business. Everyday millions of people buy products and publish their reviews online. These reviews can be used for public opinion analysis. For example, after reading other people's product reviews, customers can make a wiser decision whether to buy a product/service or not. Although the valuable data are rapidly increasing day and night, the arduous workload for reading and analyzing large scale data is hard for individuals. It brings a pressing need for building the system which can automatically perform sentiment classi cation (or opinion mining) job.

The key for building a sentiment analysis model is the extraction of feature. Good features can identify one class from others. In early work, researchers ex-tracted the features based on experience and statistical information from train-ing corpus. For example,J. Martineau[7] improved a model in which words with high TF-IDF value were selected as features. Tony Mullen and Nigel Collier[10] designed a model based on mutual information in 2004.

In 2010, Bengio[4] proposed to represent the meaning of words with word vectors. Based on Bengio's idea, Mikolov[9] proposed CBOW and Skip-gram model to train distributed representations of words in 2013. In 2014, QV Le[6] modi ed the word2vec model by adding paragraph vectors as input and the result achieved over 92% precision on IMDB dataset.

However, most of the existing word-embedding-based models just consider local information within a training window and can not the handle long-term dependency problem. Inspired by T. Mikolov's RNNLM[8] and relatd Long short-term memory (LSTM) [3][2], we introduce the idea of LSTM model in lan-guage model to train word vectors with massive amounts of Japanese customer reviews from multiple domains. Then we train and test our sentiment classi-er with the trained word vectors (distributed representation) generated by the language model. In the 10-fold cross-validation experiments, our LSTM-based language model eventually achieved 92:8% F-measure, exceeding all baselines, which proves the e ectiveness of our model.

#2	Method

#2.1	Materials

The corpus used in this project consists of 6 million reviews of commodities in various categories from Amazon Japan. The preprocessing of the material can be divided into 3 procedures, crawling, tokenization and annotating.

The crawling procedure is handled by our crawler customized for Amazon Japan. The crawler takes node IDs referring to categories as input, and it fetches all commodity IDs under corresponding categories. Then the crawler traverses the commodity IDs and retrieves the text and rating of every review. These reviews are formatted as XML and written in to XML les.

The tokenization procedure is to separate sentences into words since there are no spaces between words in Japanese. JUMAN [5], one of the most accurate Japanese tokenization and tagging tools, is used to process the raw materials. JUMAN takes original Japanese texts as input, and outputs words and their syntactic tags. Removing the tags of the words, we gain the segmented corpus whose format is that there is a space between every two words.

The annotating is based on the rating of the reviews, since the scale of the corpus is too large for manual annotation. Reviews with rating 1 and 2 are considered negative while those with rating 4 and 5 are annotated as positive ones.

#2.2	Procedure

After pre-process, we can now start building the language model and get the word embedding. Since the recurrent neural network is proved to be successful in building language models for long text[8], we choose long short-term memory (LSTM) as the core module of our framework to build the language model. LSTM is a modi ed RNN model which is designed to overcome some defacts of the RNN such as vanishing gradient and exploding gradients. Therefore, the memory cell is introduced to the LSTM node. As shown in gure 1, such memory cell contains an input gate, a memory cell, a forget gate, and an output gate.

To update memory cells for every token wt, the standard LSTM model adopts following notations and equations:

wt is the tth token input

W , U, and V are LSTM weights

b are bias vectors

it is the tth input gate

Ct is the tth candidate value for the states of the memory cell ft is the actication of forget gates

Ct is the tth new candidate state for the memory cell

ot is the value of output gate and ht is the output of the LSTM node

it =  (Wiwt + Uiht  1 + bi)

Ct = tanh(Wcwt + Ucht 1 + bc) ft = (Wf wt + Uf ht 1 + bf )

Ct = it	Ct + ft	Ct  1

ot =  (Wowt + Uoht  1 + VoCt + bo)

ht = ot	tanh(Ct)

In order to build an appropriate language model that provides high quality word embedding for the sentiment classi cation, the model we adopts adds a mean pooling layer which will calculate the mean vector of the output vectors hi of each token i in one customer review. Then, the mean vector h and the corresponding sentiment polarity label (positive:1 or negative:0) are used as the input of a logistic regression layer that helps to train the weights of LSTM node through back-propagation process. The architecture of the model is shown in gure 2. We implement this model by following this tutorial [1] and use Theano1, which is a python library for implementing deeplearning algorithms.

To train our model, we rstly convert the Japanese corpus to index rep-resentation, which means using the correspoinding index from the vocabulary to replace each real japanese word. Thus a review is translated into a list of integers. For each word, the index will rstly be represented by a random d dimensional vector as its initial distributed representation. The d is set by ourselves representing the dimension of the word embedding we want to train. Eventually, after the model converges, we fetch the word embedding from the trained weight. The word embedding will be a jV j d matrix in which each vector vi of row i is the distributed representation of ith word in the vocabulary. The jV j is the size of the vocabulary. The process is shown in gure 3. Finally, the word embedding will be used to build the sample vectors for training the sentiment classi er. We will discuss the training steps and the evaluation of the sentiment classi cation in next section.

#3 Reulst
          | Precision | Recall | Measure
--------- | --------  | ------- | --------|
Positive  | 0.978     | 0.888   | 0.933  |
Negative  | 0.876     | 0.98    | 0.928|
Average   | 0.924     | 0.932   |  0.928|

