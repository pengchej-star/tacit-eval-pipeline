# %%
import numpy as np 
import pandas as pd 
import polars as pl
import os
import re
import pickle

import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode(connected=True)
from collections import Counter
from textblob import TextBlob
import torch
import gensim
from gensim.models import CoherenceModel
import gensim.corpora as corpora
from gensim.corpora import Dictionary
from nltk import ngrams
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from tqdm import tqdm
import nltk
#nltk.download('punkt')
from nltk.corpus import stopwords
#nltk.download('stopwords')

from scipy.special import softmax
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier,GradientBoostingClassifier,BaggingClassifier
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB,MultinomialNB,ComplementNB
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.pipeline import Pipeline

from sklearn.feature_selection import SelectFromModel
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, f1_score
from sklearn.metrics import cohen_kappa_score
from lightgbm import log_evaluation, early_stopping
import lightgbm as lgb
#nltk.download('wordnet')
from nltk.corpus import wordnet


from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments,DataCollatorWithPadding
from glob import glob
from datasets import Dataset
import gc

import textstat
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import spacy

import time


import warnings
warnings.filterwarnings('ignore')

# %%
MAX_LENGTH = 1024
TEST_DATA_PATH = "/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv"
MODEL_PATH = '/kaggle/input/aes2-400-20240419134941/*/*'
EVAL_BATCH_SIZE = 1

# %%
deberta_models = sorted(p for p in glob(MODEL_PATH) if os.path.isfile(os.path.join(p, 'config.json')))
assert deberta_models, 'No local DeBERTa checkpoints found'
tokenizer = AutoTokenizer.from_pretrained(deberta_models[0])

def tokenize(sample):
    return tokenizer(sample['full_text'], max_length=MAX_LENGTH, truncation=True)

df_test = pd.read_csv(TEST_DATA_PATH)
ds = Dataset.from_pandas(df_test).map(tokenize).remove_columns(['essay_id', 'full_text'])

args = TrainingArguments(
    ".", 
    per_device_eval_batch_size=EVAL_BATCH_SIZE, 
    report_to="none"
)

predictions = []
for deberta_model in deberta_models:
    deberta_model = AutoModelForSequenceClassification.from_pretrained(deberta_model)
    trainer = Trainer(
        model=deberta_model, 
        args=args, 
        data_collator=DataCollatorWithPadding(tokenizer), 
        tokenizer=tokenizer
    )    
    preds = trainer.predict(ds).predictions
    predictions.append(softmax(preds, axis=-1))
    del deberta_model, trainer
    torch.cuda.empty_cache()
    gc.collect()
    
    

# %%
predicted_score = 0.
for p in predictions:
    predicted_score += p
    
predicted_score /= len(predictions)


# %%
def get_fb3_predicted(df_test = None):
    import pandas as pd
    import fb3_deberta_family_inference_9_28_updated_320784

    if df_test is None:
        df_test = pd.read_csv(TEST_DATA_PATH)
    if len(df_test) < 10:
        fb3_predicted = fb3_deberta_family_inference_9_28_updated_320784.predict_chunk(
            df_test.rename(columns={"essay_id": "text_id"})
        )
    else:
        fb3_predicted = fb3_deberta_family_inference_9_28_updated_320784.predict(
            df_test.rename(columns={"essay_id": "text_id"})
        )
    return fb3_predicted

# %%
import string

cList = {
  "ain't": "am not","aren't": "are not","can't": "cannot","can't've": "cannot have","'cause": "because",  "could've": "could have","couldn't": "could not","couldn't've": "could not have","didn't": "did not","doesn't": "does not","don't": "do not","hadn't": "had not","hadn't've": "had not have","hasn't": "has not",
  "haven't": "have not","he'd": "he would","he'd've": "he would have","he'll": "he will","he'll've": "he will have","he's": "he is",
  "how'd": "how did","how'd'y": "how do you","how'll": "how will","how's": "how is","I'd": "I would","I'd've": "I would have","I'll": "I will","I'll've": "I will have","I'm": "I am","I've": "I have",
  "isn't": "is not","it'd": "it had","it'd've": "it would have","it'll": "it will", "it'll've": "it will have","it's": "it is","let's": "let us","ma'am": "madam","mayn't": "may not",
  "might've": "might have","mightn't": "might not","mightn't've": "might not have","must've": "must have","mustn't": "must not","mustn't've": "must not have","needn't": "need not","needn't've": "need not have","o'clock": "of the clock","oughtn't": "ought not","oughtn't've": "ought not have","shan't": "shall not","sha'n't": "shall not",
  "shan't've": "shall not have","she'd": "she would","she'd've": "she would have","she'll": "she will","she'll've": "she will have","she's": "she is",
  "should've": "should have","shouldn't": "should not","shouldn't've": "should not have","so've": "so have","so's": "so is","that'd": "that would","that'd've": "that would have","that's": "that is","there'd": "there had","there'd've": "there would have","there's": "there is","they'd": "they would","they'd've": "they would have","they'll": "they will","they'll've": "they will have","they're": "they are","they've": "they have","to've": "to have","wasn't": "was not","we'd": "we had",
  "we'd've": "we would have","we'll": "we will","we'll've": "we will have","we're": "we are","we've": "we have",
  "weren't": "were not","what'll": "what will","what'll've": "what will have","hasn't" : "has not",
  "what're": "what are","what's": "what is","what've": "what have","when's": "when is","when've": "when have",
  "where'd": "where did","where's": "where is","where've": "where have","who'll": "who will","who'll've": "who will have","who's": "who is","who've": "who have","why's": "why is",
  "why've": "why have","will've": "will have","won't": "will not","won't've": "will not have","would've": "would have","wouldn't": "would not",
  "wouldn't've": "would not have","y'all": "you all","y'alls": "you alls","y'all'd": "you all would",
  "y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have","you'd": "you had","you'd've": "you would have","you'll": "you you will","you'll've": "you you will have","you're": "you are",  "you've": "you have"
   }

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_re.sub(replace, text)

def removeHTML(x):
    html=re.compile(r'<.*?>')
    return html.sub(r'',x)

def remove_punctuation(text):

    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def dataPreprocessing(x):
    x = x.lower()
    x = removeHTML(x)
    x = re.sub(r"@\w+", '',x)
    x = re.sub(r"'\d+", '',x)
    x = re.sub(r"\d+", '',x)
    x = re.sub(r"http\w+", '',x)
    x = re.sub(r"\s+", " ", x)
    x = expandContractions(x)
    x = re.sub(r"\.+", ".", x)
    x = re.sub(r"\,+", ",", x)
    x = x.strip()
    return x

