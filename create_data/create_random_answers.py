import argparse
import json
import random

import jsonlines

random.seed(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--answers_file', type=str, required=True)
    parser.add_argument('--output_file', type=str, default="allenai/unifiedqa-t5-small")
    args = parser.parse_args()

    answers = list(jsonlines.open(args.answers_file))

    with open(args.output_file, 'w', encoding='utf-8') as f:
        for line in answers:
            # Sample another answer to use as a random candidate
            random_answer = random.choice(answers)['references'][0]
            f.write(json.dumps({'id': line['id'], 'candidate': random_answer}) + '\n')
            

if __name__ == "__main__":
    main()