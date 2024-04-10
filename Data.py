from collections import defaultdict
from datasets import load_dataset

class SUCXProcessor:
    def __init__(self, data, mode, split):
        '''
        Initializes the NER dataset processor with dataset parameters.
        
        :param data: The dataset name.
        :param mode: The mode of the dataset.
        :param split: The split of the dataset.
        '''
        self.data = data
        self.mode = mode
        self.split = split

    def _get_ner_tags(self, tags):
        '''
        Extracts NER tags from a list of tags.
        
        :param tags: A list of NER tags.
        :returns: A dictionary with NER types as keys and lists of indices as values.
        '''
        ner_tags = defaultdict(list)
        for i, tag in enumerate(tags):
            if tag != 'O':
                ner_type = tag.split('-')[1]
                ner_tags[ner_type].append(i)
        return ner_tags

    def process_dataset(self):
        '''
        Processes the dataset and returns a list of text-entity pairs.
        
        :returns: A list of tuples, each tuple contains a string of text and a dictionary of NER entities.
        '''
        dataset = load_dataset(self.data, self.mode, split=self.split)
        ner_pair = []

        for example in dataset:
            text = ' '.join(example['tokens'])
            entities = self._get_ner_tags(example['ner_tags'])
            ner_pair.append((text, entities))
        return ner_pair



import pandas as pd

# 路径到你的TSV文件
file_path = '/Volumes/KeShu/Master_Thesis/Data/NewsEye/NewsEye-German/dev.tsv'

# 使用with语句打开文件，确保文件会被正确关闭
columns = []
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 去除每行末尾的换行符并分割行来获取各列的值
        columns.append(line.strip().split('\t'))
        # 这里你可以处理每一列，比如打印出来
    #print(columns)

        #tags.append = column[1].split('-')

ner_pairs = defaultdict(list)
ner_set = []

for co in columns:
    if len(co) == 1:
        print(co)


texts = []
tags = []

for column in columns[4:]:
    if len(column) != 1:
        texts.append(column[0])
        tags.append(column[1])
    else:
        for j,tag in enumerate(tags):
            if tag != 'O':
                tag = tag.split('-')[1]
                ner_pairs[tag].append(j)
        texts = ' '.join(texts)
        ner_set.append((texts, ner_pairs))
        texts = []
        tags = []
        ner_pairs = defaultdict(list)

print(ner_set[10])