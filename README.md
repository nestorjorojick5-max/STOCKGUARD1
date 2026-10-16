# NEKEZA B · StockGuard

Mfumo wa Django wa kusimamia bidhaa, stock, mauzo na watumiaji kwa simu na kompyuta. Lugha ya kiolesura ni Kiswahili.

## Vipengele

- Admin husajili Maboss; Boss husajili na kusimamia wafanyakazi wake.
- PIN ya mwanzo hutengenezwa kwa usalama na hudumu siku 30. PIN mpya huonyeshwa mara moja tu baada ya kusajili au kufanya reset.
- Boss anaweza kuongeza bidhaa na kurekodi manunuzi yanayoongeza stock pamoja na gharama.
- Mauzo huhifadhi bei ya wakati wa mauzo na hupunguza stock kiotomatiki ndani ya database transaction.
- Ripoti za siku na mwezi zina jumla ya mauzo na zinaweza kupakuliwa kama PDF.
- NEKEZA B inaweza kusakinishwa kwenye simu/PC kupitia browser inayotumika, na mwonekano wa mwanga/giza huhifadhiwa kwenye kifaa.
- Interface inaweza kubadilishwa kati ya Kiswahili na English kwa vitufe vya SW/EN; chaguo huhifadhiwa kwenye kifaa.
- “Umesahau nenosiri?” hutuma link ya kubadilisha nenosiri kwenye email. Link hutumika mara moja na huisha baada ya saa moja.
- Django hutumia SQLite kwa maendeleo ya ndani; Supabase PostgreSQL hutumika ukiweka `DATABASE_URL`.

## Kuendesha kwa ndani

1. Tumia Python 3.10 au mpya zaidi, kisha tengeneza mazingira na sakinisha utegemezi:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. `.env` hupakiwa moja kwa moja na Django. Nakili sehemu ya email kutoka `.env.example` kwenda `.env` bila kubadilisha `DATABASE_URL`. Kwa Gmail, tumia App Password kwenye `EMAIL_HOST_PASSWORD`, na weka anwani hiyo kwenye `EMAIL_HOST_USER` na `DEFAULT_FROM_EMAIL`. Bila SMTP credentials, email za maendeleo huonekana kwenye terminal badala ya kutumwa. Kwa deploy, weka `SECRET_KEY` salama na `DEBUG=False`; usiweke `.env` kwenye Git au kushiriki connection string.
3. Tengeneza schema na akaunti ya kwanza ya Admin:

   ```powershell
   python manage.py makemigrations inventory
   python manage.py migrate
   python manage.py createsuperuser
   ```

   Akaunti ya superuser hupewa role ya Admin moja kwa moja.

4. Washa server:

   ```powershell
   python manage.py runserver
   ```

   Fungua `http://127.0.0.1:8000/`. HTTPS inahitajika kwa kusakinisha app kwenye domain ya production; `localhost` inaruhusiwa kwa majaribio.

## Supabase PostgreSQL

Tengeneza database kwenye Supabase, kisha weka connection string yake kwenye `DATABASE_URL`. Kwa deploy, tumia Session Pooler ikiwa hosting haiwezi kutumia Direct connection; weka SSL, `DEBUG=False`, `SECRET_KEY` yenye thamani salama, na `ALLOWED_HOSTS` ya domain yako. Usihifadhi nenosiri la database wala `SECRET_KEY` kwenye Git. Kisha endesha `python manage.py migrate` dhidi ya database hiyo.

## Ukaguzi

```powershell
python manage.py check
python manage.py test inventory
```
