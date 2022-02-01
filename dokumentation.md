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
RESTful API specification til dynamisk at forespørge STAC catalogs. Det er designet med et standard set af endpoint til at søge i catalogs, collections, og items.

## Endpoints
endpoints med parametre og eksempel kald

## Output fra STAC API