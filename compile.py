import os
import glob


def merge_md(input_folder, output_md):
    """
    1. Recursively gather all .md files from 'input_folder'.
    2. Concatenate their raw text into one big string.
       (Each file is prefaced with a header showing its filename.)
    3. Write the big string to 'output_md'.
    """
    # Step 1
    md_files = glob.glob(f"{input_folder}/**/*.md", recursive=True)
    # Step 2
    all_text = ""
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            all_text += f"# {md_file}\n\n"
            all_text += f.read() + "\n\n"
    # Step 3
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(all_text)


if __name__ == "__main__":
    input_folder = "marketing-apis"
    output_pdf = "marketing-apis-combined.md"
    merge_md(input_folder, output_pdf)
