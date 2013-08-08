Požadavky na systém a jeho omezení
----------------------------------------------------------------------------------------------------

Požadavky na funkci systému
...................................................

Požadavky které jsou kladeny na funkci systému.

#. systém umožňuje ukládat elektronické předlohy tištěných publikací
#. systém umožňuje vkládat e-publikace licencované i Open Access e-publikace
#. systém umožňuje ohlašovat i tištěné publikace
#. uložené soubory v systému kontroluje pracovník akvizice
#. systém umožňuje doplňovat základní metadata e-publikace nakladatelem
#. systém umožňuje vyměnit soubor i po přijetí akvizicí
#. systém umožňuje nakladateli/vydavateli přidávat další soubory i po přijetí e-publikace akvizicí
#. e-publikace může obsahovat více souborů v různých formátech
#. každý soubor jednoho má žádný, nebo jeden, nebo více **ISBN** a může mít i jeden **ISSN**
#. tisková předloha má stejné **ISBN** jako tištěná publikace
#. e-publikace mohou být zpřístupněny za pomoci **OAI-PMH**, **OPDS**, 
   **eReading.cz**, **Flexibooks**, **ebary**, **BookJet**, **eBookEater**,
   **Publero**, **JDK** a další
#. systém při vkládání souboru vytváří **PDF** náhled 
#. systém informuje **Aleph**, že jsou e-publikace připraveny na doplnění bibliografických dat
#. systém načítá bibliografická data ze systému **Aleph**
#. systém ukládá e-publikace do systému **LTP** k trvalé archivaci
#. systém před uložením e-publikace do **LTP** provádí validaci natolik důkladnou, aby předešla odmítnutí na vstupu do **LTP**
#. do **LTP** se odesilaji data po katalogizaci
#. systém poskytuje registraci pro nakladatele
#. systém umožňuje producentovi definovat podmínky užití a řídí se jimi = komu a jakým způsobem mohou být e-publikace zpřístupněny
#. systém přijímá i e-publikace s binárními přílohami
#. systém zjišťuje přítomnost virů ve vložených souborech
#. systém umí načítat e-publikace přes vlastní **ftp** server, nebo z emailové schránky
#. systém zobrazuje **PDF** náhled
#. systém umožňuje zadávat základní bibliografický popis ručně
#. systém nabízí bibliografický popis načtený ze systému **Aleph**
#. systém automaticky načítá údaje o publikacích, které byly zaregistrovány **ISBN agenturou**
#. systém umožňuje povolit jen přihlášení za pomoci hesla, přihlašovacího jména
#. systém si pamatuje všechny verze vloženého souboru
#. systém zobrazuje historii všech zadaných **ISBN** i těch, co prošly jinou cestou, než pres e-deposit
#. systém zobrazuje přehled o tom, co se s e-publikací děje, tj. sleduje změny v Alephu, Krameriovi
#. systém informuje, jestli u vloženého souboru garantuje dlouhodobou ochranu
   nebo jen ochranu na binární úrovni
#. systém umí omezit přístup nakladatele/vydavatele na readonly přístup (např. při porušení smlouvy)
#. systém umí zakázat nakladateli/vydavateli přístup k jednotlivým e-publikacím (např. při porušení autorských práv)
#. systém umožňuje pdf náhled na soubory aniž by kopie opustila systém
#. systém umožňuje označit e-publikaci jako zakázanou (např. při zjištění, že byla autorem okopírována)
#. systém odesílá do Alephu i jednoznačnou linku na náhled e-publikace
#. v systému Aleph vzniká proklik na náhled e-publikace v e-deposit
#. systém nabízí základní informační servis (počty přírůstků, zpřístupnění, ...) podle původců a typů dokumentů, ...

Omezení systému
............................

#. pokud e-publikace prošla akvizicí, nakladatel/vydavatel má možnost jen přidávat opravy - jako další soubory. 
   Už nemůže editovat záznamy, soubory.
#. systém autorizuje uživatele vůči firemní **ActiveDirectory**, nebo vůčí **LDAP**
#. systém převádí všechny formáty do **PDF**, kvuli akvizici a katalogizaci
#. systém poskytuje snadný způsob listování e-publikací, tj. náhledy po jednotlivých stránkách (hlavně pro katalogizaci, která musí celou e-publikaci prolistovat)
#. systém přijímá e-publikace v libovolném (binárním) formátu, dlouhodobou ochranu zaručuje pouze u formátů **ePub2** a **PDF/A**
#. systém nepřijímá publikace s ochranou proti kopírování, např **DRM**. 
   Publikaci přijme i s **DRM** pokud je v něm označení "Národní knihovna"
#. web rozhraní systému je poskytnuto za pomoci **Plone**
#. middleware k implementaci využívá **RabbitMQ**, tj. je implementován odděleně od web rozhraní
#. middleware je napsaný v jazyce **Python**

.. raw:: html

	<div id="disqus_thread"></div>
	<script type="text/javascript">
        /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
        var disqus_shortname = 'edeposit'; // required: replace example with your forum shortname

        /* * * DON'T EDIT BELOW THIS LINE * * */
        (function() {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        })();
	</script>
	<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
	<a href="http://disqus.com" class="dsq-brlink">comments powered by <span class="logo-disqus">Disqus</span></a>
    