# %%
def extract_essay_parts(text):
    paragraphs = text.split('\n\n')
    introduction, body, conclusion ="", "", ""
    if len(paragraphs) == 1:
        body = paragraphs[0]
    
    if len(paragraphs) > 1 & len(paragraphs) <= 2:
        body = paragraphs[0]
        conclusion = paragraphs[1]
        
    if len(paragraphs) > 2:
        introduction = paragraphs[0]
        body = '\n\n'.join(paragraphs[1:-1])
        conclusion = paragraphs[-1]
       
    #first_para = paragraphs[0]
    
    return introduction, body, conclusion

# %%
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    # Tokenize the text into words
    words = re.findall(r'\b\w+\b', text.lower())
    # Remove stopwords
    filtered_words = [word for word in words if word not in stop_words]
    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)
    return filtered_text


# %%
PATH = "/kaggle/input/learning-agency-lab-automated-essay-scoring-2/"

df_train = pd.read_csv(PATH + "train.csv")
df_test = pd.read_csv(PATH + "test.csv")

df_train['introduction'], df_train['body'], df_train['conclusion'] = zip(*df_train['full_text'].apply(extract_essay_parts))
df_test['introduction'], df_test['body'], df_test['conclusion'] = zip(*df_test['full_text'].apply(extract_essay_parts))


# %%
"""
df_train['full_text'] = df_train['full_text'].apply(dataPreprocessing)
df_train['introduction'] = df_train['introduction'].apply(dataPreprocessing)
df_train['body'] = df_train['body'].apply(dataPreprocessing)
df_train['conclusion'] = df_train['conclusion'].apply(dataPreprocessing)

df_test['full_text'] = df_test['full_text'].apply(dataPreprocessing)
df_test['introduction'] = df_test['introduction'].apply(dataPreprocessing)
df_test['body'] = df_test['body'].apply(dataPreprocessing)
df_test['conclusion'] = df_test['conclusion'].apply(dataPreprocessing)

df_train['full_text_no_stopwords'] = df_train['full_text'].apply(remove_stopwords)

df_test['full_text_no_stopwords'] = df_test['full_text'].apply(remove_stopwords)
"""

# %%
with open('/kaggle/input/english-word-hx/words.txt', 'r') as file:
    english_vocab = set(word.strip().lower() for word in file)

# %%
import spacy

try:
    spacy.require_gpu()
    nlp = spacy.load('en_core_web_sm')
except:
    nlp = spacy.load('en_core_web_sm')
        

# %%

def extract_linguistic_features_in_batches(df, batch_size=100):
    
    texts = df['full_text'].to_list()
    docs = list(nlp.pipe(texts, batch_size=batch_size, disable=['tokenizer']))
    features_list = []
        
    for doc in docs:
        features = {}

        # NER Features
        entity_counts = {"GPE": 0, "PERCENT": 0, "NORP": 0, "ORG": 0, "CARDINAL": 0, "MONEY": 0, "DATE": 0, 
                        "LOC": 0, "PERSON": 0, "QUANTITY": 0, "EVENT": 0, "ORDINAL": 0, "WORK_OF_ART": 0, 
                        "LAW": 0, "PRODUCT": 0, "TIME": 0, "FAC": 0, "LANGUAGE": 0}
        for entity in doc.ents:
            if entity.label_ in entity_counts:
                entity_counts[entity.label_] += 1
        features['NER_Features'] = entity_counts

        # POS Features
        pos_counts = {"ADJ": 0, "NOUN": 0, "VERB": 0, "SCONJ": 0, "PRON": 0, "PUNCT": 0, "DET": 0, "AUX": 0, 
                      "PART": 0, "ADP": 0, "SPACE": 0, "CCONJ": 0, "PROPN": 0, "NUM": 0, "ADV": 0, 
                      "SYM": 0, "INTJ": 0, "X": 0}
        for token in doc:
            if token.pos_ in pos_counts:
                pos_counts[token.pos_] += 1
        features['POS_Features'] = pos_counts

        # Detailed Tagging Features
        tags = {"RB": 0, "-RRB-": 0, "PRP$": 0, "JJ": 0, "TO": 0, "VBP": 0, "JJS": 0, "DT": 0, "''": 0, "UH": 0, 
                "RBS": 0, "WRB": 0, ".": 0, "HYPH": 0, "XX": 0, "``": 0, "SYM": 0, "VB": 0, "VBN": 0, "WP": 0, 
                "CC": 0, "LS": 0, "POS": 0, "NN": 0, ",": 0, "NNPS": 0, "RP": 0, ":": 0, "$": 0, "PDT": 0, "VBZ": 0, 
                "VBD": 0, "JJR": 0, "-LRB-": 0, "IN": 0, "RBR": 0, "WDT": 0, "EX": 0, "MD": 0, "_SP": 0, "NNP": 0, 
                "CD": 0, "VBG": 0, "NNS": 0, "PRP": 0}
        for token in doc:
            if token.tag_ in tags:
                tags[token.tag_] += 1
        features['Tag_Features'] = tags

        # Tense Features
        tenses = [i.morph.get("Tense") for i in doc]
        tenses = [i[0] for i in tenses if i]
        tense_counts = Counter(tenses)
        total_tense_count = tense_counts.get("Past", 0) + tense_counts.get("Pres", 0) + 1e-5
        features['past_tense_ratio'] = tense_counts.get("Past", 0) / total_tense_count
        features['present_tense_ratio'] = tense_counts.get("Pres", 0) / total_tense_count

        
        lemmatized_tokens = [token.lemma_.lower() for token in doc]
        spelling_errors = sum(1 for token in lemmatized_tokens if token not in english_vocab)
        features['errors'] = spelling_errors
        
        features_list.append(features)
        
    features_df = pd.json_normalize(features_list)
    return features_df



# %%
"""start_time = time.time()
linguistic_features_df = extract_linguistic_features_in_batches(df_train)
end_time = time.time()

df_train = pd.concat([df_train, linguistic_features_df], axis=1)


print(f"Time taken to extract linguistic features: {end_time - start_time} seconds")

"""

# %%
"""linguistic_features_df = extract_linguistic_features_in_batches(df_test)
df_test = pd.concat([df_test, linguistic_features_df], axis=1)
"""

# %%
gc.collect()

# %%
if torch.cuda.is_available():
    device = torch.device('cuda')
    print("CUDA is available. Using GPU.")
else:
    device = torch.device('cpu')
    print("CUDA is not available. Using CPU.")

