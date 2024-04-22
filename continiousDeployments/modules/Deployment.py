def generate_deployment_manifest(args):
    deployment_manifest = f"""
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: {args.deployment}
      namespace: {args.deployment}
      labels:
        app.kubernetes.io/name: {args.deployment}
    spec:
      progressDeadlineSeconds: 600
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          app.kubernetes.io/name: {args.deployment}
      strategy:
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 25%
        type: RollingUpdate
      template:
        metadata:
          labels:
            app.kubernetes.io/name: {args.deployment}
            filebeat_logindex: {args.deployment}
            filebeat_logtype: raw
          annotations:
            linkerd.io/inject: enabled
            config.linkerd.io/proxy-cpu-limit: "1"
            config.linkerd.io/proxy-cpu-request: "0.2"
            config.linkerd.io/proxy-memory-limit: 2Gi
            config.linkerd.io/proxy-memory-request: 128Mi
            reset: "0"
            instrumentation.opentelemetry.io/inject-java: "false"
            instrumentation.opentelemetry.io/container-names: {args.deployment}
            prometheus.io/scrape: "true"
            prometheus.io/port: "metrics"
            prometheus.io/path: "{args.metrics_path}"
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
                      - {args.deployment}
                  topologyKey: kubernetes.io/hostname
          containers:
          - name: {args.deployment}
            image: {args.image_name}:{args.image_version}
            imagePullPolicy: Always
            resources: 
            requests:
              cpu: 200m
              memory: 128Mi
            limits:
              cpu: 1000m
              memory: 2Gi
            env:
              - name: MY_CPU_REQUEST
                valueFrom:
                  resourceFieldRef:
                    containerName: {args.deployment}
                    resource: requests.cpu
              - name: MY_CPU_LIMIT
                valueFrom:
                  resourceFieldRef:
                    containerName: {args.deployment}
                    resource: limits.cpu
              - name: MY_MEM_REQUEST
                valueFrom:
                  resourceFieldRef:
                    containerName: {args.deployment}
                    resource: requests.memory
              - name: MY_MEM_LIMIT
                valueFrom:
                  resourceFieldRef:
                    containerName: {args.deployment}
                    resource: limits.memory
            ports:
              - name: app
                containerPort: {args.service_port}
                protocol: TCP
              - name: metrics
                containerPort: 5000
                protocol: TCP
            {generate_env_from_configmap(args)}
            {generate_env_from_secret(args)}\
            {generate_volume_mounts(args)}
            {generate_startup_probe(args)}
            {generate_liveness_probe(args)}
          {generate_outbox_sidecar(args)}
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
          {generate_volumes(args)}\ """
    return deployment_manifest

def generate_env_from_configmap(args):
  gc = """envFrom:
            - configMapRef:
              name: kafka-global-config
            - configMapRef:
              name: mongodb-global-config"""
  
  if args.global_configmap:
    return gc
  else:
    return ''

def generate_env_from_secret(args):
  secret = f"""- secretRef:
              name: {args.deployment}-secret"""
  if args.global_configmap and args.secret:
    if args.configmap:
      return f"""{secret}\n"""
    return secret
  elif args.secret:
    if args.configmap:
      return f"""envFrom:
            {secret}\n"""
    return f"""envFrom:
            {secret}"""
  else:
    return ''

def generate_volume_mounts(args):
    volumeMount = f"""volumeMounts:
              - name: config
                mountPath: \"/opt/ctt/config\"
                readOnly: true """
    if args.configmap:
      return volumeMount
    else:
      return ''

def generate_startup_probe(args):
    startUpProbe= f"""startupProbe:
              httpGet:
                path: {args.healthcheck_path} 
                port: app
              initialDelaySeconds: 30
              periodSeconds: 60
              failureThreshold: 30
              timeoutSeconds: 60"""
    return startUpProbe if args.healthcheck_path else ''

def generate_liveness_probe(args):
    livenessProbe = f"""livenessProbe:
              httpGet:
                path: {args.healthcheck_path}
                port: app
              failureThreshold: 1
              periodSeconds: 20
              timeoutSeconds: 5"""
    return livenessProbe if args.healthcheck_path else ''
def generate_outbox_sidecar(args):
    outbox = f"""- name: outbox-sidecar
            image: {f"""232430620857.dkr.ecr.eu-west-1.amazonaws.com""" if args.environment == 'stg' else '339394754229.dkr.ecr.eu-central-1.amazonaws.com'}/shein-notifications-sidecar:latest
            envFrom:
            - configMapRef:
                name: mongodb-global-config
            - secretRef:
                name: external-secret-mongodb
            - secretRef:
                name: external-secret-outbox
            env:
            - name: ASPNETCORE_URLS
              value: "http://*:3001"
            - name: MONGODB_USERNAME
              value: "$(MONGO_DB_USER)"
            - name: MONGODB_PASSWORD
              value: "$(MONGO_DB_PASSWORD)"
            - name: MONGODB_DATABASE
              value: "$(MONGO_DB_DATABASE)"
            - name: MONGODB_URI
              value: "$(MONGO_DB_HOST1)"
            ports:
            - name: outbox
              containerPort: 3001
              protocol: TCP
            resources:
              requests:
                cpu: 50m
                memory: 200Mi
              limits:
                cpu: 200m
                memory: 600Mi
            startupProbe:
              httpGet:
                path: /health
                port: outbox
              initialDelaySeconds: 30
              periodSeconds: 60
              failureThreshold: 30
              timeoutSeconds: 60
            livenessProbe:
              httpGet:
                path: /health
                port: outbox
              failureThreshold: 1
              periodSeconds: 20
              timeoutSeconds: 5"""
    return outbox if args.outbox else ''

def generate_volumes(args):
    volume = f"""volumes:
          - name: config
            configMap:
              name: {args.deployment}-service-properties"""
    if args.configmap:
      return volume
    else:
      return ''

def make(args):
    deployment_manifest = generate_deployment_manifest(args)
    with open(f"./{args.deployment}/{args.deployment}-deployment.yaml", "w") as f:
        f.write(deployment_manifest)