import os
import sys
from pathlib import Path

from clients import hf_model_id

from unsloth import FastLanguageModel  # isort:skip
from unsloth import is_bfloat16_supported  # isort:skip
from unsloth.chat_templates import get_chat_template  # isort:skip

from paths import sft_model_path  # isort:skip
from transformers import TrainingArguments  # isort:skip
from transformers import TextStreamer  # isort:skip
from trl import SFTTrainer  # isort:skip

sys.path.append("..")  # isort:skip
from finetuning_tools import get_dataset
from huggingface_hub import login
from transformers import TrainingArguments
from trl import SFTTrainer

hf_key = os.getenv("HF_ACCESS_TOKEN")
login(token=hf_key, add_to_git_credential=True)

max_seq_length = 120_000

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=hf_model_id,
    max_seq_length=max_seq_length,
    dtype=None,
    load_in_4bit=True,
    token=hf_key,
)

tokenizer = get_chat_template(
    tokenizer,
    chat_template="chatml",
    map_eos_token=True,
)

train_dataset, dev_dataset, test_dataset = get_dataset(tokenizer)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
    use_rslora=False,
    loftq_config=None,
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_dataset,
    eval_dataset=dev_dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    dataset_num_proc=2,
    packing=False,
    args=TrainingArguments(
        disable_tqdm=True,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        eval_strategy="epoch",
        do_eval=False,
        num_train_epochs=2,
        # max_steps=10,
        learning_rate=2e-4,
        fp16=not is_bfloat16_supported(),
        bf16=is_bfloat16_supported(),
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir=sft_model_path,
        report_to="none",
    ),
)

# Training
if False:
    trainer_stats = trainer.train()


# Loading
if True:
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=str(sft_model_path),
        max_seq_length=max_seq_length,
        dtype=None,
        load_in_4bit=True,
    )

# Saving
if False:
    model.save_pretrained_merged(
        f"{sft_model_path}",
        tokenizer,
        save_method="lora",
    )
    # model.push_to_hub_merged(
    #     f"phiwi/{sft_model_path.stem}_RegulaTome_lora",
    #     tokenizer,
    #     save_method="lora",
    #     # token="",
    # )
    # model.save_pretrained_gguf(
    #     f"{sft_model_path}.GGUF", tokenizer, quantization_method=["q4_k_m", "q8_0"]
    # )

# Inference
if True:
    FastLanguageModel.for_inference(model)
    inputs = tokenizer(test_dataset[0]["doc"], return_tensors="pt").to("cuda")

    text_streamer = TextStreamer(tokenizer)
    outputs = model.generate(**inputs, streamer=text_streamer, max_new_tokens=5_000)
    pass
