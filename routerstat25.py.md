Grafikus felület:

A tkinter könyvtár segítségével létrehoztunk egy egyszerű grafikus felületet.

A felület tartalmaz egy táblázatot az eredmények megjelenítésére és egy grafikont a csomagvesztés statisztikák ábrázolására.

Tracert futtatása:

A run_tracert függvény a Windows tracert parancsot használja a hopok nyomon követésére.

Csomagvesztés számítása:

A calculate_packet_loss függvény a tracert kimenetét elemezi, és kiszámítja a csomagvesztés százalékos arányát.

Eredmények megjelenítése:

Az eredmények egy pandas DataFrame-be kerülnek, majd megjelenítésre kerülnek a felületen.

Grafikon:

A matplotlib segítségével a csomagvesztés statisztikákat ábrázoljuk a felületen.

Futtatás
Telepítsd a szükséges Python csomagokat:

bash
Copy
pip install pandas matplotlib
Futtasd a szkriptet:

bash
Copy
python traceroute_gui.py
Megjegyzések
A szkript jelenleg csak az első 10 IP címet teszteli minden tartományból. Ezt módosíthatod a generate_ips_from_range függvényben.

Ha pontosabb IP cím generálásra van szükséged, használhatod a ipaddress modult.
