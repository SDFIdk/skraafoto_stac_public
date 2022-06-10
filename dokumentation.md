# Skraafoto-stac-api - Dokumentation

## Introduktion

Skraafoto-stac-api bygger på API-specifikationen STAC (Spatio Temporal Asset Catalog), en nyere API-standard med formål at forene dynamisk søgning og forespørgsler af geospatielt data.
API'et følger specifikationen angivet i [stac-api-spec](https://github.com/radiantearth/stac-api-spec) og [OGC API - Features](https://ogcapi.ogc.org/features/), tidligere kaldt WFS3.

STAC API'ets core består af tre komponenter:

- [STAC API](#STAC-API)
- [Collections](#STAC-Collection)
- [Items](#STAC-Item)

Der opereres med collections, som indeholder en samling af items.

 ![Relationship between collection with items](media/Skråfoto-STAC-API.svg)

### STAC API

Selve APIet, der udstiller metadata i form af [STAC Items](#STAC-Item) organiseret i [STAC Collections](#STAC-Collection). En nærmere beskrivelse af STAC-spec core kan læses [her](https://github.com/radiantearth/stac-api-spec/blob/master/stac-spec/overview.md).

### STAC Collection

`Items` er inddelt i `Collections`, således at en `Collection` består af logisk beslægtede `Items`. For eksempel er skråfotos inddelt i en `Collection` per årgang.

_Eksempel_:

<details>

```json
{
    "type": "Collection",
    "id": "skraafotos2021",
    "stac_extensions": [],
    "stac_version": "1.0.0",
    "title": "Skråfotos 2021",
    "description": "Skråfotoflyvning i år 2021. Mere beskrivelse.....",
    "keywords": [],
    "storageCrs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
    "crs": [
        "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
        "http://www.opengis.net/def/crs/EPSG/0/25832"
    ],
    "license": "various",
    "providers": [
        {
            "url": "https://www.sdfe.dk",
            "name": "SDFE",
            "roles": [
                "host",
                "licensor"
            ]
        }
    ],
    "summaries": {},
    "extent": {
        "spatial": {
            "bbox": [
                [
                    8.015616423010679,
                    54.524553169133014,
                    15.254239014661186,
                    57.650387661266926
                ]
            ]
        },
        "temporal": {
            "interval": [
                [
                    "2021-03-10 08:12:40Z",
                    "2021-11-22 10:03:41Z"
                ]
            ]
        }
    },
    "links": [
        {
            "rel": "self",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021"
        },
        {
            "rel": "parent",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/"
        },
        {
            "rel": "items",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items"
        },
        {
            "rel": "root",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/"
        },
        {
            "rel": "license",
            "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
            "type": "text/html; charset=UTF-8",
            "title": "SDFE license terms"
        }
    ]
}
```
</details>

> Bemærk, at en `Collection` består af aggregeret spatiel og tidslig udstrækning for `Items` hørende til denne `Collection`, som man kan se et eksempel af i ovenstående `details`.

Dataelementerne returneret i en `Collection` er beskrevet i [STAC Collection Specificationen](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md)

### STAC Item

Grundstenen, der udgør et enkelt aktiv i API'et. Hvert item beskriver således egenskaberne for ét flyfoto, altså metadata om det billede.

_Eksempel_:

<details>

```json
{
    "type": "Feature",
    "stac_version": "1.0.0",
    "stac_extensions": [
        "https://stac-extensions.github.io/view/v1.0.0/schema.json",
        "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
        "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json"
    ],
    "id": "2021_82_24_5_0024_00005660",
    "collection": "skraafotos2021",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    10.206847701831686,
                    56.15615993575451
                ],
                [
                    10.207381952922963,
                    56.162100222097045
                ],
                [
                    10.223102119197074,
                    56.16069236402555
                ],
                [
                    10.222782336078522,
                    56.15678486408621
                ],
                [
                    10.206847701831686,
                    56.15615993575451
                ]
            ]
        ]
    },
    "bbox": [
        10.2068477018317,
        56.1561599357545,
        10.2231021191971,
        56.162100222097
    ],
    "properties": {
        "datetime": "2021-04-03T14:19:56Z",
        "gsd": 0.1,
        "license": "various",
        "platform": "Fixed-wing aircraft",
        "instruments": [
            "Osprey-80316002-f120_Rev07.00_10cm_C106"
        ],
        "providers": [
            {
                "name": "Terratec",
                "roles": [
                    "producer",
                    "processor"
                ]
            },
            {
                "url": "https://sdfe.dk/",
                "name": "SDFE",
                "roles": [
                    "licensor",
                    "host"
                ]
            }
        ],
        "proj:epsg": null,
        "proj:shape": [
            7725,
            5775
        ],
        "direction": "west",
        "estimated_accuracy": 0.13,
        "pers:omega": 1.4611,
        "pers:phi": 45.1329,
        "pers:kappa": 87.808,
        "pers:perspective_center": [
            576647.679,
            6224403.701,
            1203.014
        ],
        "pers:crs": 25832,
        "pers:vertical_crs": 5799,
        "pers:rotation_matrix": [
            0.0269828157255729,
            0.99963458505038,
            -0.00161988477158235,
            -0.704948504076337,
            0.0201773206919654,
            0.70897142560912,
            0.708745041785869,
            -0.0179881099854046,
            0.705235346280303
        ],
        "pers:interior_orientation": {
            "camera_id": "Osprey-80316002-f120_Rev07.00_10cm_C106",
            "focal_length": 122.982,
            "pixel_spacing": [
                0.0069333,
                0.0069333
            ],
            "calibration_date": "2020-05-18",
            "principal_point_offset": [
                -0.028,
                6.788
            ],
            "sensor_array_dimensions": [
                5775,
                7725
            ]
        },
        "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_614_59/1km_6145_592/2021_83_36_1_0020_00003045.tif",
        "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_614_59%2F1km_6145_592%2F2021_83_36_1_0020_00003045.tif",
        "crs": {
            "type": "name",
            "properties": {
                "name": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            }
        }
    },
    "links": [
        {
            "rel": "self",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_82_24_5_0024_00005660"
        },
        {
            "rel": "parent",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021"
        },
        {
            "rel": "collection",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021"
        },
        {
            "rel": "root",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/"
        },
        {
            "rel": "license",
            "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
            "type": "text/html; charset=UTF-8",
            "title": "SDFE license terms"
        },
        {
            "rel": "alternate",
            "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_614_59%2F1km_6145_592%2F2021_83_36_1_0020_00003045.tif",
            "type": "text/html; charset=UTF-8",
            "title": "Interactive image viewer"
        }
    ],
    "assets": {
        "data": {
            "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_614_59/1km_6145_592/2021_83_36_1_0020_00003045.tif",
            "type": "image/tiff; application=geotiff; profile=cloud-optimized",
            "roles": [
                "data"
            ],
            "title": "Raw tiff file"
        },
        "thumbnail": {
            "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_614_59%2F1km_6145_592%2F2021_83_36_1_0020_00003045.tif",
            "type": "image/jpeg",
            "roles": [
                "thumbnail"
            ],
            "title": "Thumbnail"
        }
    }
}
```
</details>

De enkelte dataelementer i et STAC Item returneret fra dette API er beskrevet i
- [stac-api-spec-item](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md)

Samt i de benyttede udvidelser til STAC:
- [Perspective Imagery](https://github.com/stac-extensions/perspective-imagery)
- [View Geometry](https://github.com/stac-extensions/view)
- [Projection](https://github.com/stac-extensions/projection)

Herudover returneres yderlige to egenskaber:
| Egenskab             | Beskrivelse |
|----------------------|-------------|
| `direction`          | Overordnet beskrivelse af optageretningen. Har en af følgende værdier (null, `north`, `east`, `south`, `west`, `nadir`). |
| `estimated_accuracy` | Estimeret nøjagtighed af billedets orientering [pixels] |

Se afsnittet [Download og visning af billeder](#Download-og-visning-af-billeder) for en beskrivelse af, hvordan det faktiske flyfoto kan hentes og bruges ud fra de metadata, som APIet returnerer.

## Endpoints og outputs

> **Bemærk** at Dataforsyningens service kræver gyldig token, som kan erhverves på https://dataforsyningen.dk/.

Servicen returnerer GeoJSON/JSON, medmindre en forespørgsel er ugyldig pga. uautoriseret token, i så fald returneres text.
Hvis token er autoriseret, men requesten har en ugyldig parameter, returneres en JSON fejlmeddelelse.

API'et udstiller følgende endpoints ...

**Landing Page**: `/`  

Denne ressource er roden af API'et, som beskriver de funktionaliteter, der er udstillet, via et `ConformsTo` array samt URIs af andre ressourcer via link relationer.

_Parametre_:

Ingen

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

Ingen

_Output_: 

Array af conformance klasser (JSON)  

_Eksempel_:

```http
GET https://api.dataforsyningen.dk/skraafotoapi_test/conformance
token: {DinToken}
```

**Get Item**: `/collections/{collectionid}/items/{itemid}`  

Denne ressource tager imod `collectionid`, `itemid` og `crs` parametre og returnerer ét GeoJSON STAC item i en bestemt collection.

_Parametre_: 

| **Parameter** | **Type** | **Description**                                                                                                                                                                                                                                                         |
| ------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| collectionid  | string   | ID'et på en collection.                                                                                                                                                                                                                                                 |
| itemid        | string   | ID'et på et item.                                                                                                                                                                                                                                                       |
| crs           | string   | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832` <br>Angiver hvilket koordinatsystem geometrier i JSON response skal returneres i. Se [Crs Extension](#Crs-Extension).</br> |

_Output_: 

Feature (STAC Item) (GeoJSON)  

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
| limit         | integer   | Default: 10, maks: 1000 <br>Angiver maks antallet af `Item` objekter i JSON response (page size). Se [Context Extension](#Context-Extension).<br/>                                                                                                   |
| pt            | string    | Page token. Angiver en bestemt side, der skal fremsøges i forhold til paging. Se [Context Extension](#Context-Extension).                                                                                                                                               |
| ids           | \[string] | Array af `Item` ID'er.                                                                                                                                                                                                                                                  |
| bbox          | \[number] | Array af fire tal. Returner kun items inden for denne box. Kan ikke angives samtidig med  `intersects`                                                                                                                                                                                                                                                           |
| bbox-crs      | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`. <br>Angiver hvilket koordinatsystem geometrier i `bbox` er angivet i.</br>                                                                    |
| intersects    | string    | GeoJSON geometri, se [Geometries](https://en.wikipedia.org/wiki/GeoJSON#Geometries) for typer. Returner kun items, der overlapper denne geometri. Kan ikke angives samtidig med `bbox`. |
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

Ingen

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
| limit         | integer   | Default: 10, maks: 1000 <br>Angiver maks antallet af `Item` objekter i JSON response som objektet indeholder (page size). Se [Context Extension](#Context-Extension).<br/>                                                                                                   |
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

Ingen

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

- [Context Extension](#Context-Extension)
- [CRS Extension](#CRS-Extension)
- [Filter Extension](#Filter-Extension)
- [Sort Extension](#Sort-Extension)

### Context Extension

Context extension tilføjer ekstra information omkring en returneret `FeatureCollection` hentet via `/search` eller `/collections/{collectionid}/items`. Den returnerer følgende tre attributter sammen med `FeatureCollection`:

- Returned: Antallet af features returneret af resultatet
- Limit: Det maksimale antal resultater returneret
- Matched: Det totale antal resultater, der matcher søgeforespørgslen

Hvis `matched` er større end `limit` kan linkrelationerne `next`/`previous` bruges til at navigere frem og tilbage i det totale antal matchede søgeresultater ved hjælp af paging. Parameteren `limit` bestemmer hvor mange `Item` objekter, der fremgår i det returneret JSON response. `limit`har et max på 10.000 resultater ad gangen. Paging fungerer ved hjælp af en "paging token" `pt`. Denne token er autogenereret, og skal altid følge paging-resultatet. Ved ændring af denne kan resultatet ikke fremfindes. Et eksempel på paged resultat:

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
POST https://api.dataforsyningen.dk/skraafotoapi_test/search
Content-Type: application/json
token: {DinToken}

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
`filter` er et CQL-JSON udtryk, som kan bruges til at lave avancerede søgninger på specifikke `Item` properties (Se [Filter Extension](#Filter-Extension)). `filter-lang` angiver hvilket query-sprog, filteret er skrevet i. Post endpointet har samme funktionalitet, men parametre angives i body.

**Bemærk** at det SQL statement, som API'et udfører, maks må tage 10 sekunder. Hvis din forespørgsel er så kompliceret at den timer ud, så kan det i nogle tilfælde afhælpes ved at begrænse forespørgslen med `bbox` og/eller `datetime` parameteren (se ovenfor).

Eksempler på brug af filter parameter: 
1. `POST /search` - Hent features hvis geometri overlapper (intersects) med input geometri
```json
POST https://api.dataforsyningen.dk/skraafotoapi_test/search
Content-Type: application/json
token: {DinToken}

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
POST https://api.dataforsyningen.dk/skraafotoapi_test/search
Content-Type: application/json
token: {DinToken}

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
POST https://api.dataforsyningen.dk/skraafotoapi_test/search
Content-Type: application/json
token: {DinToken}

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


## Download og visning af billeder

Der er flere muligheder for at gå fra de returnerede metadata (se [STAC Item](#stac-item)) til det beskrevne billede.

Relevante links findes i sektionen `links` hhv `assets`:
```json
[...]
"links": [
    [...]
    {
        "rel": "alternate",
        "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_614_59%2F1km_6145_592%2F2021_83_36_1_0020_00003045.tif",
        "type": "text/html; charset=UTF-8",
        "title": "Interactive image viewer"
    }
],
"assets": {
    "data": {
        "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_614_59/1km_6145_592/2021_83_36_1_0020_00003045.tif",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "roles": [
            "data"
        ],
        "title": "Raw tiff file"
    },
    "thumbnail": {
        "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_614_59%2F1km_6145_592%2F2021_83_36_1_0020_00003045.tif",
        "type": "image/jpeg",
        "roles": [
            "thumbnail"
        ],
        "title": "Thumbnail"
    }
}
[...]
```

> **Bemærk** at alle links til dataforsyningen kræver angivelsen af `token` enten som query parameter eller som header. 

**Download**

Det originale flyfoto i fuld opløsning kan downloades på den URL, der findes i metadata under `/assets/data/href`. Formatet er kompatibelt med almindelige TIFF-læsere og det downloadede billede kan dermed åbnes af de fleste gængse billedprogrammer.

**Thumbnail**

En thumbnail af flyfotoet kan hentes på den URL, der findes i metadata under `/assets/thumbnail/href`.

Der gives ingen garantier vedrørende dimensionerne af thumbnails. Pt er alle thumbnails mindre end 512px.

**Cloud Optimized Geotiff**

Det originale flyfoto, hvis URL findes under  `/assets/data/href`, er i "Cloud Optimized GeoTIFF" format og kan dermed tilgås meget effektivt direkte på http-serveren.

Læs mere på [www.cogeo.org](https://www.cogeo.org/).

**Viewer**

Dataforsyningen udstiller en online-viewer til meget enkel visning af et flyfoto i en browser. URLen til denne viewer findes i metadata under `/links/` med `rel=alternate` og `type=text/html; charset=UTF-8`.

**JPEG tiles**

Dataforsyningen udstiller en service, der kan udstille et flyfoto som en pyramide af jpeg-tiles. Disse kan anvendes, såfremt klienten ikke er i stand til at anvende den "Cloud Optimized GeoTIFF" direkte, som beskrevet ovenfor.

URL til denne service er ikke inkluderet i metadata, men må i stedet konstrueres. URL'en skal konstrueres som 

```
https://api.dataforsyningen.dk/skraafoto_cogtiler_test/tiles/{z}/{x}/{y}.jpg?url={DOWNLOAD_URL}
```

Tile-koordinaterne z, x, og y er i en lokal tile-pyramide.

Basal info om tile-pyramiden kan fås på endpointet 
```
https://api.dataforsyningen.dk/skraafoto_cogtiler_test/info?url={DOWNLOAD_URL}
```

## Georeferering

Hvis man har et 3D koordinat `(X, Y, Z)` på et punkt i landskabet, er det muligt at beregne, hvilken pixel `(xa, ya)` i flyfotoet dette punkt vil blive afbilledet i.

> **Det forudsættes**, at koordinaten er i samme koordinatreferencesystem, som billedet er georefereret i. Dette er beskrevet i egenskaberne `pers:crs` og `pers:vertical_crs`. Det kan således være nødvendigt først at konvertere koordinaten til det rette koordinatreferencesystem.

Først etableres en række variable ud fra flyfotoets metadata (Se [STAC Item](#stac-item)):

```python
props = item["properties"]
m11, m12, m13, m21, m22, m23, m31, m32, m33 = props["pers:rotation_matrix"]
Xc, Yc, Zc = props["pers:perspective_center"]
f_mm = props["pers:interior_orientation"]["focal_length"]
ppo_x, ppo_y = props["pers:interior_orientation"]["principal_point_offset"]
pixel_size = props["pers:interior_orientation"]["pixel_spacing"][0]
sensor_cols, sensor_rows = props["pers:interior_orientation"]["sensor_array_dimensions"]

# Calculated values. In pixels. Origo in image lower left.
f = f_mm / pixel_size
x0 = sensor_cols * 0.5 + ppo_x / pixel_size
y0 = sensor_rows * 0.5 + ppo_y / pixel_size 
```

Dernæst kan `(xa, ya)` beregnes på en af to måder. Bemærk i øvrigt, at pixelkoordinaterne `(xa, ya)` har origo i billedets nederste venstre hjørne med x-aksen positiv mod højre og y-aksen positiv op.

Den klassiske fotogrammetriske form:
```
dX = (X-Xc)
dY = (Y-Yc)
dZ = (Z-Zc)
n = (m31 * dX + m32 * dY + m33 * dZ)
xa = x0 - f * (m11 * dX + m12 * dY + m13 * dZ) / n
ya = y0 - f * (m21 * dX + m22 * dY + m23 * dZ) / n
```

Eller formuleret på matrixform:

$$
K = \begin{bmatrix} -f & 0 & x0 \\\\  0 & -f & y0 \\\\ 0 & 0 & 1 \end{bmatrix}
$$


$$
R = \begin{bmatrix} m11 & m12 & m13 \\\\ m21 & m22 & m23 \\\\ m31 & m32 & m33 \end{bmatrix} 
$$


$$
T = \begin{bmatrix} 1 & 0 & 0 & -Xc \\\\  0 & 1 & 0 & -Yc \\\\ 0 & 0 & 1 & - Zc \end{bmatrix}
$$



$$
\begin{bmatrix}xc \\\\ yc \\\\ zc \end{bmatrix} = KRT \begin{bmatrix} X \\\\ Y \\\\ Z \\\\ 1 \end{bmatrix}
$$


$$
(xa, ya) = (xc / zc, yc / zc)
$$

