# 6. Ügyféloldali beállítás
echo "### Ügyfél gépeken futtasd ezt a parancsot: ###"
echo "echo 'Acquire::http::Proxy \"http://$(hostname -I | awk '{print $1}'):3142\";' | sudo tee /etc/apt/apt.conf.d/02proxy"

# 7. Windows GPO Beállítások (útmutató)
echo -e "\n### WINDOWS GPO BEÁLLÍTÁSOK ###"
cat <<EOL
1. Nyisd meg a Csoportházirend-kezelőt (gpmc.msc)
2. Hozz létre egy új GPO-t vagy válassz egy meglévőt
3. Navigálj ide: Computer Configuration -> Policies -> Administrative Templates -> Windows Components -> Windows Update
4. Állítsd be a következő értékeket:
   - Specify intranet Microsoft update service location: Enabled
     - Set the intranet update service: http://wsus.domain.local:8530
     - Set the intranet statistics server: http://wsus.domain.local:8530
   - Configure Automatic Updates: Enabled (3 - Auto download and notify for install)
   - Automatic Updates detection frequency: Enabled (22 óra)
   - Allow non-administrators to receive update notifications: Disabled
5. Alkalmazd a szabályzatot (gpupdate /force)

Fontos: Cseréld le a "wsus.domain.local"-t a saját WSUS szervered domain nevére!
EOL

echo -e "\n### KÉSZ ###"
echo "Az APT cache elérhető a következő címen: http://$(hostname -I | awk '{print $1}'):3142"
