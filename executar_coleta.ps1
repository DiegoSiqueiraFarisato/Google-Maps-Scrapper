$queries = @(
    # --- MILANO & LOMBARDIA ---
    'py main.py -s "Ristoranti a Milano Italia" -t 40',
    'py main.py -s "Bar e Caffetterie a Milano Italia" -t 40',
    'py main.py -s "Pizzerie a Milano Italia" -t 40',
    'py main.py -s "Software house a Milano Italia" -t 50',
    'py main.py -s "Agenzie di comunicazione e marketing a Milano Italia" -t 40',
    'py main.py -s "Studi legali e avvocati a Milano Italia" -t 30',
    'py main.py -s "Commercialisti e consulenti a Milano Italia" -t 30',
    'py main.py -s "Aziende di logistica e trasporti a Milano Italia" -t 40',
    'py main.py -s "Ristoranti e Trattorie a Brescia Italia" -t 30',
    'py main.py -s "Officine meccaniche e carpenterie a Brescia Italia" -t 40',
    'py main.py -s "Software house e IT consulting a Brescia Italia" -t 30',
    'py main.py -s "Ristoranti e Trattorie a Cremona Italia" -t 30',
    'py main.py -s "Aziende agricole e agriturismi a Cremona Italia" -t 30',
    'py main.py -s "Ristoranti e Pizzerie a Bergamo Italia" -t 30',
    'py main.py -s "Aziende manifatturiere e industriali a Bergamo Italia" -t 40',

    # --- ROMA & LAZIO ---
    'py main.py -s "Ristoranti e Trattorie a Roma Italia" -t 50',
    'py main.py -s "Bar e Cocktail Bar a Roma Italia" -t 40',
    'py main.py -s "Pizzerie a Roma Italia" -t 50',
    'py main.py -s "Studi legali a Roma Italia" -t 40',
    'py main.py -s "Commercialisti e revisori a Roma Italia" -t 30',
    'py main.py -s "Software house e consulenza informatica a Roma Italia" -t 40',
    'py main.py -s "Agenzie di marketing e pubblicita a Roma Italia" -t 30',
    'py main.py -s "Hotel e alberghi a Roma Italia" -t 50',
    'py main.py -s "Aziende agricole e frantoi nel Lazio Italia" -t 40',

    # --- TORINO & PIEMONTE ---
    'py main.py -s "Ristoranti e Trattorie a Torino Italia" -t 40',
    'py main.py -s "Caffetterie e Bar a Torino Italia" -t 30',
    'py main.py -s "Studi legali e avvocati a Torino Italia" -t 30',
    'py main.py -s "Commercialisti a Torino Italia" -t 30',
    'py main.py -s "Software house e sviluppo software a Torino Italia" -t 40',
    'py main.py -s "Aziende automotive e meccanica a Torino Italia" -t 40',
    'py main.py -s "Cantine vinicole e aziende agricole nelle Langhe Piemonte Italia" -t 40',

    # --- BOLOGNA & EMILIA-ROMAGNA ---
    'py main.py -s "Ristoranti e Osterie a Bologna Italia" -t 40',
    'py main.py -s "Bar e Pub a Bologna Italia" -t 30',
    'py main.py -s "Software house e soluzioni IT a Bologna Italia" -t 40',
    'py main.py -s "Commercialisti e studi tributari a Bologna Italia" -t 30',
    'py main.py -s "Aziende agricole e produttori alimentari in Emilia-Romagna Italia" -t 50',
    'py main.py -s "Aziende di logistica e spedizioni a Parma Italia" -t 30',
    'py main.py -s "Aziende meccaniche e automazione a Modena Italia" -t 40',

    # --- FIRENZE & TOSCANA ---
    'py main.py -s "Ristoranti e Trattorie a Firenze Italia" -t 40',
    'py main.py -s "Caffetterie e Lounge Bar a Firenze Italia" -t 30',
    'py main.py -s "Hotel e Resort a Firenze Italia" -t 40',
    'py main.py -s "Cantine vinicole e tenute nel Chianti Toscana Italia" -t 50',
    'py main.py -s "Aziende agricole e produzione olio Toscana Italia" -t 40',
    'py main.py -s "Studi di architettura e design a Firenze Italia" -t 30',

    # --- VENETO (VERONA, PADOVA, VENEZIA) ---
    'py main.py -s "Ristoranti e Pizzerie a Verona Italia" -t 30',
    'py main.py -s "Cantine vinicole in Valpolicella Verona Italia" -t 40',
    'py main.py -s "Aziende di logistica e magazzinaggio a Verona Italia" -t 40',
    'py main.py -s "Software house e consulenza IT a Padova Italia" -t 30',
    'py main.py -s "Ristoranti e Trattorie a Padova Italia" -t 30',
    'py main.py -s "Ristoranti e Osterie a Venezia Italia" -t 40',
    'py main.py -s "Hotel e boutique hotel a Venezia Italia" -t 40',

    # --- NAPOLI & CAMPANIA ---
    'py main.py -s "Pizzerie e Ristoranti a Napoli Italia" -t 50',
    'py main.py -s "Bar e Pasticcerie a Napoli Italia" -t 30',
    'py main.py -s "Agenzie di marketing e e-commerce a Napoli Italia" -t 30',
    'py main.py -s "Studi legali a Napoli Italia" -t 30',
    'py main.py -s "Hotel e strutture ricettive a Salerno Campania Italia" -t 30',
    'py main.py -s "Aziende agricole e conserviere in Campania Italia" -t 40',

    # --- GENOVA & LIGURIA ---
    'py main.py -s "Ristoranti di pesce e Trattorie a Genova Italia" -t 30',
    'py main.py -s "Spedizionieri e logistica portuale a Genova Italia" -t 40',
    'py main.py -s "Software house e consulenza IT a Genova Italia" -t 30',

    # --- PALERMO, CATANIA & SICILIA ---
    'py main.py -s "Ristoranti e Trattorie a Palermo Italia" -t 40',
    'py main.py -s "Bar e Pasticcerie a Palermo Italia" -t 30',
    'py main.py -s "Ristoranti e Pizzerie a Catania Italia" -t 30',
    'py main.py -s "Aziende agricole e agrumeti in Sicilia Italia" -t 40',
    'py main.py -s "Cantine vinicole dell Etna Sicilia Italia" -t 30',

    # --- BARI & PUGLIA ---
    'py main.py -s "Ristoranti e Trattorie di pesce a Bari Italia" -t 40',
    'py main.py -s "Aziende agricole e frantoi in Puglia Italia" -t 50',
    'py main.py -s "Masserie e Agriturismi in Puglia Italia" -t 40',
    'py main.py -s "Software house e centri IT a Bari Italia" -t 30'
)
foreach ($q in $queries) {
    cmd /c "echo y | $q"
}