#!/usr/bin/env python3
"""Generate Anki deck file from word data and example sentences."""
import sys
import os

def main():
    base = os.path.dirname(os.path.abspath(__file__))

    # Read word list (pt, en, sound)
    words = []
    with open(os.path.join(base, "1000_words.tsv"), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            words.append((parts[0], parts[1], parts[2]))

    # Read extra data chunks (example_pt, example_en, notes, tag)
    extras = []
    for i in range(1, 6):
        path = os.path.join(base, f"anki_data_{i}.tsv")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line:
                    continue
                parts = line.split("\t")
                while len(parts) < 4:
                    parts.append("")
                extras.append(tuple(parts[:4]))

    if len(extras) != len(words):
        print(f"ERROR: {len(words)} words but {len(extras)} extra data entries", file=sys.stderr)
        sys.exit(1)

    out_path = os.path.join(base, "A2_Portuguese_1000words.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n")
        f.write("#html:true\n")
        f.write("#tags column:9\n")
        for (pt, en, sound), (ex_pt, ex_en, notes, tag) in zip(words, extras):
            f.write(f"{pt}\t{en}\t{ex_pt}\t{ex_en}\t{notes}\t\t\t[sound:{sound}]\t{tag}\n")

    print(f"Generated {len(words)} entries -> {out_path}")

if __name__ == "__main__":
    main()
