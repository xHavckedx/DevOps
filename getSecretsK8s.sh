#!/bin/bash

# Obtener la lista de namespaces
namespaces=$(kubectl get namespaces -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}')

# Recorrer cada namespace
for namespace in $namespaces; do
    echo "Namespace: $namespace"
    # Obtener la lista de secretos en el namespace actual
    secrets=$(kubectl get secrets -n $namespace -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}')
    
    # Recorrer cada secreto
    for secret in $secrets; do
        # Obtener los datos del secreto
        secret_data=$(kubectl get secret $secret -n $namespace -o jsonpath='{.data}')
        # Decodificar y buscar el valor específico
        decoded_data=$(echo $secret_data | base64 -d)
        if echo "$decoded_data" | grep -q "DB_HOST"; then
            echo "   Secret: $secret"
        fi
    done
done

