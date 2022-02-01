# Skraafotodistribution-stac-api - Dokumentation
## Introduktion
Skraafoto-stac-api bygger på api-teknologien STAC (Spatio Temporal Asset Catalog), som er en nyere api-standard som har til formål at forene dynamisk søgning og forespørgsler af geospatielt data.
Api'et følger specifikationen angivet i [stac-api-spec](https://github.com/radiantearth/stac-api-spec), som er udarbejdet på baggrund af [ogc-api-features](https://ogcapi.ogc.org/features/).
STAC api'et består overordnet set af fire komponenter:
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

## Conformance Classes
Servicen indeholder 

## Extensions

## Endpoints
API'et har følgende endpoints:  
**Landing Page**: `/`  
https://api.dataforsyningen.dk/skraafotoapi_test/?token=4adf32524ae6d6998565f638a1090ba1  

**Get Conformance Classes**: `/conformance`  
https://api.dataforsyningen.dk/skraafotoapi_test/conformance?token=4adf32524ae6d6998565f638a1090ba1  

**Get Item**: `/collections/{collectionid}/items/{itemid}`  
https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001113?token=4adf32524ae6d6998565f638a1090ba1  

**Get/Post Search**: `/search`  
https://api.dataforsyningen.dk/skraafotoapi_test/search?token=4adf32524ae6d6998565f638a1090ba1  

**Get Collections**: `/collections`  
https://api.dataforsyningen.dk/skraafotoapi_test/collections?token=4adf32524ae6d6998565f638a1090ba1  

**Get Collection**: `/collections/{collectionid}`  
https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token=4adf32524ae6d6998565f638a1090ba1  

**Get ItemCollection**: `/collections/{collectionid}/items`  
https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?token=4adf32524ae6d6998565f638a1090ba1  

**Get Queryables**: `/queryables`  
https://api.dataforsyningen.dk/skraafotoapi_test/queryables?token=4adf32524ae6d6998565f638a1090ba1  

**Get Collection Queryables**: `/collections/{collectionid}/queryables`  
https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/queryables?token=4adf32524ae6d6998565f638a1090ba1  

## Output fra STAC API
Servicen returnerer GeoJSON/JSON, medmindre en forespørgsel er ugyldig pga. uauoriseret token, i så fald returneres text. Hvis token er autoriseret returneres enten:  
- En fejlmeddelelse som JSON på formen ```detail:	"Invalid parameters provided"```, hvis en input parameter er ugyldig eller collectionen ikke eksisterer.
- Et succesfudt GeoJSON/JSON svar med et array af `Features`, eller `Collections`.
- Hvis parametre er gyldige men der ikke findes et `Feature` match returneres GeoJSON/JSON med et tomt array af features
