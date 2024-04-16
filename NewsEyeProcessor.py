import os
import csv
from openprompt.data_utils.data_processor import DataProcessor
from openprompt.data_utils import InputExample

class NewsEyeProcessor(DataProcessor):
    def __init__(self, labels):
        super().__init__()
        self.labels = labels

    def get_examples(self, data_dir, split):
        path = os.path.join(data_dir, "{}.tsv".format(split))
        with open(path, 'r', encoding='utf8') as f:
            data = self.load_data(f)

            examples = []

            for idx, (xs, ys, spans) in enumerate(data):
                for span in spans:
                    text_a = " ".join(xs)
                    label_id = self.get_label_id(ys[span[0]][2:])
                    meta = {
                        "entity": " ".join(xs[span[0]: span[1]+1])
                    }
                    example = InputExample(guid=str(idx), text_a=text_a, meta=meta, label=label_id)
                    examples.append(example)

            return examples

    @staticmethod
    def load_data(file):
        columns = []
        data = []
        xs = []
        ys = []
        spans = []
        next(file)
        for line in file:
            columns.append(line.strip().split('\t'))
        for column in columns:
            if len(column) == 1:
                if xs != []:
                    data.append((xs, ys, spans))
                xs = []
                ys = []
                spans = []
            elif len(column) > 1:
                xs.append(column[0])
                tag = column[1]
                if tag != 'O':
                    if tag.split('-')[0] == 'B':
                        spans.append([len(ys), len(ys)])
                    else:
                        spans[-1][-1] = len(ys)
                ys.append(tag)
        return data

import os
dataset_path = 'NewsEye'
labels = ['PER', 'LOC', 'ORG', 'HumanProd']
processor = NewsEyeProcessor(labels)
train_dataset = processor.get_train_examples(dataset_path)
dev_dataset = processor.get_dev_examples(dataset_path)
test_dataset = processor.get_test_examples(dataset_path)