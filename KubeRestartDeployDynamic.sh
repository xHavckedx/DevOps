#!/bin/bash
entorno=$1
app=$2
count=0

#PREPRODUCCION
if [ $entorno == 'stg' ]; then
  entorno='staging'
  kubectx 'staging(core)'
  echo "Entorno seleccionado staging, buscando deployments con el nombre ${app}"
  for d in $(kubectl get -n staging -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' deployments); do
    #DEBUGGING
    #let count++
    #echo "${count} ${d}"
    if [[ $d == *"$app"* ]]; then
      echo "Deployment encontrado ${d}"
      kubectl rollout restart deployment $d -n $entorno
      if [ $? == 0 ]; then
        echo "Reiniciado con exito el servicio ${d}"
      else
        echo "No se ha reiniciado con exito el servicio"
      fi
    fi
   done
elif [ $? == 1 ]; then
  echo "No se han encontrado deployments asociados en preproduccion core."
fi

#PRODUCCION
if [ $entorno == 'pro' ]; then
  entorno='production'
  kubectx 'production(core)'
  echo "Entorno seleccionado produccion, buscando deployments con el nombre ${app}"
  for d in $(kubectl get -n production -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' deployments); do
    #DEBUGGING
    #let count++
    #echo "${count} ${d}"
    if [[ $d == *"$app"* ]]; then
      echo "Deployment encontrado ${d}"
      kubectl rollout restart deployment $d -n $entorno
      if [ $? == 0 ]; then
        echo "Reiniciado con exito el servicio ${d}"
      else
        echo "No se ha reiniciado con exito el servicio"
      fi
    #else
     # echo "No se han encontrado deployments asociados en production core"
    fi
   done
fi

#PREPRODUCCION MANIFEST
if [ $entorno == 'mstg' ]; then
  kubectx 'Manifest/apps(staging)'
  echo "Entorno seleccionado manifest staging, buscando deployments con el nombre ${app}"
  for d in $(kubectl get -A -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' deployments); do
    #DEBUGGING
    #let count++
    #echo "${count} ${d}"
    if [[ $d == *"$app"* ]]; then
      echo "Deployment encontrado ${d}"
      kubectl rollout restart deployment $d -n $d
      if [ $? == 0 ]; then
        echo "Reiniciado con exito el servicio ${d}"
      else
        echo "No se ha reiniciado con exito el servicio"
      fi
    #else
      #echo "No se han encontrado deployments asociados en manifest staging"
    fi
   done
fi

#PRODUCCION MANIFEST
if [ $entorno == 'mpro' ]; then
  kubectx 'Manifest/apps(prod)'
  echo "Entorno seleccionado manifest produccion, buscando deployments con el nombre ${app}"
  for d in $(kubectl get -A -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' deployments); do
    #DEBUGGING
    #let count++
    #echo "${count} ${d}"
    if [[ $d == *"$app"* ]]; then
      echo "Deployment encontrado ${d}"
      kubectl rollout restart deployment $d -n $d
      if [ $? == 0 ]; then
        echo "Reiniciado con exito el servicio ${d}"
      else
        echo "No se ha reiniciado con exito el servicio"
      fi
    #else
      #echo "No se han encontrado deployments asociados en manifest produccion."
    fi
   done
fi
