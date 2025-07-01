# Obtiene un lista de todos los placeholders en los templates
grep -o '{{[^}]*}}' ./*.txt | sed 's/[{}]//g'