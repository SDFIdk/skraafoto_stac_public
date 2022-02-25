# Skraafoto-stac-api - How to get started

## Introduktion

Guiden er en hurtig gennemgang af, hvordan man får skråfoto billeder for et bestemt geografisk område ved hjælp af koordinater. Dokumentationen til api'et kan findes [her](https://github.com/Dataforsyningen/skraafoto_stac_public/blob/main/dokumentation.md).

## Authentication
Benyttes i webapplikationer og GIS systemer, når du kalder API’er og webservices. Dataforsyningen er stateless, derfor skal `token` altid sendes med hver forespørgsel til `Dataforsyningen`, undtagen alle DAWA og Inspire OGC-tjenesterne.

Du skal være oprettet som bruger på `Dataforsyningen` og være logget ind, for at oprette og administrere dine `tokens` på `Dataforsyningen` (direkte link til stedet):
1. Klik på brugerikonet øverst i højre hjørne
2. Gå til "Administrer token til webservices og API’er"
3. Klik på ”Opret ny token”
Der bliver generet en `token` bestående af tilfælde tal og har et navn af tilfældige bogstaver og tal. Man kan om navngive `tokens`, så den kan blive navngivet noget der giver mening for dig - er især anbefaldet hvis den skal bruges til noget specifikt. Man kan også definere udløbsdata for `tokens`.

Token benyttes til at identificere sig overfor `Dataforsyningen` uden risiko for at afsløre brugernavn og adgangskode. Det kan f.eks. være relevant, hvis `Dataforsyningens` webservices er implementeret i webapplikationer tilgængelige for alle på internettet.

Token skal angives på én af følgende måder i requesten:
1. Som header parameteren `token` (anbefalder vi at bruge, da det er den mest sikre måde)
```http
GET https://api.dataforsyningen.dk/{servicenavnet på tjenesten}
token: {DinToken}
```
2. Som queryparameter `token` i URL'en
```http
GET https://api.dataforsyningen.dk/{servicenavnet på tjenesten}?token={DinToken}
```

Alle kald til `Dataforsyningens` API'erne og webservices skal bruge HTTPS, da der ikke understøttes HTTP, og `token` skal være angivet (undtagen alle DAWA og Inspire OGC-tjenesterne). Kald uden `token` angivet eller med ugyldig `token` vil fejle.

