# Skraafoto STAC API - Dokumentation

<h2 id="skraafoto-introduktion">Introduktion</h2>

Skraafoto-stac-api bygger på API-specifikationen STAC (Spatio Temporal Asset Catalog), en nyere API-standard med formål at forene dynamisk søgning og forespørgsler af geospatielt data.
API'et følger specifikationen angivet i [stac-api-spec](https://github.com/radiantearth/stac-api-spec) og [OGC API - Features](https://ogcapi.ogc.org/features/), tidligere kaldt WFS3.

STAC API'ets core består af tre komponenter:

- [STAC API](#stac-api)
- [Collections](#stac-collection)
- [Items](#stac-item)

Der opereres med collections, som indeholder en samling af items.

 ![Relationship between collection with items](https://raw.githubusercontent.com/SDFIdk/skraafoto_stac_public/main/media/Skr%C3%A5foto-STAC-API.svg)

### STAC API

Selve APIet, der udstiller metadata i form af [STAC Items](#stac-item) organiseret i [STAC Collections](#stac-collection). En nærmere beskrivelse af STAC-spec core kan læses [her](https://github.com/radiantearth/stac-api-spec/blob/master/stac-spec/overview.md).

### STAC Collection

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
            "url": "https://www.sdfi.dk",
            "name": "SDFI",
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
            "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
        },
        {
            "rel": "parent",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/"
        },
        {
            "rel": "items",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021/items"
        },
        {
            "rel": "root",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/"
        },
        {
            "rel": "license",
            "href": "https://dataforsyningen.dk/Vilkaar",
            "type": "text/html; charset=UTF-8",
            "title": "SDFI license terms"
        }
    ]
}
```

`Items` er inddelt i `Collections`, således at en `Collection` består af logisk beslægtede `Items`. For eksempel er skråfotos inddelt i en `Collection` per årgang.

**Bemærk** at en `Collection` består af aggregeret spatiel og tidslig udstrækning for `Items` hørende til denne `Collection`, som man kan se et eksempel af i ovenstående `details`.

Dataelementerne returneret i en `Collection` er beskrevet i [STAC Collection Specificationen](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md).

### STAC Item

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
                "url": "https://sdfi.dk/",
                "name": "SDFI",
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
            "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021/items/2021_82_24_5_0024_00005660"
        },
        {
            "rel": "parent",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
        },
        {
            "rel": "collection",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
        },
        {
            "rel": "root",
            "type": "application/json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/"
        },
        {
            "rel": "license",
            "href": "https://dataforsyningen.dk/Vilkaar",
            "type": "text/html; charset=UTF-8",
            "title": "SDFI license terms"
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

Grundstenen, der udgør et enkelt aktiv i API'et. Hvert item beskriver således egenskaberne for ét flyfoto, altså metadata om det billede.

De enkelte dataelementer i et STAC Item returneret fra dette API er beskrevet i [STAC Item Specification](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md).

Samt i de benyttede udvidelser til STAC:

- [Perspective Imagery](https://github.com/stac-extensions/perspective-imagery)
- [View Geometry](https://github.com/stac-extensions/view)
- [Projection](https://github.com/stac-extensions/projection)

Herudover returneres yderlige to egenskaber:

| Egenskab             | Beskrivelse |
|----------------------|-------------|
| `direction`          | Overordnet beskrivelse af optageretningen. Har en af følgende værdier (null, `north`, `east`, `south`, `west`, `nadir`). |
| `estimated_accuracy` | Estimeret nøjagtighed af billedets orientering [pixels] |

Se afsnittet [Download og visning af billeder](#download-og-visning-af-billeder) for en beskrivelse af, hvordan det faktiske flyfoto kan hentes og bruges ud fra de metadata, som APIet returnerer.

## Endpoints og outputs

**Bemærk** at Dataforsyningens service kræver gyldig token, som kan erhverves på [https://dataforsyningen.dk](https://dataforsyningen.dk).

Servicen returnerer GeoJSON/JSON, medmindre en forespørgsel er ugyldig pga. uautoriseret token, i så fald returneres text.
Hvis token er autoriseret, men requesten har en ugyldig parameter, returneres en JSON fejlmeddelelse.

`GET /`

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/json
```

_Landing Page_

Denne ressource er roden af API'et, som beskriver de funktionaliteter, der er udstillet, via et `ConformsTo` array samt URIs af andre ressourcer via link relationer.

_Parametre_

Ingen

_Output_

STAC Catalog (JSON)

`GET /conformance`

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api/conformance HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/json
```

_Get Conformance Classes_

Denne ressource returnerer et array af links til conformance klasser. Selve links bruges ikke, men fungerer som et "universelt" ID til STAC klienter, som fortæller hvilke krav STAC og OGC-API-Features servicen understøtter og overholder.

_Parametre_

Ingen

_Output_

Array af conformance klasser (JSON)

`GET /collections/{collectionid}/items/{itemid}`

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/items/2019_83_37_2_0046_00001113 HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/json
```

_Get Item_

Denne ressource tager imod `collectionid`, `itemid` og `crs` parametre og returnerer ét GeoJSON STAC item i en bestemt collection.

_Parametre_

| **Parameter** | **Type** | **Description** |
| ------------- | -------- | --------------- |
| collectionid  | string   | ID'et på en collection. |
| itemid        | string   | ID'et på et item. |
| crs           | string   | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832` <br>Angiver hvilket koordinatsystem geometrier i JSON response skal returneres i. Se [Crs Extension](#crs-extension).</br> |

_Output_

Feature (STAC Item) (GeoJSON)

`GET/POST /search`

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api/search HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/geo+json
```

> Code samples

```http
POST https://api.dataforsyningen.dk/skraafoto_api/search HTTP/1.1
Host: api.dataforsyningen.dk
Content-Type: application/json
Accept: application/geo+json
```

_Get/Post Search_

Denne ressource tager imod diverse parametre og fremsøger en collection af STAC Items, der matcher de angivne parametre. `/search` kan søge på tværs af collections, samt i subset af collections, som kan angives i `collections` parameteren. `datetime`, `bbox`, `ids` er basale søgekriterer på hvilke `Items`, der skal returneres. Post endpointet har samme funktionalitet, men parametre angives i body.

_Parametre_

| **Parameter** | **Type**  | **Description** |
| ------------- | --------- | --------------- |
| crs           | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832` <br>Angiver hvilket koordinatsystem geometrier i JSON response skal returneres i. Se [Crs Extension](#crs-extension).</br> |
| limit         | integer   | Default: 10, maks: 1000 <br>Angiver maks antallet af `Item` objekter i JSON response (page size). Se [Context Extension](#context-extension).<br/> |
| pt            | string    | Page token. Angiver en bestemt side, der skal fremsøges i forhold til paging. Se [Context Extension](#context-extension). |
| ids           | \[string] | Array af `Item` ID'er. |
| bbox          | \[number] | Array af fire tal. Returner kun items inden for denne box. Kan ikke angives samtidig med `intersects`. Standard sorteringen korteste afstand mellem geometriens centoride og footprint af skråfotos. |
| bbox-crs      | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`. <br>Angiver hvilket koordinatsystem geometrier i `bbox` er angivet i.</br> |
| intersects    | string    | GeoJSON geometri, se [Geometries](https://en.wikipedia.org/wiki/GeoJSON#Geometries) for typer. Returner kun items, der overlapper denne geometri. Kan ikke angives samtidig med `bbox`. Standard sorteringen korteste afstand mellem geometriens centoride og footprint af skråfotos.|
| datetime      | string    | Dato og tid formateret efter [RFC 3339, sektion 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). Kan være en enkelt dato og tid eller intervaller separeret med `/`. Der kan bruges to punktummer `..` for et åbent dato- og tidsinterval. |
| filter        | string    | `CQL-JSON` udtryk til avanceret søgninger på specifikke `Item` properties. Se [Filter Extension](#filter-extension). I forbindelse med en `GET search` denne parameter URL encodes. Hvis der er angivet en geometry, er standard sorteringen korteste afstand mellem geometriens centoride og footprint af skråfotos.  |
| filter-lang   | string    | Default: `CQL-JSON` <br>Angiver hvilket query-sprog filteret er skrevet i. Se [Filter Extension](#filter-extension).</br> |
| filter-crs    | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`. <br>Angiver hvilket koordinatsystem geometrier i `filter` er angivet i. Se [Filter Extension](#filter-extension).</br> |
| collections   | \[string] | Default: Søgning over alle collections. |
| sortby        | string    | Angiver en sorteringsorden resultatet returneres i. Se [Sort Extension](#sort-extension). |

_Output_

FeatureCollection (Array af STAC Items) (GeoJSON)

`GET /collections`

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api/collections HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/json
```

_Get Collections_

Denne ressource returnerer en liste af collections som API'et udstiller.

_Parametre_

Ingen

_Output_

Collections (Array af STAC Collections) (JSON)

`GET /collections/{collectionid}`

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019 HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/json
```

_Get Collection_

Denne ressource tager imod et `collectionid` og returnerer én collection med beskrivelser og diverse linkrelationer.

_Parametre_

| **Parameter** | **Type** | **Description**         |
| ------------- | -------- | ----------------------- |
| collectionid  | string   | ID'et på en collection. |

_Output_

Collection (STAC Collection) (JSON)

`GET /collections/{collectionid}/items`

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/items HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/json
```

_Get Item Collection_

Denne ressource tager imod et `collectionid` og laver en søgning magen til `/search` endpointet i den angivne collection.

_Parametre_

| **Parameter** | **Type**  | **Description** |
| ------------- | --------- | --------------- |
| collectionid  | string    | ID'et på en collection. |
| crs           | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832` <br>Angiver hvilket koordinatsystem geometrier i JSON response skal returneres i. Se [Crs Extension](#crs-extension).</br> |
| limit         | integer   | Default: 10, maks: 1000 <br>Angiver maks antallet af `Item` objekter i JSON response som objektet indeholder (page size). Se [Context Extension](#context-extension).<br/> |
| pt            | string    | Angiver en bestemt side, der skal fremsøges i forhold til paging. Se [Context Extension](#context-extension). |
| ids           | \[string] | Array af `Item` ID'er. |
| bbox          | \[number] | Array af fire tal. Returner kun items inden for denne box. Standard sorteringen korteste afstand mellem geometriens centoride og footprint af skråfotos. |
| bbox-crs      | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`. <br>Angiver hvilket koordinatsystem geometrier i `bbox` er angivet i.</br> |
| datetime      | string    | Dato og tid formateret efter [RFC 3339, sektion 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). Kan være en enkelt dato og tid eller intervaller separeret med `/`. Der kan bruges to punktummer `..` for et åbent dato- og tidsinterval. |
| filter        | string    | `CQL-JSON` udtryk til avanceret søgninger på specifikke `Item` properties. Se [Filter Extension](#filter-extension). Denne parameter skal URL encodes. Hvis der er angivet en geometry, er standard sorteringen korteste afstand mellem geometriens centoride og footprint af skråfotos. |
| filter-lang   | string    | Default: `CQL-JSON` <br>Angiver hvilket query-sprog filteret er skrevet i. Se [Filter Extension](#filter-extension).</br> |
| filter-crs    | string    | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`. <br>Angiver hvilket koordinatsystem geometrier `filter` er angivet i. Se [Filter Extension](#filter-extension).</br> |

_Output_

FeatureCollection (Array af STAC Items) (GeoJSON)

`GET /queryables`

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api/queryables HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/json
```

_Get Queryables_

Denne ressource returnerer en samling af properties, der kan indgå i et filter udtryk på tværs af alle collections. Dvs. at properties, som kun kan indgå i et filterudtryk for én collection, ikke medtages her.

_Parametre_

Ingen

_Output_

Array af STAC Item properties, der kan bruges over alle collections i filter udtryk (JSON)

`GET /collections/{collectionid}/queryables`

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/queryables HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/json
```

_Get Collection Queryables_

Denne ressource returnerer alle properties, der kan indgå i et filterudtryk for den angivne collection.

_Parametre_

| **Parameter** | **Type** | **Description**         |
| ------------- | -------- | ----------------------- |
| collectionid  | string   | ID'et på en collection. |

_Output_

Array af STAC Item properties for den givne collection, som kan bruges i filterudtryk (JSON)

## Extensions

Ud over de nævnte fire core-komponenter, indeholder servicen også en række extensions, som udbyder ekstra funktionaliteter:

- [Context Extension](#context-extension)
- [CRS Extension](#crs-extension)
- [Filter Extension](#filter-extension)
- [Sort Extension](#sort-extension)

### Context Extension

```json
...
"links": [
    {
        "rel": "self",
        "type": "application/geo+json",
        "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/items?limit=10",
        "method": "GET",
        "body": false
    },
    {
        "rel": "next",
        "type": "application/geo+json",
        "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/items?limit=10&pt=PmR0OjIwMTktMDctMTAgMTE6MDM6MzIrMDI6MDB-czoyMDE5XzgzXzM3XzJfMDA0OF8wMDAwMDg5NQ%3D%3D",
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

Context extension tilføjer ekstra information omkring en returneret `FeatureCollection` hentet via `/search` eller `/collections/{collectionid}/items`. Den returnerer følgende tre attributter sammen med `FeatureCollection`:

- Returned: Antallet af features returneret af resultatet
- Limit: Det maksimale antal resultater returneret
- Matched: Det totale antal resultater, der matcher søgeforespørgslen

Hvis `matched` er større end `limit` kan linkrelationerne `next`/`previous` bruges til at navigere frem og tilbage i det totale antal matchede søgeresultater ved hjælp af paging. Parameteren `limit` bestemmer hvor mange `Item` objekter, der fremgår i det returneret JSON response. `limit`har et max på 10.000 resultater ad gangen. Paging fungerer ved hjælp af en "paging token" `pt`. Denne token er autogenereret, og skal altid følge paging-resultatet. Ved ændring af denne kan resultatet ikke fremfindes. Et eksempel på paged resultat kan ses til højre.

Nærmere beskrivelse af [Context Extension](https://github.com/radiantearth/stac-api-spec/tree/master/fragments/context).

### CRS Extension

Tilføjer funktionalitet til håndtering af koordinatsystemer. [GeoJSON standarden](https://datatracker.ietf.org/doc/html/rfc7946#section-4) understøtter som sådan ikke andre koordinatsystemer end WGS84, men tillader at gøre brug af andre koordinatsystemer, hvor alle parter er informeret om formatet. Parameteren `crs` i `/search` og `/collections/{collectionid/items}` bruges hvis man ønsker retursvar i et andet koordinatsystem. `crs` angives med CRS's URI, så for `WGS84` er det `http://www.opengis.net/def/crs/OGC/1.3/CRS84` (default) og for `EPSG:25832` er det `http://www.opengis.net/def/crs/EPSG/0/25832`. Desuden kan parametrene `bbox-crs` og `filter-crs` bruges til at angive hvilket koordinatsystem geometrier i parametrene `bbox` og `filter` er angivet i, og følger samme fremgangsmåde som `crs`. Dette er for at følge standarden beskrevet i [OGC API - Features Part 2](https://docs.opengeospatial.org/is/18-058/18-058.html). Understøttede CRS-parametre kan ses på hver enkel _Collection_. Desuden angiver parameteren `storageCrs` på `collection`, hvilket koordinatsystem data er lagret i.

Eksempler på brug af parametrene `crs`, `bbox-crs`, og `filter-crs`:

1. `GET /search?crs=http://www.opengis.net/def/crs/EPSG/0/25832` - Returnerer geometrier i EPSG:25832.
2. `GET /search?bbox=492283,6195600,493583,6196470&bbox-crs=http://www.opengis.net/def/crs/EPSG/0/25832` - Input `bbox` er angivet i EPSG:25832.
3. `POST /search` - Hent features, der overlapper (intersects) med geometri angivet i EPSG:25832, resultater returneres i WGS84. Eksempel på request ses ude til højre.

> Code samples

```http
POST https://api.dataforsyningen.dk/skraafoto_api/search HTTP/1.1
Host: api.dataforsyningen.dk
Content-Type: application/json
Accept: application/geo+json

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
`filter` er et CQL-JSON udtryk, som kan bruges til at lave avancerede søgninger på specifikke `Item` properties (Se [Filter Extension](#filter-extension)). `filter-lang` angiver hvilket query-sprog, filteret er skrevet i. Post endpointet har samme funktionalitet, men parametre angives i body.

**Bemærk** at det SQL statement, som API'et udfører, maks må tage 10 sekunder. Hvis din forespørgsel er så kompliceret at den timer ud, så kan det i nogle tilfælde afhælpes ved at begrænse forespørgslen med `bbox` og/eller `datetime` parameteren (se ovenfor).

Eksempler på brug af filter parameter:

1. `POST /search` - Hent features hvis geometri overlapper (intersects) med input geometri. Første eksempel ude til højre viser sådan en request.

> Code samples

```http
POST https://api.dataforsyningen.dk/skraafoto_api/search HTTP/1.1
Host: api.dataforsyningen.dk
Content-Type: application/json
Accept: application/geo+json

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

2. `POST /search` - Hent features hvor `property.direction` er sat til øst og gsd er større end 0.101. Andet eksempel ude til højre viser sådan en request.

> Code samples

```http
POST https://api.dataforsyningen.dk/skraafoto_api/search HTTP/1.1
Host: api.dataforsyningen.dk
Content-Type: application/json
Accept: application/geo+json

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

Nærmere beskrivelse af [Filter extension](https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter).

### Sort Extension

Sort extension tilføjer funktionalitet til at sortere resultater hentet via `/search` endpointet. Der kan sorteres på samtlige `Item` attributter såsom `id`, `collection`, `datetime`, samt diverse properties attributter. Der kan angives om sorteringsretningen skal være _ascending_ eller _descending_. I et GET `/search` request kan der bruges en forsimplet syntaks; `+` for _ascending_ og `-` for _descending_. Hvis intet er angivet er default _ascending_.

Eksempler på brug af sortBy parameter:

1. `GET /search?sortby=+properties.datetime` - Sortér på properties.datetime ascending.
2. `GET /search?sortby=properties.datetime,-id` - Sortér på properties.datetime ascending og id descending.
3. `POST /search` - Sortér på collection descending. Eksempel på request ses ude til højre.

> Code samples

```http
POST https://api.dataforsyningen.dk/skraafoto_api/search HTTP/1.1
Host: api.dataforsyningen.dk
Content-Type: application/json
Accept: application/geo+json

{
    "sortby": [
        {
            "field": "collection",
            "direction": "desc"
        }
    ]
}
```

Nærmere beskrivelse af [Sort Extension](https://github.com/radiantearth/stac-api-spec/tree/master/fragments/sort).

## Download og visning af billeder

```json
...
"links": [
    ...
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
...
```

Der er flere muligheder for at gå fra de returnerede metadata (se [STAC Item](#stac-item)) til det beskrevne billede.

Relevante links findes i sektionen `links` hhv `assets`, kan ses ude til højre i et JSON response eksempel.

**Bemærk** at alle links til dataforsyningen kræver angivelsen af `token` enten i header eller query parameter.

**Download**

Det originale flyfoto i fuld opløsning kan downloades på den URL, der findes i metadata under `/assets/data/href`. Formatet er kompatibelt med almindelige TIFF-læsere og det downloadede billede kan dermed åbnes af de fleste gængse billedprogrammer.

**Thumbnail**

En thumbnail af flyfotoet kan hentes på den URL, der findes i metadata under `/assets/thumbnail/href`.

Der gives ingen garantier vedrørende dimensionerne af thumbnails. Pt er alle thumbnails mindre end 512px.

**Cloud Optimized Geotiff**

Det originale flyfoto, hvis URL findes under `/assets/data/href`, er i "Cloud Optimized GeoTIFF" format og kan dermed tilgås meget effektivt direkte på http-serveren.

Læs mere på [www.cogeo.org](https://www.cogeo.org/).

**Viewer**

Dataforsyningen udstiller en online-viewer til meget enkel visning af et flyfoto i en browser. URLen til denne viewer findes i metadata under `/links/` med `rel=alternate` og `type=text/html; charset=UTF-8`.

**JPEG tiles**

Dataforsyningen udstiller en service, der kan udstille et flyfoto som en pyramide af jpeg-tiles. Disse kan anvendes, såfremt klienten ikke er i stand til at anvende den "Cloud Optimized GeoTIFF" direkte, som beskrevet ovenfor.

URL til denne service er ikke inkluderet i metadata, men må i stedet konstrueres. URL'en skal konstrueres som:

`https://api.dataforsyningen.dk/skraafoto_cogtiler_test/tiles/{z}/{x}/{y}.jpg?url={DOWNLOAD_URL}`

Tile-koordinaterne z, x, og y er i en lokal tile-pyramide.

Basal info om tile-pyramiden kan fås på endpointet:

`https://api.dataforsyningen.dk/skraafoto_cogtiler_test/info?url={DOWNLOAD_URL}`

## Georeferering

Hvis man har et 3D koordinat `(X, Y, Z)` på et punkt i landskabet, er det muligt at beregne, hvilken pixel `(xa, ya)` i flyfotoet dette punkt vil blive afbilledet i.

**Det forudsættes**, at koordinaten er i samme koordinatreferencesystem, som billedet er georefereret i. Dette er beskrevet i egenskaberne `pers:crs` og `pers:vertical_crs`. Det kan således være nødvendigt først at konvertere koordinaten til det rette koordinatreferencesystem.

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

Først etableres en række variable ud fra flyfotoets metadata (Se [STAC Item](#stac-item)), som kan ses ude til højre.

Dernæst kan `(xa, ya)` beregnes på en af to måder. Bemærk i øvrigt, at pixelkoordinaterne `(xa, ya)` har origo i billedets nederste venstre hjørne med x-aksen positiv mod højre og y-aksen positiv op.

Den klassiske fotogrammetriske form:

`dX = (X-Xc)`

`dY = (Y-Yc)`

`dZ = (Z-Zc)`

`n = (m31 * dX + m32 * dY + m33 * dZ)`

`xa = x0 - f * (m11 * dX + m12 * dY + m13 * dZ) / n`

`ya = y0 - f * (m21 * dX + m22 * dY + m23 * dZ) / n`

Eller formuleret på matrixform:

![matrix_form](https://raw.githubusercontent.com/SDFIdk/skraafoto_stac_public/main/media/matrix_form.svg)

## How to get started

Guiden er en hurtig gennemgang af, hvordan man får skråfotos for et bestemt geografisk område ved hjælp af koordinater.

### Sammenspillet mellem de tre API'er

- **Skåfoto STAC API** leverer metadata om skråfotos. Dens URL starter med `https://api.dataforsyningen.dk/skraafoto_api`, men for at bruge URL'en er det et krav, at der bliver specificeret paths og query parameters.
- **Skåfoto Server** leverer skråfotos som [Cloud Optimized Geotiff](https://www.cogeo.org) (`COG`), hvor der kan bruges range request. Dens URL starter med `https://api.dataforsyningen.dk/skraafoto_server`, men for at bruge URL'en er det et krav, at der bliver specificeret paths og query parameters.
- **Skråfoto Cogtiler** oversætter COG-formatet til JPG, der ikke understøtter COG, se mere i afsnittet [Download og visning af billeder](#download-og-visning-af-billeder). Dens URL starter med `https://api.dataforsyningen.dk/skraafoto_cogtiler`, men for at bruge URL'en er det et krav, at der bliver specificeret paths og query parameters. Cogtilers openapi dokumentation findes [her](#skraafoto_cogtiler).

<table class="center" style="width:100%">
  <tr>
     <th>For klienter med understøttelse af COGs</th>
     <th>Klienter UDEN COG support</th>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/SDFIdk/skraafoto_stac_public/main/media/Skr%C3%A5fotodistribution-HTTPServer.svg" alt="For klienter med understøttelse af COGs" width="300px"></td>
    <td><img src="https://raw.githubusercontent.com/SDFIdk/skraafoto_stac_public/main/media/Skr%C3%A5fotodistribution-TileServer.svg" alt="Klienter UDEN COG support" width="300px"></td>
  </tr>
 </table>

#### Eksempel 1

Hente en COG fra Skåfoto Server, og vise billedet med Open Layer

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/gh/openlayers/openlayers.github.io@master/en/v6.14.1/build/ol.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/openlayers/openlayers.github.io@master/en/v6.14.1/css/ol.css">
</head>
<style>
  .map {
    height: 800px;
    width: 100%;
  }
</style>
  <body>
    <p>Trying out instructions from <a href="https://openlayers.org/en/latest/examples/cog.html">OpenLayers</a></p>

    <div id="map" class="map"></div>
    <script>
        var cogUrl = "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_58/1km_6132_583/2021_83_37_2_0025_00001961.tif";

        // HACK to avoid bug looking up meters per unit for 'pixels' (https://github.com/openlayers/openlayers/issues/13564)
        const projection = new ol.proj.Projection({
            code: 'custom',
            units: 'pixels',
            metersPerUnit: 1,
        });
        const source = new ol.source.GeoTIFF({
            convertToRGB: true,
            sources: [{ url: cogUrl }],
            sourceOptions: {headers: {'token':'{}'}}
        });

        const layer = new ol.layer.WebGLTile({ source });

        // when the view resolves view properties, the map view will be updated with the HACKish projection override
        const map = new ol.Map({
            target: 'map',
            layers: [layer],
            view: source.getView().then(options => ({
                ...options,
                projection: projection
            }))
        });
    </script>
  </body>
</html>
```

#### Eksempel 2

Hente metadata om et bestemt skråfoto, for så at få vist selve billedet ved brug af Skråfoto STAC API og Skråfoto Cogtiler

```html
<!DOCTYPE html>
<html>
  <body>
    <img id="jpgImage" src="">
    <script>
      const fetchMetadaPromise = new Promise((resolve, reject) => {
        // Get metadata about a specific item using Skråfoto STAC API
        fetch('https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021/items/2021_83_36_4_0008_00004522', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'token': '{}'
          }
        })
          .then((response) => {
            if (!response.ok){
              throw new Error('Network response was not OK');
            }
            // If response is empty then return empty json
            resolve(response?.json() || {});
          })
        });

      const fetchThumbnailPromise = new Promise((resolve, reject) => {
        fetchMetadaPromise.then((jsonData) => {
        // Get the thumbnail image from the item using Skråfoto Cogtiler
        fetch(jsonData.assets.thumbnail.href, {
            method: 'GET',
            headers: {
              'token': '{}'
            }
          })
          .then((response) => {
            if (!response.ok){
              throw new Error('Network response was not OK');
            }
            // Blob is raw data
            resolve(response.blob());
          })
        });
      });

      // Be sure that the DOM has loaded before the image get populated
      window.addEventListener('DOMContentLoaded', () => {
        fetchThumbnailPromise.then((imageSrc) => {
        const objectURL = URL.createObjectURL(imageSrc);
        let image = document.querySelector("#jpgImage");
        image.src = objectURL;
        });
      });
    </script>
  </body>
</html>
```

### Håndtering af collections

**Vigtig optimering af søgninger**

Hvis der kun ønskes billeder af det samme sted fra samme årgang, så anbefales det at benytte `/collections/{collectionid}/items` endpoint i stedet for `/search` endpoint, da `/search` kræver flere resourcer at udføre.
Hvis der ønskes billeder af det samme sted, på tværs af collections skal der bruges `/search`.

**STAC Item**

Hvert skråfoto har et `Item` objekt tilknyttet, som indeholder metadata for det. Mere om [STAC Item](#stac-item).

#### Samme årgang

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/items?limit=3&bbox=10.3285,55.3556,10.4536,55.4132&bbox-crs=http://www.opengis.net/def/crs/OGC/1.3/CRS84 HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/json
```

> Example responses

> 200 Response

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json"
            ],
            "id": "2019_83_36_5_0028_00000842",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.453787768075529,
                            55.40246232920729
                        ],
                        [
                            10.436048634260915,
                            55.40105429198659
                        ],
                        [
                            10.43660132821691,
                            55.41237119451473
                        ],
                        [
                            10.454232642266255,
                            55.410275595741986
                        ],
                        [
                            10.453787768075529,
                            55.40246232920729
                        ]
                    ]
                ]
            },
            "bbox": [
                10.4360486342609,
                55.4010542919866,
                10.4542326422663,
                55.4123711945147
            ],
            "properties": {
                "datetime": "2019-06-07T10:51:10Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011019"
                ],
                "providers": [
                    {
                        "name": "MGGP_Aero",
                        "roles": [
                            "producer",
                            "processor"
                        ]
                    },
                    {
                        "url": "https://sdfi.dk/",
                        "name": "SDFI",
                        "roles": [
                            "licensor",
                            "host"
                        ]
                    }
                ],
                "proj:epsg": null,
                "proj:shape": [
                    8578.0,
                    11478.0
                ],
                "direction": "west",
                "estimated_accuracy": 0.01,
                "pers:omega": 1.08745,
                "pers:phi": 44.6841,
                "pers:kappa": 89.2089,
                "pers:perspective_center": [
                    593092.69,
                    6140947.58,
                    1510.24
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.00981716190118791,
                    0.999908851350567,
                    0.00926889006272609,
                    -0.710926523207453,
                    0.000460826228438361,
                    0.703266141826372,
                    0.703197768719703,
                    -0.0134935773602192,
                    0.710866247220709
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011019",
                    "focal_length": 108.3599,
                    "pixel_spacing": [
                        0.0046,
                        0.0046
                    ],
                    "calibration_date": "2019-02-21",
                    "principal_point_offset": [
                        0.0,
                        0.0
                    ],
                    "sensor_array_dimensions": [
                        11478.0,
                        8578.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2019/10km_614_59/1km_6140_591/2019_83_36_5_0028_00000842.tif",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_614_59%2F1km_6140_591%2F2019_83_36_5_0028_00000842.tif"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/items/2019_83_36_5_0028_00000842"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/"
                },
                {
                    "rel": "license",
                    "href": "https://dataforsyningen.dk/Vilkaar",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFI license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_614_59%2F1km_6140_591%2F2019_83_36_5_0028_00000842.tif",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2019/10km_614_59/1km_6140_591/2019_83_36_5_0028_00000842.tif",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_614_59%2F1km_6140_591%2F2019_83_36_5_0028_00000842.tif",
                    "type": "image/jpeg",
                    "roles": [
                        "thumbnail"
                    ],
                    "title": "Thumbnail"
                }
            },
            "crs": {
                "type": "name",
                "properties": {
                    "name": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                }
            }
        },
        {
            "type": "Feature",
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json"
            ],
            "id": "2019_83_36_5_0028_00000841",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.453855880561024,
                            55.399585726604926
                        ],
                        [
                            10.436165388116725,
                            55.39817713534648
                        ],
                        [
                            10.43676216790363,
                            55.40940365627251
                        ],
                        [
                            10.454300725935077,
                            55.407398996579154
                        ],
                        [
                            10.453855880561024,
                            55.399585726604926
                        ]
                    ]
                ]
            },
            "bbox": [
                10.4361653881167,
                55.3981771353465,
                10.4543007259351,
                55.4094036562725
            ],
            "properties": {
                "datetime": "2019-06-07T10:51:05Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011019"
                ],
                "providers": [
                    {
                        "name": "MGGP_Aero",
                        "roles": [
                            "producer",
                            "processor"
                        ]
                    },
                    {
                        "url": "https://sdfi.dk/",
                        "name": "SDFI",
                        "roles": [
                            "licensor",
                            "host"
                        ]
                    }
                ],
                "proj:epsg": null,
                "proj:shape": [
                    8578.0,
                    11478.0
                ],
                "direction": "west",
                "estimated_accuracy": 0.01,
                "pers:omega": 0.90731,
                "pers:phi": 44.698,
                "pers:kappa": 89.1296,
                "pers:perspective_center": [
                    593098.69,
                    6140629.92,
                    1507.26
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.0107976745977231,
                    0.999928441467627,
                    0.00514996770906703,
                    -0.710742457015353,
                    0.00405195911748076,
                    0.703440645273707,
                    0.703369440634906,
                    -0.0112558238895698,
                    0.710735349064267
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011019",
                    "focal_length": 108.3599,
                    "pixel_spacing": [
                        0.0046,
                        0.0046
                    ],
                    "calibration_date": "2019-02-21",
                    "principal_point_offset": [
                        0.0,
                        0.0
                    ],
                    "sensor_array_dimensions": [
                        11478.0,
                        8578.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2019/10km_614_59/1km_6140_591/2019_83_36_5_0028_00000841.tif",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_614_59%2F1km_6140_591%2F2019_83_36_5_0028_00000841.tif"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/items/2019_83_36_5_0028_00000841"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/"
                },
                {
                    "rel": "license",
                    "href": "https://dataforsyningen.dk/Vilkaar",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFI license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_614_59%2F1km_6140_591%2F2019_83_36_5_0028_00000841.tif",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2019/10km_614_59/1km_6140_591/2019_83_36_5_0028_00000841.tif",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_614_59%2F1km_6140_591%2F2019_83_36_5_0028_00000841.tif",
                    "type": "image/jpeg",
                    "roles": [
                        "thumbnail"
                    ],
                    "title": "Thumbnail"
                }
            },
            "crs": {
                "type": "name",
                "properties": {
                    "name": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                }
            }
        },
        {
            "type": "Feature",
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json"
            ],
            "id": "2019_83_36_5_0028_00000840",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.453892419285022,
                            55.39670949803028
                        ],
                        [
                            10.436297911943775,
                            55.39529979198281
                        ],
                        [
                            10.436894671823973,
                            55.406526317444545
                        ],
                        [
                            10.454333930289712,
                            55.40443294234298
                        ],
                        [
                            10.453892419285022,
                            55.39670949803028
                        ]
                    ]
                ]
            },
            "bbox": [
                10.4362979119438,
                55.3952997919828,
                10.4543339302897,
                55.4065263174445
            ],
            "properties": {
                "datetime": "2019-06-07T10:51:01Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011019"
                ],
                "providers": [
                    {
                        "name": "MGGP_Aero",
                        "roles": [
                            "producer",
                            "processor"
                        ]
                    },
                    {
                        "url": "https://sdfi.dk/",
                        "name": "SDFI",
                        "roles": [
                            "licensor",
                            "host"
                        ]
                    }
                ],
                "proj:epsg": null,
                "proj:shape": [
                    8578.0,
                    11478.0
                ],
                "direction": "west",
                "estimated_accuracy": 0.01,
                "pers:omega": 0.804628,
                "pers:phi": 44.7198,
                "pers:kappa": 89.1651,
                "pers:perspective_center": [
                    593102.88,
                    6140312.48,
                    1503.77
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.0103532111921644,
                    0.999939221515531,
                    0.00379002545171671,
                    -0.710480890494109,
                    0.00468899948155429,
                    0.703700872193974,
                    0.703640330894064,
                    -0.00997830440386553,
                    0.710486254744253
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011019",
                    "focal_length": 108.3599,
                    "pixel_spacing": [
                        0.0046,
                        0.0046
                    ],
                    "calibration_date": "2019-02-21",
                    "principal_point_offset": [
                        0.0,
                        0.0
                    ],
                    "sensor_array_dimensions": [
                        11478.0,
                        8578.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2019/10km_614_59/1km_6140_591/2019_83_36_5_0028_00000840.tif",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_614_59%2F1km_6140_591%2F2019_83_36_5_0028_00000840.tif"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/items/2019_83_36_5_0028_00000840"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/"
                },
                {
                    "rel": "license",
                    "href": "https://dataforsyningen.dk/Vilkaar",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFI license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_614_59%2F1km_6140_591%2F2019_83_36_5_0028_00000840.tif",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2019/10km_614_59/1km_6140_591/2019_83_36_5_0028_00000840.tif",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_614_59%2F1km_6140_591%2F2019_83_36_5_0028_00000840.tif",
                    "type": "image/jpeg",
                    "roles": [
                        "thumbnail"
                    ],
                    "title": "Thumbnail"
                }
            },
            "crs": {
                "type": "name",
                "properties": {
                    "name": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                }
            }
        }
    ],
    "links": [
        {
            "rel": "self",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/items?limit=3&bbox=10.3285%2C55.3556%2C10.4536%2C55.4132&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&servicename=skraafoto_api&service=rest",
            "method": "GET",
            "body": false
        },
        {
            "rel": "next",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2019/items?limit=3&bbox=10.3285%2C55.3556%2C10.4536%2C55.4132&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&servicename=skraafoto_api&service=rest&pt=PmR0OjIwMTktMDYtMDcgMTI6NTE6MDErMDI6MDB-czoyMDE5XzgzXzM2XzVfMDAyOF8wMDAwMDg0MA%3D%3D",
            "method": "GET",
            "body": false
        }
    ],
    "context": {
        "returned": 3,
        "limit": 3,
        "matched": 1751
    }
}
```

I URL'en angives `{collectionid}` i path, hvilken collection man ønsker at fremsøge billeder fra. Se `GET /collections/{collectionid}/items` under [Endpoints og outputs](#endpoints-og-outputs) for mulige parametre og output type.

I dette tilfælde er det `skraafotos2019` collection. Dernæst angives query parameterne. Her er det parameteren `bbox` med værdierne `10.3285,55.3556,10.4536,55.4132`, som beskriver hvilket geografisk område, der ønskes metadata om billederne fra. I dette eksempel er `bbox` i projektion `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, hvilket bliver angivet i `bbox-crs` parameteren. Limit er sat til 3, så hvis der er et match mellem den koordinaterne for den angivne `bbox` og metadata for skåfotos, vil JSON response indeholde tre `Items` objekter. I `context` objektet er attributterne `Returned`, `Limit` og `Matched`, der kan læses mere om på [Context Extension](#context-extension), hvor det også er forklaret hvordan paging fungerer.

#### På tværs af årgange

> Code samples

```http
GET https://api.dataforsyningen.dk/skraafoto_api/search?limit=3&bbox=10.3285,55.3556,10.4536,55.4132&bbox-crs=http://www.opengis.net/def/crs/OGC/1.3/CRS84 HTTP/1.1
Host: api.dataforsyningen.dk
Accept: application/geo+json
```

> Example responses

> 200 Response

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json"
            ],
            "id": "2021_83_36_4_0008_00004522",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.31381450318513,
                            55.3550628051039
                        ],
                        [
                            10.33349296655548,
                            55.35593051752134
                        ],
                        [
                            10.333086125135491,
                            55.34840745788952
                        ],
                        [
                            10.313491550991404,
                            55.35012013342645
                        ],
                        [
                            10.31381450318513,
                            55.3550628051039
                        ]
                    ]
                ]
            },
            "bbox": [
                10.3134915509914,
                55.3484074578895,
                10.3334929665555,
                55.3559305175213
            ],
            "properties": {
                "datetime": "2021-03-31T13:36:34Z",
                "gsd": 0.09,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "UCOM3p-423S81560X411059_UC-Op-Left"
                ],
                "providers": [
                    {
                        "name": "Geofly GmbH",
                        "roles": [
                            "producer",
                            "processor"
                        ]
                    },
                    {
                        "url": "https://sdfi.dk/",
                        "name": "SDFI",
                        "roles": [
                            "licensor",
                            "host"
                        ]
                    }
                ],
                "proj:epsg": null,
                "proj:shape": [
                    10300.0,
                    7700.0
                ],
                "direction": "east",
                "estimated_accuracy": 1.5,
                "pers:omega": -0.743256,
                "pers:phi": -44.956008000000004,
                "pers:kappa": -90.658737,
                "pers:perspective_center": [
                    582420.479,
                    6134828.344,
                    1509.735
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    -0.00813575866140771,
                    -0.999955149967192,
                    0.0048484518245212,
                    0.707602723548871,
                    -0.0023310412532316,
                    0.706606645788797,
                    -0.706563652516334,
                    0.00917955885471115,
                    0.707589952332571
                ],
                "pers:interior_orientation": {
                    "camera_id": "UCOM3p-423S81560X411059_UC-Op-Left",
                    "focal_length": 123.0,
                    "pixel_spacing": [
                        0.0052,
                        0.0052
                    ],
                    "calibration_date": "2019-03-01",
                    "principal_point_offset": [
                        0.0,
                        6.75
                    ],
                    "sensor_array_dimensions": [
                        7700.0,
                        10300.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_58/1km_6134_583/2021_83_36_4_0008_00004522.tif",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6134_583%2F2021_83_36_4_0008_00004522.tif"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021/items/2021_83_36_4_0008_00004522"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/"
                },
                {
                    "rel": "license",
                    "href": "https://dataforsyningen.dk/Vilkaar",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFI license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6134_583%2F2021_83_36_4_0008_00004522.tif",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_58/1km_6134_583/2021_83_36_4_0008_00004522.tif",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6134_583%2F2021_83_36_4_0008_00004522.tif",
                    "type": "image/jpeg",
                    "roles": [
                        "thumbnail"
                    ],
                    "title": "Thumbnail"
                }
            },
            "crs": {
                "type": "name",
                "properties": {
                    "name": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                }
            }
        },
        {
            "type": "Feature",
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json"
            ],
            "id": "2021_83_36_4_0008_00004521",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.313898978155779,
                            55.357928698045754
                        ],
                        [
                            10.333618031718975,
                            55.35880203471528
                        ],
                        [
                            10.333175430666753,
                            55.35128235254085
                        ],
                        [
                            10.313593966912771,
                            55.35299408532214
                        ],
                        [
                            10.313898978155779,
                            55.357928698045754
                        ]
                    ]
                ]
            },
            "bbox": [
                10.3135939669128,
                55.3512823525408,
                10.333618031719,
                55.3588020347153
            ],
            "properties": {
                "datetime": "2021-03-31T13:36:31Z",
                "gsd": 0.09,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "UCOM3p-423S81560X411059_UC-Op-Left"
                ],
                "providers": [
                    {
                        "name": "Geofly GmbH",
                        "roles": [
                            "producer",
                            "processor"
                        ]
                    },
                    {
                        "url": "https://sdfi.dk/",
                        "name": "SDFI",
                        "roles": [
                            "licensor",
                            "host"
                        ]
                    }
                ],
                "proj:epsg": null,
                "proj:shape": [
                    10300.0,
                    7700.0
                ],
                "direction": "east",
                "estimated_accuracy": 1.5,
                "pers:omega": -0.736146,
                "pers:phi": -44.877033000000004,
                "pers:kappa": -90.64290600000001,
                "pers:perspective_center": [
                    582421.89,
                    6135147.917,
                    1510.019
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    -0.00795116583183259,
                    -0.999956233346669,
                    0.00493055301741094,
                    0.708578119470888,
                    -0.00215497483770826,
                    0.705629084357036,
                    -0.705587576115832,
                    0.00910425585051554,
                    0.708564241940273
                ],
                "pers:interior_orientation": {
                    "camera_id": "UCOM3p-423S81560X411059_UC-Op-Left",
                    "focal_length": 123.0,
                    "pixel_spacing": [
                        0.0052,
                        0.0052
                    ],
                    "calibration_date": "2019-03-01",
                    "principal_point_offset": [
                        0.0,
                        6.75
                    ],
                    "sensor_array_dimensions": [
                        7700.0,
                        10300.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_58/1km_6135_583/2021_83_36_4_0008_00004521.tif",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6135_583%2F2021_83_36_4_0008_00004521.tif"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021/items/2021_83_36_4_0008_00004521"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/"
                },
                {
                    "rel": "license",
                    "href": "https://dataforsyningen.dk/Vilkaar",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFI license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6135_583%2F2021_83_36_4_0008_00004521.tif",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_58/1km_6135_583/2021_83_36_4_0008_00004521.tif",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6135_583%2F2021_83_36_4_0008_00004521.tif",
                    "type": "image/jpeg",
                    "roles": [
                        "thumbnail"
                    ],
                    "title": "Thumbnail"
                }
            },
            "crs": {
                "type": "name",
                "properties": {
                    "name": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                }
            }
        },
        {
            "type": "Feature",
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json"
            ],
            "id": "2021_83_36_4_0008_00004520",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.313994433693654,
                            55.360796788561764
                        ],
                        [
                            10.333767392307404,
                            55.36167609384993
                        ],
                        [
                            10.33323523624725,
                            55.354160832440904
                        ],
                        [
                            10.313724274388218,
                            55.35586173327727
                        ],
                        [
                            10.313994433693654,
                            55.360796788561764
                        ]
                    ]
                ]
            },
            "bbox": [
                10.3137242743882,
                55.3541608324409,
                10.3337673923074,
                55.3616760938499
            ],
            "properties": {
                "datetime": "2021-03-31T13:36:28Z",
                "gsd": 0.09,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "UCOM3p-423S81560X411059_UC-Op-Left"
                ],
                "providers": [
                    {
                        "name": "Geofly GmbH",
                        "roles": [
                            "producer",
                            "processor"
                        ]
                    },
                    {
                        "url": "https://sdfi.dk/",
                        "name": "SDFI",
                        "roles": [
                            "licensor",
                            "host"
                        ]
                    }
                ],
                "proj:epsg": null,
                "proj:shape": [
                    10300.0,
                    7700.0
                ],
                "direction": "east",
                "estimated_accuracy": 1.5,
                "pers:omega": -0.645273,
                "pers:phi": -44.917272,
                "pers:kappa": -90.59278499999999,
                "pers:perspective_center": [
                    582423.114,
                    6135467.638,
                    1509.949
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    -0.00732618684000834,
                    -0.999965335155851,
                    0.00395669976513055,
                    0.708089119365071,
                    -0.00239377521138496,
                    0.706119018917516,
                    -0.706085069961958,
                    0.00797485591615638,
                    0.708082110810557
                ],
                "pers:interior_orientation": {
                    "camera_id": "UCOM3p-423S81560X411059_UC-Op-Left",
                    "focal_length": 123.0,
                    "pixel_spacing": [
                        0.0052,
                        0.0052
                    ],
                    "calibration_date": "2019-03-01",
                    "principal_point_offset": [
                        0.0,
                        6.75
                    ],
                    "sensor_array_dimensions": [
                        7700.0,
                        10300.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_58/1km_6135_583/2021_83_36_4_0008_00004520.tif",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6135_583%2F2021_83_36_4_0008_00004520.tif"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021/items/2021_83_36_4_0008_00004520"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/"
                },
                {
                    "rel": "license",
                    "href": "https://dataforsyningen.dk/Vilkaar",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFI license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6135_583%2F2021_83_36_4_0008_00004520.tif",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_58/1km_6135_583/2021_83_36_4_0008_00004520.tif",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6135_583%2F2021_83_36_4_0008_00004520.tif",
                    "type": "image/jpeg",
                    "roles": [
                        "thumbnail"
                    ],
                    "title": "Thumbnail"
                }
            },
            "crs": {
                "type": "name",
                "properties": {
                    "name": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                }
            }
        }
    ],
    "links": [
        {
            "rel": "self",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/search?limit=3&bbox=10.3285%2C55.3556%2C10.4536%2C55.4132&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&servicename=skraafoto_api&service=rest",
            "method": "GET",
            "body": null
        },
        {
            "rel": "next",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/search?limit=3&bbox=10.3285%2C55.3556%2C10.4536%2C55.4132&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&servicename=skraafoto_api&service=rest&pt=PmR0OjIwMjEtMDMtMzEgMTU6MzY6MjgrMDI6MDB-czoyMDIxXzgzXzM2XzRfMDAwOF8wMDAwNDUyMA%3D%3D",
            "method": "GET",
            "body": null
        }
    ],
    "context": {
        "returned": 3,
        "limit": 3,
        "matched": 4276
    }
}
```

> Code samples

```http
POST https://api.dataforsyningen.dk/skraafoto_api/search HTTP/1.1
Host: api.dataforsyningen.dk
Content-Type: application/json
Accept: application/geo+json

