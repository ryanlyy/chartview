import os
import sys
import yaml

def chartparser_usage():
    print(sys.argv[0] + " is used to explore CNF Helm Charts for feature analysis")
    print("Usage: " + sys.argv[0] + "  <cmd>")
    print("cmd: ")
    print("%20s:\t%s" %('show_kind_apiversion', 'used to show all kind and apiversion supported by CNF'))
    print("%20s:\t%s" %("show_kube_resources", "used to show all Resources supported by CNF"))
    print("%20s:\t%s" %("show_securitycontext", "used to show all pod/container securityContext"))
    print("%20s:\t%s" %("show_pdb", "used to show all pdb info"))
    print("%20s:\t%s" %("show_role", "used to show all role info"))
    print("%20s:\t%s" %("show_secret", "used to show all secrets"))

if len(sys.argv) == 1: 
    chartparser_usage()
    exit()

if sys.argv[1] == "help":
    chartparser_usage()
    exit()

# get the current working directory
workRootDir = os.getcwd()
chartsAllRoot = workRootDir + "/work/templates/"
chartsDirRoot = workRootDir + "/work/templates/reg-helm-charts/charts/"
chartsYamlFile = chartsAllRoot +  "udm-helm-chart.yaml"

# Global definitions
kubeWorkloadList = ["Deployment", "StatefulSet", "Job"]
kubeWorkloadDaemonList = ['Deployment', 'StatefulSet']

#Global Variable to store Resources from ChartsYamlFile
kubeApiKindDicts = {}
kubeResourceDicts =  {}
kubePodLablesDicts = {}

def isLabelsMatched(labelsDict1, labelsDict2):
    for label1 in labelsDict1.keys():
        for label2 in labelsDict2.keys():
            if labelsDict1[label1] == labelsDict2[label2]:
                return True
    return False

def getResourceList(kind):
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind == kind:
            kubeResourceList = kubeResourceDicts[kubeKind]
            return kubeResourceList

def boldStr(s):
    return  '\033[1m' + s + '\033[0m'

def printTitle(tabCnt, paraCnt, *argv):
    tabStr = "\t" * tabCnt
    pIndex = 0
    titleStartStr = ''
    titleStartStrFmt = ''
    titleStr = ''
    titleStrFmt = ''
    titleEndStr = ''
    titleEndStrFmt = ''
    while pIndex < paraCnt * 2:
        titleStartStrFmt = titleStartStr + "%s" + tabStr
        titleStartStr = titleStartStr + "-"*argv[pIndex + 1]
        pIndex = pIndex + 2
    print(titleStartStrFmt)
    print(titleStartStr)
    print(titleStartStrFmt %(titleStartStr))
 #   print("%s\t\t\t%s\t\t\t%s" %("-"*50, "-"*50, "-"*50))
 #   print("%50s\t\t\t%50s\t\t\t%s" %('Rolebinding', 'ServiceAccount', 'Role'))
 #   print("%s\t\t\t%s\t\t\t%s" %("-"*50, "-"*50, "-"*50))

def show_kind_apiversion():
    print("%20s\t\t\t%s" %("Kind", "ApiVersion"))
    print("--------------------------------------------------------------")
    for kubeKind in kubeApiKindDicts.keys():
        kubeApiVersion = kubeApiKindDicts[kubeKind]
        print("%20s\t\t\t%s" % (kubeKind, kubeApiVersion))
    print("--------------------------------------------------------------")

def show_kube_resources():
    print("%20s\t\t\t%s" %("Kind", "Counts"))
    print("-------------------------------------------------------")
    for kubeKind in kubeResourceDicts.keys():
        print("%20s\t\t\t%s" % (kubeKind, len(kubeResourceDicts[kubeKind])))

def show_securitycontext():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
                
        for kubePod in kubePodList:
            containerNameStr = "" 
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            print("------------------------------------------" + kubeWorkload + ": " + kubeWorkloadName + "------------------------------------------")
            
            print("%50s\t\t\t%s" %("pod.securityContext", str(kubePod['spec']['template']['spec']['securityContext'])))
            
            if "containers" in kubePod['spec']['template']['spec'].keys():
                kubeContainerList = kubePod['spec']['template']['spec']['containers']
                for kubeContainer in kubeContainerList:
                    containerName = kubeContainer['name']
                    containerSecurity = kubeContainer['securityContext']
                    print("%50s\t\t\t%s" %(containerName, str(containerSecurity))) 
            if "initContainers" in kubePod['spec']['template']['spec'].keys():
                kubeInitContainerList = kubePod['spec']['template']['spec']['initContainers']
                for kubeContainer in kubeInitContainerList:
                    containerName = kubeContainer['name']
                    containerSecurity = kubeContainer['securityContext']
                    print("%50s\t\t\t%s" %(containerName, str(containerSecurity))) 
            print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")    
                    
            #if kubeInitContainerList is not None:
            #    for kubeContainer in kubeInitContainerList:
            #        containerNameStr = containerNameStr + "\t\t\t" + kubeContainer['name']
            #print(containerNameStr)

