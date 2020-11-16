"""
Provides testing functionality for language generation.
"""

from transformers import AutoTokenizer, AutoModelWithLMHead


def generate_response(question):
    input_ids = tokenizer.encode(question, return_tensors="pt")
    sample_output = model.generate(
        input_ids,
        do_sample=True,
        max_length=100,
        top_p=0.9,
        top_k=0,
    )
    output = tokenizer.decode(sample_output[0], skip_special_tokens=True)
    return output


def main():
    while True:
        question = input("Your sentence:   ")
        if question == "exit":
            break
        answer = generate_response(question)
        print("Output:\n" + 100 * '-')
        print(answer)


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("anonymous-german-nlp/german-gpt2")
    model = AutoModelWithLMHead.from_pretrained(".\\output-models\\gpt2-lindner\\")
    main()

