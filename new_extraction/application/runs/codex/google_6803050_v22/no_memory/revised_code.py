# %%
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

# %%
ROOT = '../input/google-quest-challenge/'

test_df = pd.read_csv(ROOT+'test.csv')

# %%
target_cols = ['question_asker_intent_understanding', 'question_body_critical', 
               'question_conversational', 'question_expect_short_answer', 
               'question_fact_seeking', 'question_has_commonly_accepted_answer', 
               'question_interestingness_others', 'question_interestingness_self', 
               'question_multi_intent', 'question_not_really_a_question', 
               'question_opinion_seeking', 'question_type_choice', 
               'question_type_compare', 'question_type_consequence', 
               'question_type_definition', 'question_type_entity', 
               'question_type_instructions', 'question_type_procedure', 
               'question_type_reason_explanation', 'question_type_spelling', 
               'question_well_written', 'answer_helpful', 
               'answer_level_of_information', 'answer_plausible', 
               'answer_relevance', 'answer_satisfaction', 
               'answer_type_instructions', 'answer_type_procedure', 
               'answer_type_reason_explanation', 'answer_well_written']

# %%
import torch
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
from torch.utils.data import RandomSampler, SequentialSampler
from pytorch_transformers import BertTokenizer

# %%
import pandas as pd
from pathlib import Path
import pickle

def read_data(raw_data_path):
    test = pd.read_csv(raw_data_path, encoding='utf-8')
    targets = [-1] * len(test)
    # Preserve checkpoint preprocessing, including title/body concatenation.
    sentence_a = test['question_title'].fillna('') + test['question_body'].fillna('')
    sentence_b = test['answer'].fillna('')

    return targets, sentence_a, sentence_b


def save_pickle(data, file_path):
    '''
    :param data:
    :param file_name:
    :param pickle_path:
    :return:
    '''
    if isinstance(file_path, Path):
        file_path = str(file_path)
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
        
y, X_a, X_b  = read_data(ROOT+'test.csv')

# %%
data = []
for step, (data_x_a, data_x_b, data_y) in enumerate(zip(X_a, X_b, y)):
    data.append(([data_x_a, data_x_b], data_y))

# %%
tokenizer = BertTokenizer("/kaggle/input/bertpretrained/uncased_L-24_H-1024_A-16/uncased_L-24_H-1024_A-16/vocab.txt", True)