# %% [markdown]
# https://maartengr.github.io/BERTopic/faq.html#i-am-facing-memory-issues-help
# 
# There are three steps to the BERTopic model
# 
# 1. 
# 
#  If you have an NVIDIA GPU, you can use PyTorch and RAPIDS cuML to get large speedups with the state-of-the-art BERTopic configuration used by default.
#  
#  Using cuML, we can run UMAP in about 5 seconds rather than 100 seconds, resulting in a further 2x speedup for the overall workload (84 seconds rather than 190 seconds).
#  
#  A massive impact, it turns out. HDBSCAN soft clustering took about 737 seconds on the CPU, but can be done in less than one second on the GPU. Running the same code above but setting calculate_probabilities=True, the workload takes about 85 seconds to complete rather than 1583 seconds (about 19x faster).

# %%
embedding_model = SentenceTransformer('/kaggle/input/sentence-embedding-models/paraphrase-MiniLM-L12-v2', device=device)


topic_model = BERTopic(embedding_model=embedding_model,
                       #vectorizer_model=bert_vectorizer_model,
                       verbose=True,
                       min_topic_size=15,
                       nr_topics= 6, #'auto',
                       n_gram_range=(1, 4))

# %%
"""train_headline_topics, _  = topic_model.fit_transform(df_train['full_text_no_stopwords'])
df_train['topic'] = train_headline_topics
"""

# %%
"""freq = topic_model.get_topic_info()
print("Number of topics: {}".format( len(freq)))
freq"""

# %%
"""test_headline_topics, _ = topic_model.transform(df_test['full_text_no_stopwords'])
df_test['topic'] = test_headline_topics
"""

# %%
"""df_train = pd.get_dummies(df_train, columns=['topic'], prefix='topic', dtype=np.int64)
df_test = pd.get_dummies(df_test, columns=['topic'], prefix='topic', dtype=np.int64)
"""

# %%
"""all_topic_columns = [col for col in df_train.columns if col not in ('essay_id', 'full_text', 'score', 'introduction', 'body', 'conclusion',
       'full_text_no_stopwords')]

# Add missing columns to the test dataframe with zeros
for col in all_topic_columns:
    if col not in df_test.columns:
        df_test[col] = 0"""

# %%
del topic_model, embedding_model
gc.collect()
torch.cuda.empty_cache()

# %%
sentence_model = SentenceTransformer("/kaggle/input/sentence-embedding-models/paraphrase-MiniLM-L12-v2").to(device)

def coherence_score(sentences):
    
    embeddings = sentence_model.encode(sentences, show_progress_bar=False, device=device)
    similarities = sentence_model.similarity(embeddings, embeddings)
    
    # Calculate average similarity between consecutive sentences
    coherence = np.mean([similarities[i, i+1] for i in range(len(sentences) - 1)])
    return coherence

def calculate_coherence(df,col):
    coherence_scores = []
    for index, essay in tqdm(df.iterrows(), total=len(df), desc=f"Calculating Coherence Scores for {col}"):
        sentences = sent_tokenize(essay[col])
        if len(sentences) > 1:
            score = coherence_score(sentences)
        else:
            score = 0  # Assign 0 if there's only one sentence or empty text
        coherence_scores.append(score)
    return coherence_scores

# %%
def calculate_similarity_score(df):

    intro_embeddings = sentence_model.encode(df['introduction'].tolist(), show_progress_bar= False)
    body_embeddings = sentence_model.encode(df['body'].tolist(), show_progress_bar= False)
    conclusion_embeddings = sentence_model.encode(df['conclusion'].tolist(), show_progress_bar= False)

    intro_body_scores = []
    intro_conclusion_scores = []
    body_conclusion_scores = []
    for i in tqdm(range(len(df)), desc="Calculating similarity scores"):
        intro_emb = intro_embeddings[i].reshape(1, -1)
        body_emb = body_embeddings[i].reshape(1, -1)
        conclusion_emb = conclusion_embeddings[i].reshape(1, -1)
        
        intro_body_similarity = sentence_model.similarity(intro_emb, body_emb)[0][0]
        intro_conclusion_similarity = sentence_model.similarity(intro_emb, conclusion_emb)[0][0]
        body_conclusion_similarity = sentence_model.similarity(body_emb, conclusion_emb)[0][0]
        
        
        intro_body_scores.append(intro_body_similarity)
        intro_conclusion_scores.append(intro_conclusion_similarity)
        body_conclusion_scores.append(body_conclusion_similarity)
    
    df['intro_body_scores'] = intro_body_scores
    df['intro_conclusion_scores'] = intro_conclusion_scores
    df['body_conclusion_scores'] = body_conclusion_scores
    return df

# %%
"""df_train = calculate_similarity_score(df_train)
df_train['intro_body_scores'] = df_train['intro_body_scores'].apply(lambda x: x.item())
df_train['intro_conclusion_scores'] = df_train['intro_conclusion_scores'].apply(lambda x: x.item())
df_train['body_conclusion_scores'] = df_train['body_conclusion_scores'].apply(lambda x: x.item())"""

# %%
"""df_test = calculate_similarity_score(df_test)
df_test['intro_body_scores'] = df_test['intro_body_scores'].apply(lambda x: x.item())
df_test['intro_conclusion_scores'] = df_test['intro_conclusion_scores'].apply(lambda x: x.item())
df_test['body_conclusion_scores'] = df_test['body_conclusion_scores'].apply(lambda x: x.item())"""

# %%
del sentence_model
gc.collect()
torch.cuda.empty_cache()

# %%
"""df_train.drop([ 'full_text', 'score', 'introduction', 'body', 'conclusion',
       'full_text_no_stopwords'], axis=1, inplace = True)

df_test.drop([ 'full_text', 'introduction', 'body', 'conclusion',
       'full_text_no_stopwords'], axis=1, inplace = True)"""

# %%
columns = [  
    (
        pl.col("full_text").str.split(by="\n\n").alias("paragraph")
    ),
]

train = pl.read_csv(PATH + "train.csv").with_columns(columns)
test = pl.read_csv(PATH + "test.csv").with_columns(columns)



# %%
train = train.with_columns([
    pl.col("full_text").map_elements(lambda x: extract_essay_parts(x)[0]).alias("introduction"),
    pl.col("full_text").map_elements(lambda x: extract_essay_parts(x)[1]).alias("body"),
    pl.col("full_text").map_elements(lambda x: extract_essay_parts(x)[2]).alias("conclusion")
])

