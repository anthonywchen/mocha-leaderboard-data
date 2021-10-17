import hashlib
import json
from typing import List

import xmltodict

DATASET = "mcscript"


def create_hash(context: str, question: str) -> str:
    hashlib_input = context + question
    hash = hashlib.md5(hashlib_input.encode("utf-8")).hexdigest()
    return hash


def create_dataset_split(dataset: List[dict], split: str):
    all_questions = []
    all_answers = []
    seen_ids = set()

    for instance in dataset:
        context = instance['text']
        for query in instance['questions']['question']:
            question = query['@text']
            answers = [answer_dict['@text'] for answer_dict in query['answer']
                       if answer_dict['@correct'] == 'True']
            assert len(answers) == 1
            query_id = create_hash(context, question)
            if query_id in seen_ids:
                continue
            seen_ids.add(query_id)

            all_questions.append({
                "id": query_id,
                "metadata": {"dataset": DATASET},
                "context": context,
                "question": question
            })
            all_answers.append({"id": query_id, "references": answers})

    # Write question and answers to file
    with open(f'data/tmp/{DATASET}_{split}_questions.jsonl', 'w', encoding='utf-8') as f:
        for entry in all_questions:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    with open(f'data/tmp/{DATASET}_{split}_answers.jsonl', 'w', encoding='utf-8') as f:
        for entry in all_answers:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def main():
    with open('data/tmp/raw_mcscript-dev-data.xml') as f:
        data = xmltodict.parse(''.join(f.readlines()))['data']['instance']

    # Get first 30% of contexts as validation and the last 70% as test
    dev_dataset = data[:int(len(data) * .3)]
    test_dataset = data[int(len(data) * .3):]

    create_dataset_split(dev_dataset, 'dev')
    create_dataset_split(test_dataset, 'test')


if __name__ == "__main__":
    main()
