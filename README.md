# Ziņu Analizators
Viegli izmantojams rīks ziņu analizēšanai

## Galvenās funkcijas
- Viegla rakstu meklēšana no dažādiem ziņu avotiem
- Automātiski izveidota diagramma, cik daudz katrs ziņu avots izveidojis rakstus par meklējamo tematu
- Automātiski izveidota diagramma, cik daudz raksti kopumā izveidoti katrā dienā par meklējamo tematu
- Rezultātu eksportēšana uz MS Excel failu

## Atbalstītie ziņu avoti
- Latviešu valodā
    - Delfi
    - LSM
    - TVNET
    - Apollo
- Angļu valodā
    - AP News
    - CNN

## Instalācijas instrukcijas
1. Instalēt jaunāko python versiju (Projekts veidots Python 3.11.5)
2. Ja tas nav izdarīts, instalēt Google Chrome
3. Instalēt bibliotēkas
    - Tkinter
    - Beautiful Soup 4
    - Selenium
    - Pandas
    - Matplotlib
    - Openpyxl
4. Palaist main.py failu

## Zināmās problēmas
- Delfi ļauj meklēt tikai no esošā gada 1.janvāra
- LSM mēdz dažkārt izmest captcha pārbaudi
    - Tādā gadījumā pagaidām vienīgais risinājums ir atvērt lsm.lv meklēšanas funkciju kādā pārlūkprogrammā un manuāli atrisināt captcha