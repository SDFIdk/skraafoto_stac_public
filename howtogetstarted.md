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
Hvis der kun ønskes billeder af det samme sted fra samme årgang, så anbefales det at benytte `/collections/{collectionid}/items` endpoint i stedet for `/search` endpoint, da `/search` kræver flere resourcer at udføre.
Hvis der ønskes billeder af det samme sted, på tværs af collectionerne skal der bruges `/search`.

**Samme årgang**

_Parametre_: collectionid, crs, limit, pt, ids, bbox, bbox-crs, datetime, filter, filter-lang, filter-crs,
_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)  
_Eksempel_: https://api.dataforsyningen.dk/skraafotoapi_test/collections/skraafotos2019/items?token=

**På tværs af årgange**
_Parametre_: crs, limit, pt (page*token), ids, bbox, bbox-crs, datetime, filter, filter-lang, filter-crs, collections, sortby  
_Output_: FeatureCollection (Array af STAC Items) (GeoJSON)
https://api.dataforsyningen.dk/skraafotoapi_test/search&token=

## Tips og tricks
Hvis man kun ønsker skråfoto billeder fra samme årgang, så anbefales det at benytte  `/collections/{collectionid}` endpoint i stedet for `/search` endpoint.

https://api.dataforsyningen.dk/skraafotoapi_test?token=
