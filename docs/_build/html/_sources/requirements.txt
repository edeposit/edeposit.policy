Požadavky na systém a jeho omezení
----------------------------------

Požadavky na funkci systému
............................

Požadavky které jsou kladeny na funkci systému.

- systém umožňuje podávat žádosti o registraci **ISBN**
- systém umožňuje vkládat e-publikace
- systém umožňuje doplňovat bibliografický popis e-publikace
- e-publikace jsou zabezpečeny podle běžných standardů a postupů
- e-publikace může obsahovat více souborů
- každý soubor jedné e-publikace má vlastní **ISBN** a společný **ISSN**
- e-publikace mohou být zpřístupněny za pomoci **OAI-PMH**, **OPDS**, 
  **eReading.cz**, **Flexibooks**, **ebary**, **BookJet**, **eBookEater**,
  **Publero**, **JDK**
- e-publikace může být vložena za pomoci **Webarchiv** ci **ingest** modul
- systém při vkládání souboru vytváří *PDF* náhled 
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
- systém umožňuje autentifikaci za pomoci *Google*, *Facebook*, *Twitter*, *MSN*

Omezení systému
...............

- systém přijímá e-publikace pouze ve formátě **PDF**, **ePub**, **TXT**, **DjVu**, **mobi**
- systém nepřijímá publikace s ochranou proti kopírování, např **DRM**
- systém ukládá do **LTP** jen ty **PDF** soubory, co mají textovou vrstvu
- každý uložený formát té samé e-publikace má své vlastní **ISBN** kód
- všechny uložené formáty té samé e-publikace mají ten samý **ISSN** kód
