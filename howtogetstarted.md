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
STAC API'et returnerer metadata om skråfoto billederne, som er inddelt i collection niveau, som hver har items i sig. I hvert `item object` som indeholder metadata om ét bestemt billede, er der også URL'er til at få returneret det billede. Man kan få returneret billede på flere forskellige måder.
Hvis der kun ønskes billeder af det samme sted fra samme årgang, så anbefales det at benytte `/collections/{collectionid}/items` endpoint i stedet for `/search` endpoint, da `/search` kræver flere resourcer at udføre.
Hvis der ønskes billeder af det samme sted, på tværs af collectionerne skal der bruges `/search`.

**Samme årgang**
Man angiver ved {collectionid} i URL pathen, hvilken collection man ønsker at fremsøge billeder fra. I dette tilfælde er det `skraafotos2019` collection. Dernæst angiver man i parameterne, i dette tilfælde ved hjælp af en bbox, hvilket geografisk område man ønsker metadata om billederne fra

_URL_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/{collectionid}/items?token={DinToken}
_Parametre_: collectionid, crs (default: http://www.opengis.net/def/crs/OGC/1.3/CRS84), limit, pt, ids, bbox, bbox-crs (default: http://www.opengis.net/def/crs/EPSG/0/25832), datetime, filter, filter-lang, filter-crs,
_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?bbox=7,54,15,57&bbox-crs=http://www.opengis.net/def/crs/OGC/1.3/CRS84&token={DinToken}
_Response_:
<details>
``` json
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001110.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001110.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0046_00001110?token=4adf32524ae6d6998565f638a1090ba1"
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
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001110.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0046_00001110.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0046_00001110.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000900.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000900.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0047_00000900?token=4adf32524ae6d6998565f638a1090ba1"
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
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000900.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000900.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000900.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000899.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000899.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0047_00000899?token=4adf32524ae6d6998565f638a1090ba1"
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
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000899.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000899.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000899.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000898.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000898.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0047_00000898?token=4adf32524ae6d6998565f638a1090ba1"
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
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000898.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000898.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000898.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000897.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000897.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0047_00000897?token=4adf32524ae6d6998565f638a1090ba1"
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
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000897.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6130_580/2019_83_37_2_0047_00000897.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6130_580%2F2019_83_37_2_0047_00000897.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_580/2019_83_37_2_0047_00000896.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0047_00000896.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0047_00000896?token=4adf32524ae6d6998565f638a1090ba1"
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
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0047_00000896.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_580/2019_83_37_2_0047_00000896.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_580%2F2019_83_37_2_0047_00000896.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
                "asset:data": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_581/2019_83_37_2_0048_00000895.tif?token=4adf32524ae6d6998565f638a1090ba1",
                "asset:thumbnail": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_581%2F2019_83_37_2_0048_00000895.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1"
            },
            "links": [
                {
                    "rel": "self",
                    "type": "application/geo+json",
                    "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items/2019_83_37_2_0048_00000895?token=4adf32524ae6d6998565f638a1090ba1"
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
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/viewer.html?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_581%2F2019_83_37_2_0048_00000895.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "text/html; charset=UTF-8",
                    "title": "Interactive image viewer"
                }
            ],
            "assets": {
                "data": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_server_test/COG_oblique_2019/10km_613_58/1km_6131_581/2019_83_37_2_0048_00000895.tif?token=4adf32524ae6d6998565f638a1090ba1",
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                    "roles": [
                        "data"
                    ],
                    "title": "Raw tiff file"
                },
                "thumbnail": {
                    "href": "https://api.dataforsyningen.dk/skraafoto_cogtiler_test/thumbnail.jpg?url=https%3A%2F%2Fapi.dataforsyningen.dk%2Fskraafoto_server_test%2FCOG_oblique_2019%2F10km_613_58%2F1km_6131_581%2F2019_83_37_2_0048_00000895.tif%3Ftoken%3D4adf32524ae6d6998565f638a1090ba1&token=4adf32524ae6d6998565f638a1090ba1",
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
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?bbox=7%2C54%2C15%2C57&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&token=4adf32524ae6d6998565f638a1090ba1&limit=10",
            "method": "GET",
            "body": false
        },
        {
            "rel": "next",
            "type": "application/geo+json",
            "href": "https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?bbox=7%2C54%2C15%2C57&bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FOGC%2F1.3%2FCRS84&token=4adf32524ae6d6998565f638a1090ba1&limit=10&pt=PmR0OjIwMTktMDctMTAgMTE6MDM6MzIrMDI6MDB-czoyMDE5XzgzXzM3XzJfMDA0OF8wMDAwMDg5NQ%3D%3D",
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
_Parametre_: crs, limit, pt (page*token), ids, bbox, bbox-crs, datetime, filter, filter-lang, filter-crs, collections, sortby  
_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)
https://api.dataforsyningen.dk/skraafotoapi_test/search&token={DinToken}

## Tips og tricks
Hvis man kun ønsker skråfoto billeder fra samme årgang, så anbefales det at benytte  `/collections/{collectionid}` endpoint i stedet for `/search` endpoint.

https://api.dataforsyningen.dk/skraafotoapi_test?token={DinToken}
