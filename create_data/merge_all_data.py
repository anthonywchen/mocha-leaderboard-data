import glob
import json
import random

import jsonlines

random.seed(0)


def merge_data(split: str, max_dp_per_dataset: int = 999999) -> None:
    answer_files = sorted(glob.glob(f"data/tmp/*{split}_answers.jsonl"))
    question_files = sorted(glob.glob(f"data/tmp/*{split}_questions.jsonl"))

    # Load all data
    all_answers = []
    all_questions = []
    for ans_file, ques_file in zip(answer_files, question_files):
        print(ans_file, ques_file)
        answers = list(jsonlines.open(ans_file))
        questions = list(jsonlines.open(ques_file))
        assert len(answers) == len(questions)

        # Sample data points by sampling indices
        num_dp = len(answers)
        idxs = random.sample(range(num_dp), min(num_dp, max_dp_per_dataset))
        sampled_answers = [answers[idx] for idx in idxs]
        sampled_questions = [questions[idx] for idx in idxs]

        all_answers += sampled_answers
        all_questions += sampled_questions

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
    merge_data('dev', 1500)
    merge_data('test', 2500)
    merge_data('train', 20000)


if __name__ == "__main__":
    main()
