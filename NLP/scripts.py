
def createLDA(data):

    import pandas as pd
    import numpy as np
    import gensim as gs
    from nltk import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.stem.porter import PorterStemmer
    from gensim.utils import simple_preprocess
    from gensim.parsing.preprocessing import STOPWORDS

    stemmer = PorterStemmer()

    def lemmatize_stemming(text):
        return stemmer.stem(WordNetLemmatizer().lemmatize(text))

    def preprocess(text):
        result = []
        lookup = []
        for tk in word_tokenize(str(text)):
            if tk not in STOPWORDS and len(tk)>3:
                result.append(lemmatize_stemming(tk))
                lookup.append([tk,lemmatize_stemming(tk)])
        return([result,lookup])

    stop_words = set(stopwords.words('english'))
    path = "C:\\Users\\gfevola\\Documents\\Samples\\RN Survey.xlsx"

    data = pd.read_excel(path)

    data = data.dropna(subset=['value'])
    i = 0
     

    texts = data.loc[:,"value"]
    doc_clean = [preprocess(w)[0] for w in data.loc[:,"value"]]

    convertlist = pd.concat([pd.DataFrame(preprocess(w)[1]) for w in data.loc[:,"value"]])
    convertlist = convertlist.drop_duplicates(1,keep="first")


    dictionary = gs.corpora.Dictionary(doc_clean)
    dictionary.filter_extremes(no_below=.01,no_above=.05)

    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    LDA = gs.models.ldamodel.LdaModel

    ldafit = LDA(doc_term_matrix,num_topics=10,id2word=dictionary,passes=10)



    #--------------------

    bigram = gs.models.Phrases(doc_clean,min_count=5,threshold=100)
    bigrams = [bigram[doc] for doc in doc_clean]

    ldafit.log_perplexity(doc_term_matrix)

    #visualization
    #gs.models.CoherenceModel(corpus=doc_term_matrix,texts=texts, dictionary=dictionary,coherence="c_v")
    #vis = pyLDAvis.gensim.prepare(ldafit,doc_term_matrix,dictionary)

    def pulltopicmatch(doc):
        kind = pd.DataFrame(ldafit[doc])
        topic = [t for t, j in enumerate(kind[1]) if j==max(kind[1])]
        return(list([kind.loc[topic[0],0],kind.loc[topic[0],1]]))
        
    kind = pd.DataFrame([pulltopicmatch(doc_term_matrix[i]) for i in range(len(texts))])

    def basetopic(n):
        top = pd.DataFrame(ldafit.show_topic(n))
        top['TopicNo']=[n for i in range(len(top))]
        return(top)

    topics = pd.concat([basetopic(t) for t in range(10)])
    topics = topics.merge(convertlist,left_on=0,right_on=1)
    topics  = topics.drop(["0_x","key_0","1_y"],axis=1)
    topics.columns = ["WordPct","TopicNo","Word"]

    data_output = data
    data_output['Topic']=kind.loc[:,0]
    data_output['TopicStrength']=kind.loc[:,1]
     
    data_output = data_output.dropna(subset=["Topic"]) #remove where topic is blank
    data_output['Score'] = data_output['Score'].fillna(value=0)
        
    return([data_output,topics])
