# CV szerkesztése

A két CV-PDF-et (`assets/Lodri_Gergo_oneletrajz.pdf` és `assets/Lodri_Gergo_CV_EN.pdf`) a `make_cv.py` szkript állítja elő. A dizájn (színek, elrendezés) a szkript elején van, a **tartalom** pedig a `HU = dict(...)` és `EN = dict(...)` blokkokban — sima szövegként.

## Tartalom módosítása

1. Nyisd meg a `make_cv.py`-t bármilyen szerkesztőben (pl. VS Code).
2. Keresd meg a `HU = dict(` részt (a magyar tartalom) vagy az `EN = dict(` részt (angol).
3. Írd át a szöveget az idézőjelek között. Példa — új munkahely hozzáadása a tapasztalathoz:

```python
exp=[('Új cég — Pozíció','2026. január – jelen',['Rövid leírás.']),
     ...a többi tétel...],
```

Minden tétel formátuma: `('Cím','Dátum',['felsorolás 1','felsorolás 2'])`.

## PDF-ek újragenerálása

Egyszeri előkészület (ha még nincs Python a gépeden: python.org/downloads):

```bash
pip3 install reportlab
```

Utána a projekt mappájából:

```bash
python3 tools/cv/make_cv.py
```

Ez felülírja a két PDF-et az `assets/` mappában. Ellenőrizd őket megnyitva, majd:

```bash
git add -A && git commit -m "CV frissítés" && git push
```

és 1-2 perc múlva az élő oldalon is az új CV-k lesznek.

## Színek módosítása

A szkript elején: `NAVY`, `CYAN`, `CYAND` stb. — ugyanazok a hex-kódok, mint a weboldal `styles.css`-ében.
