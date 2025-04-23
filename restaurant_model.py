import os
from contextlib import nullcontext
import torch
import tiktoken
from jam.model import GPTConfig, GPT
from typing import Literal

SEED = 1337

class RestaurantModel:
    def __init__(self, device: Literal['cpu', 'cuda'] = 'cuda', compile_model: bool = False):
        self.configure(device, compile_model)
        self.load_encoding()
    
    def configure(self, device: str, compile_model: bool) -> None:
        self.device = device
        self.compile = compile_model

        torch.manual_seed(SEED)
        torch.cuda.manual_seed(SEED)
        torch.backends.cuda.matmul.allow_tf32 = True # allow tf32 on matmul
        torch.backends.cudnn.allow_tf32 = True # allow tf32 on cudnn
        device_type = 'cuda' if 'cuda' in self.device else 'cpu' # for later use in torch.autocast
        self.ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=torch.bfloat16)

    def load_encoding(self):
        gpt_enc = tiktoken.get_encoding("gpt2")
        enc = tiktoken.Encoding(
            name="gpt2-restaurant-bot",
            pat_str=gpt_enc._pat_str,
            mergeable_ranks=gpt_enc._mergeable_ranks,
            special_tokens={
                **gpt_enc._special_tokens,
                '<|start_fn|>' : 50001,
                '<|end_fn|>' : 50002,
            }
        )

        def decode(l: list[int]) -> str:
            if 50001 in l:
                if not 50002 in l:
                    print("Warning: <|start_fn|> token found but no <|end_fn|> token found")
                else:
                    return enc.decode(l[:l.index(50001)]) + "<|start_fn|>" + enc.decode(l[l.index(50001) + 1: l.index(50002)]) + "<|end_fn|>" + enc.decode(l[l.index(50002) + 1:])
            else:
                return enc.decode(l)
        
        def encode(s: str) -> list[int]:
            return enc.encode(s, allowed_special={"<|endoftext|>", "<|start_fn|>", "<|end_fn|>"})

        self.decode = decode
        self.encode = encode

    def load(self, out_dir: str):
        checkpoint = torch.load(os.path.join(out_dir, 'ckpt.pt'), map_location=self.device)
        self.model = GPT(GPTConfig(**checkpoint['model_args']))
        state_dict = checkpoint['model']
        unwanted_prefix = '_orig_mod.'
        for k,v in list(state_dict.items()):
            if k.startswith(unwanted_prefix):
                state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
        self.model.load_state_dict(state_dict)
        self.model.eval()
        self.model.to(self.device)
        if self.compile:
            self.model = torch.compile(self.model) # requires PyTorch 2.0 (optional)
    
    def generate(self, prompt:str, num_samples: int = 1, max_new_tokens: int = 500, temperature: float = 0.8, top_k: int = 200) -> str:
        start_ids = self.encode(prompt)
        x = (torch.tensor(start_ids, dtype=torch.long, device=self.device)[None, ...])

        # run generation
        with torch.no_grad():
            with self.ctx:
                for k in range(num_samples):
                    y = self.model.generate(x, max_new_tokens, temperature=temperature, top_k=top_k)
                    ret = self.decode(y[0].tolist())
                    ret = ret[:ret.find('<|endoftext|>')]
        
        return ret