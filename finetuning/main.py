from transformers import AutoTokenizer, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments, AutoModelWithLMHead

import sys


def load_dataset(train_path, test_path, tokenizer):
    """
    Loads training and validation data from text files into a TextDataset.
    """
    train_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=train_path,
          block_size=128)

    test_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=test_path,
          block_size=128)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset, test_dataset, data_collator


def main(politician, epochs):
    """
    High-level management of model training process.
    """
    train_path = f"..\\data\\{politician}\\training_data.txt"
    val_path = f"..\\data\\{politician}\\validation_data.txt"

    tokenizer = AutoTokenizer.from_pretrained("anonymous-german-nlp/german-gpt2")

    special_tokens_dict = {
        'bos_token': '<BOS>',
        'eos_token': '<EOS>',
        'pad_token': '<PAD>',
        'additional_special_tokens': ['<EOQ>']
    }
    tokenizer.add_special_tokens(special_tokens_dict)

    train_dataset, test_dataset, data_collator = load_dataset(train_path, val_path, tokenizer)

    model = AutoModelWithLMHead.from_pretrained("anonymous-german-nlp/german-gpt2")
    model.resize_token_embeddings(len(tokenizer))

    training_args = TrainingArguments(
        output_dir=f".\\output-models\\gpt2-{politician}-{epochs}",  # output directory
        overwrite_output_dir=True,  # overwrite the content of the output directory
        num_train_epochs=epochs,  # number of training epochs
        per_device_train_batch_size=32,  # batch size for training
        per_device_eval_batch_size=64,  # batch size for evaluation
        eval_steps=400,  # Number of update steps between two evaluations.
        save_steps=800,  # after # steps model is saved
        warmup_steps=500,  # number of warmup steps for learning rate scheduler
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        prediction_loss_only=True,
    )

    trainer.train()
    trainer.save_model()


if __name__ == "__main__":
    politician = sys.argv[1]
    for epoch in [2, 4, 6, 8, 10]:
        main(politician, epoch)
