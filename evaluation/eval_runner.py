from pathlib import Path


def parse_eval_file(filepath: Path) -> list:
    results = []

    # get all lines
    with open(filepath, "r") as file:
        lines: list = []
        lines = file.readlines()
        line_number = 0

        while line_number < len(lines):
            while lines[line_number].strip() == "":
                line_number += 1

            (id, _, question) = lines[line_number].partition(")")
            line_number += 1
            answer = ""

            if line_number >= len(lines):
                break

            while line_number < len(lines) and lines[line_number].strip() != "":
                answer += lines[line_number]
                answer += " "
                line_number += 1

            result = {}
            result["id"] = id
            result["question"] = question.strip()
            result["answer"] = answer.strip()

            results.append(result)
    return results


results = parse_eval_file(Path("./evaluation/eval_set.txt"))
# print(results)
for result in results:
    print(f"id: {result['id']}")
    print(f"question: {result['question']}")
    print(f"answer {result['answer']}")
