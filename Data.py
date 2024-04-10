from collections import defaultdict
from datasets import load_dataset
import pandas as pd

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


from collections import defaultdict

class NewseyeProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ner_set = []

    def read_file(self):
        columns = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                columns.append(line.strip().split('\t'))
        return columns

    def process_columns(self, columns):
        texts = []
        tags = []
        ner_pairs = defaultdict(list)

        for column in columns[4:]:
            if len(column) != 1:
                texts.append(column[0])
                tags.append(column[1])
            else:
                for j, tag in enumerate(tags):
                    if tag != 'O':
                        tag = tag.split('-')[1]
                        ner_pairs[tag].append(j)
                texts = ' '.join(texts)
                self.ner_set.append((texts, ner_pairs))
                texts = []
                tags = []
                ner_pairs = defaultdict(list)

    def run(self):
        columns = self.read_file()
        self.process_columns(columns)

    def get_ner_set(self):
        return self.ner_set


'''file_path = '/Volumes/KeShu/Master_Thesis/Data/NewsEye/NewsEye-German/dev.tsv'


columns = []
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        columns.append(line.strip().split('\t'))


texts = []
tags = []

ner_pairs = defaultdict(list)
ner_set = []

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
        ner_pairs = defaultdict(list)'''


