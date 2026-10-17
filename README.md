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

## Kudeploy Render

1. Hakikisha project imepushiwa kwenye GitHub, kisha Render Dashboard → **New** → **Blueprint** na chagua repository hii. Render itasoma `render.yaml` na kuunda web service.
2. Render itaomba `DATABASE_URL` wakati wa kuunda Blueprint. Weka connection string ya PostgreSQL ya Supabase; tumia **Session Pooler** na hakikisha URL ina SSL. `SECRET_KEY` inazalishwa na Render na `DEBUG=False` imewekwa kwa production.
3. Bonyeza **Apply**. Build itaweka dependencies na kukusanya static files; service itafanya migrations kisha iwake. Fungua domain ya `onrender.com` inayoonekana kwenye service.
4. Kwa kutuma password-reset email, fungua service → **Environment** na weka `EMAIL_HOST_USER` kuwa `nestorjorojick5@gmail.com`, `EMAIL_HOST_PASSWORD` kuwa Gmail App Password, na `DEFAULT_FROM_EMAIL` kuwa `NEKEZA B <nestorjorojick5@gmail.com>`. Tumia App Password, si nenosiri la kawaida la Gmail. Usiiweke kwenye Git wala kuituma kwenye chat; Render huihifadhi kama environment secret.
5. Tengeneza Admin wa kwanza kupitia **Shell** ya web service kwa kuendesha `python manage.py createsuperuser`. Ikiwa plan yako haina Shell, endesha `.\.venv\Scripts\python.exe manage.py createsuperuser` kwenye kompyuta yako, ukiwa na `DATABASE_URL` ya Supabase kwenye `.env`. Kisha ingia kwenye `/django-admin/` kwa domain ya Render na uanze kusajili Maboss.

`DATABASE_URL` ni lazima kwenye production; app itakataa kuwaka ikiwa haijawekwa ili isitumie SQLite ya muda ya Render. Kila kuanza service huendesha migrations moja kwa moja. Tumia GitHub repository ya private ikiwa hutaki code yako ionekane hadharani.

## Ukaguzi

```powershell
python manage.py check
python manage.py test inventory
```
