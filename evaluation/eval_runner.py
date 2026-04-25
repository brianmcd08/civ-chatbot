import csv

import anthropic
from dotenv import load_dotenv

from evaluation.schema import JudgeScore
from src.chains.response_generator import generate_response
from src.config import ANTHROPIC_JUDGE

load_dotenv()
client = anthropic.Anthropic()


def judge_response(
    question: str, ideal_answer: str, generated_response: str
) -> JudgeScore:
    # call Claude API with a prompt that includes all three
    # parse the response into {"faithfulness": int, "relevance": int, "reasoning": str}
    # return that dict

    faithfulness_prompt = """
    Faithfulness: Does the answer stick to what the ideal answer says, or does it
    hallucinate / add things not in the source material?

    Respond with one of the following numbers as a measure of faithfulness 
    (reasoning and example given for clarity):

    1: Answer contradicts the context or adds clearly fabricated facts.
    Example: States wrong stat, invents a unit name.

    2: Mostly grounded but contains at least one unsupported claim or small error.
    Example: Gets the right unit but wrong production cost.

    3: Every factual claim is supported by the retrieved context. No hallucination.
    Example: All stats match context exactly. 
    """

    relevance_prompt = """
    Relevance: Does the answer address what was asked? A technically correct answer about the wrong thing
    should score low here.

    Respond with one of the following numbers as a measure of relevance 
    (reasoning and example given for clarity):

    1. Answer misses the question entirely or addresses a different topic.
    Example: Asked about Feudalism boost, answered about Feudalism era.

    2. Partially answers the question--right domain, missing key info or includes significant padding.
    Example: Gives partial unit list or omits era.

    3. Directly and completely answers what was asked.
    Example: Names both Mayan leaders when asked for all.
    """

    reasoning_prompt = """
    Reasoning: Explain specifically what the response got right or wrong before giving your scores.
    """

    system_prompt = f"""
    You are an impartial evaluator. Your job is to assess the quality of a model-generated response based on a
      defined rubric.

    Follow these rules strictly:
    - Be objective and consistent.
    - Do not be influenced by writing style unless explicitly part of the rubric.
    - Base your evaluation only on the provided inputs.
    - Do not hallucinate missing facts—if something is unclear, note it.
    - Output and return ONLY in this JSON format and nothing else, replacing your
      faithfulness score, relevance score, and reasoning:
    {{"faithfulness": <1|2|3>, "relevance": <1|2|3>, "reasoning": "<your reasoning>"}}

    {faithfulness_prompt}

    {relevance_prompt}

    {reasoning_prompt}
    """

    response = client.messages.parse(
        model=ANTHROPIC_JUDGE,
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"""
                Question: {question}
                Ideal Answer: {ideal_answer}
                Generated Response: {generated_response}
            """,
            }
        ],
        output_format=JudgeScore,
    )
    return response.parsed_output or JudgeScore(
        faithfulness=0, relevance=0, reasoning="Parse failed"
    )


def parse_eval_file(filepath: str) -> list:
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


items = parse_eval_file("./evaluation/eval_set.txt")
fieldnames = [
    "id",
    "question",
    "answer",
    "response",
    "faithfulness",
    "relevance",
    "reasoning",
]

with open("judgment.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for item in items:
        answer_given = generate_response(item["question"], [])
        score = judge_response(item["question"], item["answer"], answer_given)
        item["response"] = answer_given
        item["faithfulness"] = score.faithfulness
        item["relevance"] = score.relevance
        item["reasoning"] = score.reasoning
        print(f"Q{item['id']}: F={score.faithfulness} R={score.relevance}")
        writer.writerow(item)
