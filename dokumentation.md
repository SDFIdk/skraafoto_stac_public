# Skraafoto-stac-api - Dokumentation

## Introduktion

Skraafoto-stac-api bygger på api-specifikationen STAC (Spatio Temporal Asset Catalog), en nyere api-standard med formål at forene dynamisk søgning og forespørgsler af geospatielt data.
Api'et følger specifikationen angivet i [stac-api-spec](https://github.com/radiantearth/stac-api-spec), som er udarbejdet på baggrund af [OGC API - Features](https://ogcapi.ogc.org/features/), tidligere kaldt WFS3. Det vil sige, at de fleste OGCAPI klienter også vil kunne læse et STAC API, hvis det er konfigureret efter standarden.

STAC api'ets core består af fire komponenter:

- [Items](#STAC-Item)
- [Catalogs](#STAC-Catalog)
- [Collections](#STAC-Collection)
- [STAC API](#STAC-API)

### STAC Item

Grundstenen der udgør et enkelt aktiv (asset) i api'et. Det er formatteret som GeoJSON suppleret med ekstra metadata (id, type, geometry, bbox, datetime, properties, mm.), som muliggører en klient at søge eller gennemløbe kataloger af spatio temporale aktiver. Ekstra data er tilføjet som pkt. 6 i GeoJSON standarden "Foreign Members" [geojson-standard](https://datatracker.ietf.org/doc/html/rfc7946#section-6).
Et spatio temporalt aktiv udgør et bestemt geografisk område på et bestemt tidspunkt. Alle aktiver der opfylder "item" specifikationen er valid STAC [stac-api-spec-item](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md).

### STAC Catalog

Udgangspunktet for navigering af STAC. Det består af links til items og andre catalogs. Det kan forstås som en mappe eller folder i en klassisk fil struktur - den er selv en "beholder" til items, men kan også indeholde andre "beholdere" (foldere/catalogs).

### STAC Collection

En udvidelse til catalog, som indeholder yderligere metadata der beskriver en samling af items som er defineret med samme attributter og deler samme metadata. STAC Collections er kompatible med "Collection" termet specificeret i [OGC API - Features](https://ogcapi.ogc.org/features/) men er udvidet med yderligere felter. En liste af felter er givet i STAC specificationen for Collections [her](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md)

### STAC API

RESTful API specification til dynamisk at forespørge STAC catalogs. Det er designet med et standard set af endpoints til at søge i catalogs, collections, og items.

En nærmere beskrivelse af stac-spec core'en kan læses [her](https://github.com/radiantearth/stac-api-spec/blob/master/stac-spec/overview.md)

## Endpoints og outputs

Servicen udstillet af Dataforsyningen kræver gyldig token, som kan erhverves på https://dataforsyningen.dk/.

Servicen returnerer GeoJSON/JSON, medmindre en forespørgsel er ugyldig pga. uauoriseret token, i så fald returneres text.
Hvis token er autoriseret men har en ugyldig parameter returneres en fejlmeddelelse som JSON på formen `detail: "error message here"`

API'et udstiller endpoints:  
**Landing Page**: `/`  
Denne ressource er roden af api'et som beskriver hvilke funktionaliteter der er udstillet via et `ConformsTo` array samt URIs af andre ressourcer via link relationer.

_Parametre_:  
_Output_: STAC Catalog (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test?token={DinToken}

**Get Conformance Classes**: `/conformance`  
Denne ressource returnerer et array af links til conformance klasser. Selve linksene bruges ikke, men fungerer som et "universelt" id til STAC klienter, som fortæller hvilke STAC og OGC API - Features krav servicen understøtter og overholder.

_Parametre_:  
_Output_: Array af conformance klasser (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/conformance?token={DinToken}

**Get Item**: `/collections/{collectionid}/items/{itemid}`
Denne ressource tager imod et collectionid, itemid, og en crs og returnerer ét STAC Item i en bestemt collection, som er et GeoJSON objekt. Geometrier i output returneres i angivet crs parameter.

_Parametere_: collectionid, itemid, crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`)
_Output_: Feature (STAC Item) (GeoJSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001113?token={DinToken}

**Get/Post Search**: `/search`
Denne ressource tager imod diverse parametre og bruges til at fremsøge en collection af STAC Items, der matcher de angivede parametre. Search kan søge på tværs af collectioner, samt i subset af collections som kan angives i 'collections' parametren. Hvis `collections` er tom er default en søgning over alle collections. `datetime`, `bbox`, `ids` er basale søgekriterer på hvilke Items der skal returneres. `crs` angiver hvilket koordinatsystemet eventuelle geometrier i retur objekter skal returneres i, mens `bbox-crs` og `filter-crs` angiver hvilket koordinatsystem geometrier i parametrene bbox og filter er angivet i. `pt` (page_token) angiver en bestemt side der skal fremsøges i forhold til paging og `limit` angiver hvor mange features der skal returneres i et svar. `sortby` angiver en sorteringsorden resultatet returneres i (se [Sort Extension](#Sort-Extension)). `filter` er et CQL-json udtryk som kan bruges til at lave avanceret søgninger på specifikke Item properties (Se [Filter Extension](#Filter-Extension)). `filter-lang` angiver hvilket query-sprog filteret er skrevet i. Post endpointet har samme funktionalitet, men parametre angives i body.

_Parametre_: crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), limit (default: 10, maks: 10000), pt (page*token), ids, bbox, bbox-crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), datetime, filter, filter-lang (default: `cql-json`), filter-crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), collections, sortby
_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/search?token={DinToken}

**Get Collections**: `/collections`  
Denne ressource returnerer en liste af collectioner API'et udstiller.

_Parametre_:  
_Output_: Collections (Array af STAC Collections) (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections?token={DinToken}

**Get Collection**: `/collections/{collectionid}`  
Denne ressource tager imod et collectionid og returnerer én collection med beskrivelser og diverse link relationer.

_Parametre_: collectionid
_Output_: Collection (STAC Collection) (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}

**Get ItemCollection**: `/collections/{collectionid}/items`  
Denne ressource tager imod et collectionid og laver en søgning magen til `/search` endpointet i den angivet collection.

_Parametre_: collectionid, crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), limit (default: 10, maks: 10000), pt, ids, bbox, bbox-crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), datetime, filter, filter-lang (default: `cql-json`), filter-crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`)
_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?token={DinToken}

**Get Queryables**: `/queryables`  
Denne ressource returnerer en union af properties der kan indgå i et filter udtryk på tværs af alle collectioner. Dvs. at properties som kun kan indgå i et filter udtryk for én collection men ikke en anden, medtages ikke her.

_Paramtre_:  
_Output_: Array af STAC Item properties der kan bruges over alle collection i filter udtryk (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/queryables?token={DinToken}

**Get Collection Queryables**: `/collections/{collectionid}/queryables`  
Denne ressource returnerer alle properties der kan indgå i et filter udtryk for den angivede collection.

_Parametre_: collectionid
_Output_: Array af STAC Item properties for den givne collection, som kan bruges i filter udtryk (JSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/queryables?token={DinToken}

## Extensions

Ud over de nævnte fire core komponenter indeholder servicen en række extensions som udbyder ekstra funktionalitet:

- Filter Extension
- Crs Extension
- Context Extension
- Sort Extension

### Filter Extension

Filter extensionen tilføjer særlig funktionalitet til at søge ved hjælp af forespørgsler i CQL (Common Query Language). Extensionen implementerer specifikationer beskrevet i [OGC Api Features - Part 3: Filtering and the Common Query Language (CQL)](https://portal.ogc.org/files/96288). Den tilføjer desuden to ekstra endpoints `/queryables` og `/collections/{collectionid}/queryables`. Queryables beskriver hvilke properties der kan indgå i filter forespørgsler. Alle filter properties valideres mod queryables, og der returneres en validation fejl hvis der bruges en ugyldig property.
`filter` er et CQL-json udtryk som kan bruges til at lave avanceret søgninger på specifikke Item properties (Se [Filter Extension](#Filter-Extension)). `filter-lang` angiver hvilket query-sprog filteret er skrevet i. Post endpointet har samme funktionalitet, men parametre angives i body.

Eksempler på brug af filter parameter:  
1. `POST /search` - Hent features, hvis geometri intersecter med input geometri
```
{
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
2. `POST /search` - Hent features hvor property.direction er lig øst og gsd er større end 0.1
```
{
  "filter": { 
      "and": [ 
        {"eq": [ { "property": "direction" }, "east" ] }, 
        {"gt": [ { "property": "gsd" }, 0.101 ] } 
   ]
  }
}
``` 
Nærmere beskrivelse af Filter extension: https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter

### Crs Extension

Crs extension tilføjer funktionalitet til håndtering af koordinatsystemer. [GeoJSON standarden](https://datatracker.ietf.org/doc/html/rfc7946#section-4) understøtter som sådan ikke andre koordinatsystemer end WGS84, men tillader at gøre brug af andre koordinatsystemer, hvorom alle parter er informeret om format. Parameteren `crs` i `/search` og `/collections/{collectionid/items}` bruges hvis man ønsker retursvar i et andet coordinatsystem, som f.eks. `http://www.opengis.net/def/crs/EPSG/0/25832`. Desuden kan parametrene `bbox-crs` og `filter-crs` bruges til at angive hvilket koordinatsystem geometrier i parametrene `bbox` og `filter` er angivet i. Crs Extensionen benytter crs URI's til at angive en ønsket crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), f.eks. skrives `WGS84` som `http://www.opengis.net/def/crs/OGC/1.3/CRS84` og EPSG:25832 som `http://www.opengis.net/def/crs/EPSG/0/25832`. Dette er for at følge standarden beskrevet i [OGC API - Features Part 2](https://docs.opengeospatial.org/is/18-058/18-058.html). Understøttede CRS parametre kan ses på hver enkel _Collection_. Desuden angiver parametren `storageCrs` på _Collectionen_ hvilket koordinatsystem data er lagret i.

Eksempler på brug af crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), bbox-crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), og filter-crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`) parametre:

1. `GET /search?crs=http://www.opengis.net/def/crs/EPSG/0/25832` - Returner geometrier i EPSG:25832
2. `GET /search?bbox=492283,6195600,493583,6196470&bbox-crs=http://www.opengis.net/def/crs/EPSG/0/25832` - Input bbox er angivet i EPSG:25832
3. `POST /search` - Hent features der intersecter med geometri angivet i EPSG 25832, resultater returneres i WGS84

```
{
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
  "filter-crs": "25832",
  "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
}
```

### Context Extension

Context extensionen tilføjer ekstra information omkring en returneret `FeatureCollection` hentet via `/search` eller `/collections/{collectionid}/items`. Den returnerer følgenede tre attributter sammen med FeatureCollectionen:

- Returned: Antallet af features returneret af resultatet
- Limit: Det maksimale antal resultater returneret
- Matched: Det totale antal resultater der matcher søge forespørgslen

Hvis `matched` er større end `limit` kan links relationerne `next`/`previous` bruges til at navigere frem og tilbage i det totale antal matchede søgeresultater. Der anvendes paging, og ønskes en større mængde data returneret ved hver "page" kan parametren `limit` bruges. Der kan forespørges på 10.000 resultater af gangen. Paging fungerer ved hjælp af en "paging token" `pt`. Denne token er autogeneret, og skal altid følge paging-resultatet. Ved ændring af denne kan resultatet ikke fremfindes. Et eksempel på paged resultat:

```
...
  "links": [
    {
      "rel": "self",
      "type": "application/geo+json",
      "href": ".../collections/skraafotos2019/items?token={DinToken}xxx&limit=10",
      "method": "GET",
      "body": false
    },
    {
      "rel": "next",
      "type": "application/geo+json",
      "href": ".../collections/skraafotos2019/items?token={DinToken}xxx&limit=10&pt=PmR0OjIwMTktMDctMTAgMTE6MDM6MzIrMDI6MDB-czoyMDE5XzgzXzM3XzJfMDA0OF8wMDAwMDg5NQ%3D%3D",
      "method": "GET",
      "body": false
    }
  ],
  "context": {
    "returned": 10,
    "limit": 10,
    "matched": 2657
  }
```

Nærmere beskrivelse af Context extension: https://github.com/radiantearth/stac-api-spec/tree/master/fragments/context

### Sort Extension

Sort extensionen tilføjer funktionalitet til at sortere resultater hentet via `/search` endpointet. Der kan sorteres på samtlige Item attributter såsom `id`, `collection`, `datetime`, samt diverse properties attributter. Der kan angives om sorteringsretningen skal være _ascending_ eller _descending_. I et GET `/search` request kan der bruges en forsimplet syntaks; `+` for _ascending_ og `-` for _descending_, ingen fortegn defaulter til _ascending_.  

Eksempler på brug af sortBy parameter:

1. `GET /search?sortby=+properties.datetime` - Sorter på properties.datetime ascending
2. `GET /search?sortby=properties.datetime,-id` - Sorter på properties.datetime ascending og id descending
3. `POST /search` - Sorter på collection descending

```
  {
    "sortby": [
        {
            "field": "collection",
            "direction": "desc"
        }
    ]
}
```
Nærmere beskrivelse af Sort Extension: https://github.com/radiantearth/stac-api-spec/tree/master/fragments/sort