# %%
class InputExample(object):
    def __init__(self, guid, text_a, text_b=None, label=None):
        """Constructs a InputExample.
        Args:
            guid: Unique id for the example.
            text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
            text_b: (Optional) string. The untokenized text of the second sequence.
            Only must be specified for sequence pair tasks.
            label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label
        
class InputFeature(object):
    '''
    A single set of features of data.
    '''

    def __init__(self, input_ids, input_mask, segment_ids, label_id, input_len):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_id = label_id
        self.input_len = input_len
        
def create_examples(lines, example_type):
    '''
    Creates examples for data
    '''
    examples = []
    for i, line in enumerate(lines):
        guid = '%s-%d' % (example_type, i)
        text_a = line[0][0]
        text_b = line[0][1]
        label = line[1]
        example = InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label)
        examples.append(example)
    return examples

def truncate_seq_pair(tokens_a, tokens_b, max_length=512):
    # This is a simple heuristic which will always truncate the longer sequence
    # one token at a time. This makes more sense than truncating an equal percent
    # of tokens from each, since if one sequence is very short then each token
    # that's truncated likely contains more information than a longer sequence.
    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()
                
def create_features(examples, max_seq_len=512):
    '''
    # The convention in BERT is:
    # (a) For sequence pairs:
    #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
    #  type_ids:   0   0  0    0    0     0       0   0   1  1  1  1   1   1
    # (b) For single sequences:
    #  tokens:   [CLS] the dog is hairy . [SEP]
    #  type_ids:   0   0   0   0  0     0   0
    '''
    features = []
    for ex_id, example in enumerate(examples):
        tokens_a = tokenizer.tokenize(example.text_a)
        tokens_b = None
        label_id = example.label

        if example.text_b:
            tokens_b = tokenizer.tokenize(example.text_b)
            # Modifies `tokens_a` and `tokens_b` in place so that the total
            # length is less than the specified length.
            # Account for [CLS], [SEP], [SEP] with "- 3"
            truncate_seq_pair(tokens_a, tokens_b, max_length=max_seq_len - 3)
        else:
            # Account for [CLS] and [SEP] with '-2'
            if len(tokens_a) > max_seq_len - 2:
                tokens_a = tokens_a[:max_seq_len - 2]
        tokens = ['[CLS]'] + tokens_a + ['[SEP]']
        segment_ids = [0] * len(tokens)
        if tokens_b:
            tokens += tokens_b + ['[SEP]']
            segment_ids += [1] * (len(tokens_b) + 1)

        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        input_mask = [1] * len(input_ids)
        padding = [0] * (max_seq_len - len(input_ids))
        input_len = len(input_ids)

        input_ids += padding
        input_mask += padding
        segment_ids += padding

        assert len(input_ids) == max_seq_len
        assert len(input_mask) == max_seq_len
        assert len(segment_ids) == max_seq_len

        feature = InputFeature(input_ids=input_ids,
                                input_mask=input_mask,
                                segment_ids=segment_ids,
                                label_id=label_id,
                                input_len=input_len)
        features.append(feature)
    return features

# %%
test_examples = create_examples(data, 'test')
test_features = create_features(test_examples)

# %%
def create_dataset(features, is_sorted=False):
    # Convert to Tensors and build dataset
    if is_sorted:
        logger.info("sorted data by th length of input")
        features = sorted(features, key=lambda x: x.input_len, reverse=True)
    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
    all_label_ids = torch.tensor([f.label_id for f in features], dtype=torch.float)
    dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)
    return dataset

# %%
test_dataset = create_dataset(test_features)
test_sampler = SequentialSampler(test_dataset)
# One model at a time and a conservative batch size keep BERT-large memory bounded.
# Right-padding can be removed per batch without changing token positions.
def trim_padding(batch):
    columns = [torch.stack(items) for items in zip(*batch)]
    width = int(columns[1].sum(dim=1).max().item())
    return tuple([column[:, :width] for column in columns[:3]] + [columns[3]])


test_dataloader = DataLoader(
    test_dataset, sampler=test_sampler, batch_size=8, collate_fn=trim_padding
)

# %%
import torch.nn as nn
from pytorch_transformers.modeling_bert import BertPreTrainedModel, BertModel


class BertForMultiClass(BertPreTrainedModel):
    def __init__(self, config):
        super(BertForMultiClass, self).__init__(config)
        self.bert = BertModel(config)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size, config.num_labels)
        self.apply(self.init_weights)

    def forward(self, input_ids, token_type_ids=None, attention_mask=None, head_mask=None):
        outputs = self.bert(input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask,
                            head_mask=head_mask)
        pooled_output = outputs[1]
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return logits

# %%
def prepare_device(use_gpu=0):
    """
    setup GPU device if available, move model into configured device
    # 如果n_gpu_use为数字，则使用range生成list
    # 如果输入的是一个list，则默认使用list[0]作为controller
    Example:
        use_gpu = '' : cpu
        use_gpu = '0': cuda:0
        use_gpu = '0,1' : cuda:0 and cuda:1
     """
    n_gpu_use = [int(x) for x in use_gpu.split(",")]
    if not use_gpu:
        device_type = 'cpu'
    else:
        device_type = f"cuda:{n_gpu_use[0]}"
    n_gpu = torch.cuda.device_count()
    if len(n_gpu_use) > 0 and n_gpu == 0:
        device_type = 'cpu'
    if len(n_gpu_use) > n_gpu:
        msg = f"Warning: The number of GPU\'s configured to use is {n_gpu}, but only {n_gpu} are available on this machine."
        n_gpu_use = range(n_gpu)
    device = torch.device(device_type)
    list_ids = n_gpu_use
    return device, list_ids

def model_device(n_gpu, model):
    '''
    :param n_gpu:
    :param model:
    :return:
    '''
    device, device_ids = prepare_device(n_gpu)
    if len(device_ids) > 1:
        model = torch.nn.DataParallel(model, device_ids=device_ids)
    if len(device_ids) == 1:
        os.environ['CUDA_VISIBLE_DEVICES'] = str(device_ids[0])
    model = model.to(device)
    return model, device

class Predictor(object):
    def __init__(self, model, n_gpu):
        self.model = model
        self.model, self.device = model_device(n_gpu=n_gpu, model=self.model)

    def predict(self, data):
        batches = []
        self.model.eval()
        with torch.no_grad():
            for batch in data:
                input_ids, input_mask, segment_ids, _ = batch
                logits = self.model(
                    input_ids.to(self.device),
                    segment_ids.to(self.device),
                    input_mask.to(self.device),
                )
                batches.append(torch.sigmoid(logits).cpu().numpy())
        if not batches:
            return np.empty((0, len(target_cols)), dtype=np.float32)
        return np.concatenate(batches, axis=0)

# %%
import gc

# v21's five-fold probability mean outperformed the single-fold v22 model.
# Keep equal weights: no held-out predictions are available to tune them.
checkpoint_paths = [f"/kaggle/input/bert-fold{fold}/" for fold in range(1, 6)]
for checkpoint_path in checkpoint_paths:
    if not os.path.isdir(checkpoint_path):
        raise FileNotFoundError("Required ensemble checkpoint: " + checkpoint_path)

prediction_sum = np.zeros((len(test_df), len(target_cols)), dtype=np.float64)
for fold, checkpoint_path in enumerate(checkpoint_paths, start=1):
    model = BertForMultiClass.from_pretrained(checkpoint_path, num_labels=len(target_cols))
    predictor = Predictor(model=model, n_gpu='0')
    fold_predictions = predictor.predict(data=test_dataloader)
    if fold_predictions.shape != prediction_sum.shape:
        raise ValueError("Unexpected prediction shape for fold %d" % fold)
    if not np.isfinite(fold_predictions).all():
        raise ValueError("Non-finite predictions for fold %d" % fold)
    prediction_sum += fold_predictions
    print("Finished fold %d/%d" % (fold, len(checkpoint_paths)))
    # Predictor also owns the model: release both before loading the next fold.
    del predictor, model, fold_predictions
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

test_predictions = prediction_sum / len(checkpoint_paths)

# %%
# Leave the ensemble continuous; unvalidated discretization introduces rank ties.
submission_df = pd.read_csv(ROOT+'sample_submission.csv')
if set(submission_df.columns) != set(['qa_id'] + target_cols):
    raise ValueError("Submission target columns do not match the model outputs")
if not test_df['qa_id'].is_unique or not submission_df['qa_id'].is_unique:
    raise ValueError("qa_id must be unique")
if set(test_df['qa_id']) != set(submission_df['qa_id']):
    raise ValueError("Test and sample submission IDs do not match")
predictions_df = pd.DataFrame(test_predictions, index=test_df['qa_id'], columns=target_cols)
submission_df[target_cols] = predictions_df.loc[submission_df['qa_id'], target_cols].to_numpy()
assert np.isfinite(submission_df[target_cols].to_numpy()).all()
assert ((submission_df[target_cols] >= 0) & (submission_df[target_cols] <= 1)).all().all()

# %%
sub_file_name = 'submission.csv'
submission_df.to_csv(sub_file_name, index=False)