## Jeg har en bbox, hvordan får jeg vist billeder af stedet?
STAC API'et returnerer metadata om skråfoto billederne, som er inddelt i collection niveau, som hver har items i sig. Hvert `item object` indeholder metadata om ét bestemt billede, og der er også URL'er til de forskellige måder det `items` billeder kan hentes ned/ses:
1. I features -> assets -> data -> title `Raw tiff file`. Linket starter med `https://api.dataforsyningen.dk/skraafoto_server_test` downloader en [Cloud Optimized Geotiff](https://www.cogeo.org) (`COG`), og den kan man hente ned som en range request.
2. I features -> assets -> data -> title `Thumbnail`. Linket starter med `https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg` henter en thumbnail af COG'en som en jpg.
3. features -> links -> title `Interactive image viewer`. Linket starter med `https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html` er en viewer til browseren, som viser COG'en og man kan zoome og full screene COG'en i ens browser.

Hvis der kun ønskes billeder af det samme sted fra samme årgang, så anbefales det at benytte `/collections/{collectionid}/items` endpoint i stedet for `/search` endpoint, da `/search` kræver flere resourcer at udføre.
Hvis der ønskes billeder af det samme sted, på tværs af collectionerne skal der bruges `/search`.

**Samme årgang**

Man angiver ved {collectionid} i URL pathen, hvilken collection man ønsker at fremsøge billeder fra. I dette tilfælde er det `skraafotos2019` collection. Dernæst angiver man i parameterne, i dette tilfælde ved hjælp af en bbox, i parameteren `bbox` med værdierne `7,54,15,57`, hvilket geografisk område, man ønsker metadata om billederne fra. I dette eksempel er bbox i projektion `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, hvilket bliver angivet i `bbox-crs` parameteren. Limit er sat til 3, så hvis der er et match mellem den angivets bbox koordinater og metadataen for skåfoto billederne vil json response indeholder tre `items` objekter. Man kan se i `context` objektet attributter `Returned`, `Limit` og `Matched`, som kan læses mere om på [dokumentation](https://github.com/Dataforsyningen/skraafoto_stac_public/blob/main/dokumentation.md#context-extension), hvor der også er forklaret hvordan paging fungerer.

_URL_: 
```http
https://api.dataforsyningen.dk/skraafotoapi_test/collections/{collectionid}/items?token={DinToken}
```

_Parametre_:

| **Parameter** | **Type**   | **Description**                                                                                                                                                                 |
|---------------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| collectionid  | \[string]  |                                                                                                                                                                                 |
| crs           | string     | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`                                                        |
| limit         | integer    |                                                                                                                                                                                 |
| pt            | string     |                                                                                                                                                                                 |
| ids           | \[string]  | Array of Item ids to return.                                                                                                                                                    |
| bbox          | \[number]  |                                                                                                                                                                                 |
| bbox-crs      | string     | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`                                                        |
| datetime      | string     | Single date+time, or a range ('/' separator), formatted to [RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). Use double dots `..` for open date ranges. |
| filter        | string     |                                                                                                                                                                                 |
| filter-lang   | string     |                                                                                                                                                                                 |
| filter-crs    | string     | Default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`                                                        |
collectionid, crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), limit (default: 10, maks: 10000), pt (page*token), ids, bbox, bbox-crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), datetime, filter, filter-lang (default: `cql-json`), filter-crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`)

_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)  

_Eksempel_: 
```http
https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?bbox=7,54,15,57&bbox-crs=http://www.opengis.net/def/crs/OGC/1.3/CRS84&limit=3&token={DinToken}
```

_Response_:
<details>

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
            "id": "2019_83_37_2_0046_00001113",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.256902168437476,
                            55.31540683597307
                        ],
                        [
                            10.254352853154417,
                            55.325498148133846
                        ],
                        [
                            10.274061541671555,
                            55.32520434258585
                        ],
                        [
                            10.270493845560978,
                            55.31517636484912
                        ],
                        [
                            10.256902168437476,
                            55.31540683597307
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2543528531544,
                55.3151763648491,
                10.2740615416716,
                55.3254981481338
            ],
            "properties": {
                "datetime": "2019-07-10T09:24:28Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011017"
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
                    8578.0,
                    11478.0
                ],
                "direction": "north",
                "estimated_accuracy": 0.01,
                "pers:omega": 45.1494,
                "pers:phi": -0.500588,
                "pers:kappa": -0.368475,
                "pers:perspective_center": [
                    580185.73,
                    6129577.28,
                    1504.27
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999941154780583,
                    -0.0107293797111696,
                    0.00160230680185256,
                    0.00643081200712992,
                    0.70520627422282,
                    0.708973028720908,
                    -0.00873679764002093,
                    -0.708921004913652,
                    0.705233774828755
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011017",
                    "focal_length": 108.2837,
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_580/2019_83_37_2_0046_00001113.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0046_00001113.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001113?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0046_00001113.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_580/2019_83_37_2_0046_00001113.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0046_00001113.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
            "id": "2019_83_37_2_0046_00001112",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.256845575470791,
                            55.31262153628505
                        ],
                        [
                            10.254296413824072,
                            55.32271285097639
                        ],
                        [
                            10.27406962443831,
                            55.322508241343854
                        ],
                        [
                            10.270483554894435,
                            55.312390584659546
                        ],
                        [
                            10.256845575470791,
                            55.31262153628505
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2542964138241,
                55.3123905846595,
                10.2740696244383,
                55.3227128509764
            ],
            "properties": {
                "datetime": "2019-07-10T09:24:24Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011017"
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
                    8578.0,
                    11478.0
                ],
                "direction": "north",
                "estimated_accuracy": 0.01,
                "pers:omega": 45.1428,
                "pers:phi": -0.647623,
                "pers:kappa": -0.183337,
                "pers:perspective_center": [
                    580183.39,
                    6129264.44,
                    1503.38
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.99993100089976,
                    -0.0102691995567487,
                    0.00570411956995191,
                    0.00319962447753112,
                    0.70531238857521,
                    0.708889410927779,
                    -0.0113029130230848,
                    -0.708822247155657,
                    0.705296580237277
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011017",
                    "focal_length": 108.2837,
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001112.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001112.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001112?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001112.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001112.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001112.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
            "id": "2019_83_37_2_0046_00001111",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.256675898750547,
                            55.309747531646885
                        ],
                        [
                            10.254142621809663,
                            55.319838685031996
                        ],
                        [
                            10.273801242300337,
                            55.31954542009687
                        ],
                        [
                            10.270249892107573,
                            55.30951725898986
                        ],
                        [
                            10.256675898750547,
                            55.309747531646885
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2541426218097,
                55.3095172589899,
                10.2738012423003,
                55.319838685032
            ],
            "properties": {
                "datetime": "2019-07-10T09:24:19Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011017"
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
                    8578.0,
                    11478.0
                ],
                "direction": "north",
                "estimated_accuracy": 0.01,
                "pers:omega": 45.1192,
                "pers:phi": -0.511871,
                "pers:kappa": -0.349494,
                "pers:perspective_center": [
                    580181.98,
                    6128951.8,
                    1502.34
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999941490461688,
                    -0.0106343155137821,
                    0.0019816626378911,
                    0.00609953994682159,
                    0.705582922039916,
                    0.708601111866225,
                    -0.00893371511154277,
                    -0.708547564711902,
                    0.705606503141191
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011017",
                    "focal_length": 108.2837,
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001111.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001111.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001111?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001111.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001111.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001111.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?bbox=7%2C54%2C15%2C57&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&limit=3&token=4adf32524ae6d6998565f638a1090ba1",
            "method": "GET",
            "body": false
        },
        {
            "rel": "next",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?bbox=7%2C54%2C15%2C57&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&limit=3&token=4adf32524ae6d6998565f638a1090ba1&pt=PmR0OjIwMTktMDctMTAgMTE6MjQ6MTkrMDI6MDB-czoyMDE5XzgzXzM3XzJfMDA0Nl8wMDAwMTExMQ%3D%3D",
            "method": "GET",
            "body": false
        }
    ],
    "context": {
        "returned": 3,
        "limit": 3,
        "matched": 13347
    }
}
```

