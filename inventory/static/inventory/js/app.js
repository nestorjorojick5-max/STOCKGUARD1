(() => {
  const body = document.body;
  const root = document.documentElement;
  const languageButtons = document.querySelectorAll("[data-language-option]");
  const languageKey = "nekezab-language";
  const textOriginals = new WeakMap();
  const attributeOriginals = new WeakMap();
  const english = {
    "Kiswahili": "Swahili",
    "Chagua lugha": "Choose language",
    "Fungua menyu": "Open menu",
    "Funga menyu": "Close menu",
    "StockGuard": "StockGuard",
    "Mwanga": "Light",
    "Giza": "Dark",
    "Mwonekano": "Theme",
    "Sakinisha App": "Install app",
    "Sakinisha App kwenye kifaa": "Install app on this device",
    "Dashboard": "Dashboard",
    "Bidhaa na Stock": "Products & Stock",
    "Ripoti za mauzo": "Sales reports",
    "Manage Maboss": "Manage Bosses",
    "Manage Wafanyakazi": "Manage Workers",
    "Settings": "Settings",
    "Kuhusu App": "About the app",
    "Contact Admin": "Contact Admin",
    "Logout": "Log out",
    "Toka": "Log out",
    "Home": "Home",
    "Stock": "Stock",
    "Watu": "People",
    "Menyu kuu": "Main menu",
    "Menyu ya haraka": "Quick menu",
    "Karibu tena": "Welcome back",
    "Ingia kusimamia bidhaa, stock na mauzo.": "Sign in to manage products, stock, and sales.",
    "Jina la mtumiaji": "Username",
    "PIN / Nenosiri": "PIN / Password",
    "Nenosiri": "Password",
    "Thibitisha nenosiri": "Confirm password",
    "Ingia kwenye akaunti": "Sign in",
    "PIN imeisha muda? Wasiliana na Boss au Admin wako ili akubadilishie.": "Has your PIN expired? Contact your Boss or Admin to reset it.",
    "Umesahau nenosiri? Tuma link ya kulibadilisha kwa email": "Forgot your password? Email me a reset link",
    "StockGuard": "StockGuard",
    "Mfanyakazi": "Worker",
    "Wafanyakazi": "Workers",
    "Muhtasari wa biashara": "Business overview",
    "Habari,": "Hello,",
    "Huu hapa muhtasari wa stock na mauzo ya leo.": "Here is today's stock and sales summary.",
    "Bidhaa": "Products",
    "Aina za bidhaa": "Product types",
    "Stock iliyopo": "Current stock",
    "Vipande kwa jumla": "Total units",
    "Mauzo ya leo": "Today's sales",
    "miamala": "transactions",
    "Rekodi ya haraka": "Quick entry",
    "Rekodi mauzo": "Record a sale",
    "Chagua bidhaa": "Select a product",
    "Idadi ya kuuza": "Quantity to sell",
    "Hifadhi mauzo": "Save sale",
    "Inahitaji uangalizi": "Needs attention",
    "Stock inayoisha": "Low stock",
    "Tazama zote": "View all",
    "Hali": "Status",
    "Ongeza stock": "Restock",
    "Hakuna bidhaa zenye stock ndogo kwa sasa. ✅": "No products are low in stock right now. ✅",
    "Miamala ya karibuni": "Recent transactions",
    "Mauzo ya hivi karibuni": "Recent sales",
    "Ripoti zote": "All reports",
    "Idadi": "Quantity",
    "Jumla": "Total",
    "Aliyeuza": "Sold by",
    "Tarehe": "Date",
    "Bado hakuna mauzo yaliyorekodiwa.": "No sales have been recorded yet.",
    "Usimamizi wa mfumo": "System management",
    "Dashboard ya Admin": "Admin dashboard",
    "Karibu": "Welcome",
    ". Unaweza kusajili na kudhibiti Maboss hapa.": ". Register and manage Boss accounts here.",
    "Maboss": "Bosses",
    "Akaunti za biashara": "Business accounts",
    "Wafanyakazi": "Workers",
    "Katika biashara zote": "Across all businesses",
    "Sajili Boss Mpya": "Register a new Boss",
    "Tengeneza akaunti ya biashara na PIN ya kuanzia yenye muda wa siku 30.": "Create a business account with an initial PIN valid for 30 days.",
    "Fungua usimamizi wa Maboss": "Open Boss management",
    "Manage Maboss": "Manage Bosses",
    "Tazama hali ya akaunti, badilisha PIN au simamisha akaunti.": "View account status, reset a PIN, or suspend an account.",
    "Simamia akaunti": "Manage accounts",
    "Usimamizi wa bidhaa": "Product management",
    "Stock hupungua yenyewe kila mauzo yanaporekodiwa.": "Stock decreases automatically whenever a sale is recorded.",
    "Anza na bidhaa mpya": "Start with a new product",
    "Ongeza bidhaa": "Add a product",
    "Jina la bidhaa": "Product name",
    "Bei ya kununulia (TSh)": "Purchase price (TSh)",
    "Bei ya kuuza (TSh)": "Selling price (TSh)",
    "Idadi ya kuanzia": "Opening quantity",
    "Tahadhari ya stock ikifika": "Low-stock alert threshold",
    "Hifadhi bidhaa": "Save product",
    "Mizigo iliyonunuliwa": "Purchased stock",
    "Ongeza stock iliyofika": "Add received stock",
    "Idadi iliyonunuliwa": "Quantity purchased",
    "Bei ya kununulia kwa moja (TSh)": "Purchase price per unit (TSh)",
    "Rekodi manunuzi": "Record purchase",
    "Orodha ya bidhaa": "Product list",
    "Bei ya kununua": "Purchase price",
    "Bei ya kuuza": "Selling price",
    "Stock ndogo": "Low stock",
    "Inapatikana": "In stock",
    "Bado hakuna bidhaa. Boss anaweza kuongeza ya kwanza hapo juu.": "No products yet. The Boss can add the first one above.",
    "Mapato na miamala": "Revenue and transactions",
    "Ripoti za mauzo": "Sales reports",
    "Linganisha mauzo ya leo na jumla ya mwezi huu.": "Review today's sales or this month's total.",
    "Leo": "Today",
    "Mwezi huu": "This month",
    "⬇ Pakua PDF": "⬇ Download PDF",
    "Jumla ya mauzo": "Total sales",
    "Rekodi za mauzo": "Sales records",
    "Bidhaa zilizouzwa": "Items sold",
    "Maelezo ya mauzo": "Sales details",
    "Tarehe na muda": "Date and time",
    "Bei moja": "Unit price",
    "Jumla ya": "Total for",
    "Hakuna mauzo yaliyorekodiwa katika kipindi hiki.": "No sales were recorded during this period.",
    "Akaunti na ruhusa": "Accounts and permissions",
    "Usimamizi wa akaunti": "Account management",
    "PIN ya mwanzo hudumu siku 30. Mtumiaji abadilishe nenosiri kupitia Settings.": "The initial PIN lasts 30 days. Users should change their password in Settings.",
    "Akaunti mpya": "New account",
    "Sajili": "Register",
    "mpya": "new",
    "Barua pepe": "Email address",
    "Tengeneza akaunti": "Create account",
    "PIN ya kuanzia (hifadhi sasa):": "Initial PIN (save it now):",
    "PIN hii huonekana mara moja pekee na itaisha baada ya siku 30.": "This PIN is shown only once and expires after 30 days.",
    "Username": "Username",
    "PIN expiry": "PIN expiry",
    "Haijawekwa": "Not set",
    "Aliundwa": "Created",
    "Status": "Status",
    "✓ Active": "✓ Active",
    "Imesitishwa": "Suspended",
    "Reset PIN": "Reset PIN",
    "Sitisha": "Suspend",
    "Washa tena": "Reactivate",
    "Bado hakuna akaunti zilizosajiliwa.": "No accounts have been registered yet.",
    "Badilisha nenosiri lako la sasa.": "Change your password or recovery email.",
    "Email ya kurejesha akaunti": "Account recovery email",
    "Weka email unayoweza kufungua. Ukitaka kubadilisha nenosiri baadaye, link ya kurejesha itatumwa hapo.": "Add an email address you can access. Password recovery links will be sent there.",
    "Anwani ya barua pepe": "Email address",
    "Thibitisha nenosiri lako": "Confirm your password",
    "Hifadhi email": "Save email",
    "Inapendekezwa": "Recommended",
    "Badilisha nenosiri": "Change password",
    "Nenosiri la sasa": "Current password",
    "Nenosiri jipya": "New password",
    "Rudia nenosiri jipya": "Confirm new password",
    "Hifadhi nenosiri jipya": "Save new password",
    "STOCK": "STOCK",
    "SALES": "SALES",
    "GROWTH": "GROWTH",
    "Inapakia StockGuard": "Loading StockGuard",
    "Tunaandaa biashara yako...": "Preparing your business...",
    "StockGuard · Stock na mauzo yako, sehemu moja.": "StockGuard · Your stock and sales, all in one place.",
    "Rejesha akaunti yako": "Recover your account",
    "Umesahau nenosiri?": "Forgot your password?",
    "Weka email iliyosajiliwa. Tutakutumia link ya kubadilisha nenosiri.": "Enter your registered email and we will send you a password reset link.",
    "Tuma link ya kurejesha": "Send recovery link",
    "Rudi kwenye kuingia": "Back to sign in",
    "Hatua inayofuata": "Next step",
    "Angalia email yako": "Check your email",
    "Ikiwa akaunti inayolingana na email hiyo ipo na ina email iliyosajiliwa, tumekutumia link ya kubadilisha nenosiri. Angalia pia sehemu ya spam/junk.": "If an account with that email exists, we have sent a password reset link. Check your spam/junk folder too.",
    "Linda akaunti yako": "Secure your account",
    "Weka nenosiri jipya": "Set a new password",
    "Hifadhi nenosiri jipya": "Save new password",
    "Link haiwezi kutumika": "This link cannot be used",
    "Link hii imetumika au muda wake umeisha. Omba link mpya ili kuendelea.": "This link has already been used or has expired. Request a new link to continue.",
    "Omba link mpya": "Request a new link",
    "Imekamilika": "Complete",
    "Nenosiri limebadilishwa": "Password changed",
    "Sasa unaweza kuingia kwa kutumia nenosiri lako jipya.": "You can now sign in with your new password.",
    "Ingia kwenye akaunti": "Sign in",
    "Kuhusu StockGuard": "About StockGuard",
    "Wasiliana na msimamizi": "Contact the administrator",
    "Stock na mauzo yako, sehemu moja.": "Your stock and sales, all in one place.",
    "StockGuard ni mfumo wa kusimamia bidhaa, kurekodi manunuzi na mauzo, na kufuatilia mapato ya biashara.": "StockGuard helps you manage products, record purchases and sales, and track business revenue.",
    "Stock hupungua kiotomatiki mauzo yanapohifadhiwa.": "Stock decreases automatically when a sale is saved.",
    "Ripoti za mauzo ya siku na mwezi zinapatikana kama PDF.": "Daily and monthly sales reports are available as PDFs.",
    "Admin, Boss na Worker wana ruhusa tofauti.": "Admins, Bosses, and Workers have different permissions.",
    "Unahitaji msaada?": "Need help?",
    "Wasiliana na Admin wako kwa msaada wa akaunti, PIN iliyoisha muda au mipangilio ya biashara.": "Contact your Admin for account help, an expired PIN, or business settings.",
    "Unataka kutoka kwenye akaunti yako?": "Are you sure you want to log out?",
    "Badilisha mwonekano": "Change theme",
    "Sakinisha kwenye kifaa chako": "Install on your device",
    "Fuata maelekezo ya browser yako ili kuongeza app kwenye kifaa.": "Follow your browser's instructions to add the app to your device.",
    "Sakinisha sasa": "Install now",
    "Sawa": "Done",
    "Funga maelekezo": "Close instructions",
    "Kwenye Safari, gusa kitufe cha Share (mraba wenye mshale juu), telezesha menyu kisha chagua “Add to Home Screen” / “Ongeza kwenye Skrini ya Mwanzo”.": "In Safari, tap Share (the square with an up arrow), scroll the menu, then tap “Add to Home Screen”.",
    "Kwenye Chrome, gusa menyu ya nukta tatu (⋮) kisha chagua “Install app” au “Add to Home screen”.": "In Chrome, tap the three-dot menu (⋮), then choose “Install app” or “Add to Home screen”.",
    "Kwenye Safari ya Mac, fungua Share kisha chagua “Add to Dock”.": "In Safari on Mac, open Share and choose “Add to Dock”.",
    "Kwenye Chrome au Edge, fungua menyu ya browser kisha chagua “Install StockGuard” au “Install this site as an app”. Unaweza pia kutumia alama ya install iliyo karibu na anwani ya tovuti.": "In Chrome or Edge, open the browser menu and choose “Install StockGuard” or “Install this site as an app”. You can also use the install icon beside the address bar.",
    "Vipengele": "Features",
    "Jinsi inavyofanya kazi": "How it works",
    "Jisajili Admin": "Register as Admin",
    "Usimamizi wa biashara, rahisi zaidi": "Simpler business management",
    "Biashara yako.": "Your business.",
    "Udhibiti wako.": "Your control.",
    "Simamia bidhaa, fuatilia stock, rekodi mauzo na elewa mapato yako—vyote sehemu moja, kwenye simu au kompyuta.": "Manage products, track stock, record sales, and understand your revenue—all in one place, on phone or computer.",
    "Anza kusimamia biashara": "Start managing your business",
    "Gundua StockGuard": "Discover StockGuard",
    "Salama · Rahisi kutumia · Tayari kwa simu": "Secure · Easy to use · Mobile ready",
    "Mchoro wa dashboard ya StockGuard": "StockGuard dashboard illustration",
    "Mchoro wa dashboard inayoonyesha bidhaa, stock, mauzo na ngao ya ulinzi wa mapato": "Dashboard illustration showing products, stock, sales, and a shield protecting revenue",
    "Stock inadhibitiwa": "Stock under control",
    "Hali ya bidhaa kwa wakati": "Product status at a glance",
    "Mauzo yanafuatiliwa": "Sales tracked",
    "Ripoti zinazoeleweka": "Clear reports",
    "Faida za StockGuard": "StockGuard benefits",
    "Usikose bidhaa zinazoisha": "Know when stock is running low",
    "Rekodi mauzo kwa urahisi": "Record sales with ease",
    "Fanya maamuzi kwa taarifa": "Make informed decisions",
    "Biashara yako, kwa mtazamo mmoja": "Your business, at a glance",
    "Kila kitu muhimu.": "Everything that matters.",
    "Bila usumbufu.": "Without the hassle.",
    "StockGuard inaunganisha kazi za kila siku ili uweze kutumia muda wako kukuza biashara.": "StockGuard brings daily work together so you can focus on growing your business.",
    "Bidhaa na stock": "Products and stock",
    "Ongeza bidhaa, rekodi manunuzi na angalia kiasi kilichopo. Stock husasishwa mauzo yanapofanyika.": "Add products, record purchases, and check available quantities. Stock updates when sales are recorded.",
    "Usimamizi wa bidhaa": "Product management",
    "Mauzo na mapato": "Sales and revenue",
    "Rekodi mauzo kwa hatua chache na uone mapato ya siku pamoja na miamala ya karibuni.": "Record sales in a few steps and see daily revenue and recent transactions.",
    "Rekodi za mauzo": "Sales records",
    "Ripoti na uchambuzi": "Reports and insights",
    "Linganisha mauzo ya siku na mwezi, kisha pakua ripoti ya biashara yako kama PDF.": "Compare daily and monthly sales, then download your business report as a PDF.",
    "Ripoti zilizo wazi": "Clear reports",
    "Wafanyakazi na ruhusa": "Staff and permissions",
    "Admin, Boss na Worker hupata uwezo unaolingana na jukumu lao katika biashara.": "Admins, Bosses, and Workers get access suited to their role in the business.",
    "Udhibiti wa akaunti": "Account control",
    "Rahisi kuanza": "Easy to get started",
    "Kuanzia stock": "From stock",
    "hadi mauzo.": "to sales.",
    "Mtazamo unaoeleweka kwa mmiliki na timu yake. Taarifa husasishwa pamoja kila hatua inaporekodiwa.": "A clear view for the owner and team. Information stays in sync as each activity is recorded.",
    "Weka bidhaa": "Add products",
    "Jaza bidhaa zako na kiasi cha stock cha kuanzia.": "Enter your products and opening stock quantities.",
    "Rekodi manunuzi na mauzo": "Record purchases and sales",
    "Stock hubadilika yenyewe kulingana na shughuli za biashara.": "Stock updates automatically as business activity is recorded.",
    "Kagua matokeo": "Review results",
    "Tumia dashboard na ripoti kuona mwenendo wa biashara.": "Use the dashboard and reports to see how your business is doing.",
    "Anza leo": "Get started today",
    "Chukua usukani wa biashara yako.": "Take control of your business.",
    "StockGuard—stock, mauzo na ripoti, sehemu moja.": "StockGuard—stock, sales, and reports, all in one place.",
    "Ingia kwenye StockGuard": "Sign in to StockGuard",
    "Ingia kwenye akaunti": "Sign in to your account",
    "Jisajili kama Admin": "Register as Admin",
    "Usajili wa Admin": "Admin registration",
    "Usajili haujawashwa": "Admin registration is not enabled",
    "Mmiliki wa mfumo anahitaji kuwasha usajili wa Admin kwanza.": "The system owner must enable Admin registration first.",
    "Rudi StockGuard": "Back to StockGuard",
    "Usajili umefungwa": "Registration is closed",
    "Akaunti ya kwanza ya Admin tayari imetengenezwa. Admin anaweza kusajili Maboss kupitia dashboard.": "The first Admin account has already been created. Admins can register Bosses from the dashboard.",
    "Tayari una akaunti? Ingia": "Already have an account? Sign in",
    "Usajili wa kwanza tu": "First registration only",
    "Jisajili kama Admin": "Register as Admin",
    "Akaunti hii itasimamia mfumo mzima na kusajili Maboss wa biashara.": "This account manages the entire system and registers business Bosses.",
    "Ufunguo wa usajili": "Registration key",
    "Ufunguo huu unatolewa na mmiliki wa mfumo. Usishiriki na mtu mwingine.": "This key is provided by the system owner. Do not share it.",
    "Tengeneza akaunti ya Admin": "Create Admin account",
    "Ufunguo wa usajili si sahihi.": "The registration key is incorrect.",
    "Akaunti ya Admin imetengenezwa.": "The Admin account has been created.",
    "Umetengeneza PIN mpya kwa ": "Reset the PIN for ",
    "? PIN ya sasa haitafanya kazi.": "? The current PIN will stop working.",
    "Unataka kubadilisha hali ya akaunti ya ": "Change the account status for ",
    "Database": "Database",
    "Anwani ya barua pepe imehifadhiwa kwa akaunti yako.": "Your account email address has been saved.",
    "Nenosiri limebadilishwa kikamilifu.": "Your password has been changed successfully.",
    "Mauzo yamehifadhiwa; stock imepungua.": "Sale saved; stock has been reduced.",
    "Taarifa za mauzo si sahihi.": "The sale details are invalid.",
    "Taarifa za kuongeza stock si sahihi.": "The stock entry details are invalid.",
    "Stock haitoshi. Zilizopo: ": "Insufficient stock. Available: ",
    "Bidhaa yenye jina hili tayari ipo.": "A product with this name already exists.",
    "Jina hili tayari linatumika.": "This username is already in use.",
    "Barua pepe hii tayari inatumika.": "This email address is already in use.",
    "Nenosiri la sasa si sahihi.": "The current password is incorrect.",
    "Nenosiri si sahihi.": "The password is incorrect.",
    "Nenosiri ulilorudia halifanani.": "The passwords do not match.",
    "Muda wa PIN umeisha. Tafadhali wasiliana na msimamizi wako.": "Your PIN has expired. Please contact your administrator.",
    "Ni Boss pekee anayeweza kuongeza bidhaa.": "Only a Boss can add products.",
    "Ni Boss pekee anayeweza kuongeza stock.": "Only a Boss can add stock.",
    "Huna ruhusa ya kusimamia akaunti.": "You are not allowed to manage accounts.",
    "Huna ruhusa ya kubadilisha PIN.": "You are not allowed to reset PINs.",
    "Huna ruhusa ya kubadilisha akaunti.": "You are not allowed to change accounts.",
    "Huna ruhusa ya kusimamia akaunti hii.": "You are not allowed to manage this account.",
    "Akaunti hii haina biashara iliyounganishwa.": "This account is not connected to a business.",
    "Akaunti hii haijaunganishwa na biashara.": "This account is not connected to a business.",
    "Akaunti haijaunganishwa": "Account not connected",
    "Wasiliana na Admin ili akaunti yako iunganishwe na biashara.": "Contact your Admin to connect your account to a business.",
  };
  let currentLanguage = "sw";

  const translatedText = (original) => {
    const value = original.trim();
    if (english[value] !== undefined) return english[value];
    let match = value.match(/^(\d+)\s+miamala$/);
    if (match) return `${match[1]} transactions`;
    match = value.match(/^Jumla ya (.+)$/);
    if (match) return `Total for ${match[1]}`;
    match = value.match(/^Akaunti ya (.+) imetengenezwa\. Hifadhi PIN iliyoonyeshwa hapa\.$/);
    if (match) return `Account ${match[1]} was created. Save the PIN shown here.`;
    match = value.match(/^PIN mpya ya (.+): (\d+)$/);
    if (match) return `New PIN for ${match[1]}: ${match[2]}`;
    match = value.match(/^Akaunti ya (.+) (imewashwa|imesitishwa)\.$/);
    if (match) return `Account ${match[1]} ${match[2] === "imewashwa" ? "activated" : "suspended"}.`;
    match = value.match(/^Umetengeneza PIN mpya kwa (.+)\? PIN ya sasa haitafanya kazi\.$/);
    if (match) return `Reset the PIN for ${match[1]}? The current PIN will stop working.`;
    match = value.match(/^Unataka kubadilisha hali ya akaunti ya (.+)\?$/);
    if (match) return `Change the account status for ${match[1]}?`;
    match = value.match(/^Stock haitoshi\. Zilizopo: (\d+)\.$/);
    if (match) return `Insufficient stock. Available: ${match[1]}.`;
    return value;
  };

  const translateNode = (node) => {
    let original = textOriginals.get(node);
    if (original === undefined) {
      original = node.nodeValue;
      textOriginals.set(node, original);
    }
    const value = original.trim();
    node.nodeValue = original.replace(
      value,
      currentLanguage === "en" ? translatedText(original) : value,
    );
  };

  const applyLanguage = (language) => {
    currentLanguage = language;
    root.lang = language;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      if (!["SCRIPT", "STYLE"].includes(node.parentElement?.tagName)) translateNode(node);
    }
    document.querySelectorAll("[placeholder], [title], [aria-label]").forEach((element) => {
      let originals = attributeOriginals.get(element);
      if (!originals) {
        originals = {};
        for (const attribute of ["placeholder", "title", "aria-label"]) {
          if (element.hasAttribute(attribute)) originals[attribute] = element.getAttribute(attribute);
        }
        attributeOriginals.set(element, originals);
      }
      for (const [attribute, original] of Object.entries(originals)) {
        element.setAttribute(attribute, language === "en" ? translatedText(original) : original);
      }
    });
    languageButtons.forEach((button) => {
      const selected = button.dataset.languageOption === language;
      button.classList.toggle("selected", selected);
      button.setAttribute("aria-pressed", String(selected));
    });

    const splash = document.querySelector("[data-splash-screen]");
    const splashMessage = document.querySelector("[data-splash-message]");
    if (splash && root.classList.contains("show-splash")) {
      try {
        sessionStorage.setItem("stockguard-splash-seen", "true");
      } catch (error) {
        console.warn("StockGuard could not save the splash-screen session:", error);
      }
      const splashMessages = {
        sw: [
          "Tunaandaa biashara yako...",
          "Tunasawazisha stock na mauzo...",
          "Karibu StockGuard!",
        ],
        en: [
          "Preparing your business...",
          "Getting stock and sales ready...",
          "Welcome to StockGuard!",
        ],
      };
      let messageIndex = 0;
      const messageTimer = window.setInterval(() => {
        messageIndex = (messageIndex + 1) % splashMessages[currentLanguage].length;
        splashMessage.textContent = splashMessages[currentLanguage][messageIndex];
      }, 1300);
      window.setTimeout(() => {
        window.clearInterval(messageTimer);
        splash.classList.add("splash-leaving");
        window.setTimeout(() => {
          splash.remove();
          root.classList.remove("show-splash");
        }, 300);
      }, 4700);
    } else {
      splash?.remove();
    }
    document.cookie = `nekezab_language=${language}; Path=/; Max-Age=31536000; SameSite=Lax`;
    applyTheme(root.dataset.theme || "light");
  };

  const themeButtons = document.querySelectorAll("[data-theme-toggle]");
  const themeKey = "nekezab-theme";
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)");

  const applyTheme = (theme) => {
    root.dataset.theme = theme;
    themeButtons.forEach((button) => {
      const isDark = theme === "dark";
      const label = currentLanguage === "en" ? (isDark ? "Light" : "Dark") : (isDark ? "Mwanga" : "Giza");
      button.innerHTML = `${isDark ? "☀️" : "🌙"} <span class="theme-label">${label}</span>`;
      button.setAttribute("aria-label", currentLanguage === "en" ? `Switch to ${label.toLowerCase()} theme` : `Washa mwonekano wa ${label.toLowerCase()}`);
      button.setAttribute("aria-pressed", String(isDark));
    });
    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) themeColor.content = theme === "dark" ? "#0f172a" : "#1d4ed8";
  };

  let savedTheme = null;
  try {
    savedTheme = localStorage.getItem(themeKey);
  } catch (error) {
    console.warn("StockGuard could not read the saved theme preference:", error);
  }
  applyTheme(savedTheme === "light" || savedTheme === "dark" ? savedTheme : (systemDark.matches ? "dark" : "light"));
  let savedLanguage = null;
  try {
    savedLanguage = localStorage.getItem(languageKey);
  } catch (error) {
    console.warn("StockGuard could not read the saved language preference:", error);
  }
  applyLanguage(savedLanguage === "en" ? "en" : "sw");
  languageButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const language = button.dataset.languageOption;
      try {
        localStorage.setItem(languageKey, language);
      } catch (error) {
        console.warn("StockGuard could not save the language preference:", error);
      }
      applyLanguage(language);
    });
  });

  themeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const theme = root.dataset.theme === "dark" ? "light" : "dark";
      savedTheme = theme;
      applyTheme(theme);
      try {
        localStorage.setItem(themeKey, theme);
      } catch (error) {
        console.warn("StockGuard could not save the theme preference:", error);
      }
    });
  });

  const updateSystemTheme = (event) => {
    if (!savedTheme) applyTheme(event.matches ? "dark" : "light");
  };
  if (systemDark.addEventListener) systemDark.addEventListener("change", updateSystemTheme);
  else systemDark.addListener(updateSystemTheme);

  const openButton = document.querySelector(".menu-toggle");
  const closeButton = document.querySelector(".menu-close");

  const closeMenu = () => {
    body.classList.remove("menu-open");
    openButton?.setAttribute("aria-expanded", "false");
  };

  openButton?.addEventListener("click", () => {
    const isOpen = body.classList.toggle("menu-open");
    openButton.setAttribute("aria-expanded", String(isOpen));
  });
  closeButton?.addEventListener("click", closeMenu);
  document.querySelector("[data-menu-close]")?.addEventListener("click", closeMenu);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });

  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });

  let deferredInstallPrompt = null;
  const installButton = document.querySelector("[data-install-app]");
  const installDialog = document.querySelector("[data-install-dialog]");
  const installInstructions = document.querySelector("[data-install-instructions]");
  const confirmInstall = document.querySelector("[data-install-confirm]");
  const closeInstall = document.querySelector("[data-install-close]");

  const isInstalled = window.matchMedia("(display-mode: standalone)").matches
    || window.navigator.standalone === true;
  if (isInstalled) installButton?.classList.add("is-installed");

  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    deferredInstallPrompt = event;
  });

  window.addEventListener("appinstalled", () => {
    deferredInstallPrompt = null;
    installButton?.classList.add("is-installed");
    if (installDialog?.open) installDialog.close();
  });

  installButton?.addEventListener("click", () => {
    const ua = navigator.userAgent;
    const isIOS = /iphone|ipad|ipod/i.test(ua);
    const isAndroid = /android/i.test(ua);
    const isMacSafari = /macintosh/i.test(ua) && /safari/i.test(ua) && !/chrome|chromium/i.test(ua);

    if (deferredInstallPrompt) {
      confirmInstall.hidden = false;
      installInstructions.textContent = currentLanguage === "en"
        ? "Install StockGuard as an app on this device."
        : "Sakinisha StockGuard kama app kwenye kifaa hiki.";
    } else {
      confirmInstall.hidden = true;
      if (currentLanguage === "en") {
        if (isIOS) {
          installInstructions.textContent = english["Kwenye Safari, gusa kitufe cha Share (mraba wenye mshale juu), telezesha menyu kisha chagua “Add to Home Screen” / “Ongeza kwenye Skrini ya Mwanzo”."];
        } else if (isAndroid) {
          installInstructions.textContent = english["Kwenye Chrome, gusa menyu ya nukta tatu (⋮) kisha chagua “Install app” au “Add to Home screen”."];
        } else if (isMacSafari) {
          installInstructions.textContent = english["Kwenye Safari ya Mac, fungua Share kisha chagua “Add to Dock”."];
        } else {
          installInstructions.textContent =           english["Kwenye Chrome au Edge, fungua menyu ya browser kisha chagua “Install StockGuard” au “Install this site as an app”. Unaweza pia kutumia alama ya install iliyo karibu na anwani ya tovuti."];
        }
      } else if (isIOS) {
        installInstructions.textContent = "Kwenye Safari, gusa kitufe cha Share (mraba wenye mshale juu), telezesha menyu kisha chagua “Add to Home Screen” / “Ongeza kwenye Skrini ya Mwanzo”.";
      } else if (isAndroid) {
        installInstructions.textContent = "Kwenye Chrome, gusa menyu ya nukta tatu (⋮) kisha chagua “Install app” au “Add to Home screen”.";
      } else if (isMacSafari) {
        installInstructions.textContent = "Kwenye Safari ya Mac, fungua Share kisha chagua “Add to Dock”.";
      } else {
        installInstructions.textContent = "Kwenye Chrome au Edge, fungua menyu ya browser kisha chagua “Install StockGuard” au “Install this site as an app”. Unaweza pia kutumia alama ya install iliyo karibu na anwani ya tovuti.";
      }
    }

    if (installDialog?.showModal) installDialog.showModal();
  });

  confirmInstall?.addEventListener("click", async () => {
    if (!deferredInstallPrompt) return;
    deferredInstallPrompt.prompt();
    await deferredInstallPrompt.userChoice;
    deferredInstallPrompt = null;
    if (installDialog?.open) installDialog.close();
  });

  closeInstall?.addEventListener("click", () => {
    if (installDialog?.open) installDialog.close();
  });

  if ("serviceWorker" in navigator && window.isSecureContext) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/service-worker.js").catch((error) => {
        console.error("StockGuard service worker registration failed:", error);
      });
    });
  }
})();