test = test.with_columns([
    pl.col("full_text").map_elements(lambda x: extract_essay_parts(x)[0]).alias("introduction"),
    pl.col("full_text").map_elements(lambda x: extract_essay_parts(x)[1]).alias("body"),
    pl.col("full_text").map_elements(lambda x: extract_essay_parts(x)[2]).alias("conclusion")
])

# %%
def calculate_vocabulary_diversity(text):
    words = text.split()
    unique_words = set(words)
    diversity_ratio = len(unique_words) / len(words) if words else 0
    return diversity_ratio

def count_quoted_sents(text):
    # Find all quoted parts of the text
    quoted_parts = re.findall(r'"(.*?)"', text)
    sentence_count = 0
    for part in quoted_parts:
        # Count the number of sentences within each quoted part
        sentences = re.split(r'[.!?]', part)
        # Filter out empty strings resulting from the split
        sentences = [s for s in sentences if s.strip()]
        sentence_count += len(sentences)
    return sentence_count


def sentiment_analysis(text):
    analysis = TextBlob(text)
    return [analysis.sentiment.polarity, analysis.sentiment.subjectivity]
          

# %%
def pos_tag_counts(doc):
    pos_counts = doc.count_by(spacy.attrs.POS)
    noun_count = pos_counts.get(nlp.vocab.strings['NOUN'], 0)
    verb_count = pos_counts.get(nlp.vocab.strings['VERB'], 0)
    pronoun_count = pos_counts.get(nlp.vocab.strings['PRON'], 0)
    adjective_count = pos_counts.get(nlp.vocab.strings['ADJ'], 0)
    adverb_count = pos_counts.get(nlp.vocab.strings['ADV'], 0)
    
    return noun_count, verb_count, pronoun_count, adjective_count, adverb_count


def named_entity_count(doc):
    return len(doc.ents)

def count_spelling_errors(doc):
    lemmatized_tokens = [token.lemma_.lower() for token in doc]
    spelling_errors = sum(1 for token in lemmatized_tokens if token not in english_vocab)
    return spelling_errors
    
"""
    texts = tmp[essay_part].to_list() # + '_no_punc'
    docs = list(nlp.pipe(texts, disable=['tokenizer'], batch_size = 50))  # Disable tokenizer since texts are already tokenized

    # Add POS and NER counts
    tmp = tmp.with_columns([pl.Series([pos_tag_counts(doc)[0] for doc in docs]).alias(f'{essay_part}_noun_counts')])
    tmp = tmp.with_columns([pl.Series([pos_tag_counts(doc)[1] for doc in docs]).alias(f'{essay_part}_verb_counts')])
    tmp = tmp.with_columns([pl.Series([pos_tag_counts(doc)[2] for doc in docs]).alias(f'{essay_part}_pron_counts')])
    tmp = tmp.with_columns([pl.Series([pos_tag_counts(doc)[3] for doc in docs]).alias(f'{essay_part}_adj_counts')])
    tmp = tmp.with_columns([pl.Series([pos_tag_counts(doc)[4] for doc in docs]).alias(f'{essay_part}_adv_counts')])
    tmp = tmp.with_columns([pl.Series([named_entity_count(doc) for doc in docs]).alias(f'{essay_part}_ner_counts')])
    
    tmp = tmp.with_columns([pl.Series([count_spelling_errors(doc) for doc in docs]).alias(f'{essay_part}_error_counts')])
    
    
    ,
                      f'{essay_part}_noun_counts', f'{essay_part}_verb_counts', f'{essay_part}_pron_counts',
                      f'{essay_part}_adj_counts', f'{essay_part}_adv_counts', f'{essay_part}_ner_counts',
                      f'{essay_part}_error_counts'

"""