</details>

**På tværs af årgange**

Man angiver i parameterne, i dette tilfælde ved hjælp af en bbox, i parameteren `bbox` med værdierne `7,54,15,57`, hvilket geografisk område, man ønsker metadata om billederne fra. I dette eksempel er bbox i projektion `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, hvilket bliver angivet i `bbox-crs` parameteren. Limit er sat til 3, så hvis der er et match mellem den angivets bbox koordinater og metadataen for skåfoto billederne vil json response indeholder tre `items` objekter. Man kan se i `context` objektet attributter `Returned`, `Limit` og `Matched`, som kan læses mere om på [dokumentation](https://github.com/Dataforsyningen/skraafoto_stac_public/blob/main/dokumentation.md#context-extension), hvor der også er forklaret hvordan paging fungerer. 

_URL_: 
```http
https://api.dataforsyningen.dk/skraafotoapi_test/search?token={DinToken}
```

_Parametre_: crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), limit (default: 10, maks: 10000), (page*token), ids, bbox, bbox-crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), datetime, filter, filter-lang (default: `cql-json`), filter-crs (default: `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, understøtter også `http://www.opengis.net/def/crs/EPSG/0/25832`), collections, sortby

_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)

_Eksempel_: 
```http
https://api.dataforsyningen.dk/skraafotoapi_test/search?bbox=7,54,15,57&bbox-crs=http://www.opengis.net/def/crs/OGC/1.3/CRS84&limit=3&token={DinToken}
```

_Response_:
<details>

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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_59/1km_6130_593/2021_83_38_2_0032_00003342.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_593%2F2021_83_38_2_0032_00003342.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_38_2_0032_00003342?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_593%2F2021_83_38_2_0032_00003342.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_59/1km_6130_593/2021_83_38_2_0032_00003342.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_593%2F2021_83_38_2_0032_00003342.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_59/1km_6130_592/2021_83_38_2_0032_00003341.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_592%2F2021_83_38_2_0032_00003341.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_38_2_0032_00003341?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_592%2F2021_83_38_2_0032_00003341.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_59/1km_6130_592/2021_83_38_2_0032_00003341.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_592%2F2021_83_38_2_0032_00003341.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
            "id": "2021_83_37_4_0021_00002251",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.261103512566743,
                            55.313460052304826
                        ],
                        [
                            10.288341655671402,
                            55.31485841870833
                        ],
                        [
                            10.287953118247627,
                            55.3044632084613
                        ],
                        [
                            10.260829105954477,
                            55.306592793623594
                        ],
                        [
                            10.261103512566743,
                            55.313460052304826
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2608291059545,
                55.3044632084613,
                10.2883416556714,
                55.3148584187083
            ],
            "properties": {
                "datetime": "2021-06-17T11:33:50Z",
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
                    14144.0,
                    10560.0
                ],
                "direction": "east",
                "estimated_accuracy": null,
                "pers:omega": -0.05256,
                "pers:phi": -44.98416,
                "pers:kappa": -90.15237,
                "pers:perspective_center": [
                    578812.785,
                    6130024.641,
                    2113.848
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    -0.00188096778416517,
                    -0.999997767692113,
                    -0.000962585572927537,
                    0.707299739926167,
                    -0.00201087475648397,
                    0.706910909721366,
                    -0.706911267317597,
                    0.000648840122072455,
                    0.707301943406015
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6130_580/2021_83_37_4_0021_00002251.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_4_0021_00002251.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_37_4_0021_00002251?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token=4adf32524ae6d6998565f638a1090ba1"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_4_0021_00002251.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6130_580/2021_83_37_4_0021_00002251.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_4_0021_00002251.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/search?bbox=7%2C54%2C15%2C57&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&limit=3&token=4adf32524ae6d6998565f638a1090ba1",
            "method": "GET",
            "body": null
        },
        {
            "rel": "next",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/search?bbox=7%2C54%2C15%2C57&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&limit=3&token=4adf32524ae6d6998565f638a1090ba1&pt=PmR0OjIwMjEtMDYtMTcgMTM6MzM6NTArMDI6MDB-czoyMDIxXzgzXzM3XzRfMDAyMV8wMDAwMjI1MQ%3D%3D",
            "method": "GET",
            "body": null
        }
    ],
    "context": {
        "returned": 3,
        "limit": 3,
        "matched": 22342
    }
}
```

</details>


## Tips og tricks
Hvis man kun ønsker skråfoto billeder fra samme årgang, så anbefales det at benytte  `/collections/{collectionid}` endpoint i stedet for `/search` endpoint.