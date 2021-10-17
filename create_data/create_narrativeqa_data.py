import hashlib
import json
from typing import List

import datasets

DATASET = "narrativeqa"


def create_hash(context: str, question: str) -> str:
    hashlib_input = context + question
    hash = hashlib.md5(hashlib_input.encode("utf-8")).hexdigest()
    return hash


def create_dataset_split(dataset: List[dict], split: str):
    all_questions = []
    all_answers = []
    seen_ids = set()

    for query in dataset:
        context = query['document']['summary']['text']
        question = query['question']['text']
        answers = sorted(set(e['text'] for e in query['answers']))
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
    narrativeqa = datasets.load_dataset("narrativeqa")
    create_dataset_split(narrativeqa['validation'], 'dev')
    create_dataset_split(narrativeqa['test'], 'test')


if __name__ == "__main__":
    main()