# %%
def Essay_Parts_Preprocess(tmp, essay_part, mode):

    if essay_part == 'paragraph':
        tmp = tmp.explode(essay_part)
    tmp = tmp.with_columns(pl.col(essay_part).map_elements(dataPreprocessing))
    tmp = tmp.with_columns(pl.col(essay_part).map_elements(remove_punctuation).alias(f'{essay_part}_no_punc'))
    #tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(avg_spelling_mistakes).alias(f'{essay_part}_mistakes_num'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(calculate_vocabulary_diversity).alias(f'{essay_part}_vocab_num'))
    tmp = tmp.with_columns(pl.col(essay_part).map_elements(count_quoted_sents).alias(f'{essay_part}_quotes_num'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.flesch_reading_ease(x)).alias(f'{essay_part}_flesch_reading_ease')) 
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.flesch_kincaid_grade(x)).alias(f'{essay_part}_flesch_kincaid_grade'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.smog_index(x)).alias(f'{essay_part}_smog_index'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.coleman_liau_index(x)).alias(f'{essay_part}_coleman_liau_index'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.automated_readability_index(x)).alias(f'{essay_part}_automated_readability_index'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.dale_chall_readability_score(x)).alias(f'{essay_part}_dale_chall_readability_score'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.difficult_words(x)).alias(f'{essay_part}_difficult_words'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.linsear_write_formula(x)).alias(f'{essay_part}_linsear_write_formula'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.gunning_fog(x)).alias(f'{essay_part}_gunning_fog'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.text_standard(x, float_output=True)).alias(f'{essay_part}_text_standard'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.spache_readability(x)).alias(f'{essay_part}_spache_readability'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.reading_time(x)).alias(f'{essay_part}_reading_time'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.mcalpine_eflaw(x)).alias(f'{essay_part}_mcalpine_eflaw'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.syllable_count(x)).alias(f'{essay_part}_syllable_count'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.lexicon_count(x)).alias(f'{essay_part}_lexicon_count'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(lambda x: textstat.monosyllabcount(x)).alias(f'{essay_part}_monosyllab_count'))

    tmp = tmp.with_columns(pl.col(f'{essay_part}_no_punc').map_elements(sentiment_analysis).alias(f'{essay_part}_sentiment_score'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_sentiment_score').list.get(0).alias(f'{essay_part}_subj_score'))
    tmp = tmp.with_columns(pl.col(f'{essay_part}_sentiment_score').list.get(1).alias(f'{essay_part}_pol_score'))
    
    tmp = tmp.with_columns(pl.col(essay_part).map_elements(lambda x: len(x)).alias(f'{essay_part}_len'))
    tmp = tmp.with_columns(pl.col(essay_part).map_elements(lambda x: len(x.split('.'))).alias(f'{essay_part}_sentence_cnt'),
                    pl.col(essay_part).map_elements(lambda x: len(x.split(' '))).alias(f'{essay_part}_word_cnt'),)
    
    tmp = tmp.drop([f'{essay_part}_sentiment_score'])
    torch.cuda.empty_cache()

    return tmp

# feature_eng

def Essay_Parts_Eng(train_tmp, essay_part):
    paragraph_fea = [f'{essay_part}_len',f'{essay_part}_sentence_cnt',f'{essay_part}_word_cnt']
    paragraph_fea2 = [f'{essay_part}_vocab_num', f'{essay_part}_quotes_num', f'{essay_part}_flesch_reading_ease',
                      f'{essay_part}_flesch_kincaid_grade', f'{essay_part}_smog_index', f'{essay_part}_coleman_liau_index',
                      f'{essay_part}_automated_readability_index', f'{essay_part}_dale_chall_readability_score' , f'{essay_part}_difficult_words',
                      f'{essay_part}_linsear_write_formula', f'{essay_part}_gunning_fog', f'{essay_part}_text_standard',
                      f'{essay_part}_spache_readability', f'{essay_part}_reading_time', f'{essay_part}_mcalpine_eflaw',
                      f'{essay_part}_syllable_count', f'{essay_part}_lexicon_count', f'{essay_part}_monosyllab_count',
                      f'{essay_part}_subj_score', f'{essay_part}_pol_score'] + paragraph_fea
   

    aggs = [
        *[pl.col(essay_part).filter(pl.col(f'{essay_part}_len') >= i).count().alias(f'{essay_part}_>{i}_cnt') for i in [0, 50,75,100,125,150,175,200,250,300,350,400,500,600,700] ], 
        *[pl.col(essay_part).filter(pl.col(f'{essay_part}_len') <= i).count().alias(f'{essay_part}_<{i}_cnt') for i in [25,49]], 
        *[pl.col(fea).max().alias(f"{fea}_max") for fea in paragraph_fea2],
        *[pl.col(fea).mean().alias(f"{fea}_mean") for fea in paragraph_fea2],
        *[pl.col(fea).min().alias(f"{fea}_min") for fea in paragraph_fea2],
        *[pl.col(fea).sum().alias(f"{fea}_sum") for fea in paragraph_fea2],
        *[pl.col(fea).first().alias(f"{fea}_first") for fea in paragraph_fea2],
        *[pl.col(fea).last().alias(f"{fea}_last") for fea in paragraph_fea2],
        *[pl.col(fea).kurtosis().alias(f"{fea}_kurtosis") for fea in paragraph_fea2],
        *[pl.col(fea).quantile(0.25).alias(f"{fea}_q1") for fea in paragraph_fea2],
        *[pl.col(fea).quantile(0.75).alias(f"{fea}_q3") for fea in paragraph_fea2],
        ]
    aggs = [agg for agg in aggs if agg is not None]
    df = train_tmp.group_by(['essay_id'], maintain_order=True).agg(aggs).sort("essay_id")
    df = df.to_pandas()
    return df


# %%
"""tmp_para = Essay_Parts_Preprocess(train, 'paragraph', mode= 'train')
train_feats_para = Essay_Parts_Eng(tmp_para, 'paragraph')

tmp_intro = Essay_Parts_Preprocess(train, 'introduction', mode= 'train')
train_feats_intro = Essay_Parts_Eng(tmp_intro, 'introduction')
train_feats_intro.drop(['essay_id'],axis=1,inplace= True)


tmp_body = Essay_Parts_Preprocess(train, 'body', mode= 'train')
train_feats_body = Essay_Parts_Eng(tmp_body, 'body')
train_feats_body.drop(['essay_id'],axis=1,inplace= True)


tmp_concl = Essay_Parts_Preprocess(train, 'conclusion', mode= 'train')
train_feats_concl = Essay_Parts_Eng(tmp_concl, 'conclusion')
train_feats_concl.drop(['essay_id'],axis=1,inplace= True)

train_feats = pd.concat([train_feats_para, train_feats_intro, train_feats_body, train_feats_concl], axis =1)
"""

"""import time

start_time = time.time()
tmp_para = Essay_Parts_Preprocess(train, 'paragraph', mode= 'train')
end_time = time.time()

print(f"Time taken to extract Paragraph features: {end_time - start_time} seconds")

train_feats = Essay_Parts_Eng(tmp_para, 'paragraph')

train_feats['score'] = train['score']

feature_names = list(filter(lambda x: x not in ['essay_id','score'], train_feats.columns))
print('Features Number: ',len(feature_names))
train_feats.head(3)"""

# %%
def Sentence_Preprocess(tmp):
    tmp = tmp.with_columns(pl.col('full_text').map_elements(dataPreprocessing).str.split(by=".").alias("sentence"))
    tmp = tmp.explode('sentence')
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.flesch_reading_ease(x)).alias('sentence_flesch_reading_ease')) 
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.flesch_kincaid_grade(x)).alias('sentence_flesch_kincaid_grade'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.smog_index(x)).alias('sentence_smog_index'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.coleman_liau_index(x)).alias('sentence_coleman_liau_index'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.automated_readability_index(x)).alias('sentence_automated_readability_index'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.dale_chall_readability_score(x)).alias('sentence_dale_chall_readability_score'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.difficult_words(x)).alias('sentence_difficult_words'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.linsear_write_formula(x)).alias('sentence_linsear_write_formula'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.gunning_fog(x)).alias('sentence_gunning_fog'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.text_standard(x, float_output=True)).alias('sentence_text_standard'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.spache_readability(x)).alias('sentence_spache_readability'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.reading_time(x)).alias('sentence_reading_time'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.mcalpine_eflaw(x)).alias('sentence_mcalpine_eflaw'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.syllable_count(x)).alias('sentence_syllable_count'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.lexicon_count(x)).alias('sentence_lexicon_count'))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: textstat.monosyllabcount(x)).alias('sentence_monosyllab_count'))


    texts = tmp['sentence'].to_list()
    docs = list(nlp.pipe(texts, disable=['tokenizer'], batch_size = 100))  # Disable tokenizer since texts are already tokenized

    # Add POS and NER counts
    tmp = tmp.with_columns([pl.Series([pos_tag_counts(doc)[0] for doc in docs]).alias('sentence_noun_counts')])
    tmp = tmp.with_columns([pl.Series([pos_tag_counts(doc)[1] for doc in docs]).alias('sentence_verb_counts')])
    tmp = tmp.with_columns([pl.Series([pos_tag_counts(doc)[2] for doc in docs]).alias('sentence_pron_counts')])
    tmp = tmp.with_columns([pl.Series([pos_tag_counts(doc)[3] for doc in docs]).alias('sentence_adj_counts')])
    tmp = tmp.with_columns([pl.Series([pos_tag_counts(doc)[4] for doc in docs]).alias('sentence_adv_counts')])

    tmp = tmp.with_columns([pl.Series([named_entity_count(doc) for doc in docs]).alias('sentence_ner_counts')])

    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: len(x)).alias("sentence_len"))
    tmp = tmp.with_columns(pl.col('sentence').map_elements(lambda x: len(x.split(' '))).alias("sentence_word_cnt")) 
    

    return tmp

