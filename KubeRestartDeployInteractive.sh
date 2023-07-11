#!/bin/bash
entorno=$1
target='null'

## SI LA VARIABLE DE ENTORNO NO ESTÁ VACIA
if [ "$entorno" ]; then
  #PREPRODUCCION
  if [ $entorno == 'stg' ]; then
    entorno='staging'
    kubectx 'staging(core)'
    target=$(kubectl get -A -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' deployments | fzf)
    kubectl rollout restart deployment $target -n $entorno
    if [ $? == 0 ]; then
      echo "Reiniciado con exito el servicio ${d}"
    else
      echo "No se ha reiniciado con exito el servicio"
    fi
  elif [ $? == 1 ]; then
    echo "No se han encontrado deployments asociados en preproduccion core."
  fi
  
  #PRODUCCION
  if [ $entorno == 'pro' ]; then
    entorno='production'
    kubectx 'production(core)'
    target=$(kubectl get -A -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' deployments | fzf)
    kubectl rollout restart deployment $target -n $entorno
    if [ $? == 0 ]; then
      echo "Reiniciado con exito el servicio ${d}"
    else
      echo "No se ha reiniciado con exito el servicio"
    fi
  fi
  
  #PREPRODUCCION MANIFEST
  if [ $entorno == 'mstg' ]; then
    kubectx 'Manifest/apps(staging)'
    target=$(kubectl get -A -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' deployments | fzf)
    echo "Entorno seleccionado manifest produccion, buscando deployments con el nombre ${target}"
    kubectl rollout restart deployment $target -n $target
    if [ $? == 0 ]; then
        echo "Reiniciado con exito el servicio ${target}"
    else
        echo "No se ha reiniciado con exito el servicio"
    fi
  fi
  #PRODUCCION MANIFEST
  if [ $entorno == 'mpro' ]; then
    kubectx 'Manifest/apps(prod)'
    target=$(kubectl get -A -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' deployments | fzf)
    echo "Entorno seleccionado manifest produccion, buscando deployments con el nombre ${target}"
    kubectl rollout restart deployment $target -n $target
        if [ $? == 0 ]; then
          echo "Reiniciado con exito el servicio ${target}"
        else
          echo "No se ha reiniciado con exito el servicio"
        fi
  fi
else
  echo "USAGE: restart {stg | prod | mstg | mpro}" 
  echo "  {Environment to affect}"
fi
