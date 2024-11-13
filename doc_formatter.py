import locale
from datetime import datetime

from pandoc import Document


def split_name_title(line: str) -> tuple[str, str]:
    words = line.split()
    capitalized_words = []
    for word in words:
        if word[0] == word[0].capitalize():
            capitalized_words.append(word)
        else:
            break
    author_name = " ".join(capitalized_words[:-1])
    return author_name, line.replace(author_name, "")


doc = Document()
with open("pandoc/ACQUISITIONS DE NOVEMBRE.docx", "rb") as f:
    doc.docx = f.read()  # type: ignore

md: str = doc.markdown.decode()  # type: ignore
md = (
    md.replace("**", "")
    .replace("En bleu, les livres très récents", "")
    .replace("\r", "")
    .replace("\n\n", "\n")
    .replace("   ", " ")
)
lines = md.split("\n")
for index, line in enumerate(lines):
    if len(line) != 0 and line[0].isalpha():
        lines[index] = "\n## " + line + "\n"
    elif len(line) != 0 and line[0] != "#":
        author, title = split_name_title(line)
        lines[index] = f"{author},{title}"

md = "\n".join(lines[1:])

year = datetime.today().year
locale.setlocale(locale.LC_TIME, "fr_FR")
month = datetime.today().strftime("%B")

md = f"# Les nouveautés du mois: {month.capitalize()} {year}" + md

with open("nouveautes.md", "w", encoding="utf-8") as f:
    f.write(md)

# with open("pandoc/LISTE ANNOTEE DE NOVEMBRE 2024.docx", "rb") as f:
#     doc.docx = f.read()  # type: ignore
# md: str = doc.markdown.decode()  # type: ignore
