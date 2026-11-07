"""One-time CV update: add DevOps & CI/CD line while preserving the 2-page PDF."""
import fitz
from pathlib import Path

target = Path("cv/backend-engineer.pdf")
original = fitz.open(target)
if "DevOps & CI/CD:" in original[0].get_text():
    print("Already updated")
    raise SystemExit(0)
updated = fitz.open()
source = original[0]
width, height = source.rect.width, source.rect.height
cut, shift = 351.7, 16.7
page = updated.new_page(width=width, height=height)
page.show_pdf_page(fitz.Rect(0, 0, width, cut), original, 0,
                   clip=fitz.Rect(0, 0, width, cut))
page.show_pdf_page(fitz.Rect(0, cut + shift, width, height + shift), original, 0,
                   clip=fitz.Rect(0, cut, width, height))
color = (34/255, 42/255, 43/255)
label = "DevOps & CI/CD: "
description = "GitHub Actions; automated Django testing; system checks; 3-day build artifacts"
baseline = 363.3
page.insert_text((59.15, baseline), label, fontname="hebo", fontsize=9, color=color)
page.insert_text((59.15 + fitz.get_text_length(label, fontname="hebo", fontsize=9), baseline),
                 description, fontname="helv", fontsize=9, color=color)
for link in source.get_links():
    item = {k: v for k, v in link.items()
            if k in ("kind", "from", "uri", "page", "to", "zoom")}
    if item["from"].y0 >= cut:
        box = item["from"]
        item["from"] = fitz.Rect(box.x0, box.y0 + shift, box.x1, box.y1 + shift)
    page.insert_link(item)
updated.insert_pdf(original, from_page=1, to_page=len(original)-1, links=True, annots=True)
updated.set_metadata(original.metadata)
temporary = target.with_suffix(".updated.pdf")
updated.save(temporary, garbage=4, deflate=True)
updated.close()
original.close()
temporary.replace(target)
verify = fitz.open(target)
assert len(verify) == 2 and "DevOps & CI/CD:" in verify[0].get_text()
print("CV updated and verified:", target)