def show_pdb():
    kubePdbList = getResourceList('PodDisruptionBudget')
    print("%40s\t\t\t%15s\t\t\t%15s\t\t\t%s" %("PDB",  "maxUnavailable", "minAvailable", "app"))
    print("----------------------------------------------------------------------------")
    for kubePdb in kubePdbList:
        kubeMaxUnavailable = ""
        kubeMinAvailable = ""
        if 'maxUnavailable' in kubePdb['spec'].keys():
            kubeMaxUnavailable = kubePdb['spec']['maxUnavailable']
        if 'minAvailable' in kubePdb['spec'].keys():
            kubeMinAvailable = kubePdb['spec']['minAvailable']
        appStr = ''
        if 'app.kubernetes.io/name' in kubePdb['spec']['selector']['matchLabels'].keys():
            appStr = kubePdb['spec']['selector']['matchLabels']['app.kubernetes.io/name']
        if 'app' in kubePdb['spec']['selector']['matchLabels'].keys():
            appStr = kubePdb['spec']['selector']['matchLabels']['app']
        if appStr == 'cdb':
            appStr = appStr + ":" + kubePdb['spec']['selector']['matchLabels']['type']
        print("%40s\t\t\t%15s\t\t\t%15s\t\t\t%s" %(kubePdb['metadata']['name'], kubeMaxUnavailable, kubeMinAvailable, appStr))
    
    # Check if there is pod w/o PDB defined
    print('-------------------------------------------------------------------------------------')
    print("%50s\t\t\t%s" %('Pod Name', 'Is PDB defined'))
    for pod in kubePodLablesDicts.keys():
        isPdbDefined = False
        for kubePdb in kubePdbList:
            isPdbDefined = isLabelsMatched(kubePodLablesDicts[pod], kubePdb['spec']['selector']['matchLabels'])
            if isPdbDefined:
                break
        print("%50s\t\t\t%s" %(pod, isPdbDefined))

def show_role():
    kubeRolebindingList = getResourceList('RoleBinding')
    #kubeServiceAccountList = getResourceList('ServiceAccount') 
    #kubeRolebindingList = getResourceList('RoleBinding')
    print("%s\t\t\t%s\t\t\t%s" %("-"*50, "-"*50, "-"*50))
    print("%50s\t\t\t%50s\t\t\t%s" %('Rolebinding', 'ServiceAccount', 'Role'))
    print("%s\t\t\t%s\t\t\t%s" %("-"*50, "-"*50, "-"*50))
    for rolebinding in kubeRolebindingList:
        rolebindingName = rolebinding['metadata']['name']
        saName = rolebinding['subjects'][0]['name']
        roleName = rolebinding['roleRef']['name']
        print("%50s\t\t\t%50s\t\t\t%s" %(rolebindingName, saName, roleName))

    print('')
    print("%s\t\t\t%s" %("-"*50, "-"*50))
    print("%50s\t\t\t%s" %('Workload', 'ServiceAccount'))
    print("%s\t\t\t%s" %("-"*50, "-"*50))
    for workload in kubeWorkloadList:
        kubeResourceList = getResourceList(workload)
        for pod in kubeResourceList:
            #print(pod)
            podName = pod['metadata']['name']
            podSaName = pod['spec']['template']['spec']['serviceAccountName']
            print("%50s\t\t\t%s" %(podName, podSaName))

    print('')
    kubeRoleList = getResourceList('Role')
    print("%s\t%s\t%s\t%s" %("-"*50, "-"*20, '-'*40, '-'*50))
    print("%50s\t%20s\t%40s\t%s" %('RoleName', 'apiGroups', 'resources', 'verbs'))
    print("%s\t%s\t%s\t%s" %("-"*50, "-"*20, '-'*40, '-'*50))
    for role in kubeRoleList:
        roleName = role['metadata']['name']
        for rule in role['rules']:
            print("%50s\t%20s\t%40s\t%s" %(roleName, str(rule['apiGroups']), str(rule['resources']), str(rule['verbs'])))

def show_secret():
    secretList = getResourceList('Secret')
    for secret in secretList:
        print("%50s\t%10s\t%s" %(secret['metadata']['name'], secret['type'], str(secret['metadata']['labels']['app.kubernetes.io/name'])))


#print("Loadding " + chartsYamlFile)
#Loading AUSF/UDM Manifests
with open(chartsYamlFile, 'r') as file:
    udmHelmCharts = yaml.safe_load_all(file)
    for helmChart in udmHelmCharts:
        if helmChart is None or len(helmChart) == 0:
            continue

        kubeApi = helmChart['apiVersion']
        kubeKind = helmChart['kind']
        
        #Popuate the kind and api supported by AUSF/UDM
        kubeApiKind =  kubeKind + ": " + kubeApi
        if kubeKind not in kubeApiKindDicts.keys():
            kubeApiKindDicts[kubeKind] = kubeApi

        #Popuate the Resource supported by AUSF/UDM
        if  kubeKind in kubeResourceDicts.keys():
            kubeResourceDicts[kubeKind].append(helmChart)
        else:
            kubeResourceDicts[kubeKind] = []
            kubeResourceDicts[kubeKind].append(helmChart)
        
        #Popuate the pod Labels information
        if kubeKind in kubeWorkloadDaemonList:
            kubePodLabels = helmChart['metadata']['labels']
            kubePodName = helmChart['metadata']['name']
            kubePodLablesDicts[kubePodName] = kubePodLabels

if sys.argv[1] == "show_kind_apiversion":
    show_kind_apiversion()
elif sys.argv[1] == "show_kube_resources":
    show_kube_resources()
elif sys.argv[1] == "show_securitycontext":
    show_securitycontext()
elif sys.argv[1] == "show_pdb":
    show_pdb()
elif sys.argv[1] == 'show_role':
    show_role()
elif sys.argv[1] == 'show_secret':
    show_secret()
else:
    chartparser_usage()
