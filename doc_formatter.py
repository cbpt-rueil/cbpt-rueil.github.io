import locale
from datetime import datetime


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


with open("tmp/nouveautes.md", "rb") as f:
    nouveautes: str = f.read().decode()

nouveautes = (
    nouveautes.replace("**", "")
    .replace("En bleu, les livres très récents", "")
    .replace("\r", "")
    .replace("\n\n", "\n")
    .replace("   ", " ")
)
lines = nouveautes.split("\n")

for index, line in enumerate(lines):
    if len(line) != 0 and line[0].isalpha():
        lines[index] = "\n## " + line + "\n"
    elif len(line) != 0 and line[0] != "#":
        author, title = split_name_title(line)
        lines[index] = f"{author},{title}"

nouveautes = "\n".join(lines[1:])

year = datetime.today().year
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
month = datetime.today().strftime("%B")

nouveautes = f"# Les nouveautés du mois: {month.capitalize()} {year}" + nouveautes

with open("nouveautes.md", "w", encoding="utf-8") as f:
    f.write(nouveautes)

with open("tmp/conseils.md", "rb") as f:
    conseils = f.read().decode()

advice_header = """# Nos conseils de lecture

Au moins une fois par trimestre, nous proposons une liste de livres accompagnés
de commentaires de nos lecteurs. Si vous cherchez votre prochaine lecture, cette
page peut être pour vous !

## """

conseils = advice_header + (
    conseils.replace("**", "")
    .replace("\r", "")
    .replace("\n\n", "\n")
    .replace("ANNOTEE", "ANNOTÉE")
)

with open("conseils.md", "w", encoding="utf-8") as f:
    f.write(conseils)
