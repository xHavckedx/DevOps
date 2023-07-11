#!/bin/bash
for n in $(kubectl get -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' namespaces); do 
  for d in $(kubectl get -n $n -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' deployments); do 
    kubectl rollout restart deployment/$d -n $n
  done
  echo $n
done
