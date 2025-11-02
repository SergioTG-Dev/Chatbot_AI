#!/usr/bin/env python3
"""Generate NLU examples from gcba_faqs_db.py into a small YAML file.

Usage:
  python generate_faq_nlu.py --out ../data/faq_nlu_examples.yml

The script imports the `gcba_faqs_db.py` module (same approach as seed_faqs)
and extracts `pregunta` fields as training examples for an `faq_gcba` intent.
"""
from pathlib import Path
import importlib.util
import argparse
import textwrap


def load_faqs_module(base_dir: Path):
    """Load FAQs module trying both repo-root and backend-root layouts.
    This makes the script resilient to being run from different working dirs.
    """
    candidates = [
        base_dir / "backend" / "rasa-chat" / "src" / "rasa-chat" / "actions" / "gcba_faqs_db.py",
        base_dir / "rasa-chat" / "src" / "rasa-chat" / "actions" / "gcba_faqs_db.py",
    ]
    faqs_path = None
    for p in candidates:
        if p.exists():
            faqs_path = p
            break
    if faqs_path is None:
        # Provide helpful message with both attempted paths
        raise FileNotFoundError(
            "FAQ module not found. Tried: "
            + ", ".join(str(p) for p in candidates)
        )
    spec = importlib.util.spec_from_file_location("gcba_faqs_db", str(faqs_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module spec for {faqs_path}")
    module = importlib.util.module_from_spec(spec)
    # mypy/pyright: spec is guaranteed not None and loader is present above
    spec.loader.exec_module(module)  # type: ignore
    return getattr(module, "faqs_database", [])


def generate_nlu(faqs, max_examples=200):
    lines = ["version: '3.1'", "", "nlu:", "", "- intent: faq_gcba", "  examples: |"]
    count = 0
    for faq in faqs:
        if count >= max_examples:
            break
        p = faq.get("pregunta") or faq.get("question")
        if not p:
            continue
        # clean and indent
        for line in textwrap.wrap(p.strip(), width=200):
            lines.append(f"    - {line}")
            count += 1
            if count >= max_examples:
                break
    if count == 0:
        lines.append("    - ejemplo de pregunta frecuente")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="../data/faq_nlu_examples.yml")
    parser.add_argument("--merge", action="store_true", help="Merge generated examples into data/nlu.yml (deduplicate)")
    parser.add_argument("--nlu-path", type=str, default="../data/nlu.yml", help="Path to existing nlu.yml to merge into (relative to script)")
    parser.add_argument("--fuzzy-threshold", type=float, default=0.85, help="Fuzzy dedupe threshold (0-1) using difflib ratio")
    args = parser.parse_args()

    # Prefer repo root if available, else backend folder
    this_path = Path(__file__).resolve()
    parents = this_path.parents
    # Typical layout: .../Chatbot_AI/backend/rasa-chat/src/rasa-chat/scripts/generate_faq_nlu.py
    # - parents[4] -> .../Chatbot_AI/backend
    # - parents[5] -> .../Chatbot_AI (repo root)
    base_dir = parents[5] if len(parents) > 5 else parents[4]
    faqs = load_faqs_module(base_dir)
    # Generate examples list (as plain strings)
    examples = []
    for faq in faqs:
        p = faq.get("pregunta") or faq.get("question")
        if p:
            examples.append(p.strip())

    if not args.merge:
        content = generate_nlu(faqs)
        out_path = Path(__file__).resolve().parents[1] / args.out
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"Wrote {out_path} with {len(examples)} FAQ items (up to 200 examples).")
        return

    # Merge mode: read existing nlu.yml and replace or append the faq_gcba block
    nlu_path = Path(__file__).resolve().parents[1] / args.nlu_path
    if not nlu_path.exists():
        print(f"NLU file not found at {nlu_path}. Creating new one.")
        nlu_text = ""
    else:
        nlu_text = nlu_path.read_text(encoding="utf-8")

    import re, datetime

    # Extract existing faq_gcba examples
    pattern = re.compile(r"(?ms)^-\s*intent:\s*faq_gcba\s*\n\s*examples:\s*\|\s*\n(.*?)(?=^-[ \t]*intent:|\Z)")
    m = pattern.search(nlu_text)
    existing_examples = []
    if m:
        block = m.group(1)
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("-"):
                item = line.lstrip("- ").strip()
                if item:
                    existing_examples.append(item)

    # Combine and deduplicate preserving order (existing first)
    # Use fuzzy matching (difflib.SequenceMatcher) to detect near-duplicates
    import difflib

    combined = []
    normalized_list = []
    threshold = float(args.fuzzy_threshold or 0.85)

    def normalize(s: str) -> str:
        s2 = s.strip().lower()
        # remove punctuation
        s2 = re.sub(r"[\p{P}\p{S}]", " ", s2) if False else re.sub(r"[^\w\s]", " ", s2)
        s2 = re.sub(r"\s+", " ", s2).strip()
        return s2

    # Start with existing examples (if any)
    for ex in existing_examples:
        combined.append(ex)
        normalized_list.append(normalize(ex))

    # Add generated examples, skipping those that fuzzy-match existing ones
    for ex in examples:
        n = normalize(ex)
        is_dup = False
        for prev in normalized_list:
            # compute similarity
            ratio = difflib.SequenceMatcher(None, n, prev).ratio()
            if ratio >= threshold:
                is_dup = True
                break
        if not is_dup:
            combined.append(ex)
            normalized_list.append(n)

    # Build new block
    block_lines = ["- intent: faq_gcba", "  examples: |"]
    for ex in combined:
        # Escape any leading hyphen in the example
        safe = ex.replace('\n', ' ').strip()
        block_lines.append(f"    - {safe}")
    new_block = "\n".join(block_lines) + "\n"

    if m:
        # replace existing block
        new_text = nlu_text[: m.start()] + new_block + nlu_text[m.end() :]
    else:
        # append at end with a separating newline
        if nlu_text and not nlu_text.endswith("\n"):
            nlu_text += "\n"
        new_text = nlu_text + "\n" + new_block

    # Backup original
    bak_path = nlu_path.with_suffix(nlu_path.suffix + f".bak.{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}")
    if nlu_path.exists():
        bak_path.write_text(nlu_text, encoding="utf-8")
        print(f"Backed up original NLU to {bak_path}")

    nlu_path.parent.mkdir(parents=True, exist_ok=True)
    nlu_path.write_text(new_text, encoding="utf-8")
    print(f"Merged {len(examples)} generated examples into {nlu_path} (total {len(combined)} examples).")


if __name__ == "__main__":
    main()
