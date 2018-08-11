from nltk.corpus import brown, stopwords
from nltk.cluster.util import cosine_distance
import re,string
import numpy as np
from operator import itemgetter
f=open("news.txt","r")
l=[]
sentences=[]
x=(f.readlines())
l=x[0].split(". ")
for i in range(len(l)):
	sentences.append(l[i].split())
#sentences = brown.sents('ca01')
print(sentences)

regex = re.compile('[%s]' % re.escape(string.punctuation))
M=np.zeros((len(sentences), len(sentences)))
stopwords=stopwords.words('english')
def sentence_similarity(s1,s2,stopwords):
	if stopwords is None:
		stopwords=[]

	#s1=regex.sub('', s1)
	#s2=regex.sub('',s2)
	sent1 = [k.lower() for k in s1]
	sent2 = [k.lower() for k in s2]
	all_words = list(set(sent1 + sent2))
	vec1= [0]*len(all_words)
	vec2=[0]*len(all_words)
	for w in sent1:
		if w in stopwords:
			continue
		vec1[all_words.index(w)] += 1
	for w in sent2:
		if w in stopwords:
			continue
		vec2[all_words.index(w)] += 1
	return 1 - cosine_distance(vec1, vec2)


def similarity_matrix(sentence_list,stopwords):
	for i1 in range(len(sentence_list)):
		for i2 in range(len(sentence_list)):
			if i1==i2:
				continue
			M[i1][i2]=sentence_similarity(sentence_list[i1],sentence_list[i2],stopwords)

	for i1 in range(len(M)):
		M[i1]=M[i1]/M[i1].sum()

	return M

def rank(A):
	d=0.85
	e=0.0001
	R=np.ones(len(A))/len(A)
	while(True):
		new_R=np.ones(len(A)) * (1 - d) / len(A) + d * A.T.dot(R)
		diff=abs(R-new_R).sum()
		if(diff<=e):
			return new_R
		R=new_R

def textrank(sentences,stopwords):
	l_s=5
	summary=""
	S=similarity_matrix(sentences,stopwords)
	print(S)
	R=rank(S)
	ranked_sentence_indexes = [item[0] for item in sorted(enumerate(R), key=lambda item: -item[1])]
	print(ranked_sentence_indexes)
	selected_sentences = sorted(ranked_sentence_indexes[:l_s])
	for i in range(len(selected_sentences)):
		summary+=' '.join(sentences[selected_sentences[i]])+"."
	f1=open("summary.txt",'w')
	f1.write(summary)
	return summary
print(textrank(sentences,stopwords))