# Skraafoto-stac-api - Dokumentation

## Introduktion

Skraafoto-stac-api bygger på API-specifikationen STAC (Spatio Temporal Asset Catalog), en nyere API-standard med formål at forene dynamisk søgning og forespørgsler af geospatielt data.
API'et følger specifikationen angivet i [stac-api-spec](https://github.com/radiantearth/stac-api-spec), som er udarbejdet på baggrund af [OGC API - Features](https://ogcapi.ogc.org/features/), tidligere kaldt WFS3. Det vil sige, at de fleste OGC API klienter også vil kunne læse et STAC API, hvis det er konfigureret efter standarden.

STAC API'ets core består af fire komponenter:

- [Items](#STAC-Item)
- [Catalogs](#STAC-Catalog)
- [Collections](#STAC-Collection)
- [STAC API](#STAC-API)

### STAC Item

Grundstenen, der udgør et enkelt asset i API'et. Det er formateret som GeoJSON suppleret med ekstra metadata (id, type, geometry, bbox, datetime, properties, mm.), som muliggør det for en klient at søge eller gennemløbe kataloger af spatio temporale aktiver. Ekstra data er tilføjet som pkt. 6 i [GeoJSON standarden](https://datatracker.ietf.org/doc/html/rfc7946#section-6) "Foreign Members".
Et spatio temporalt aktiv udgør et bestemt geografisk område på et bestemt tidspunkt. Alle aktiver, der opfylder `Item` specifikationen er valid STAC [stac-api-spec-item](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md).

### STAC Catalog

Udgangspunktet for navigering af STAC. Det består af links til items og andre catalogs. Det kan forstås som en mappe i en klassisk filstruktur - den er selv en "beholder" til items, men kan også indeholde andre "beholdere" (foldere/catalogs).

### STAC Collection

Collection kan ses som en årgang, der indholder metadata om hvert eneste `Item` for den collection. `Item` i en collection deler de samme attributter og metadata på tværs af collections.

En udvidelse til catalog, som indeholder yderligere metadata. Metadataene beskriver en samling af items, som er defineret med samme attributter og deler samme metadata. STAC Collections er kompatibel med `Collection` termet, specificeret i [OGC API - Features](https://ogcapi.ogc.org/features/), men er udvidet med yderligere felter. En liste af felter er angivet i [STAC Collection Specificationen](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md)

### STAC API

RESTful API specification er til dynamisk at forespørge STAC catalogs. Det er designet med et standard set af endpoints til at søge i catalogs, collections, og items.

En nærmere beskrivelse af STAC-spec core kan læses [her](https://github.com/radiantearth/stac-api-spec/blob/master/stac-spec/overview.md).

## Endpoints og outputs

Servicen udstillet af Dataforsyningen kræver gyldig token, som kan erhverves på https://dataforsyningen.dk/.

Servicen returnerer GeoJSON/JSON, medmindre en forespørgsel er ugyldig pga. uautoriseret token, i så fald returneres text.
Hvis token er autoriseret, men ens request har en ugyldig parameter, returneres en JSON fejlmeddelelse.

API'et udstiller endpoints:  
**Landing Page**: `/`  

Denne ressource er roden af API'et, som beskriver hvilke funktionaliteter, der er udstillet via et `ConformsTo` array samt URIs af andre ressourcer via link relationer.

_Parametre_:  
_Output_: 

STAC Catalog (JSON)  

_Eksempel_:

```http
GET https://api.dataforsyningen.dk/skraafotoapi_test
token: {DinToken}
```

**Get Conformance Classes**: `/conformance`  

Denne ressource returnerer et array af links til conformance klasser. Selve links bruges ikke, men fungerer som et "universelt" ID til STAC klienter, som fortæller hvilke krav STAC og OGC-API-Features servicen understøtter og overholder.

_Parametre_:  
_Output_: 

Array af conformance klasser (JSON)  

_Eksempel_:
```http
GET https://api.dataforsyningen.dk/skraafotoapi_test/conformance
token: {DinToken}
```

**Get Item**: `/collections/{collectionid}/items/{itemid}`  

Denne ressource tager imod et `collectionid`, `itemid`, og en `crs` og returnerer ét STAC Item i en bestemt collection, som er et GeoJSON objekt.

_Parametre_: 

| **Parameter** | **Type** | **Description**                                                                                                                                                                                                                                                         |
| ------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| collectionid  | string   | ID'et på en collection.                                                                                                                                                                                                                                                 |
| itemid        | string   | ID'et på et item.                                                                                                                                                                                                                                                       |
| crs           | string   | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832` <br>Angiver hvilket koordinatsystem geometrier i JSON response skal returneres i. Se [Crs Extension](#Crs-Extension).</br> |

_Output_: Feature (STAC Item) (GeoJSON)  
_Eksempel_:

```http
GET https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001113
token: {DinToken}
```

**Get/Post Search**: `/search`  

Denne ressource tager imod diverse parametre og fremsøger en collection af STAC Items, der matcher de angivne parametre. `/search` kan søge på tværs af collections, samt i subset af collections, som kan angives i `collections` parameteren. `datetime`, `bbox`, `ids` er basale søgekriterer på hvilke `Items`, der skal returneres. Post endpointet har samme funktionalitet, men parametre angives i body.

_Parametre_:

| **Parameter** | **Type**  | **Description**                                                                                                                                                                                                                                                         |
| ------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| crs           | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832` <br>Angiver hvilket koordinatsystem geometrier i JSON response skal returneres i. Se [Crs Extension](#Crs-Extension).</br> |
| limit         | integer   | Default: 10, maks: 10000 <br>Angiver maks antallet af `Item` objekter i JSON response (page size). Se [Context Extension](#Context-Extension).<br/>                                                                                                   |
| pt            | string    | Page token. Angiver en bestemt side, der skal fremsøges i forhold til paging. Se [Context Extension](#Context-Extension).                                                                                                                                               |
| ids           | \[string] | Array af `Item` ID'er.                                                                                                                                                                                                                                                  |
| bbox          | \[number] | Array af fire tal.                                                                                                                                                                                                                                                           |
| bbox-crs      | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`. <br>Angiver hvilket koordinatsystem geometrier i `bbox` er angivet i.</br>                                                                    |
| datetime      | string    | Dato og tid formateret efter [RFC 3339, sektion 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). Kan være en enkelt dato og tid eller intervaller separeret med `/`. Der kan bruges to punktummer `..` for et åbent dato- og tidsinterval.                       |
| filter        | string    | `CQL-JSON` udtryk til avanceret søgninger på specifikke `Item` properties. Se [Filter Extension](#Filter-Extension).                                                                                                                                                      |
| filter-lang   | string    | Default: `CQL-JSON` <br>Angiver hvilket query-sprog filteret er skrevet i. Se [Filter Extension](#Filter-Extension).</br>                                                                                                                                               |
| filter-crs    | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`. <br>Angiver hvilket koordinatsystem geometrier i `filter` er angivet i. Se [Filter Extension](#Filter-Extension).</br>                        |
| collections   | \[string] | Default: Søgning over alle collections.                                                                                                                                                                                                                                |
| sortby        | string    | Angiver en sorteringsorden resultatet returneres i. Se [Sort Extension](#Sort-Extension).                                                                                                                                                                               |

_Output_: 

FeatureCollection (Array af STAC Items) (GeoJSON)  

_Eksempel_:

```http
GET https://api.dataforsyningen.dk/skraafotoapi_test/search
token: {DinToken}
```

```http
POST https://api.dataforsyningen.dk/skraafotoapi_test/search
token: {DinToken}
```

**Get Collections**: `/collections`  

Denne ressource returnerer en liste af collections som API'et udstiller.

_Parametre_:  
_Output_: 

Collections (Array af STAC Collections) (JSON)  

_Eksempel_:

```http
GET https://api.dataforsyningen.dk/skraafotoapi_test/collections
token: {DinToken}
```

**Get Collection**: `/collections/{collectionid}`  

Denne ressource tager imod et `collectionid` og returnerer én collection med beskrivelser og diverse linkrelationer.

_Parametre_:

| **Parameter** | **Type** | **Description**         |
| ------------- | -------- | ----------------------- |
| collectionid  | string   | ID'et på en collection. |

_Output_: 

Collection (STAC Collection) (JSON)  

_Eksempel_:

```http
GET https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019
token: {DinToken}
```

**Get ItemCollection**: `/collections/{collectionid}/items`  

Denne ressource tager imod et `collectionid` og laver en søgning magen til `/search` endpointet i den angivne collection.

_Parametre_:

| **Parameter** | **Type**  | **Description**                                                                                                                                                                                                                                                         |
| ------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| collectionid  | string    | ID'et på en collection.                                                                                                                                                                                                                                                 |
| crs           | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832` <br>Angiver hvilket koordinatsystem geometrier i JSON response skal returneres i. Se [Crs Extension](#Crs-Extension).</br> |
| limit         | integer   | Default: 10, maks: 10000 <br>Angiver maks antallet af `Item` objekter i JSON response som objektet indeholder (page size). Se [Context Extension](#Context-Extension).<br/>                                                                                                   |
| pt            | string    | Angiver en bestemt side, der skal fremsøges i forhold til paging. Se [Context Extension](#Context-Extension).                                                                                                                                                           |
| ids           | \[string] | Array af `Item` ID'er.                                                                                                                                                                                                                                                  |
| bbox          | \[number] | Array af fire tal                                                                                                                                                                                                                                                            |
| bbox-crs      | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`. <br>Angiver hvilket koordinatsystem geometrier i `bbox` er angivet i.</br>                                                                    |
| datetime      | string    | Dato og tid formateret efter [RFC 3339, sektion 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). Kan være en enkelt dato og tid eller intervaller separeret med `/`. Der kan bruges to punktummer `..` for et åbent dato- og tidsinterval.                        |
| filter        | string    | `CQL-JSON` udtryk til avanceret søgninger på specifikke `Item` properties. Se [Filter Extension](#Filter-Extension).                                                                                                                                                      |
| filter-lang   | string    | Default: `CQL-JSON` <br>Angiver hvilket query-sprog filteret er skrevet i. Se [Filter Extension](#Filter-Extension).</br>                                                                                                                                               |
| filter-crs    | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`. <br>Angiver hvilket koordinatsystem geometrier `filter` er angivet i. Se [Filter Extension](#Filter-Extension).</br>                          |

_Output_: 

FeatureCollection (Array af STAC Items) (GeoJSON)  

_Eksempel_:

```http
GET https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items
token: {DinToken}
```

**Get Queryables**: `/queryables`  

Denne ressource returnerer en samling af properties, der kan indgå i et filter udtryk på tværs af alle collections. Dvs. at properties, som kun kan indgå i et filterudtryk for én collection, ikke medtages her.

_Paramtre_:  
_Output_: 

Array af STAC Item properties, der kan bruges over alle collections i filter udtryk (JSON)  

_Eksempel_:

```http
GET https://api.dataforsyningen.dk/skraafotoapi_test/queryables
token: {DinToken}
```

**Get Collection Queryables**: `/collections/{collectionid}/queryables`  

Denne ressource returnerer alle properties, der kan indgå i et filterudtryk for den angivne collection.

_Parametre_:

| **Parameter** | **Type** | **Description**         |
| ------------- | -------- | ----------------------- |
| collectionid  | string   | ID'et på en collection. |

_Output_: 

Array af STAC Item properties for den givne collection, som kan bruges i filterudtryk (JSON)  

_Eksempel_:

```http
GET https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/queryables
token: {DinToken}
```

## Extensions

Ud over de nævnte fire core-komponenter, indeholder servicen også en række extensions, som udbyder ekstra funktionaliteter:

- Context Extension
- CRS Extension
- Filter Extension
- Sort Extension

### Context Extension

Context extension tilføjer ekstra information omkring en returneret `FeatureCollection` hentet via `/search` eller `/collections/{collectionid}/items`. Den returnerer følgende tre attributter sammen med `FeatureCollection`:

- Returned: Antallet af features returneret af resultatet
- Limit: Det maksimale antal resultater returneret
- Matched: Det totale antal resultater, der matcher søgeforespørgslen

Hvis `matched` er større end `limit` kan linkrelationerne `next`/`previous` bruges til at navigere frem og tilbage i det totale antal matchede søgeresultater ved hjælp af paging. Paramteren `limit` bestemmer, hvor mange `Item` objekter, der fremgår i det returneret JSON response. `limit`har et max på 10.000 resultater ad gangen. Paging fungerer ved hjælp af en "paging token" `pt`. Denne token er autogenereret, og skal altid følge paging-resultatet. Ved ændring af denne kan resultatet ikke fremfindes. Et eksempel på paged resultat:

```json
...
  "links": [
    {
        "rel": "self",
        "type": "application/geo+json",
        "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?limit=10",
        "method": "GET",
        "body": false
    },
    {
        "rel": "next",
        "type": "application/geo+json",
        "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?limit=10&pt=PmR0OjIwMTktMDctMTAgMTE6MDM6MzIrMDI6MDB-czoyMDE5XzgzXzM3XzJfMDA0OF8wMDAwMDg5NQ%3D%3D",
        "method": "GET",
        "body": false
    }
],
"context": {
    "returned": 10,
    "limit": 10,
    "matched": 13347
}
```

Nærmere beskrivelse af Context extension: https://github.com/radiantearth/stac-api-spec/tree/master/fragments/context

### CRS Extension

Tilføjer funktionalitet til håndtering af koordinatsystemer. [GeoJSON standarden](https://datatracker.ietf.org/doc/html/rfc7946#section-4) understøtter som sådan ikke andre koordinatsystemer end WGS84, men tillader at gøre brug af andre koordinatsystemer, hvor alle parter er informeret om formatet. Parameteren `crs` i `/search` og `/collections/{collectionid/items}` bruges hvis man ønsker retursvar i et andet koordinatsystem. `crs` angives med CRS's URI, så for `WGS84` er det `http://www.opengis.net/def/crs/OGC/1.3/CRS84` (default) og for `EPSG:25832` er det `http://www.opengis.net/def/crs/EPSG/0/25832`. Desuden kan parametrene `bbox-crs` og `filter-crs` bruges til at angive hvilket koordinatsystem geometrier i parametrene `bbox` og `filter` er angivet i, og følger samme fremgangsmåde som `crs`. Dette er for at følge standarden beskrevet i [OGC API - Features Part 2](https://docs.opengeospatial.org/is/18-058/18-058.html). Understøttede CRS-parametre kan ses på hver enkel _Collection_. Desuden angiver parameteren `storageCrs` på `collection`, hvilket koordinatsystem data er lagret i.

Eksempler på brug af parametrene `crs`, `bbox-crs`, og `filter-crs`:

1. `GET /search?crs=http://www.opengis.net/def/crs/EPSG/0/25832` - Returnerer geometrier i EPSG:25832
2. `GET /search?bbox=492283,6195600,493583,6196470&bbox-crs=http://www.opengis.net/def/crs/EPSG/0/25832` - Input `bbox` er angivet i EPSG:25832
3. `POST /search` - Hent features, der overlapper (intersects) med geometri angivet i EPSG:25832, resultater returneres i WGS84

```json
{
    "filter-lang": "cql-json",
    "filter": {
        "intersects": [
            { "property": "geometry" },
            {
                "type": "Polygon",
                "coordinates": [[
                [721250.0000012278, 6190390.000002561], [721244.0000012267, 6191220.000002562],
                [722491.0000012581, 6191080.000002566], [722493.0000012588, 6190540.000002567],
                [721250.0000012278, 6190390.000002561]
                ]]
            }
        ]
    },
  "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
  "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
}
```

### Filter Extension

Filter extension tilføjer særlig funktionalitet til at søge ved hjælp af forespørgsler i CQL (Common Query Language). Denne extension implementerer specifikationer beskrevet i [OGC Api Features - Part 3: Filtering and the Common Query Language (CQL)](https://portal.ogc.org/files/96288). Den tilføjer desuden to ekstra endpoints `/queryables` og `/collections/{collectionid}/queryables`.`/queryables` beskriver hvilke properties, der kan indgå i filter-forespørgsler. Alle filter-properties valideres mod `/queryables`, og der returneres en validation-fejl hvis der bruges en ugyldig property.
`filter` er et CQL-JSON udtryk, som kan bruges til at lave avancerede søgninger på specifikke `Item` properties (Se [Filter Extension](#Filter-Extension)). `filter-lang` angiver hvilket query-sprog filteret er skrevet i. Post endpointet har samme funktionalitet, men parametre angives i body.

Eksempler på brug af filter parameter:  
1. `POST /search` - Hent features hvis geometri overlapper (intersects) med input geometri
```json
{
    "filter-lang": "cql-json",
    "filter": { 
        "intersects": [
            { "property": "geometry" },
            {
                "type": "Polygon",
                "coordinates": [[
                [721250.0000012278, 6190390.000002561], [721244.0000012267, 6191220.000002562],
                [722491.0000012581, 6191080.000002566], [722493.0000012588, 6190540.000002567],
                [721250.0000012278, 6190390.000002561]
                ]]
            }
        ]
    },
  "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
}
```
2. `POST /search` - Hent features hvor `property.direction` er sat til øst og gsd er større end 0.101
```json
{
    "filter-lang": "cql-json",
    "filter": { 
        "and": [ 
            {"eq": [ { "property": "direction" }, "east" ] }, 
            {"gt": [ { "property": "gsd" }, 0.101 ] } 
        ]
    }
}
``` 
Nærmere beskrivelse af Filter extension: https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter.

### Sort Extension

Sort extension tilføjer funktionalitet til at sortere resultater hentet via `/search` endpointet. Der kan sorteres på samtlige `Item` attributter såsom `id`, `collection`, `datetime`, samt diverse properties attributter. Der kan angives om sorteringsretningen skal være _ascending_ eller _descending_. I et GET `/search` request kan der bruges en forsimplet syntaks; `+` for _ascending_ og `-` for _descending_. Hvis intet er angivet er default _ascending_.  

Eksempler på brug af sortBy parameter:

1. `GET /search?sortby=+properties.datetime` - Sortér på properties.datetime ascending
2. `GET /search?sortby=properties.datetime,-id` - Sortér på properties.datetime ascending og id descending
3. `POST /search` - Sortér på collection descending

```json
  {
    "sortby": [
        {
            "field": "collection",
            "direction": "desc"
        }
    ]
}
```
Nærmere beskrivelse af Sort Extension: https://github.com/radiantearth/stac-api-spec/tree/master/fragments/sort.
