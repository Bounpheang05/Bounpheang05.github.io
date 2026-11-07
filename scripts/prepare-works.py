"""Makes web-sized copies of the chosen works. The originals are only read.
Run from the project root: python -X utf8 scripts/prepare-works.py"""
import json, os, re
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
SRC = r"D:\works\ຜົນງານ"
MAX_SIDE = 2400
T, B, L, C, P = "Temple and community", "Book covers", "Logos and branding", "Commercial", "Personal"
# Wall order: strongest and most varied first. (file, title, category)
WORKS = [
 ("david-marcu-78A265wPiO4-unsplash.png", "Soft drink advert", C),
 ("Untitled-5.png 2.png", "Let's travel together", P),
 ("Journey-Notebook-Set-Free-psd-Mockup.png", "The Art of Being Alone book cover", B),
 ("ວັດລາດຫານ.png", "Boun Maha Xat festival banner", T),
 ("Bitcoin.png", "Bitcoin concept poster", P),
 ("house design.png", "Modern house advert", C),
 ("logo file3.png", "Toung FX logo", L),
 ("ວັດດອນແອ່ນ 550x250 cm.png", "Lao New Year welcome banner", T),
 ("Free_Book_Mockup_1.png", "Life-lessons book cover", B),
 ("ທິດ.png", "Language school advert", C),
 ("OYHIU71.png", "Cap logo", L),
 ("ວັດດອນແກ້ວ 300-150.png", "Lao New Year temple banner", T),
 ("family poster.png", "BP Graphic thank-you poster", P),
 ("111111.png", "Vesak Day poster", T),
 ("Untitled-1.png", "Empty pot, empty head", P),
 ("ຄູບາໂດ້ 200-300  2222.png", "Pha Pa Samakkhi banner", T),
 ("IMG_8185.png", "End of Buddhist Lent poster", T),
 ("ສາທຸແກ້ວ ປີໃໝ່.jpg", "New Year 2025-26 greeting", T),
 ("ຂະບວນແຫ່.png", "Pha Pa procession banner", T),
 ("thai.png", "Temple fundraising poster", T),
 ("quote poster 1.png", "Be strong quote poster", P),
 ("New folder (4)\ວັດດອນແອນ.jpg", "Thera Phisek ceremony banner", T),
 ("ບໍລິຈາກເຄື່ອງ.png", "Donation drive poster", T),
 ("ແຮງບັນດານໃຈ.png", "Reading quote poster", P),
 ("ສາລະວັນ.png", "New Year poster, Salavan", T),
 ("ຈົວ ນີ້ງ-Recovered.png", "Community appeal poster", T),
 ("ກະຖິນແຂວງວຽງຈັນ.png", "Kathin announcement", T),
 ("ສະຫວັນນະເຂດ3.png", "Buddha statue welcome poster", T),
 ("poster.png", "Anniversary tribute poster", T),
 ("ບຸນມະຫາຊາດ.png", "Boun Maha Xat programme", T),
 ("ສະຫວັນນະເຂດ5.png", "Temple sponsors welcome banner", T),
 ("ສະຫວັນນະເຂດ2x3.png", "Buddha statue celebration poster", T),
 ("ສະຫວັນນະເຂດ11.png", "Temple grounds sponsor banner", T),
 ("Birthday.png", "Birthday poster", P),
 ("Amazon.png", "Anniversary greeting card", T),
 ("ordination poster.png", "Ordination invitation", T),
 ("ເບັ້ນ.png", "Ordination invitation, Salavan", T),
 ("ວັດມີໄຊ.jpg", "Kathin festival poster", T),
 ("temple poster.png", "Temple building appeal", T),
 ("ເມືອງຂວາ.png", "Pha Pa Samakkhi poster", T),
 ("ເມືອງຂວາ11.png", "Thera Phisek programme", T),
 ("ຄູບາແກ້ວ.png", "Novice portrait invitation", T),
 ("ທຸແກ້ວ-2.png", "Pha Pa banner with sponsors", T),
 ("ສາທຸແກ້ວ 2.jpg", "Pha Pa invitation banner", T),
 ("ສາທຸແກ້ວ img.png", "Pha Pa festival programme", T),
 ("ສາທຸແກ້ວ.png", "Temple sponsors thank-you banner", T),
 ("ງາ.png", "Pha Pa fundraising poster", T),
 ("ດໍ້າມີ້.png", "Thera Phisek invitation", T),
 ("ຄູບາອາເທີ.png", "Thera Phisek announcement", T),
 ("ພຣະ.png", "Temple event programme", T),
 ("ສົມໂພດ.png", "Temple celebration banner", T),
 ("ວັດຫ້ວຍຂູມ.png", "Temple building sponsors banner", T),
 ("ປ້າຍ 2x3.png", "Temple hall fundraising banner", T),
 ("ວັດດອນແອນ.png", "Temple construction appeal", T),
 ("ຄູບາບຸນຫຼາຍ.png", "Temple restoration appeal", T),
 ("monk keo-Recovered.png", "Merit-making programme banner", T),
 ("ມສ ສົງ1.png", "New Year merit invitation", T),
 ("WhatsApp Image 2024-12-14 at 7.47.09 PM.jpeg", "Birthday merit appeal", T),
 ("Niphong.png", "Merit-making announcement", T),
 ("2x4 ປ້າຍເຂົ້າພັນສາວັດໂພນສະອາດ.png", "Buddhist Lent banner", T),
 ("ຂະໜາດ240-900.png", "Extra-wide temple banner", T),
 ("WhatsApp Image 2024-12-01 at 2.33.27 PM.jpeg", "Temple event header", T),
 ("ໄທຍ.png", "Memorial post", T),
 ("Untitled-2.png", "Curious Learner page cover", P),
]
os.makedirs("src/assets/works", exist_ok=True); os.makedirs("src/content/works", exist_ok=True)
slugs = {}
for order, (name, title, cat) in enumerate(WORKS, 1):
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, name)))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg
    im = im.convert("RGB"); w, h = im.size
    im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    assert slug not in slugs, slug
    slugs[slug] = 1
    im.save(f"src/assets/works/{slug}.jpg", quality=86, optimize=True, progressive=True)
    json.dump({"title": title, "category": cat, "order": order, "image": f"../../assets/works/{slug}.jpg"},
              open(f"src/content/works/{slug}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(WORKS), "works")
# Brand files, cut from the supplied logo with the paper colour made transparent
logo = Image.open(r"D:\works\Designing logo\Designing page logo.png").convert("L")
def ink(box, path):
    a = ImageOps.invert(logo.crop(box)).point(lambda v: max(0, min(255, int((v - 8) * 255 / 215))))
    out = Image.new("RGBA", a.size, (35, 35, 35, 0)); out.putalpha(a); out.save(path, optimize=True)
ink((400, 345, 850, 705), "public/mark.png")
ink((300, 340, 960, 930), "public/logo.png")
fav = Image.new("RGBA", (256, 256), (251, 249, 246, 255)); m = Image.open("public/mark.png"); m.thumbnail((200, 200), Image.LANCZOS)
fav.alpha_composite(m, ((256 - m.width) // 2, (256 - m.height) // 2)); fav.save("public/favicon.png", optimize=True)
og = Image.new("RGBA", (1200, 630), (251, 249, 246, 255)); l = Image.open("public/logo.png"); l.thumbnail((460, 460), Image.LANCZOS)
og.alpha_composite(l, ((1200 - l.width) // 2, (630 - l.height) // 2)); og.convert("RGB").save("public/og.jpg", quality=90)
