def make(deployment, database, env):
  with open(f"./{deployment}/monitoring/{deployment}-mongodb-database-exporter-deployment.yaml", "w") as f:
        f.write(f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus-mongodb-exporter
  labels:
    app.kubernetes.io/name: prometheus-mongodb-exporter
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: prometheus-mongodb-exporter
  template:
    metadata:
      labels:
        app.kubernetes.io/name: prometheus-mongodb-exporter
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "metrics"
    spec:
      containers:
      - name: mongodb-exporter
        env:
        - name: MONGO_USERNAME
          valueFrom:
            secretKeyRef:
              name: external-secret-mongodb
              key: MONGODB_USERNAME
        - name: MONGO_PASSWORD
          valueFrom:
            secretKeyRef:
              name: external-secret-mongodb
              key: MONGODB_PASSWORD
        - name: MONGODB_URI
          value: mongodb+srv://$(MONGO_USERNAME):$(MONGO_PASSWORD)@{'production' if env == 'pro' else 'preproduction'}.3ewev.mongodb.net/{database}?ssl=true&retryWrites=true&w=majority
        image: percona/mongodb_exporter:0.37.0
        imagePullPolicy: IfNotPresent
        args:
        - --web.listen-address=:9216
        - --collector.dbstats
        - --discovering-mode
        - --no-mongodb.direct-connect
        - --mongodb.collstats-colls=manifest-file.*
        - --mongodb.indexstats-colls=manifest-file.*
        - --compatible-mode
        ports:
        - name: metrics
          containerPort: 9216
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /
            port: metrics
          initialDelaySeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: metrics
          initialDelaySeconds: 10
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - all
          readOnlyRootFilesystem: true
          runAsGroup: 10000
          runAsNonRoot: true
          runAsUser: 10000
      terminationGracePeriodSeconds: 30
""")