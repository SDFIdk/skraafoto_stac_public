# Skraafotodistribution-stac-api - Dokumentation
## Introduktion
Skraafoto-stac-api bygger på api-teknologien STAC (Spatio Temporal Asset Catalog), som er en nyere api-standard som har til formål at forene dynamisk søgning og forespørgsler af geospatielt data.
Api'et følger specifikationen angivet i [stac-api-spec](https://github.com/radiantearth/stac-api-spec), som er udarbejdet på baggrund af [ogc-api-features](https://ogcapi.ogc.org/features/).
STAC api'ets core består af fire komponenter:
- [Items](#STAC-Item)
- [Catalogs](#STAC-Catalog)
- [Collections](#STAC-Collection)
- [STAC API](#STAC-API)

### STAC Item
Grundstenen der udgør et enkelt aktiv (asset) i api'et. Det er formatteret som GeoJSON suppleret med ekstra metadata (id, type, geometry, bbox, datetime, properties, mm.), som muliggører en klient at søge eller gennemløbe kataloger af spatio temporale aktiver.
Et spatio temporalt aktiv udgør et bestemt geografisk område på et bestemt tidspunkt. 

### STAC Catalog
Udgangspunktet for navigering af STAC. Det består af links til items og andre catalogs. Det kan forstås som en mappe eller folder i en klassisk fil struktur - den er selv en "beholder" til items, men kan også indeholde andre "beholdere" (foldere/catalogs).

### STAC Collection
Magen til catalog, men indeholder yderligere metadata der beskriver en samling af items som er defineret med samme attributter og deler samme metadata. I GIS termer udgør et STAC item en _feature_, og en STAC collection et _layer_

### STAC API
RESTful API specification til dynamisk at forespørge STAC catalogs. Det er designet med et standard set af endpoints til at søge i catalogs, collections, og items.

## Extensions
Ud over de nævnte fire core komponenter indeholder servicen en række extensions som udbyder ekstra funktionalitet:  
- Filter Extension
- Crs Extension
- Context Extension
- Sort Extension


### Filter Extension
Filter extensionen tilføjer særlig funktionalitet til at søge ved hjælp af forespørgsler i CQL (Common Query Language). Extensionen implementerer specifikationer beskrevet i [OGC Api Features - Part 3: Filtering and the Common Query Language (CQL)](https://portal.ogc.org/files/96288). Den tilføjer desuden to ekstra endpoints `/queryables` og `/collections/{collectionid}/queryables` som uddybes i [Filter & queryables](#Filter-&-queryables)
### Crs Extension
### Context Extension
### Sort Extension

## Filter & queryables
Skriv om filter udtryk og queryables

## Endpoints og outputs
Servicen returnerer GeoJSON/JSON, medmindre en forespørgsel er ugyldig pga. uauoriseret token, i så fald returneres text. 
Hvis token er autoriseret men har en ugyldig parameter returneres en fejlmeddelelse som JSON på formen ```detail:	"error message here"```  

API'et har følgende endpoints:  

**Landing Page**: `/`  
Denne ressource er roden af api'et som beskriver hvilke funktionaliteter der er udstillet via et `ConformsTo` array samt URIs af andre ressourcer via link relationer.  

_Parametre_:  
_Output_: STAC Catalog (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/?token=4adf32524ae6d6998565f638a1090ba1


**Get Conformance Classes**: `/conformance`  
Denne ressource returnerer et array af links til conformance klasser. Selve linksene bruges ikke, men fungerer som et "universelt" id til STAC klienter, som fortæller hvilke STAC og OGC API Features krav servicen understøtter og overholder. 

_Parametre_:  
_Output_: Array af conformance klasser (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/conformance?token=4adf32524ae6d6998565f638a1090ba1


**Get Item**: `/collections/{collectionid}/items/{itemid}`
Denne ressource tager i mod et collectionid, itemid, og en crs og returnerer ét STAC Item i en bestemt collection, som et GeoJSON objekt. Geometrier i output returneres i angivet crs parameter.

_Parametere_: collectionid, itemid, crs
_Output_: Feature (STAC Item) (GeoJSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001113?token=4adf32524ae6d6998565f638a1090ba1


**Get/Post Search**: `/search`  
Denne ressource tager i mod diverse parametre og bruges til at fremsøge en collection af STAC Items, der matcher de angivede parametre. Search kan søge på tværs af collectioner, samt i subset af collectioner som kan angives i 'collections' parametren. Hvis `collections` er tom er default en søgning over alle collectioner. `datetime`, `bbox`, `ids` er basale søgekriterer på hvilke Items der skal returneres. `crs` angiver hvilket koordinatsystemet eventuelle geometrier i retur objekter skal returneres i, mens `bbox-crs` og `filter-crs` angiver hvilket koordinatsystem geometrier i parametrene bbox og filter er angivet i. `pt` (page_token) angiver en bestemt side der skal fremsøges i forhold til paging og `limit` angiver hvor mange features der skal returneres per side.  `sortby` angiver en sorteringsorden resultatet returneres i. `filter` er et CQL-json udtryk som kan bruges til at lave avanceret søgninger på specifikke Item properties. `filter-lang` angiver hvilket sprog filteret er skrevet i. Post endpointet har samme funktionalitet, men parametre angives i body. 

_Parametre_: crs, limit, pt (page_token), ids, bbox, bbox-crs, datetime, filter, filter-lang, filter-crs, collections, sortby  
_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/search?token=4adf32524ae6d6998565f638a1090ba1


**Get Collections**: `/collections`  
Denne ressource returnerer en liste af collectioner API'et udstiller.  

_Parametre_:  
_Output_: Collections (Array af STAC Collections) (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections?token=4adf32524ae6d6998565f638a1090ba1


**Get Collection**: `/collections/{collectionid}`  
Denne ressource tager i mod et collectionid og returnerer én collection med beskrivelser og diverse link relationer.  

_Parametre_: collectionid
_Output_: Collection (STAC Collection) (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token=4adf32524ae6d6998565f638a1090ba1


**Get ItemCollection**: `/collections/{collectionid}/items`  
Denne ressource tager i mod et collectionid og laver en søgning magen til `/search` endpointet i den angivet collection. 

_Parametre_: collectionid, crs, limit, pt, ids, bbox, bbox-crs, datetime, filter, filter-lang, filter-crs,
_Output_: FeatureCollection (Array af STAC Items) ( GeoJSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?token=4adf32524ae6d6998565f638a1090ba1


**Get Queryables**: `/queryables`  
Denne ressource returnerer en union af properties der kan indgå i et filter udtryk på tværs af alle collectioner. Dvs. at properties som kun kan indgå i et filter udtryk for én collection men ikke en anden, medtages ikke her.

_Paramtre_:  
_Output_: Array af STAC Item properties der kan bruges over alle collection i filter udtryk (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/queryables?token=4adf32524ae6d6998565f638a1090ba1


**Get Collection Queryables**: `/collections/{collectionid}/queryables`  
Denne ressource returnerer alle properties der kan indgå i et filter udtryk for den angivede collection.

_Parametre_: collectionid
_Output_: Array af STAC Item properties for den givne collection, som kan bruges i filter udtryk (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/queryables?token=4adf32524ae6d6998565f638a1090ba1








