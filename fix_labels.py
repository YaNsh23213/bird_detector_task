from pathlib import Path
import re

DATASET_DIR = Path("dataset")
YAML_PATH = DATASET_DIR / "data.yaml"

def fix_labels():
    label_dirs = [p for p in DATASET_DIR.rglob("*") if p.is_dir() and p.name == "labels"]
    if not label_dirs:
        print("No 'labels' folders found. Check your dataset folder structure.")
        return

    total_files = 0
    for labels_dir in label_dirs:
        txt_files = list(labels_dir.glob("*.txt"))
        for txt_file in txt_files:
            lines = txt_file.read_text().strip().splitlines()
            new_lines = []
            for line in lines:
                if not line.strip():
                    continue
                parts = line.split()
                parts[0] = "0"
                new_lines.append(" ".join(parts))
            txt_file.write_text("\n".join(new_lines) + "\n")
        total_files += len(txt_files)
        print(f"Processed {labels_dir}: {len(txt_files)} files")

    print(f"Labels fixed: {total_files} files updated, all class ids set to 0 (bird).")

def fix_yaml():
    content = YAML_PATH.read_text()
    content = re.sub(r"nc:\s*\d+", "nc: 1", content)
    content = re.sub(r"names:\s*\[.*?\]", "names: ['bird']", content)
    YAML_PATH.write_text(content)
    print("data.yaml updated: nc=1, names=['bird'].")

if __name__ == "__main__":
    fix_labels()
    fix_yaml()