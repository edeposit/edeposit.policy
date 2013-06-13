Požadavky na systém a jeho omezení
----------------------------------

Požadavky na funci systému
..........................

Požadavky které jsou kladeny na funkci systému.

- systém umí registrovat **ISBN**
- systém umožňuje vkládat **PDF**
- epublikace jsou zabezpečeny podle běžných standardů a postupů
- epublikace může obsahovat více souborů
- epublikace mohou být zpřístupněny za pomoci **OAI-PMH**, **OPDS**, 
  **eReading.cz**, **Flexibooks**, **ebary**, **BookJet**, **eBookEater**,
  **Publero**, **JDK**
- epublikace může být vložena za pomoci **Webarchiv** ci **ingest** modul
- systém při vkládání souboru vytváří *PDF* náhled 
- systém informuje **Aleph**, že jsou epublikace připraveny na doplnění bibliografických dat
- systém načítá bibliografická data ze systému **Aleph**
- systém ukládá epublikace do systému **LTP** k trvalé archivaci
- systém přijímá i anonymní epublikace
- systém před uložením epublikace do **LTP** provádí validaci
- systém poskytuje registraci pro nakladatele, jednoduchou, nebo s více rolemi
- systém kontroluje **ISBN**
- systém aplikuje podmínky užití
- systém přijímá i epublikace s binárními přílohami
- systém autorizuje uživatele vůči firemní **ActiveDirectory**, nebo vůčí **LDAP**
- systém zjišťuje přítomnost virů ve vložených souborech
- systém umí načítat epublikace z **ftp**, nebo z emailové schránky
- systém nabízí možnost generovat **Mobi**
- systém zobrazuje **PDF** náhled

Omezení systému
...............

- systém nepřijímá publikace s ochranou proti kopírování, např **DRM**
- systém ukládá do **LTP** jen ty **PDF** soubory, co mají textovou vrstvu
