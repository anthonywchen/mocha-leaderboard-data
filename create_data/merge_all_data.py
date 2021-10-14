import glob
import json

import jsonlines


def merge_data(split: str):
    answer_files = sorted(glob.glob(f"data/*{split}_answers.jsonl"))
    question_files = sorted(glob.glob(f"data/*{split}_questions.jsonl"))

    # Load all data
    all_answers = []
    for filename in answer_files:
        all_answers += list(jsonlines.open(filename))

    all_questions = []
    for filename in question_files:
        all_questions += list(jsonlines.open(filename))

    # Run some checks of the data
    seen_ids = set()
    assert len(all_answers) == len(all_questions)

    for i in range(len(all_answers)):
        assert all_answers[i]['id'] not in seen_ids
        seen_ids.add(all_answers[i]['id'])
        assert all_answers[i]['id'] == all_questions[i]['id']
        assert 'context' in all_questions[i]
        assert 'question' in all_questions[i]
        assert len(all_answers[i]['references']) > 0

    # Merge into one file
    with open(f'data/{split}_answers.jsonl', 'w', encoding='utf-8') as f:
        for entry in all_answers:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    with open(f'data/{split}_questions.jsonl', 'w', encoding='utf-8') as f:
        for entry in all_questions:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def main():
    merge_data('dev')
    merge_data('test')


if __name__ == "__main__":
    main()
