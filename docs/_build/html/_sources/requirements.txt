Požadavky na systém a jeho omezení
----------------------------------

Požadavky na funkci systému
............................

Požadavky které jsou kladeny na funkci systému.

- systém umožňuje podávat žádosti o registraci **ISBN**
- systém umožňuje vkládat e-publikace
- systém umožňuje doplňovat bibliografický popis e-publikace
- e-publikace jsou zabezpečeny podle běžných standardů a postupů
- e-publikace může obsahovat více souborů v různých formátech
- každý soubor jedné e-publikace má vlastní **ISBN** a společný **ISSN**
- e-publikace mohou být zpřístupněny za pomoci **OAI-PMH**, **OPDS**, 
  **eReading.cz**, **Flexibooks**, **ebary**, **BookJet**, **eBookEater**,
  **Publero**, **JDK**
- e-publikace může být vložena za pomoci **Webarchiv** ci **ingest** modul
- systém při vkládání souboru vytváří **PDF** náhled 
- systém informuje **Aleph**, že jsou e-publikace připraveny na doplnění bibliografických dat
- systém načítá bibliografická data ze systému **Aleph**
- systém ukládá e-publikace do systému **LTP** k trvalé archivaci
- systém přijímá i anonymní e-publikace
- systém před uložením e-publikace do **LTP** provádí validaci
- systém poskytuje registraci pro nakladatele, jednoduchou, nebo s více rolemi
- systém kontroluje **ISBN**
- systém aplikuje podmínky užití
- systém přijímá i e-publikace s binárními přílohami
- systém autorizuje uživatele vůči firemní **ActiveDirectory**, nebo vůčí **LDAP**
- systém zjišťuje přítomnost virů ve vložených souborech
- systém umí načítat e-publikace přes vlastní **ftp** server, nebo z emailové schránky
- systém umí e-publikace stáhnout z externího **ftp** serveru
- systém nabízí možnost generovat **mobi**
- systém zobrazuje **PDF** náhled
- systém umožňuje zadávat základní bibliografický popis ručně
- systém nabízí bibliografický popis načtený ze systému **Aleph**
- systém umožňuje sloučení ručně zadaných bibliografických dat a dat z **Aleph**
- systém automaticky načítá údaje o publikacích, které byly zaregistrovány **ISBN agenturou**
- systém umožňuje autentifikaci za pomoci *Google*, *Facebook*, *Twitter*, *MSN*
- systém si pamatuje všechny verze vloženého souboru
- opravené soubory k jedné e-publikaci mají svůj **ISBN** a odkazují se na jednu e-publikaci
- systém zobrazuje historii všech zadaných **ISBN**, 
  i těch, co prošly jinou cestou, než pres e-deposit
- systém zobrazuje přehled o tom, co se s e-publikací děje
- systém informuje, jestli u vloženého souboru garantuje dlouhodobou ochranu,
  nebo jen ochranu na binární úrovni
- systém získává informace o aplikaci dlouhodobé ochrany (tj. e-publikace byla přeformátována na novější formát)
- systém umí omezit přístup nakladatele/vydavatele na readonly přístup (jen status vložených knih)

Omezení systému
...............

- systém soubory a údaje zabezbečuje asymetrickou šifrou na základě **X509** standardu
- systém přijímá e-publikace pouze ve formátě **PDF**, **ePub**, **TXT**, **DjVu**, **mobi**
- systém nepřijímá publikace s ochranou proti kopírování, např **DRM**
- systém ukládá do **LTP** jen ty **PDF** soubory, co mají textovou vrstvu
- každý uložený formát té samé e-publikace má své vlastní **ISBN** kód
- všechny uložené formáty té samé e-publikace mají ten samý **ISSN** kód
- web rozhraní systému je poskytnuto za pomoci **Plone**
- middleware k implementaci využívá **RabbitMQ**, tj. je implementován odděleně od web rozhraní
- middleware je napsaný v jazyce **Python**
