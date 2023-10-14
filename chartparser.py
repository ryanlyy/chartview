import yaml

chartAllRoot = "./work/templates/"
chartDirRoot = "./work/templates/reg-helm-charts/charts/"
chartFile = chartAllRoot +  "udm-helm-chart.yaml"

#arpf  ccasapache  clustermonitoragent  commonudm  crdbredisio  debugassist  ee  http2lb  lcm  mt  nidd  nim  pp  sdm  servicemesh  sidf  sim  sor  tcpproxy  trigger  udmueauth  ueauthn  uecm  upu  vnfclusterenvoylb

'''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: release-name-udmarpf
  namespace: default
  labels:
    app.kubernetes.io/name: release-name-udmarpf
    app.kubernetes.io/version: arpf-2311.78.0
    app.kubernetes.io/component: UDM-ARPF
    app.kubernetes.io/managed-by: helm
  annotations:
    description: Defines deployment of ARPF POD
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 0
      maxUnavailable: 20%
  selector:
    matchLabels:
      app.kubernetes.io/name: release-name-udmarpf
  template:
    metadata:
      labels:
        app.kubernetes.io/name: release-name-udmarpf
        serviceType: UDMARPF
        vnfType: REGSTR
      annotations:
        vnfType: REGSTR
        vnfName: "udm2"
        serviceType: UDMARPF
        vnfcType: ARPF
        vnfMajorRelease: "23"
        vnfMinorRelease: "8.0"

        k8s.v1.cni.cncf.io/networks: hsm1lan@hsm1, hsm2lan@hsm2, acreencryptionlan@trigger
    spec:
'''

print "Loadding " + chartFile

with open(chartFile, 'r') as file:
    udmHelmCharts = yaml.safe_load_all(file)
    for helmChart in udmHelmCharts:
        print(helmChart['apiVersion'])
        print(helmChart['kind'])
        print(helmChart['metadata']['name'])
