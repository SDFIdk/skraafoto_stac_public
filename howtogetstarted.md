Eksempler på fulde use cases i kode (fra bbox til billede på skærmen)
Til udvikleren uden det avancerede behov
"Jeg har en koordinat i hånden, hvordan får jeg vist et billede af stedet"-opskrift
Hvis man altid ønsker billeder fra 2021, så gå på den collection i stedet for ”/search”, da den er tungere rent database
Hvordan får man vist et billede, hente som COG, thumbnail eller vieweren, og at man går igennem metadataen først.

# Skraafoto-stac-api - How to get started

## Introduktion

Guiden er en hurtig gennemgang af, hvordan man får skråfoto billeder for et bestemt geografisk område ved hjælp af koordinater.

## Authentication
Der skal altid anvendes token, når der benyttes Dataforsyningens services. Du kan oprette og administrere dine tokens {tag guiden som supporterne sender til brugere) på Dataforsyningens hjemmeside.
https://dataforsyningen.dk/news/3808

## Tips og tricks
Hvis man kun ønsker skråfoto billeder fra samme årgang, så anbefales det at benytte  `/collections/{collectionid}` endpoint i stedet for `/search` endpoint.

https://api.dataforsyningen.dk/skraafotoapi_test/?token=
