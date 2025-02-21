from transformers import MistralForCausalLM, AutoTokenizer,pipeline, TextStreamer
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch,os
# os.environ['CUDA_VISIBLE_DEVICES']='0'
base_model="/home/ruben/disk2/HF_MODELS/DeepSeek-R1-Distill-Qwen-1.5B"# 31
# base_model="/home/ruben/disk2/HF_MODELS/DeepSeek-R1-Distill-Qwen-7B"# 74
# base_model="/home/ruben/disk2/HF_MODELS/Meta-Llama-3-8B-Instruct" #32.9

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    # quantization_config=bnb_config,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    # trust_remote_code=False,
    offload_buffers=False,
    local_files_only=True
)

tokenizer= AutoTokenizer.from_pretrained(base_model,local_files_only=True, padding=True, truncation=True)


def build_prompt(role,query):
    prompt={"role": role,"content": query}
    return prompt