# feature_eng
sentence_fea1 = ['sentence_len','sentence_word_cnt']
sentence_fea = ['sentence_flesch_reading_ease', 'sentence_flesch_kincaid_grade', 'sentence_smog_index', 'sentence_coleman_liau_index', 
                'sentence_automated_readability_index', 'sentence_dale_chall_readability_score', 'sentence_difficult_words', 'sentence_linsear_write_formula', 
                'sentence_gunning_fog', 'sentence_text_standard', 'sentence_spache_readability',  'sentence_reading_time', 'sentence_mcalpine_eflaw', 
                'sentence_syllable_count', 'sentence_lexicon_count', 'sentence_monosyllab_count', 'sentence_noun_counts','sentence_verb_counts', 
                'sentence_pron_counts', 'sentence_adj_counts', 'sentence_adv_counts', 'sentence_ner_counts'] + sentence_fea1
def Sentence_Eng(train_tmp):
    aggs = [
        *[pl.col('sentence').filter(pl.col('sentence_len') >= i).count().alias(f"sentence_>{i}_cnt") for i in [0,15,50,100,150,200,250,300] ], 
        *[pl.col('sentence').filter(pl.col('sentence_len') <= i).count().alias(f"sentence_<{i}_cnt") for i in [15,50] ], 
        *[pl.col(fea).max().alias(f"{fea}_max") for fea in sentence_fea],
        *[pl.col(fea).mean().alias(f"{fea}_mean") for fea in sentence_fea],
        *[pl.col(fea).min().alias(f"{fea}_min") for fea in sentence_fea],
        *[pl.col(fea).sum().alias(f"{fea}_sum") for fea in sentence_fea],
        *[pl.col(fea).first().alias(f"{fea}_first") for fea in sentence_fea],
        *[pl.col(fea).last().alias(f"{fea}_last") for fea in sentence_fea],
        *[pl.col(fea).kurtosis().alias(f"{fea}_kurtosis") for fea in sentence_fea],
        *[pl.col(fea).quantile(0.25).alias(f"{fea}_q1") for fea in sentence_fea],
        *[pl.col(fea).quantile(0.75).alias(f"{fea}_q3") for fea in sentence_fea],
    
        ]
    df = train_tmp.group_by(['essay_id'], maintain_order=True).agg(aggs).sort("essay_id")
    df = df.to_pandas()
    return df


# %%
"""tmp = Sentence_Preprocess(train)
train_feats = train_feats.merge(Sentence_Eng(tmp), on='essay_id', how='left')

feature_names = list(filter(lambda x: x not in ['essay_id','score'], train_feats.columns))
print('Features Number: ',len(feature_names))
train_feats.head(3)"""

# %%
# word feature
def Word_Preprocess(tmp):
    tmp = tmp.with_columns(pl.col('full_text').map_elements(dataPreprocessing).str.split(by=" ").alias("word"))
    tmp = tmp.explode('word')
    tmp = tmp.with_columns(pl.col('word').map_elements(lambda x: len(x)).alias("word_len"))
    tmp = tmp.filter(pl.col('word_len')!=0)    
    return tmp

# feature_eng
def Word_Eng(train_tmp):
    aggs = [
        *[pl.col('word').filter(pl.col('word_len') >= i+1).count().alias(f"word_{i+1}_cnt") for i in range(15) ], 
        pl.col('word_len').max().alias(f"word_len_max"),
        pl.col('word_len').mean().alias(f"word_len_mean"),
        pl.col('word_len').std().alias(f"word_len_std"),
        pl.col('word_len').quantile(0.25).alias(f"word_len_q1"),
        pl.col('word_len').quantile(0.50).alias(f"word_len_q2"),
        pl.col('word_len').quantile(0.75).alias(f"word_len_q3"),
        ]
    df = train_tmp.group_by(['essay_id'], maintain_order=True).agg(aggs).sort("essay_id")
    df = df.to_pandas()
    return df

"""tmp = Word_Preprocess(train)
train_feats = train_feats.merge(Word_Eng(tmp), on='essay_id', how='left')

feature_names = list(filter(lambda x: x not in ['essay_id','score'], train_feats.columns))
print('Features Number: ',len(feature_names))
train_feats.head(3)"""

# %%
"""train_feats = train_feats.merge(df_train, on='essay_id', how='left')"""

# %%
"""import pickle

file_name1 = '/kaggle/working/train_df.pkl'
train_feats.to_pickle(file_name1)
print(f'Features saved to {file_name1}')

file_name2 = '/kaggle/working/df_test.pkl'
df_test.to_pickle(file_name2)
print(f'Features saved to {file_name2}')"""

# %%
import pickle
with open('/kaggle/input/essay-scoring-features/train_df_30jun.pkl', mode='br') as fi:
  train_feats_pkl = pickle.load(fi)
train_feats = pd.DataFrame(train_feats_pkl)
assert train_feats['essay_id'].is_unique
# Cached rows may be sorted differently from the competition CSV.
train_feats = train_feats.set_index('essay_id').loc[df_train['essay_id']].reset_index()
train_feats['score'] = df_train['score'].to_numpy()

# %%
vectorizer = TfidfVectorizer(
            tokenizer=lambda x: x,
            preprocessor=lambda x: x,
            token_pattern=None,
            strip_accents='unicode',
            analyzer = 'word',
            ngram_range=(3,6),
            min_df=0.05,
            max_df=0.95,
            sublinear_tf=True,
)

train_tfid = vectorizer.fit_transform([i for i in train['full_text']])
dense_matrix = train_tfid.toarray()
df = pd.DataFrame(dense_matrix)
tfid_columns = [ f'tfid_{i}' for i in range(len(df.columns))]
df.columns = tfid_columns
df['essay_id'] = train['essay_id'].to_list()
train_feats = train_feats.merge(df, on='essay_id', how='left')
feature_names = list(filter(lambda x: x not in ['essay_id','score'], train_feats.columns))
print('Number of Features: ',len(feature_names))
train_feats.head(3)

