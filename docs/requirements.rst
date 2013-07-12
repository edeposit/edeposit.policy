Požadavky na systém a jeho omezení
----------------------------------------------------------------------------------------------------

Požadavky na funkci systému
...................................................

Požadavky které jsou kladeny na funkci systému.

- systém umožňuje ukládat elektronické předlohy tištěných publikací
- tisková předloha má stejné **ISBN** jako tištěná publikace
- systém umožňuje vkládat e-publikace
- systém umožňuje doplňovat bibliografický popis e-publikace
- systém umožňuje vyměnit soubor i po přijetí akvizicí
- systém umožňuje nakladateli/vydavateli přidávat další soubory i k zamčeném záznamu
- e-publikace jsou zabezpečeny podle běžných standardů a postupů
- bibliografický záznam může obsahovat více souborů v různých formátech
- každý soubor jednoho má žádný, nebo jeden, nebo více **ISBN** a může mít i jeden **ISSN**
- e-publikace mohou být zpřístupněny za pomoci **OAI-PMH**, **OPDS**, 
  **eReading.cz**, **Flexibooks**, **ebary**, **BookJet**, **eBookEater**,
  **Publero**, **JDK**
- e-publikace může být vložena za pomoci **Webarchiv** ci **ingest** modulu
- systém při vkládání souboru vytváří **PDF** náhled 
- systém informuje **Aleph**, že jsou e-publikace připraveny na doplnění bibliografických dat
- systém načítá bibliografická data ze systému **Aleph**
- systém ukládá e-publikace do systému **LTP** k trvalé archivaci
- systém před uložením e-publikace do **LTP** provádí validaci
- systém poskytuje registraci pro nakladatele, jednoduchou, nebo s více rolemi
- systém aplikuje podmínky užití
- systém přijímá i e-publikace s binárními přílohami
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
- systém umožňuje povolit jen přihlášení za pomoci hesla, jména
- systém si pamatuje všechny verze vloženého souboru
- systém zobrazuje historii všech zadaných **ISBN** i těch, co prošly jinou cestou, než pres e-deposit
- systém zobrazuje přehled o tom, co se s e-publikací děje, tj. sleduje změny v Alephu, Krameriovi
- systém informuje, jestli u vloženého souboru garantuje dlouhodobou ochranu
  nebo jen ochranu na binární úrovni
- systém získává informace o aplikaci dlouhodobé ochrany (tj. e-publikace byla přeformátována na novější formát)
- systém umí omezit přístup nakladatele/vydavatele na readonly přístup
- systém umí zakázat nakladateli/vydavateli přístup k jednotlivým e-publikacím
- akvizice má možnost opravovat údaje v systému i po přijetí akvizicí
- systém umožňuje pdf náhled na soubory aniž by kopie opustila systém
- systém umožňuje označit e-publikaci jako zakázanou (např. při zjištění, že byla autorem okopírována)
- systém odesílá do Alephu i jednoznačnou linku na náhled e-publikace
- v systému Aleph vzniká proklik na náhled e-publikace v e-deposit

Omezení systému
............................

- pokud e-publikace prošla akvizicí, nakladatel/vydavatel má možnost jen přidávat opravy - jako další soubory. 
  Už nemůže editovat záznamy, soubory.
- systém autorizuje uživatele vůči firemní **ActiveDirectory**, nebo vůčí **LDAP**
- systém neumožňuje nikomu kromě nakladatele/vydavatele stáhnout si vložené soubory ani náhledy
- systém převádí všechny formáty do **PDF**, kvuli akvizici a katalogizaci
- systém poskytuje snadný způsob listování e-publikací, tj. náhledy po jednotlivých stránkách (hlavně pro katalogizaci, která musí celou e-publikaci prolistovat)
- systém soubory a údaje zabezbečuje asymetrickou šifrou na základě **X509** standardu
- systém přijímá e-publikace pouze ve formátě **PDF**, **ePub**, **TXT**, **DjVu**, **mobi**
- systém nepřijímá publikace s ochranou proti kopírování, např **DRM**
- systém ukládá do **LTP** jen ty **PDF** soubory, co mají textovou vrstvu
- web rozhraní systému je poskytnuto za pomoci **Plone**
- middleware k implementaci využívá **RabbitMQ**, tj. je implementován odděleně od web rozhraní
- middleware je napsaný v jazyce **Python**
