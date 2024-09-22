# Tavaroiden hallintajärjestelmä

## Sovelluksen tilanne
Sovelluksella voi katsella luotuja kategorioita ja päätasolle voi luoda uusia kategorioita.
Järjestelmää voi testata osoitteessa https://item-management-system.fly.dev/

## Käynnistysohjeet paikallisen version käyttämiseen
Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
DATABASE_URL=<tietokannan-paikallinen-osoite>

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```
Määritä vielä tietokannan skeema komennolla
```
$ psql < schema.sql
```
Nyt voit käynnistää sovelluksen komennolla
```
$ flask run
```

## Tavoitteet
Sovelluksella voi hallita tavaroiden luokittelujärjestelmää, johon voidaan tallentaa tavaroiden sijaintipaikkoja. Järjestelmällä voidaan käsitellä myös tavaroiden luokitteluun ja sijaintiin liittyviä tehtäviä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Järjestelmän toimintaan liittyvät termit, joita käytetään tässä dokumentissa:
- **kategoriat** - Määrittelee mihin kategorioihin tavarat jaetaan. Kategoriat voivat sisältää alakategorioita, muodostaen puumaisen rakenteen. Esim. _kierteelliset - ruuvit - kateruuvit_.
- **paikat** - Fyysisiä paikkoja joihin tavaroita on mahdollista sijoittaa. Paikat voivat sisältää osinaan toisia paikkoja. Esim. _kiinteistö - rakennus - rakennuksen osa - huone - kaappi_.
- **tavaroiden sijainnit** - Kertoo missä paikoissa jonkin kategorian tavaroita on.

Sovelluksen ominaisuuksia:
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä voi hakea merkkijonoa. Sovellus näyttää tavaroiden kategoriat, paikat ja tavaroiden sijainnit, joista annettu merkkijono löytyy.
- Käyttäjä voi tallentaa järjestelmään tavaroihin liittyvän tehtävän. Käyttäjä voi valita kategorian, paikan tai tavaran sijainnin, johon tehtävä liittyy, mutta se ei ole pakollista. Käyttäjälle tarjotaan myös mahdollisuus valita jokin usein käytetty toimenpide, joka määrittelee tehtävän tyypin. Käyttäjä voi luoda myös vapaamuotoisen tehtäväviestin.
  - Usein käytettyjä toimenpiteitä ovat esimerkiksi: tavaran sijainnin tiedustelu, kysely mihin kategoriaan tavara kuuluu, kategorian jakaminen, kategorian muutos, virheellinen sijainti ja suurempi tilan tarve.
- Käyttäjä voi nähdä luomansa tehtävät luokiteltuna käsittelemättömiin ja käsiteltyihin.
- Ylläpitäjä voi lisätä, poistaa ja muuttaa kategorioita, paikkoja ja tavaroiden sijainteja.
- Ylläpitäjä voi merkitä tehtävän käsitellyksi ja lisätä siihen kommentin, joka näkyy tehtävän lisänneelle käyttäjälle.
