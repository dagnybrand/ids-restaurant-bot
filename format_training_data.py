import os

OUT_DIR = 'tmp'

with open("new_training_data.txt", "r") as f:
    text = f.read()

groups = text.split("\n\n")

examples = []
for i in range(len(groups) // 2):
    query = groups[i * 2].strip()
    response = groups[i * 2 + 1].strip()
    header, fetch_cmd, format_cmd = response.split("\n", maxsplit=2)
    examples.append((query, header, fetch_cmd))

if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)

for i, example in enumerate(examples):
    with open(f"{OUT_DIR}/{i}.txt", "w") as fh:
        fh.write(f"{example[0]}\n{example[1]}\n<|start_fn|> {example[2]} <|end_fn|>\n\n")