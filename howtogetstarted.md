Eksempler på fulde use cases i kode (fra bbox til billede på skærmen)
Til udvikleren uden det avancerede behov
"Jeg har en koordinat i hånden, hvordan får jeg vist et billede af stedet"-opskrift
Hvis man altid ønsker billeder fra 2021, så gå på den collection i stedet for ”/search”, da den er tungere rent database
Hvordan får man vist et billede, hente som COG, thumbnail eller vieweren, og at man går igennem metadataen først.

# Skraafoto-stac-api - How to get started

## Introduktion

Guiden er en hurtig gennemgang af, hvordan man får et skråfoto billeder af et bestemt koordinat.
Hvis man kun ønsker skråfoto billeder fra samme årgang, så anbefales det at benytte  `/collections/{collectionid}` endpointet i stedet for `/search`.

https://api.dataforsyningen.dk/skraafotoapi_test/?token=

Der skal altid benyttes token for at benytte API'erne