# %%
vectorizer_cnt = CountVectorizer(
            tokenizer=lambda x: x,
            preprocessor=lambda x: x,
            token_pattern=None,
            strip_accents='unicode',
            analyzer = 'word',
            ngram_range=(2,3),
            min_df=0.10,
            max_df=0.85,
)
train_tfid = vectorizer_cnt.fit_transform([i for i in train['full_text']])
dense_matrix = train_tfid.toarray()
df = pd.DataFrame(dense_matrix)
tfid_columns = [ f'tfid_cnt_{i}' for i in range(len(df.columns))]
df.columns = tfid_columns
df['essay_id'] = train['essay_id'].to_list()
train_feats = train_feats.merge(df, on='essay_id', how='left')

# %%
import joblib

deberta_oof = joblib.load('/kaggle/input/aes2-400-20240419134941/oof.pkl')
print(deberta_oof.shape, train_feats.shape)

def probability_features(probabilities):
    p = np.asarray(probabilities, dtype=np.float64)
    assert p.ndim == 2 and p.shape[1] == 6
    assert np.isfinite(p).all(), 'Nonfinite transformer outputs'
    # Accept either logits or probabilities, using the same scale at test time.
    if p.min() < 0 or p.max() > 1.00001 or not np.allclose(p.sum(axis=1), 1, atol=1e-3):
        p = softmax(p, axis=1)
    else:
        p = p / p.sum(axis=1, keepdims=True)
    values = np.arange(1, 7, dtype=np.float64)
    mean = p @ values
    return pd.DataFrame({
        **{f'deberta_oof_{i}': p[:, i] for i in range(6)},
        'deberta_mean': mean,
        'deberta_variance': p @ (values ** 2) - mean ** 2,
        'deberta_entropy': -(p * np.log(np.clip(p, 1e-12, 1))).sum(axis=1),
        **{f'deberta_above_{i}': p[:, i:].sum(axis=1) for i in range(1, 6)},
    })

# oof.pkl has no essay IDs: preserve its original train.csv row convention.
assert len(deberta_oof) == len(df_train)
deberta_train = probability_features(deberta_oof)
for col in deberta_train:
    train_feats[col] = deberta_train[col].to_numpy()

feature_names = list(filter(lambda x: x not in ['essay_id','score'], train_feats.columns))
print('Features Number: ',len(feature_names))    

train_feats.shape


# %%
fb_oof = pd.read_csv("/kaggle/usr/lib/fb3_deberta_family_inference_9_28_updated_320784/submission.csv")
fb_oof.head(6)


train_feats = pd.merge(train_feats, fb_oof, left_on="essay_id", right_on="text_id", how="left", sort=False, validate="one_to_one").drop("text_id", axis=1)
feature_names += list(fb_oof.columns.drop("text_id"))



# %%
feature_names = list(filter(lambda x: x not in ['essay_id','score'], train_feats.columns))
print('Features Number: ',len(feature_names))    

train_feats.shape

# %%
# QWK is unweighted: keep the natural essay/score distribution.
a = float(train_feats['score'].mean())

def quadratic_weighted_kappa(y_true, y_pred):
    truth = np.rint(y_true + a).astype(int)
    pred = np.rint(y_pred + a).clip(1, 6).astype(int)
    return 'QWK', cohen_kappa_score(truth, pred, weights='quadratic'), True

def qwk_obj(y_true, y_pred):
    # Continuous QWK surrogate, using only this fold's training labels.
    labels = y_true + a
    preds = y_pred + a
    center = labels.mean()
    variance = max(float(labels.var()), 1e-6)
    f = 0.5 * np.sum((preds - labels) ** 2)
    g = max(0.5 * np.sum((preds - center) ** 2 + variance), 1e-12)
    grad = ((preds - labels) / g - f * (preds - center) / g ** 2) * len(labels)
    return grad, np.ones(len(labels))

# %%
import pickle
with open('/kaggle/input/essay-scoring-features/usefe_list_30jun.pkl', mode='br') as fi:
  feature_names = pickle.load(fi)
feature_select = feature_names

feature_select = feature_select[0:4500]

# %%
# Append compact ordinal summaries even if the old feature selection omitted them.
feature_select = list(dict.fromkeys(feature_select + list(deberta_train.columns)))
feature_select = [col for col in feature_select if col in train_feats.columns]
X = train_feats[feature_select].replace([np.inf, -np.inf], np.nan).astype(np.float32)
y_split = train_feats['score'].to_numpy(dtype=np.int32)
y = y_split.astype(np.float64) - a

# No downsampling/SMOTE: synthetic neighbors created before CV leak validation
# information and distort the label marginals used by QWK. LightGBM handles NaNs.
n_splits = 5
seeds = [42, 2024]
models_by_family = {'qwk': [], 'l2': []}
oof_by_family = {name: np.zeros(len(y), dtype=np.float64) for name in models_by_family}
fold_ids = np.full(len(y), -1, dtype=np.int32)
os.makedirs('/kaggle/working/aes_models', exist_ok=True)

for seed_index, seed in enumerate(seeds):
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    for fold, (train_index, valid_index) in enumerate(skf.split(X, y_split)):
        if seed_index == 0:
            fold_ids[valid_index] = fold
        for family in models_by_family:
            model = lgb.LGBMRegressor(
                objective=qwk_obj if family == 'qwk' else 'regression',
                metric='None', learning_rate=0.035,
                max_depth=5 if family == 'qwk' else 6,
                num_leaves=10 if family == 'qwk' else 20,
                min_child_samples=30, colsample_bytree=0.3,
                reg_alpha=0.7, reg_lambda=0.1 if family == 'qwk' else 2.0,
                n_estimators=1400, random_state=seed + fold,
                extra_trees=True, verbosity=-1, device='cpu', n_jobs=-1,
            )
            model.fit(
                X.iloc[train_index], y[train_index],
                eval_set=[(X.iloc[valid_index], y[valid_index])],
                eval_metric=quadratic_weighted_kappa,
                callbacks=[log_evaluation(period=100),
                           early_stopping(stopping_rounds=100, first_metric_only=True)],
            )
            pred = model.predict(X.iloc[valid_index]) + a
            oof_by_family[family][valid_index] += pred / len(seeds)
            models_by_family[family].append(model)
            model.booster_.save_model(
                f'/kaggle/working/aes_models/{family}_{seed}_{fold}.txt')
            print(family, seed, fold, cohen_kappa_score(
                y_split[valid_index], np.rint(pred).clip(1, 6), weights='quadratic'))

# Keep continuous OOF predictions; never assign them into an integer label array.
oof_matrix = np.column_stack([oof_by_family['qwk'], oof_by_family['l2'],
                              train_feats['deberta_mean'].to_numpy()])
