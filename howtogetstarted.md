# Skråfoto STAC API - How to get started

## Introduktion

Guiden er en hurtig gennemgang af, hvordan man får skråfotos for et bestemt geografisk område ved hjælp af koordinater.

## Sammenspillet mellem de tre API'er

- **Skåfoto STAC API** leverer metadata om skråfotos. Dens URL starter med `https://api.dataforsyningen.dk/skraafoto_api`, men for at bruge URL'en er det et krav, at der bliver specificeret paths og query parameters.
- **Skåfoto Server** leverer skråfotos som [Cloud Optimized Geotiff](https://www.cogeo.org) (`COG`), hvor der kan bruges range request. Dens URL starter med `https://api.dataforsyningen.dk/skraafoto_server`, men for at bruge URL'en er det et krav, at der bliver specificeret paths og query parameters.
- **Skråfoto Cogtiler** oversætter COG-formatet til JPG, der ikke understøtter COG, se mere i afsnittet [Download og visning af billeder](#download-og-visning-af-billeder). Dens URL starter med `https://api.dataforsyningen.dk/skraafoto_cogtiler`, men for at bruge URL'en er det et krav, at der bliver specificeret paths og query parameters. Cogtilers openapi dokumentation findes [her](#skraafoto_cogtiler).

<table class="center" style="width:100%">
  <tr>
     <th>For klienter med understøttelse af COGs</th>
     <th>Klienter UDEN COG support</th>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/SDFIdk/skraafoto_stac_public/main/media/Skr%C3%A5fotodistribution-HTTPServer.svg" alt="For klienter med understøttelse af COGs" style="max-width: 70%; max-height: 70%;"></td>
    <td><img src="https://raw.githubusercontent.com/SDFIdk/skraafoto_stac_public/main/media/Skr%C3%A5fotodistribution-TileServer.svg" alt="Klienter UDEN COG support" style="max-width: 100%; max-height: 100%;"></td>
  </tr>
 </table>

### Eksempel 1

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

### Eksempel 2

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

## Håndtering af collections

**Vigtig optimering af søgninger**

Hvis der kun ønskes billeder af det samme sted fra samme årgang, så anbefales det at benytte `/collections/{collectionid}/items` endpoint i stedet for `/search` endpoint, da `/search` kræver flere resourcer at udføre.
Hvis der ønskes billeder af det samme sted, på tværs af collections skal der bruges `/search`.

**STAC Item**

Hvert skråfoto har et `Item` objekt tilknyttet, som indeholder metadata for det. Mere om [STAC Item](#stac-item).

### Samme årgang

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

I dette tilfælde er det `skraafotos2019` collection. Dernæst angives query parameterne. Her er det parameteren `bbox` med værdierne `10.3285,55.3556,10.4536,55.4132`, som beskriver hvilket geografisk område, der ønskes metadata om billederne fra. I dette eksempel er `bbox` i projektion `http://www.opengis.net/def/crs/OGC/1.3/CRS84`, hvilket bliver angivet i `bbox-crs` parameteren. Limit er sat til 3, så hvis der er et match mellem den koordinaterne for den angivne `bbox` og metadata for skåfotos, vil JSON response indeholde tre `Items` objekter. I `context` objektet er attributterne `Returned`, `Limit` og `Matched`, der kan læses mere om på [dokumentation](https://github.com/Dataforsyningen/skraafoto_stac_public/blob/main/dokumentation.md#context-extension), hvor det også er forklaret hvordan paging fungerer.

### På tværs af årgange

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