{
    "filter-lang": "cql-json",
    "filter": {
        "intersects": [
            { "property": "geometry" },
            {
                "type": "Polygon",
                "coordinates": [[
                [10.2113,55.3226],
                [10.4106,55.2783],
                [10.5213,55.3580],
                [10.4040,55.4466],
                [10.2888,55.4267]
                ]]
            }
        ]
    },
  "filter-crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
  "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
  "limit": 3
}
```

> Example responses

> 200 Response

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json"
            ],
            "id": "2021_83_38_2_0032_00003342",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.473812237435594,
                            55.307083098013585
                        ],
                        [
                            10.456787846703763,
                            55.30724192475617
                        ],
                        [
                            10.453859449959696,
                            55.31952326834094
                        ],
                        [
                            10.477465830047741,
                            55.31933747403768
                        ],
                        [
                            10.473812237435594,
                            55.307083098013585
                        ]
                    ]
                ]
            },
            "bbox": [
                10.4538594499597,
                55.3070830980136,
                10.4774658300477,
                55.3195232683409
            ],
            "properties": {
                "datetime": "2021-06-17T16:22:00Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "UCOM4-434S42016X419232_UC-Op-FWD"
                ],
                "providers": [
                    {
                        "name": "Geofly GmbH",
                        "roles": [
                            "producer",
                            "processor"
                        ]
                    },
                    {
                        "url": "https://sdfi.dk/",
                        "name": "SDFI",
                        "roles": [
                            "licensor",
                            "host"
                        ]
                    }
                ],
                "proj:epsg": null,
                "proj:shape": [
                    10560.0,
                    14144.0
                ],
                "direction": "north",
                "estimated_accuracy": null,
                "pers:omega": 44.98029,
                "pers:phi": 0.176283,
                "pers:kappa": 0.192033,
                "pers:perspective_center": [
                    593018.213,
                    6128463.396,
                    2107.559
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999989650297892,
                    0.00454556004639101,
                    0.000192823662054385,
                    -0.00335158598411061,
                    0.707338725138201,
                    0.706866815454832,
                    0.00307671391115711,
                    -0.706860145858945,
                    0.707346639228448
                ],
                "pers:interior_orientation": {
                    "camera_id": "UCOM4-434S42016X419232_UC-Op-FWD",
                    "focal_length": 123.38,
                    "pixel_spacing": [
                        0.00376,
                        0.00376
                    ],
                    "calibration_date": "2021-03-29",
                    "principal_point_offset": [
                        0.0,
                        0.0
                    ],
                    "sensor_array_dimensions": [
                        14144.0,
                        10560.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_59/1km_6130_593/2021_83_38_2_0032_00003342.tif",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_593%2F2021_83_38_2_0032_00003342.tif"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021/items/2021_83_38_2_0032_00003342"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/"
                },
                {
                    "rel": "license",
                    "href": "https://dataforsyningen.dk/Vilkaar",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFI license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_593%2F2021_83_38_2_0032_00003342.tif",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_59/1km_6130_593/2021_83_38_2_0032_00003342.tif",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_593%2F2021_83_38_2_0032_00003342.tif",
                    "type": "image/jpeg",
                    "roles": [
                        "thumbnail"
                    ],
                    "title": "Thumbnail"
                }
            },
            "crs": {
                "type": "name",
                "properties": {
                    "name": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                }
            }
        },
        {
            "type": "Feature",
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json"
            ],
            "id": "2021_83_38_5_0032_00003342",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.44622353593845,
                            55.290658963473525
                        ],
                        [
                            10.42009555405466,
                            55.28921665761426
                        ],
                        [
                            10.420342653259898,
                            55.29921152910762
                        ],
                        [
                            10.446365584487257,
                            55.2972812153131
                        ],
                        [
                            10.44622353593845,
                            55.290658963473525
                        ]
                    ]
                ]
            },
            "bbox": [
                10.4200955540547,
                55.2892166576143,
                10.4463655844873,
                55.2992115291076
            ],
            "properties": {
                "datetime": "2021-06-17T16:22:00Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "UCOM4-434S42016X419232_UC-Op-Left"
                ],
                "providers": [
                    {
                        "name": "Geofly GmbH",
                        "roles": [
                            "producer",
                            "processor"
                        ]
                    },
                    {
                        "url": "https://sdfi.dk/",
                        "name": "SDFI",
                        "roles": [
                            "licensor",
                            "host"
                        ]
                    }
                ],
                "proj:epsg": null,
                "proj:shape": [
                    14144.0,
                    10560.0
                ],
                "direction": "west",
                "estimated_accuracy": null,
                "pers:omega": -0.277632,
                "pers:phi": 44.981847,
                "pers:kappa": 90.324774,
                "pers:perspective_center": [
                    593018.773,
                    6128463.357,
                    2107.201
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    -0.00400939507039167,
                    0.999991610642069,
                    -0.000838687456751705,
                    -0.707319414655841,
                    -0.00224308157577215,
                    0.706890524930107,
                    0.706882713328094,
                    0.00342742330695016,
                    0.707322474100312
                ],
                "pers:interior_orientation": {
                    "camera_id": "UCOM4-434S42016X419232_UC-Op-Left",
                    "focal_length": 123.38,
                    "pixel_spacing": [
                        0.00376,
                        0.00376
                    ],
                    "calibration_date": "2021-03-29",
                    "principal_point_offset": [
                        0.0,
                        6.68
                    ],
                    "sensor_array_dimensions": [
                        10560.0,
                        14144.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_612_59/1km_6128_590/2021_83_38_5_0032_00003342.tif",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_612_59%2F1km_6128_590%2F2021_83_38_5_0032_00003342.tif"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021/items/2021_83_38_5_0032_00003342"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/"
                },
                {
                    "rel": "license",
                    "href": "https://dataforsyningen.dk/Vilkaar",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFI license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_612_59%2F1km_6128_590%2F2021_83_38_5_0032_00003342.tif",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_612_59/1km_6128_590/2021_83_38_5_0032_00003342.tif",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_612_59%2F1km_6128_590%2F2021_83_38_5_0032_00003342.tif",
                    "type": "image/jpeg",
                    "roles": [
                        "thumbnail"
                    ],
                    "title": "Thumbnail"
                }
            },
            "crs": {
                "type": "name",
                "properties": {
                    "name": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                }
            }
        },
        {
            "type": "Feature",
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json"
            ],
            "id": "2021_83_38_2_0032_00003341",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.473480187736165,
                            55.30236497714729
                        ],
                        [
                            10.456466377857192,
                            55.302529028424004
                        ],
                        [
                            10.453541049373822,
                            55.314803196505316
                        ],
                        [
                            10.477107387145127,
                            55.31456243074976
                        ],
                        [
                            10.473480187736165,
                            55.30236497714729
                        ]
                    ]
                ]
            },
            "bbox": [
                10.4535410493738,
                55.3023649771473,
                10.4771073871451,
                55.3148031965053
            ],
            "properties": {
                "datetime": "2021-06-17T16:21:55Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "UCOM4-434S42016X419232_UC-Op-FWD"
                ],
                "providers": [
                    {
                        "name": "Geofly GmbH",
                        "roles": [
                            "producer",
                            "processor"
                        ]
                    },
                    {
                        "url": "https://sdfi.dk/",
                        "name": "SDFI",
                        "roles": [
                            "licensor",
                            "host"
                        ]
                    }
                ],
                "proj:epsg": null,
                "proj:shape": [
                    10560.0,
                    14144.0
                ],
                "direction": "north",
                "estimated_accuracy": null,
                "pers:omega": 44.987886,
                "pers:phi": 0.277083,
                "pers:kappa": 0.088164,
                "pers:perspective_center": [
                    593013.761,
                    6127938.753,
                    2107.165
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999987122658373,
                    0.00450712710308846,
                    -0.00233244993632013,
                    -0.00153873348114172,
                    0.707250170341625,
                    0.706961688389842,
                    0.00483599180136276,
                    -0.706948995583853,
                    0.707247998106943
                ],
                "pers:interior_orientation": {
                    "camera_id": "UCOM4-434S42016X419232_UC-Op-FWD",
                    "focal_length": 123.38,
                    "pixel_spacing": [
                        0.00376,
                        0.00376
                    ],
                    "calibration_date": "2021-03-29",
                    "principal_point_offset": [
                        0.0,
                        0.0
                    ],
                    "sensor_array_dimensions": [
                        14144.0,
                        10560.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_59/1km_6130_592/2021_83_38_2_0032_00003341.tif",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_592%2F2021_83_38_2_0032_00003341.tif"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021/items/2021_83_38_2_0032_00003341"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/collections/skraafotos2021"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafoto_api/"
                },
                {
                    "rel": "license",
                    "href": "https://dataforsyningen.dk/Vilkaar",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFI license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_592%2F2021_83_38_2_0032_00003341.tif",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server/COG_oblique_2021/10km_613_59/1km_6130_592/2021_83_38_2_0032_00003341.tif",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_592%2F2021_83_38_2_0032_00003341.tif",
                    "type": "image/jpeg",
                    "roles": [
                        "thumbnail"
                    ],
                    "title": "Thumbnail"
                }
            },
            "crs": {
                "type": "name",
                "properties": {
                    "name": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                }
            }
        }
    ],
    "links": [
        {
            "rel": "self",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/search",
            "method": "POST",
            "body": {
                "filter-lang": "cql-json",
                "filter": {
                    "intersects": [
                        {
                            "property": "geometry"
                        },
                        {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [
                                        10.2113,
                                        55.3226
                                    ],
                                    [
                                        10.4106,
                                        55.2783
                                    ],
                                    [
                                        10.5213,
                                        55.358
                                    ],
                                    [
                                        10.404,
                                        55.4466
                                    ],
                                    [
                                        10.2888,
                                        55.4267
                                    ]
                                ]
                            ]
                        }
                    ]
                },
                "filter-crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                "limit": 3
            }
        },
        {
            "rel": "next",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafoto_api/search",
            "method": "POST",
            "body": {
                "filter-lang": "cql-json",
                "filter": {
                    "intersects": [
                        {
                            "property": "geometry"
                        },
                        {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [
                                        10.2113,
                                        55.3226
                                    ],
                                    [
                                        10.4106,
                                        55.2783
                                    ],
                                    [
                                        10.5213,
                                        55.358
                                    ],
                                    [
                                        10.404,
                                        55.4466
                                    ],
                                    [
                                        10.2888,
                                        55.4267
                                    ]
                                ]
                            ]
                        }
                    ]
                },
                "filter-crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                "limit": 3,
                "pt": "PmR0OjIwMjEtMDYtMTcgMTg6MjE6NTUrMDI6MDB-czoyMDIxXzgzXzM4XzJfMDAzMl8wMDAwMzM0MQ=="
            }
        }
    ],
    "context": {
        "returned": 3,
        "limit": 3,
        "matched": 20126
    }
}
```

Se `GET/POST /search` under [Endpoints og outputs](#endpoints-og-outputs) for mulige parametre og output type.

Angiver query parameterne. Her er det parameteren `bbox` med værdierne `10.3285,55.3556,10.4536,55.4132`, som beskriver hvilket geografisk område, man ønsker metadata om billederne fra. I dette eksempel er bbox i projektion `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, hvilket bliver angivet i `bbox-crs` parameteren. Limit er sat til 3, så hvis der er et match mellem den angivet `bboxs` koordinater og metadata for skåfotos, vil JSON response indeholde tre `items` objekter. I `context` objektet er attributterne `Returned`, `Limit` og `Matched`, der kan læses mere om på [Context Extension](#context-extension), hvor det også er forklaret hvordan paging fungerer.