Eksempler på fulde use cases i kode (fra bbox til billede på skærmen)
Til udvikleren uden det avancerede behov
"Jeg har en koordinat i hånden, hvordan får jeg vist et billede af stedet"-opskrift
Hvis man altid ønsker billeder fra 2021, så gå på den collection i stedet for ”/search”, da den er tungere rent database
Hvordan får man vist et billede, hente som COG, thumbnail eller vieweren, og at man går igennem metadataen først.

# Skraafoto-stac-api - How to get started

## Introduktion

Guiden er en hurtig gennemgang af, hvordan man får skråfoto billeder for et bestemt geografisk område ved hjælp af koordinater.

## Authentication
Der skal altid anvendes `token`, når der benyttes Dataforsyningens services. Du kan oprette og administrere dine `tokens` på `dataforsyningen.dk` ved at følge denne [guide](https://dataforsyningen.dk/news/3808).

Token skal angives på én af følgende måder i requesten (URL'erne er til testmiljøet og derfor ikke de blivende!):
1. Som header parameteren `token`
```
https://api.dataforsyningen.dk/skraafotoapi_test
token: {DinToken}
```
2. Som queryparameter `token` i URL'en
```
https://api.dataforsyningen.dk/skraafotoapi_test?token={DinToken}
```

Alle kald til API'erne skal bruge HTTPS, da der ikke understøttes HTTP. Kald hvor token ikke er angivet eller er ugyldig vil fejle.

## Jeg har en bbox, hvordan får jeg vist billeder af stedet?
STAC API'et returnerer metadata om skråfoto billederne, som er inddelt i collection niveau, som hver har items i sig. Hvert `item object` indeholder metadata om ét bestemt billede, og der er også URL'er til de forskellige måder det `items` billeder kan hentes ned/ses:
1. I features -> assets -> data -> title `Raw tiff file`. Linket starter med `https://api.dataforsyningen.dk/skraafoto_server_test` downloader en [Cloud Optimized Geotiff](https://www.cogeo.org) (`COG`), og den kan man hente ned som en range request.
2. I features -> assets -> data -> title `Thumbnail`. Linket starter med `https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg` henter en thumbnail af COG'en som en jpg.
3. features -> links -> title `Interactive image viewer`. Linket starter med `https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html` er en viewer til browseren, som viser COG'en og man kan zoome og full screene COG'en i ens browser.

Hvis der kun ønskes billeder af det samme sted fra samme årgang, så anbefales det at benytte `/collections/{collectionid}/items` endpoint i stedet for `/search` endpoint, da `/search` kræver flere resourcer at udføre.
Hvis der ønskes billeder af det samme sted, på tværs af collectionerne skal der bruges `/search`.

**Samme årgang**
Man angiver ved {collectionid} i URL pathen, hvilken collection man ønsker at fremsøge billeder fra. I dette tilfælde er det `skraafotos2019` collection. Dernæst angiver man i parameterne, i dette tilfælde ved hjælp af en bbox `7,54,15,57`, hvilket geografisk område, man ønsker metadata om billederne fra. I dette eksempel er bbox i projektion `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, hvilket bliver angivet i `bbox-crs` parameteren.

_URL_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/{collectionid}/items?token={DinToken}

_Parametre_: collectionid, crs (default: http://www.opengis.net/def/crs/OGC/1.3/CRS84), limit, pt (page*token), ids, bbox, bbox-crs (default: http://www.opengis.net/def/crs/EPSG/0/25832), datetime, filter, filter-lang, filter-crs

_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)  

_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?bbox=7,54,15,57&bbox-crs=http://www.opengis.net/def/crs/OGC/1.3/CRS84&token={DinToken}

_Response_:
<details>
```
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_580/2019_83_37_2_0046_00001113.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0046_00001113.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001113?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0046_00001113.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_580/2019_83_37_2_0046_00001113.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0046_00001113.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001112.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001112.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001112?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001112.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001112.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001112.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001111.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001111.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001111?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001111.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001111.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001111.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2019_83_37_2_0046_00001110",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.256433183149118,
                            55.30705401145479
                        ],
                        [
                            10.253855580891987,
                            55.317235486701705
                        ],
                        [
                            10.273701955260005,
                            55.31694030344154
                        ],
                        [
                            10.270116503377482,
                            55.306822623941684
                        ],
                        [
                            10.256433183149118,
                            55.30705401145479
                        ]
                    ]
                ]
            },
            "bbox": [
                10.253855580892,
                55.3068226239417,
                10.27370195526,
                55.3172354867017
            ],
            "properties": {
                "datetime": "2019-07-10T09:24:14Z",
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
                "pers:omega": 45.2249,
                "pers:phi": -0.397848,
                "pers:kappa": -0.411287,
                "pers:perspective_center": [
                    580179.5,
                    6128639.06,
                    1503.93
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.99995012885802,
                    -0.00998487363554757,
                    -0.000205171420520499,
                    0.00717807779108025,
                    0.704272300187369,
                    0.70989365568937,
                    -0.00694370189847259,
                    -0.709859725218493,
                    0.704308849523184
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001110.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001110.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001110?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001110.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001110.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001110.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2019_83_37_2_0047_00000900",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.26616204542547,
                            55.30434739366341
                        ],
                        [
                            10.26342525533843,
                            55.314890208338625
                        ],
                        [
                            10.283790187181783,
                            55.31458801460657
                        ],
                        [
                            10.280080582238458,
                            55.3041124456598
                        ],
                        [
                            10.26616204542547,
                            55.30434739366341
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2634252553384,
                55.3041124456598,
                10.2837901871818,
                55.3148902083386
            ],
            "properties": {
                "datetime": "2019-07-10T09:05:56Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011009"
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
                "pers:omega": 45.9422,
                "pers:phi": -0.436825,
                "pers:kappa": -0.177618,
                "pers:perspective_center": [
                    580806.79,
                    6128315.09,
                    1512.69
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999966132273789,
                    -0.00763454490437985,
                    0.0030737647114294,
                    0.00309992379687096,
                    0.695363556202759,
                    0.718651455976752,
                    -0.00762396077192256,
                    -0.718617588449625,
                    0.695363672327648
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011009",
                    "focal_length": 108.2201,
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000900.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000900.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0047_00000900?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000900.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000900.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000900.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2019_83_37_2_0047_00000899",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.26630088006868,
                            55.3072217108691
                        ],
                        [
                            10.263532433270042,
                            55.31776485047064
                        ],
                        [
                            10.28394900081554,
                            55.31755197173626
                        ],
                        [
                            10.280204672896632,
                            55.3069869071341
                        ],
                        [
                            10.26630088006868,
                            55.3072217108691
                        ]
                    ]
                ]
            },
            "bbox": [
                10.26353243327,
                55.3069869071341,
                10.2839490008155,
                55.3177648504706
            ],
            "properties": {
                "datetime": "2019-07-10T09:05:52Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011009"
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
                "pers:omega": 46.0987,
                "pers:phi": -0.43415,
                "pers:kappa": -0.165554,
                "pers:perspective_center": [
                    580809.37,
                    6128627.94,
                    1511.58
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999967117668806,
                    -0.00746327723902381,
                    0.00317223485791632,
                    0.00288937545235508,
                    0.693398912397936,
                    0.720548124551618,
                    -0.00757727461793739,
                    -0.720515265472018,
                    0.693397676035298
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011009",
                    "focal_length": 108.2201,
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000899.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000899.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0047_00000899?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000899.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000899.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000899.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2019_83_37_2_0047_00000898",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.266512764388851,
                            55.30991553465912
                        ],
                        [
                            10.26375995178632,
                            55.32045851217281
                        ],
                        [
                            10.284036111338976,
                            55.32024707887222
                        ],
                        [
                            10.280325890301366,
                            55.30977152989664
                        ],
                        [
                            10.266512764388851,
                            55.30991553465912
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2637599517863,
                55.3097715298966,
                10.284036111339,
                55.3204585121728
            ],
            "properties": {
                "datetime": "2019-07-10T09:05:47Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011009"
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
                "pers:omega": 46.1154,
                "pers:phi": -0.484161,
                "pers:kappa": -0.109302,
                "pers:perspective_center": [
                    580812.25,
                    6128940.86,
                    1508.9
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999962477688368,
                    -0.00741271274558638,
                    0.00448273410887036,
                    0.00190761049878102,
                    0.693195273313504,
                    0.720747302511776,
                    -0.0084501028114662,
                    -0.720711707096234,
                    0.693183403593095
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011009",
                    "focal_length": 108.2201,
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000898.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000898.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0047_00000898?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000898.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000898.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000898.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2019_83_37_2_0047_00000897",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.266554276579267,
                            55.31270099103731
                        ],
                        [
                            10.263858599226998,
                            55.32306363861314
                        ],
                        [
                            10.284025798984567,
                            55.32285334148327
                        ],
                        [
                            10.280349724182368,
                            55.3124673047216
                        ],
                        [
                            10.266554276579267,
                            55.31270099103731
                        ]
                    ]
                ]
            },
            "bbox": [
                10.263858599227,
                55.3124673047216,
                10.2840257989846,
                55.3230636386131
            ],
            "properties": {
                "datetime": "2019-07-10T09:05:43Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011009"
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
                "pers:omega": 45.8226,
                "pers:phi": -0.387937,
                "pers:kappa": -0.30207,
                "pers:perspective_center": [
                    580813.7,
                    6129253.62,
                    1507.3
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999963181117068,
                    -0.00852982632450736,
                    0.000937268962572972,
                    0.00527197066069585,
                    0.696847251698912,
                    0.717200191107772,
                    -0.00677072637072446,
                    -0.717168843343425,
                    0.696866563555654
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011009",
                    "focal_length": 108.2201,
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000897.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000897.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0047_00000897?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000897.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000897.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000897.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2019_83_37_2_0047_00000896",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.26671895496472,
                            55.31539530183857
                        ],
                        [
                            10.264051802775409,
                            55.32566778570772
                        ],
                        [
                            10.284078514145909,
                            55.325458940599106
                        ],
                        [
                            10.280452326595139,
                            55.31516225278969
                        ],
                        [
                            10.26671895496472,
                            55.31539530183857
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2640518027754,
                55.3151622527897,
                10.2840785141459,
                55.3256677857077
            ],
            "properties": {
                "datetime": "2019-07-10T09:05:39Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "PhaseOne-IXU-RS-1000_RS011009"
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
                "pers:omega": 45.5414,
                "pers:phi": -0.496169,
                "pers:kappa": -0.120987,
                "pers:perspective_center": [
                    580811.47,
                    6129566.49,
                    1507.15
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.99996027492783,
                    -0.00765985544235753,
                    0.00455797991017816,
                    0.00211154072272163,
                    0.700378610855903,
                    0.71376840981605,
                    -0.00865967447631204,
                    -0.713730430954263,
                    0.700366962361737
                ],
                "pers:interior_orientation": {
                    "camera_id": "PhaseOne-IXU-RS-1000_RS011009",
                    "focal_length": 108.2201,
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_580/2019_83_37_2_0047_00000896.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0047_00000896.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0047_00000896?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0047_00000896.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_580/2019_83_37_2_0047_00000896.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0047_00000896.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2019_83_37_2_0048_00000895",
            "collection": "skraafotos2019",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.275710818690401,
                            55.315211861539204
                        ],
                        [
                            10.273166299947297,
                            55.32530354239699
                        ],
                        [
                            10.292858948297976,
                            55.325006869875956
                        ],
                        [
                            10.289302287007313,
                            55.31497929859674
                        ],
                        [
                            10.275710818690401,
                            55.315211861539204
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2731662999473,
                55.3149792985967,
                10.292858948298,
                55.325303542397
            ],
            "properties": {
                "datetime": "2019-07-10T09:03:32Z",
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
                "pers:omega": 45.1363,
                "pers:phi": -0.455349,
                "pers:kappa": -0.391851,
                "pers:perspective_center": [
                    581381.23,
                    6129577.55,
                    1498.78
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999945034317378,
                    -0.010457190365524,
                    0.000758626176811709,
                    0.00683882097526344,
                    0.705367835585696,
                    0.708808469933041,
                    -0.00794725560714194,
                    -0.708764321683032,
                    0.705400579413928
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_581/2019_83_37_2_0048_00000895.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_581%2F2019_83_37_2_0048_00000895.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0048_00000895?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_581%2F2019_83_37_2_0048_00000895.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_581/2019_83_37_2_0048_00000895.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_581%2F2019_83_37_2_0048_00000895.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?bbox=7%2C54%2C15%2C57&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&token={DinToken}&limit=10",
            "method": "GET",
            "body": false
        },
        {
            "rel": "next",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?bbox=7%2C54%2C15%2C57&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&token={DinToken}&limit=10&pt=PmR0OjIwMTktMDctMTAgMTE6MDM6MzIrMDI6MDB-czoyMDE5XzgzXzM3XzJfMDA0OF8wMDAwMDg5NQ%3D%3D",
            "method": "GET",
            "body": false
        }
    ],
    "context": {
        "returned": 10,
        "limit": 10,
        "matched": 13347
    }
}
```
</details>

**På tværs af årgange**
Man angiver i parameterne, i dette tilfælde ved hjælp af en bbox i parameteren `bbox` med værdierne `7,54,15,57`, hvilket geografisk område, man ønsker metadata om billederne fra. I dette eksempel er bbox i projektion `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, hvilket bliver angivet i `bbox-crs` parameteren.

_URL_: https://api.dataforsyningen.dk/skraafotoapi_test/search?token={DinToken}

_Parametre_: crs (default: http://www.opengis.net/def/crs/OGC/1.3/CRS84), limit, (page*token), ids, bbox, bbox-crs (default: http://www.opengis.net/def/crs/EPSG/0/25832), datetime, filter, filter-lang, filter-crs, collections, sortby

_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)

_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/search?bbox=7,54,15,57&bbox-crs=http://www.opengis.net/def/crs/OGC/1.3/CRS84&token={DinToken}

_Response_:
<details>
```
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_59/1km_6130_593/2021_83_38_2_0032_00003342.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_593%2F2021_83_38_2_0032_00003342.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_38_2_0032_00003342?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_593%2F2021_83_38_2_0032_00003342.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_59/1km_6130_593/2021_83_38_2_0032_00003342.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_593%2F2021_83_38_2_0032_00003342.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_59/1km_6130_592/2021_83_38_2_0032_00003341.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_592%2F2021_83_38_2_0032_00003341.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_38_2_0032_00003341?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_592%2F2021_83_38_2_0032_00003341.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_59/1km_6130_592/2021_83_38_2_0032_00003341.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_59%2F1km_6130_592%2F2021_83_38_2_0032_00003341.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6130_580/2021_83_37_4_0021_00002251.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_4_0021_00002251.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_37_4_0021_00002251?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_4_0021_00002251.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6130_580/2021_83_37_4_0021_00002251.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_4_0021_00002251.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2021_83_37_4_0021_00002250",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.26122504762325,
                            55.318180752205535
                        ],
                        [
                            10.288451221171037,
                            55.31957126120616
                        ],
                        [
                            10.288056794444392,
                            55.30918239121614
                        ],
                        [
                            10.260941294045809,
                            55.31131875103928
                        ],
                        [
                            10.26122504762325,
                            55.318180752205535
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2609412940458,
                55.3091823912161,
                10.288451221171,
                55.3195712612062
            ],
            "properties": {
                "datetime": "2021-06-17T11:33:45Z",
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
                "pers:omega": -0.04842,
                "pers:phi": -44.97264,
                "pers:kappa": -90.19638,
                "pers:perspective_center": [
                    578812.019,
                    6130549.604,
                    2114.269
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    -0.00242474493791024,
                    -0.999995816286913,
                    -0.00157734608014581,
                    0.707440204273647,
                    -0.00283019089453542,
                    0.706767534198311,
                    -0.706769041476242,
                    0.000597852967678068,
                    0.707444107037851
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6130_580/2021_83_37_4_0021_00002250.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_4_0021_00002250.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_37_4_0021_00002250?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_4_0021_00002250.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6130_580/2021_83_37_4_0021_00002250.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_4_0021_00002250.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2021_83_37_4_0021_00002249",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.261203532651773,
                            55.322866278761886
                        ],
                        [
                            10.288446366101452,
                            55.32425752844161
                        ],
                        [
                            10.28811995557766,
                            55.31386024534555
                        ],
                        [
                            10.260962130958665,
                            55.31600082190092
                        ],
                        [
                            10.261203532651773,
                            55.322866278761886
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2609621309587,
                55.3138602453456,
                10.2884463661015,
                55.3242575284416
            ],
            "properties": {
                "datetime": "2021-06-17T11:33:40Z",
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
                "pers:omega": -0.11133,
                "pers:phi": -44.99424,
                "pers:kappa": -90.1368,
                "pers:perspective_center": [
                    578801.296,
                    6131074.428,
                    2114.533
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    -0.00168846362971193,
                    -0.999998542045159,
                    0.000254947303839918,
                    0.707175848042627,
                    -0.00101378500531941,
                    0.707036980776221,
                    -0.707035691486478,
                    0.00137409880270116,
                    0.707176528751286
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6131_580/2021_83_37_4_0021_00002249.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6131_580%2F2021_83_37_4_0021_00002249.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_37_4_0021_00002249?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6131_580%2F2021_83_37_4_0021_00002249.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6131_580/2021_83_37_4_0021_00002249.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6131_580%2F2021_83_37_4_0021_00002249.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2021_83_37_1_0022_00002248",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.27794801794131,
                            55.31312400976231
                        ],
                        [
                            10.24538936757348,
                            55.31358883088469
                        ],
                        [
                            10.245853941940002,
                            55.326211678453355
                        ],
                        [
                            10.278435876693363,
                            55.32584379870174
                        ],
                        [
                            10.27794801794131,
                            55.31312400976231
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2453893675735,
                55.3131240097623,
                10.2784358766934,
                55.3262116784534
            ],
            "properties": {
                "datetime": "2021-06-17T11:29:05Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "UCOM4-434S42016X419232_Nadir"
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
                    14016.0,
                    20544.0
                ],
                "direction": "nadir",
                "estimated_accuracy": null,
                "pers:omega": -0.03834,
                "pers:phi": -0.10296,
                "pers:kappa": 179.91684,
                "pers:perspective_center": [
                    580067.02,
                    6131088.026,
                    2113.728
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    -0.999997332110076,
                    0.00145021250029302,
                    -0.00179795896349851,
                    -0.00145141295292686,
                    -0.999998724554754,
                    0.000666550302214,
                    -0.00179699003071996,
                    0.000669158104859617,
                    0.99999816152544
                ],
                "pers:interior_orientation": {
                    "camera_id": "UCOM4-434S42016X419232_Nadir",
                    "focal_length": 79.6,
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
                        20544.0,
                        14016.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6131_580/2021_83_37_1_0022_00002248.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6131_580%2F2021_83_37_1_0022_00002248.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_37_1_0022_00002248?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6131_580%2F2021_83_37_1_0022_00002248.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6131_580/2021_83_37_1_0022_00002248.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6131_580%2F2021_83_37_1_0022_00002248.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2021_83_37_2_0022_00002248",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.271210262365193,
                            55.333436444603215
                        ],
                        [
                            10.253573883651855,
                            55.33361714049787
                        ],
                        [
                            10.250685309969922,
                            55.34629927935417
                        ],
                        [
                            10.275104370451219,
                            55.34607157310619
                        ],
                        [
                            10.271210262365193,
                            55.333436444603215
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2506853099699,
                55.3334364446032,
                10.2751043704512,
                55.3462992793542
            ],
            "properties": {
                "datetime": "2021-06-17T11:29:05Z",
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
                "pers:omega": 44.95275,
                "pers:phi": -0.18684,
                "pers:kappa": -0.14175,
                "pers:perspective_center": [
                    580066.913,
                    6131087.864,
                    2113.749
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999991622701095,
                    -0.00405476819869449,
                    0.000559805756997102,
                    0.00247398853674251,
                    0.707681803310828,
                    0.706526959601299,
                    -0.00326096739492715,
                    -0.706519655860748,
                    0.707685906298874
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6133_580/2021_83_37_2_0022_00002248.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6133_580%2F2021_83_37_2_0022_00002248.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_37_2_0022_00002248?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6133_580%2F2021_83_37_2_0022_00002248.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6133_580/2021_83_37_2_0022_00002248.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6133_580%2F2021_83_37_2_0022_00002248.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2021_83_37_4_0022_00002248",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.308227347389607,
                            55.31387749414288
                        ],
                        [
                            10.281085320575208,
                            55.31600175801174
                        ],
                        [
                            10.281345040940748,
                            55.32288826850448
                        ],
                        [
                            10.308714756411497,
                            55.324298011512425
                        ],
                        [
                            10.308227347389607,
                            55.31387749414288
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2810853205752,
                55.3138774941429,
                10.3087147564115,
                55.3242980115124
            ],
            "properties": {
                "datetime": "2021-06-17T11:29:05Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "UCOM4-434S42016X419232_UC-Op-Right"
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
                "pers:omega": -0.09909,
                "pers:phi": -45.08874,
                "pers:kappa": -90.07578,
                "pers:perspective_center": [
                    580066.835,
                    6131087.941,
                    2113.749
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    -0.000933776980907945,
                    -0.999999249786403,
                    0.000792771834499172,
                    0.706010145365614,
                    -9.78137248850333e-05,
                    0.708201712136662,
                    -0.708201103290142,
                    0.00122100741474933,
                    0.706009707043408
                ],
                "pers:interior_orientation": {
                    "camera_id": "UCOM4-434S42016X419232_UC-Op-Right",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6131_582/2021_83_37_4_0022_00002248.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6131_582%2F2021_83_37_4_0022_00002248.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_37_4_0022_00002248?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6131_582%2F2021_83_37_4_0022_00002248.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6131_582/2021_83_37_4_0022_00002248.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6131_582%2F2021_83_37_4_0022_00002248.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2021_83_37_1_0022_00002247",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.277877336238065,
                            55.30840175108965
                        ],
                        [
                            10.245284639661035,
                            55.308857627725786
                        ],
                        [
                            10.245813541702546,
                            55.32148285418071
                        ],
                        [
                            10.27836602610349,
                            55.32112286796883
                        ],
                        [
                            10.277877336238065,
                            55.30840175108965
                        ]
                    ]
                ]
            },
            "bbox": [
                10.245284639661,
                55.3084017510896,
                10.2783660261035,
                55.3214828541807
            ],
            "properties": {
                "datetime": "2021-06-17T11:29:00Z",
                "gsd": 0.1,
                "license": "various",
                "platform": "Fixed-wing aircraft",
                "instruments": [
                    "UCOM4-434S42016X419232_Nadir"
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
                    14016.0,
                    20544.0
                ],
                "direction": "nadir",
                "estimated_accuracy": null,
                "pers:omega": -0.04914,
                "pers:phi": -0.09189,
                "pers:kappa": 179.90685,
                "pers:perspective_center": [
                    580072.49,
                    6130563.23,
                    2114.315
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    -0.999997392371359,
                    0.00162439739445886,
                    -0.00160517400502857,
                    -0.00162577139119917,
                    -0.999998312880292,
                    0.000855046169958005,
                    -0.00160378236213725,
                    0.000857653586290395,
                    0.999998346154863
                ],
                "pers:interior_orientation": {
                    "camera_id": "UCOM4-434S42016X419232_Nadir",
                    "focal_length": 79.6,
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
                        20544.0,
                        14016.0
                    ]
                },
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6130_580/2021_83_37_1_0022_00002247.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_1_0022_00002247.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_37_1_0022_00002247?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_1_0022_00002247.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6130_580/2021_83_37_1_0022_00002247.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6130_580%2F2021_83_37_1_0022_00002247.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "id": "2021_83_37_2_0022_00002247",
            "collection": "skraafotos2021",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            10.271142754623119,
                            55.32871559210943
                        ],
                        [
                            10.253502769962937,
                            55.32890875248057
                        ],
                        [
                            10.250624885178226,
                            55.34157860443118
                        ],
                        [
                            10.275042187420224,
                            55.34135493360484
                        ],
                        [
                            10.271142754623119,
                            55.32871559210943
                        ]
                    ]
                ]
            },
            "bbox": [
                10.2506248851782,
                55.3287155921094,
                10.2750421874202,
                55.3415786044312
            ],
            "properties": {
                "datetime": "2021-06-17T11:29:00Z",
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
                "pers:omega": 44.94195,
                "pers:phi": -0.18585,
                "pers:kappa": -0.15597,
                "pers:perspective_center": [
                    580072.383,
                    6130563.068,
                    2114.336
                ],
                "pers:crs": 25832,
                "pers:vertical_crs": 5799,
                "pers:rotation_matrix": [
                    0.999991034090373,
                    -0.00421812668377324,
                    0.000373022984083673,
                    0.00272217235148383,
                    0.707813973048701,
                    0.706393636250144,
                    -0.00324368872671709,
                    -0.706386287355786,
                    0.70781910932042
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6132_580/2021_83_37_2_0022_00002247.tif?token={DinToken}",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6132_580%2F2021_83_37_2_0022_00002247.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021/items/2021_83_37_2_0022_00002247?token={DinToken}"
                },
                {
                    "rel": "parent",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "collection",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2021?token={DinToken}"
                },
                {
                    "rel": "root",
                    "type": "application/json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/?token={DinToken}"
                },
                {
                    "rel": "license",
                    "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                    "type": "text/html; charset=UTF-8",
                    "title": "SDFE license terms"
                },
                {
                    "rel": "alternate",
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6132_580%2F2021_83_37_2_0022_00002247.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2021/10km_613_58/1km_6132_580/2021_83_37_2_0022_00002247.tif?token={DinToken}",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2021%2F10km_613_58%2F1km_6132_580%2F2021_83_37_2_0022_00002247.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token={DinToken}",
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
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/search?bbox=7%2C54%2C15%2C57&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&token={DinToken}&limit=10",
            "method": "GET",
            "body": null
        },
        {
            "rel": "next",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/search?bbox=7%2C54%2C15%2C57&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&token={DinToken}&limit=10&pt=PmR0OjIwMjEtMDYtMTcgMTM6Mjk6MDArMDI6MDB-czoyMDIxXzgzXzM3XzJfMDAyMl8wMDAwMjI0Nw%3D%3D",
            "method": "GET",
            "body": null
        }
    ],
    "context": {
        "returned": 10,
        "limit": 10,
        "matched": 22342
    }
}
```
</details>


## Tips og tricks
Hvis man kun ønsker skråfoto billeder fra samme årgang, så anbefales det at benytte  `/collections/{collectionid}` endpoint i stedet for `/search` endpoint.

https://api.dataforsyningen.dk/skraafotoapi_test?token={DinToken}
