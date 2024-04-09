#TODO Falta agregar scrape de metricas con prometheus, seleccionar una flag si quiero instrumentación o no y generar el archivo opentelemtry y carpeta monitoring

def make(deployment, metrics_path, healthcheck_path, service_port, global_configmap, configmap, image_name, image_version,secret):
    with open(f"./{deployment}/{deployment}-deployment.yaml", "w") as f:
        f.write(
    f"""---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {deployment}
  namespace: {deployment}
  labels:
    app.kubernetes.io/name: {deployment}
spec:
  progressDeadlineSeconds: 600
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app.kubernetes.io/name: {deployment}
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  #replicas: 1
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {deployment}
        filebeat_logindex: {deployment}
        filebeat_logtype: raw
      annotations:
        linkerd.io/inject: enabled
        config.linkerd.io/proxy-cpu-limit: "1"
        config.linkerd.io/proxy-cpu-request: "0.2"
        config.linkerd.io/proxy-memory-limit: 2Gi
        config.linkerd.io/proxy-memory-request: 128Mi
        reset: "0"
        instrumentation.opentelemetry.io/inject-java: "false"
        instrumentation.opentelemetry.io/container-names: {deployment}
        prometheus.io/scrape: "true"
        prometheus.io/port: "metrics"
        prometheus.io/path: "{metrics_path}"
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app.kubernetes.io/name
                  operator: In
                  values:
                  - {deployment}
              topologyKey: kubernetes.io/hostname
      containers:
      - name: {deployment}
        image: {image_name}:{image_version}
        imagePullPolicy: Always
        resources: 
        requests:
          cpu: 200m
          memory: 128Mi
        limits:
          cpu: 1000m
          memory: 2Gi
        ports:
          - name: app
            containerPort: {service_port}
            protocol: TCP
          - name: metrics
            containerPort: 5000
            protocol: TCP
        {f"""envFrom:
        - configMapRef:
          name: kafka-global-config
        - configMapRef:
          name: mongodb-global-config {"\n        " if (configmap or secret) else ''}""" if global_configmap else ''}{f"""- secretRef:
          name: {deployment}-secret {"\n        " if (configmap or healthcheck_path) else ''}""" if secret else ''}{f"""volumeMounts:
        - name: config
          mountPath: \"/opt/ctt/config\"
          readOnly: true {"\n        " if healthcheck_path else ''}""" if configmap else ''}{f"""startupProbe:
          httpGet:
            path: {healthcheck_path} 
            port: app
          initialDelaySeconds: 30
          periodSeconds: 60
          failureThreshold: 30
          timeoutSeconds: 60
        livenessProbe:
          httpGet:
            path: {healthcheck_path}
            port: app
          failureThreshold: 1
          periodSeconds: 20
          timeoutSeconds: 5 """ if healthcheck_path else ''}
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      terminationGracePeriodSeconds: 30
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
          - all
          readOnlyRootFilesystem: true
          runAsGroup: 10000
          runAsNonRoot: true
          runAsUser: 10000
      {f"""volumes:
      - name: config
        configMap:
          name: {deployment}-service-properties""" if configmap else ''}\
""")
