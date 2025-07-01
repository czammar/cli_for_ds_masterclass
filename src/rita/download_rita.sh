# Script para descargar la base completa de RITA 
# No olvidemos darle permisos chmod +x download_rita.sh
# Ejecutamos como: ./download_rita.sh

# Direccion base para formar el url donde esta el archivo
BASE_URL="https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_"

function download_data() {
    for url in "${BASE_URL}"{2024..2025}"_"{1..12}".zip"
    do
        echo ${url}
        wget ${url} >2 /dev/null &
    done
}

download_data