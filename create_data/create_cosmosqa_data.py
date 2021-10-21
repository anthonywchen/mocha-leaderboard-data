import collections
import hashlib
import json
import random
from typing import List

import datasets

DATASET = "cosmosqa"
random.seed(0)


def create_hash(context: str, question: str) -> str:
    hashlib_input = context + question
    hash = hashlib.md5(hashlib_input.encode("utf-8")).hexdigest()
    return hash


def create_dataset_split(dataset: List[dict], split: str):
    all_questions = []
    all_answers = []
    seen_ids = set()

    for query in dataset:
        context = query['context']
        question = query['question']
        answers = [query[f"answer{query['label']}"]]
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
    cosmosqa = datasets.load_dataset("cosmos_qa")

    # Split the validation set of original CosmosQA into dev/test sets by context
    context_to_position = collections.defaultdict(list)
    for pos, query in enumerate(cosmosqa['validation']):
        context_to_position[query['context']].append(pos)

    # Sample 30% of contexts as validation, 70% as test
    dev_contexts = random.sample(context_to_position.keys(),
                                 int(len(context_to_position)*.3))
    test_contexts = [context for context in context_to_position
                     if context not in dev_contexts]

    # Get all data points corresponding to the contexts
    dev_dataset = [cosmosqa['validation'][pos] for context in dev_contexts
                   for pos in context_to_position[context]]
    test_dataset = [cosmosqa['validation'][pos] for context in test_contexts
                   for pos in context_to_position[context]]

    create_dataset_split(cosmosqa['train'], 'train')
    create_dataset_split(dev_dataset, 'dev')
    create_dataset_split(test_dataset, 'test')


if __name__ == "__main__":
    main()