np.savez_compressed('/kaggle/working/aes_oof.npz',
                    essay_id=train_feats['essay_id'].to_numpy(dtype=str),
                    target=y_split, predictions=oof_matrix, fold=fold_ids)

# A small blend grid avoids an unconstrained meta-model on already stacked OOF.
# Cross-fit the blend selection; this is a meta-validation diagnostic, not a
# fully nested estimate (the supplied transformer OOF split is not available).
blend_candidates = np.array([
    [1., 0., 0.], [.85, .15, 0.], [.70, .30, 0.], [.50, .50, 0.],
    [.90, 0., .10], [.80, .10, .10], [.65, .25, .10], [.70, .10, .20],
])
def qwk_score(target, pred):
    return cohen_kappa_score(target, np.rint(pred).clip(1, 6).astype(int),
                            weights='quadratic')

def select_blend(matrix, target):
    scores = np.array([qwk_score(target, matrix @ w) for w in blend_candidates])
    # Prefer the original family when gains are negligible.
    scores -= 0.0005 * (1 - blend_candidates[:, 0])
    return blend_candidates[np.argmax(scores)]

meta_oof = np.empty(len(y), dtype=np.float64)
fold_weights = []
for fold in range(n_splits):
    valid = fold_ids == fold
    weights = select_blend(oof_matrix[~valid], y_split[~valid])
    meta_oof[valid] = oof_matrix[valid] @ weights
    fold_weights.append(weights)
base_score = qwk_score(y_split, oof_matrix[:, 0])
meta_score = qwk_score(y_split, meta_oof)
blend_weights = (np.mean(fold_weights, axis=0) if meta_score > base_score + 0.0005
                 else np.array([1., 0., 0.]))
print('OOF base QWK:', base_score, 'cross-fitted blend QWK:', meta_score,
      'chosen weights:', blend_weights)
import json
with open('/kaggle/working/aes_blend.json', 'w') as file:
    json.dump({'weights': blend_weights.tolist(), 'feature_names': feature_select,
               'base_qwk': base_score, 'meta_qwk': meta_score}, file)
gc.collect()
torch.cuda.empty_cache()

# %%
import pickle
with open('/kaggle/input/essay-scoring-features/df_test.pkl', mode='br') as fi:
    df_test_pkl = pickle.load(fi)
df_test = pd.DataFrame(df_test_pkl)

# %%
"""tmp_para = Essay_Parts_Preprocess(test, 'paragraph', mode= 'test')
test_feats_para = Essay_Parts_Eng(tmp_para, 'paragraph')

tmp_intro = Essay_Parts_Preprocess(test, 'introduction', mode= 'test')
test_feats_intro = Essay_Parts_Eng(tmp_intro, 'introduction')
test_feats_intro.drop(['essay_id'],axis=1,inplace= True)


tmp_body = Essay_Parts_Preprocess(test, 'body', mode= 'test')
test_feats_body = Essay_Parts_Eng(tmp_body, 'body')
test_feats_body.drop(['essay_id'],axis=1,inplace= True)


tmp_concl = Essay_Parts_Preprocess(test, 'conclusion', mode= 'test')
test_feats_concl = Essay_Parts_Eng(tmp_concl, 'conclusion')
test_feats_concl.drop(['essay_id'],axis=1,inplace= True)

test_feats = pd.concat([test_feats_para, test_feats_intro, test_feats_body, test_feats_concl], axis =1)

"""

tmp_para = Essay_Parts_Preprocess(test, 'paragraph', mode= 'test')
test_feats = Essay_Parts_Eng(tmp_para, 'paragraph')


# Sentence
tmp = Sentence_Preprocess(test)
test_feats = test_feats.merge(Sentence_Eng(tmp), on='essay_id', how='left')
# Word
tmp = Word_Preprocess(test)
test_feats = test_feats.merge(Word_Eng(tmp), on='essay_id', how='left')

test_feats = test_feats.merge(df_test, on='essay_id', how='left')

# Tfidf
test_tfid = vectorizer.transform([i for i in test['full_text']])
dense_matrix = test_tfid.toarray()
df = pd.DataFrame(dense_matrix)
tfid_columns = [ f'tfid_{i}' for i in range(len(df.columns))]
df.columns = tfid_columns
df['essay_id'] = test['essay_id'].to_list()
test_feats = test_feats.merge(df, on='essay_id', how='left')

# CountVectorizer
test_tfid = vectorizer_cnt.transform([i for i in test['full_text']])
dense_matrix = test_tfid.toarray()
df = pd.DataFrame(dense_matrix)
tfid_columns = [ f'tfid_cnt_{i}' for i in range(len(df.columns))]
df.columns = tfid_columns
df['essay_id'] = test['essay_id'].to_list()
test_feats = test_feats.merge(df, on='essay_id', how='left')

deberta_test = probability_features(predicted_score)
deberta_test['essay_id'] = pd.read_csv(TEST_DATA_PATH)['essay_id'].to_numpy()
test_feats = test_feats.merge(deberta_test, on='essay_id', how='left',
                              sort=False, validate='one_to_one')
    
fb3_predicted = get_fb3_predicted()
test_feats = pd.merge(test_feats,fb3_predicted, left_on="essay_id", right_on="text_id", how="left", sort=False, validate="one_to_one").drop("text_id", axis=1)   
    

# Features number
feature_names = list(filter(lambda x: x not in ['essay_id','score'], test_feats.columns))
print('Features number: ',len(feature_names))
test_feats.head(3)

# %%
X_test = test_feats.reindex(columns=feature_select).replace(
    [np.inf, -np.inf], np.nan).astype(np.float32)
test_matrix = np.column_stack([
    np.mean([model.predict(X_test) + a for model in models_by_family[family]], axis=0)
    for family in ['qwk', 'l2']
] + [test_feats['deberta_mean'].to_numpy()])
continuous_predictions = test_matrix @ blend_weights
np.save('/kaggle/working/aes_test_predictions.npy', test_matrix)
prediction_frame = pd.DataFrame({
    'essay_id': test_feats['essay_id'],
    'score': np.rint(continuous_predictions).clip(1, 6).astype(int),
})

# %%
submission = pd.read_csv(PATH + 'sample_submission.csv')[['essay_id']]
submission = submission.merge(prediction_frame, on='essay_id', how='left',
                              sort=False, validate='one_to_one')
assert submission['score'].notna().all(), 'Missing predictions for test essay IDs'
submission['score'] = submission['score'].astype(int)
assert submission['score'].between(1, 6).all()
submission.to_csv('submission.csv', index=False)
print(submission.head())
