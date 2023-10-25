import os
import sys
import yaml

def chartparser_usage():
    print(sys.argv[0] + " is used to explore CNF Helm Charts for feature analysis")
    print("Usage: " + sys.argv[0] + "  <cmd>")
    print("cmd: ")
    print("%20s:\t%s" %('show_all', 'used to show all resources by CNF'))
    print("%20s:\t%s" %('show_kind_apiversion', 'used to show all kind and apiversion supported by CNF'))
    print("%20s:\t%s" %("show_kube_resources", "used to show all Resources supported by CNF"))
    print("%20s:\t%s" %("show_securitycontext", "used to show all pod/container securityContext"))
    print("%20s:\t%s" %("show_pdb", "used to show all pdb info"))
    print("%20s:\t%s" %("show_role", "used to show all role info"))
    print("%20s:\t%s" %("show_secret", "used to show all secrets"))
    print("%20s:\t%s" %("show_tolerations", "used to show all telerations"))
    print("%20s:\t%s" %("show_nodeselector", "used to show all nodeSelector"))
    print("%20s:\t%s" %("show_cpus", "used to show all CPU"))
    print("%20s:\t%s" %("show_memory", "used to show all MEMORY"))
    print("%20s:\t%s" %("show_disks", "used to show all disk"))
    print("%20s:\t%s" %("show_probes", "used to show all probles"))
    print("%20s:\t%s" %("show_labels", "used to show all labels"))
    print("%20s:\t%s" %("show_affinity", "used to show all affinity"))
    print("%20s:\t%s" %("show_volumes", "used to show all volumes"))  
    print("%20s:\t%s" %("show_upgrade", "used to show all upgrade strategy")) 
    print("%20s:\t%s" %("show_networks", "used to show all networks"))   
    print("%20s:\t%s" %("show_lifecycle", "used to show all containers lifecycle"))
    print("%20s:\t%s" %("show_images", "used to show all containers image policy"))
    print("%20s:\t%s" %("show_services", "used to show all services")) 
    print("%20s:\t%s" %("show_others", "used to show others info"))
    exit()

# get the current working directory
workRootDir = os.getcwd()
chartsTemplateRootDir = workRootDir + "/work/templates/"
chartsYamlFile = "udm-helm-chart.yaml"

# Global definitions
kubeWorkloadList = ["Deployment", "StatefulSet", "Job"]
kubeWorkloadDaemonList = ['Deployment', 'StatefulSet']
kubeWorkloadContainerTypeList = ['containers', 'initContainers']

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

def removeReleaseName(resName):
    if resName[:len("release-name-")] == "release-name-":
        return resName[len("release-name-"):]
    else:
        return resName

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

def show_nodeselector():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
                
        for kubePod in kubePodList:
            containerNameStr = "" 
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            print("------------------------------------------" + kubeWorkload + ": " + kubeWorkloadName + "------------------------------------------")
            if 'nodeSelector' not in kubePod['spec']['template']['spec'].keys():
                print('nodeSelector is None')
                continue
            print("%s\t%s" %("pod.nodeSelector", str(kubePod['spec']['template']['spec']['nodeSelector'])))
            print()

def show_tolerations():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
                
        for kubePod in kubePodList:
            containerNameStr = "" 
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            print("------------------------------------------" + kubeWorkload + ": " + kubeWorkloadName + "------------------------------------------")
            if 'tolerations' not in kubePod['spec']['template']['spec'].keys():
                print('tolerations is None')
                continue
            print("%s\t%s" %("pod.tolerations", str(kubePod['spec']['template']['spec']['tolerations'])))
            print()

def show_cpus():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
                
        for kubePod in kubePodList:
            print("%s" %('-'*120))
            print("%30s\t%20s\t%15s\t%10s\t%s" %("Pod", "Container", "Container Type", "Limit", "Requests"))
            print("%s" %('-'*120))

            containerNameStr = "" 
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            #print("------------------------------------------" + kubeWorkload + ": " + kubeWorkloadName + "------------------------------------------")
            totalLimit = 0
            totalRequests = 0
            for containerType in kubeWorkloadContainerTypeList:
                if containerType in kubePod['spec']['template']['spec'].keys():
                    kubeContainerList = kubePod['spec']['template']['spec'][containerType]
                    for kubeContainer in kubeContainerList:
                        containerName = kubeContainer['name']
                        containerResource = kubeContainer['resources']
                        containerLimit = containerResource['limits']['cpu']
                        containerRequests = containerResource['requests']['cpu']
                        if containerType == 'containers':
                            totalLimit = totalLimit + int(containerLimit[:-1])
                            totalRequests = totalRequests + int(containerRequests[:-1])
                        print("%30s\t%20s\t%15s\t%10s\t%s" %(kubeWorkloadName, containerName, containerType, containerLimit, containerRequests)) 
            print("%30s\t%20s\t%15s\t%10s\t%s" %("-"*len(kubeWorkloadName), "-"*len("sum(containers)"), "", "-"*len(containerLimit), "-"*len(containerRequests)))
            print("%30s\t%20s\t%15s\t%10dm\t%dm\n" %(kubeWorkloadName, "sum(containers)", "", totalLimit, totalRequests))
 
def show_memory():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
                
        for kubePod in kubePodList:
            print("%s" %('-'*100))
            print("%30s\t%20s\t%15s\t%10s\t%s" %("Pod", "Container", "Container Type", "Limit", "Requests"))
            print("%s" %('-'*100))
            
            containerNameStr = "" 
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            kubeWorkloadName = removeReleaseName(kubeWorkloadName)
            #print("------------------------------------------" + kubeWorkload + ": " + kubeWorkloadName + "------------------------------------------")
            totalLimit = 0
            totalRequests = 0
            for containerType in kubeWorkloadContainerTypeList:
                if containerType in kubePod['spec']['template']['spec'].keys():
                    kubeContainerList = kubePod['spec']['template']['spec'][containerType]
                    for kubeContainer in kubeContainerList:
                        containerName = kubeContainer['name']
                        containerName = removeReleaseName(containerName)
                        containerResource = kubeContainer['resources']
                        containerLimit = containerResource['limits']['memory']
                        containerRequests = containerResource['requests']['memory']
                        if containerType == 'containers':
                            tempLimit = int(containerLimit[:-2])
                            tempRequests = int(containerRequests[:-2])
                            if containerLimit[-2:] == "Gi":
                                tempLimit = tempLimit * 1024
                            if containerRequests[-2:] == "Gi":
                                tempRequests = tempRequests * 1024
                            totalLimit = totalLimit + tempLimit
                            totalRequests = totalRequests + tempRequests
                        print("%30s\t%20s\t%15s\t%10s\t%s" %(kubeWorkloadName, containerName, containerType, containerLimit, containerRequests)) 
            print("%30s\t%20s\t%15s\t%10s\t%s" %("-"*len(kubeWorkloadName), "-"*len("sum(containers)"), "", "-"*len(containerLimit), "-"*len(containerRequests)))
            print("%30s\t%20s\t%15s\t%10dMi\t%dMi\n" %(kubeWorkloadName, "sum(containers)", "", totalLimit, totalRequests))

def show_disks():
    pass

def show_probes():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadDaemonList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
                
        for kubePod in kubePodList:
            print("%s" %('-'*100))
            print("%30s\t%20s\t%10s\t%s" %("Pod", "Container", "ProbeType", "Probe"))
            print("%s" %('-'*100))
            containerNameStr = "" 
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            kubeWorkloadName = removeReleaseName(kubeWorkloadName)
            #print("------------------------------------------" + kubeWorkload + ": " + kubeWorkloadName + "------------------------------------------")
            totalLimit = 0
            totalRequests = 0
            for containerType in kubeWorkloadContainerTypeList:
                if containerType == 'initContainers':
                    continue
                if containerType in kubePod['spec']['template']['spec'].keys():
                    kubeContainerList = kubePod['spec']['template']['spec'][containerType]
                    for kubeContainer in kubeContainerList:
                        containerName = kubeContainer['name']
                        containerName = removeReleaseName(containerName)
                        containerReadiness = 'NoneProbe'
                        containerLiveness = 'NoneProbe'
                        if 'readinessProbe' in kubeContainer.keys():
                            containerReadiness = kubeContainer['readinessProbe']
                        if 'livenessProbe' in kubeContainer.keys():
                            containerLiveness = kubeContainer['livenessProbe']
                        print("%30s\t%20s\t%10s\t%s" %(kubeWorkloadName, containerName, 'livenessProbe', containerLiveness)) 
                        print("%30s\t%20s\t%10s\t%s" %(kubeWorkloadName, containerName, 'readinessProbe', containerReadiness)) 
                        if containerLiveness == containerReadiness:
                            print("%30s\t%20s\t%10s\t%s" %("", "", "", "livenessProbe = readinessProbe"))
                        else:
                            print("%30s\t%20s\t%10s\t%s" %("", "", "", "livenessProbe != readinessProbe"))

def show_labels():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            kubeResList = kubeResourceDicts[kubeKind]  
            print("%s" %('-'*100))
            print("%20s\t%40s\t%s" %("Kind", "Name", "Labels"))
            print("%s" %('-'*100))  
            for kubeRes in kubeResList:
                resName = kubeRes['metadata']['name']
                resName = removeReleaseName(resName)
                if 'labels' in kubeRes['metadata'].keys():
                    resLabels = kubeRes['metadata']['labels']
                    if resLabels is None:
                        print("%20s\t%40s\t%s" %(kubeKind, resName, "NonLabels"))
                        continue
                    labelPairs = resLabels.items()
                    count = 0
                    for labelPair in labelPairs:
                        if count == 0:
                            print("%20s\t%40s\t%s" %(kubeKind, resName, labelPair))   
                        else:
                            print("%20s\t%40s\t%s" %("", "", labelPair))   
                        count = 1
                print("%10s\t%40s\t%s" %("", "", "-"*30))
            print('')
        if kubeKind in kubeWorkloadList:                        
            kubePodList = kubeResourceDicts[kubeKind]  
            print("%s" %('-'*100))
            print("%20s\t%40s\t%s" %("Kind", "Name", "Labels"))
            print("%s" %('-'*100))           
            for kubePod in kubePodList:           
                containerNameStr = "" 
                kubeWorkload = kubePod['kind']
                kubeWorkloadName = kubePod['metadata']['name']
                kubeWorkloadName = removeReleaseName(kubeWorkloadName)
                deploymentLabels = kubePod['metadata']['labels']
                labelPairs = deploymentLabels.items()
                count = 0
                for labelPair in labelPairs:
                    if count == 0:
                        print("%20s\t%40s\t%s" %(kubeKind, kubeWorkloadName, labelPair))   
                    else:
                        print("%20s\t%40s\t%s" %("", "", labelPair))   
                    count = 1

                if 'metadata' not in kubePod['spec']['template'].keys():
                    continue
                podLabels = kubePod['spec']['template']['metadata']['labels']
                labelPairs = podLabels.items()
                count = 0
                for labelPair in labelPairs:
                    if count == 0:
                        print("%20s\t%40s\t%s" %('Pod', kubeWorkloadName, labelPair))   
                    else:
                        print("%20s\t%40s\t%s" %("", "", labelPair))   
                    count = 1 
                print("%10s\t%40s\t%s" %("", "", "-"*30))
                if deploymentLabels == podLabels:
                    print("%10s\t%40s\t%s" %("", "", "workload label = pod label"))
                else:
                    print("%10s\t%40s\t%s" %("", "", "workload label != pod label"))
                print('')              

def show_volumes():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
        print("%s" %('-'*100))
        print("%30s\t%20s\t%s" %("Kind", "Name", "Volumes"))
        print("%s" %('-'*100))               
        for kubePod in kubePodList:          
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            kubeWorkloadName = removeReleaseName(kubeWorkloadName)
            if 'volumes' not in kubePod['spec']['template']['spec'].keys():
                continue
            podVolumes = kubePod['spec']['template']['spec']['volumes']
            count = 0
            for volume in podVolumes:
                if count == 0:
                    print("%30s\t%20s\t%s" %(kubeKind, kubeWorkloadName, volume))
                else:
                    print("%30s\t%20s\t%s" %("", "", volume))
                count = 1
            print("%30s\t%20s\t%s" %("", "", "-"*30))

def show_affinity():
    podHardAntiAffinityDicts = {}
    podSoftAntiAffinityDicts = {}
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadDaemonList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
        print("%s" %('-'*100))
        print("%10s\t%10s\t%20s\t%50s\t%s" %("Kind", "Name", "Affinity Type", "hard/soft", "Affinity"))
        print("%s" %('-'*100))               
        for kubePod in kubePodList:          
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            kubeWorkloadName = removeReleaseName(kubeWorkloadName)
            if 'affinity' not in kubePod['spec']['template']['spec'].keys():
                continue
            affinityList = kubePod['spec']['template']['spec']['affinity']
            count = 0
            podHardAntiAffinityDicts[kubeWorkloadName] = "No"
            podSoftAntiAffinityDicts[kubeWorkloadName] = "No"
            for antiAffinityKey in affinityList.keys():
                for antiAffinity in affinityList[antiAffinityKey].keys():
                    if antiAffinity == 'requiredDuringSchedulingIgnoredDuringExecution':
                        podHardAntiAffinityDicts[kubeWorkloadName] = 'Yes'
                    if antiAffinity == 'preferredDuringSchedulingIgnoredDuringExecution':
                        podSoftAntiAffinityDicts[kubeWorkloadName] = "Yes"
                    condition = affinityList[antiAffinityKey][antiAffinity]
                    if count == 0:
                        print("%10s\t%10s\t%20s\t%50s\t%s" %(kubeKind, kubeWorkloadName, antiAffinityKey, antiAffinity, condition))
                    else:
                        print("%10s\t%10s\t%20s\t%50s\t%s" %("", "", "", "", condition))
                    count = 1
            print("%10s\t%10s\t%20s\t%50s\t%s" %("", "", "", "", "-"*30))
    print("-"*30)   
    print("%20s\t%50s\t%s" %("Name", "requiredDuringSchedulingIgnoredDuringExecution", 'preferredDuringSchedulingIgnoredDuringExecution'))     
    for pod in podHardAntiAffinityDicts.keys():
        print("%20s\t%50s\t%s" %(pod, podHardAntiAffinityDicts[pod], podSoftAntiAffinityDicts[pod]))

def show_upgrade():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadDaemonList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
        print("%s" %('-'*100))
        print("%10s\t%20s\t%10s\t%s" %("Kind", "Name", "replicas", "Strategy"))
        print("%s" %('-'*100))               
        for kubePod in kubePodList:          
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            kubeWorkloadName = removeReleaseName(kubeWorkloadName)
            if 'replicas' not in kubePod['spec'].keys():
                podReplicas = "default(1)"
            else:
                podReplicas = kubePod['spec']['replicas']
            if kubeWorkload == 'StatefulSet':
                strategy = kubePod['spec']['updateStrategy']
            else:
                strategy = kubePod['spec']['strategy']
            print("%10s\t%20s\t%10s\t%s" %(kubeWorkload, kubeWorkloadName, podReplicas, strategy))
        print("")

def show_networks():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
        print("%s" %('-'*100))
        print("%10s\t%35s\t%s" %("Kind", "Name", "Networks"))
        print("%s" %('-'*100))               
        for kubePod in kubePodList:          
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            kubeWorkloadName = removeReleaseName(kubeWorkloadName)
            if 'metadata' not in kubePod['spec']['template'].keys():
                networks = 'default(cluster)'
            elif 'annotations' not in kubePod['spec']['template']['metadata'].keys():
                networks = 'default(cluster)'
            elif 'k8s.v1.cni.cncf.io/networks' not in kubePod['spec']['template']['metadata']['annotations'].keys():
                networks = 'default(cluster)'
            else:
                networks = kubePod['spec']['template']['metadata']['annotations']['k8s.v1.cni.cncf.io/networks']
            print("%10s\t%35s\t%s" %(kubeWorkload, kubeWorkloadName, networks))
        print("")

def show_others():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
        print("%s" %('-'*100))      
        print("%10s\t%35s\t%25s\t%25s\t%25s\t%s" %("Kind", "Name", "shareProcessNamespace", "restartPolicy", "priorityClassName", "serviceAccountName"))
        print("%s" %('-'*100))               
        for kubePod in kubePodList:          
            kubeWorkload = kubePod['kind']
            kubeWorkloadName = kubePod['metadata']['name']
            kubeWorkloadName = removeReleaseName(kubeWorkloadName) 
            shareProcessNamespace = "default(false)"
            restartPolicy = "default(Always)"
            serviceAccountName = "default"
            priorityClassName = "default(0)"
            if 'shareProcessNamespace' in kubePod['spec']['template']['spec'].keys():
                shareProcessNamespace = kubePod['spec']['template']['spec']['shareProcessNamespace']
            if 'restartPolicy' in kubePod['spec']['template']['spec'].keys():
                restartPolicy = kubePod['spec']['template']['spec']['restartPolicy']
            if 'serviceAccountName' in kubePod['spec']['template']['spec'].keys():
                serviceAccountName = kubePod['spec']['template']['spec']['serviceAccountName']
            if 'priorityClassName' in kubePod['spec']['template']['spec'].keys():
                priorityClassName = kubePod['spec']['template']['spec']['priorityClassName']     
            print("%10s\t%35s\t%25s\t%25s\t%25s\t%s" %(kubeWorkload, kubeWorkloadName, shareProcessNamespace, restartPolicy, priorityClassName, serviceAccountName))
        print("")

def show_images():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
        print("%s" %('-'*120))
        print("%10s\t%30s\t%25s\t%15s\t%s" %("kind", "Name", "Container", "Container Type", "imagePullPolicy"))
        print("%s" %('-'*120))               
        for kubePod in kubePodList:
            kubeWorkloadName = kubePod['metadata']['name']
            kubeWorkloadName = removeReleaseName(kubeWorkloadName) 
            #print("------------------------------------------" + kubeWorkload + ": " + kubeWorkloadName + "------------------------------------------")
            count = 0
            for containerType in kubeWorkloadContainerTypeList:
                if containerType in kubePod['spec']['template']['spec'].keys():
                    kubeContainerList = kubePod['spec']['template']['spec'][containerType]
                    for kubeContainer in kubeContainerList:
                        containerName = kubeContainer['name']
                        containerName = removeReleaseName(containerName)
                        if 'imagePullPolicy' in kubeContainer.keys():
                            imagePullPolicy = kubeContainer['imagePullPolicy']
                        else:
                            imagePullPolicy = 'default(Always)'
                        if count == 0:
                            print("%10s\t%30s\t%25s\t%15s\t%s" %(kubeKind, kubeWorkloadName, containerName, containerType, imagePullPolicy)) 
                        else:
                            print("%10s\t%30s\t%25s\t%15s\t%s" %("", "", containerName, containerType, imagePullPolicy))
                        count = 1
            print("%10s\t%30s\t%25s\t%15s\t%s" %("", "", "", "", "-"*20))
        print("")

def show_lifecycle():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind not in kubeWorkloadList:
            continue
        kubePodList = kubeResourceDicts[kubeKind]
        print("%s" %('-'*120))
        print("%10s\t%30s\t%25s\t%15s\t%10s\t%s" %("kind", "Name", "Container", "Container Type", "lifecycle", "Operations"))
        print("%s" %('-'*120))               
        for kubePod in kubePodList:
            kubeWorkloadName = kubePod['metadata']['name']
            kubeWorkloadName = removeReleaseName(kubeWorkloadName) 
            #print("------------------------------------------" + kubeWorkload + ": " + kubeWorkloadName + "------------------------------------------")
            count = 0
            for containerType in kubeWorkloadContainerTypeList:
                if containerType in kubePod['spec']['template']['spec'].keys():
                    kubeContainerList = kubePod['spec']['template']['spec'][containerType]
                    for kubeContainer in kubeContainerList:
                        containerName = kubeContainer['name']
                        containerName = removeReleaseName(containerName)
                        if 'lifecycle' in kubeContainer.keys():
                            lifecycle = kubeContainer['lifecycle']
                        else:
                            lifecycle = 'None'

                        if lifecycle == 'None':
                            if count == 0:
                                print("%10s\t%30s\t%25s\t%15s\t%10s\t%s" %(kubeKind, kubeWorkloadName, containerName, containerType, lifecycle, "")) 
                            else:
                                print("%10s\t%30s\t%25s\t%15s\t%10s\t%s" %("", "", containerName, containerType, lifecycle, "")) 
                            count = 1
                        else:
                            for prepost in lifecycle.keys():
                                if count == 0:
                                    print("%10s\t%30s\t%25s\t%15s\t%10s\t%s" %(kubeKind, kubeWorkloadName, containerName, containerType, prepost, lifecycle[prepost])) 
                                else:
                                    print("%10s\t%30s\t%25s\t%15s\t%10s\t%s" %("", "", containerName, containerType, prepost, lifecycle[prepost]))
                                count = 1
            print("%10s\t%30s\t%25s\t%15s\t%10s\t%s" %("", "", "", "", "", "-"*100))
        print("")

def show_services():
    for kubeKind in kubeResourceDicts.keys():
        if kubeKind != 'Service':
            continue
        kubeServiceList = kubeResourceDicts[kubeKind]
        print("%s" %('-'*120))
        print("%10s\t%30s\t%25s\t%20s\t%20s\t%s" %("kind", "Name", "Pod", "Type", "clusterIP", "publishNotReadyAddresses"))
        print("%s" %('-'*120))               
        for kubeService in kubeServiceList:
            svcName = kubeService['metadata']['name']
            svcName = removeReleaseName(svcName)
            svcType = 'default(ClusterIP)'
            svcClusterIP = 'default'
            svcPublishNotReadyAddresses = 'default'
            if 'type' in kubeService['spec'].keys():
                svcType = kubeService['spec']['type']
            if 'clusterIP' in kubeService['spec'].keys():
                svcClusterIP = kubeService['spec']['clusterIP']
            if 'publishNotReadyAddresses' in kubeService['spec'].keys():
                svcPublishNotReadyAddresses = kubeService['spec']['publishNotReadyAddresses']
            svcSelector = kubeService['spec']['selector']
            podName = "None"
            if 'app.kubernetes.io/name' in svcSelector.keys():
                podName = svcSelector['app.kubernetes.io/name']
            elif 'app' in svcSelector.keys():
                podName = svcSelector['app']
            if 'cnf.ce.nokia.com/role' in svcSelector.keys():
                podName = podName + '-' + svcSelector['cnf.ce.nokia.com/role']
            if 'type' in svcSelector.keys():
                podName = podName + '-' + svcSelector['type']
            if 'redisio_role' in svcSelector.keys():
                podName = podName + '-' + svcSelector['redisio_role']
            podName = removeReleaseName(podName)
            print("%10s\t%30s\t%25s\t%20s\t%20s\t%s" %(kubeKind, svcName,  podName, svcType, svcClusterIP, svcPublishNotReadyAddresses))
        print("")

def show_all():
    show_kind_apiversion()
    show_kube_resources()
    show_securitycontext()
    show_pdb()
    show_role()
    show_secret()
    show_tolerations()
    show_nodeselector()
    show_cpus()
    show_memory()
    show_disks()
    show_probes()
    show_labels()
    show_affinity()
    show_volumes()
    show_upgrade()
    show_networks()
    show_images()
    show_lifecycle()
    show_services()
    show_others()

def loadChartYamlFile(yamlFile):
    print("Loadding " + yamlFile + "...")
    #Loading AUSF/UDM Manifests
    with open(yamlFile, 'r') as file:
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

chartParserMenu = {
    1: ("show_kind_apiversion", show_kind_apiversion),
    2: ("show_kube_resources", show_kube_resources),
    3: ("show_securitycontext", show_securitycontext),
    4: ("show_pdb", show_pdb),
    5: ("show_role", show_role),
    6: ("show_secret", show_secret),
    7: ("show_tolerations", show_tolerations),
    8: ("show_nodeselector", show_nodeselector),
    9: ("show_cpus", show_cpus),
    10: ("show_memory", show_memory),
    11: ("show_disks", show_disks),
    12: ("show_probes", show_probes),
    13: ("show_labels", show_labels),
    14: ("show_affinity", show_affinity),
    15: ("show_volumes", show_volumes),
    16: ("show_upgrade", show_upgrade),
    17: ("show_networks", show_networks),
    18: ("show_images", show_images),
    19: ("show_lifecycle", show_lifecycle),
    20: ("show_services", show_services),
    21: ("show_others", show_others),
    22: ("show_all", show_all),
    23: ("help", chartparser_usage)
}

if len(sys.argv) > 1:
    if sys.argv[1] == 'help':
        chartparser_usage()

try:
    releaseList = os.listdir(chartsTemplateRootDir)
except:
    print("You need to download your helm charts firstly using below command, and then try again")
    print("\t./chartview.sh")
    exit()

count = 1
print("-"*30)
for release in releaseList:
    print("\t%d: %s" %(count, release))
    count = count + 1
print("-"*30)
userInput = input("Enter a release version and press enter:> ")
releaseSelected = releaseList[userInput - 1]

buildList = os.listdir(chartsTemplateRootDir + "/" + releaseSelected + "/")
count = 1
print("-"*50)
for build in buildList:
    print("\t%d: %s" %(count, build))
    count = count + 1
print("-"*50)
userInput = input("Enter a build version and press enter:> ")
buildSelected = buildList[userInput - 1]

yamlFile = chartsTemplateRootDir + "/" + releaseSelected + "/" + buildSelected + "/" + chartsYamlFile

loadChartYamlFile(yamlFile)

if len(sys.argv) == 1: 
    while 1: 
        print("-" * 50)
        print("MENU:")
        print("-" * 50)
        for key in sorted(chartParserMenu.keys()):
            print("\t" + str(key) + ": " + chartParserMenu[key][0])
        print("-"*50)
        try:
            userInput = input("Enter a operation and press enter:> ")
        except:
            print("")
            exit()
        #print("-"*20 + chartParserMenu[str(useInput)][0] + "-"*20)
        #print(userInput)
        chartParserMenu[userInput][1]()
    exit()

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
elif sys.argv[1] == 'show_tolerations':
    show_tolerations()
elif sys.argv[1] == 'show_nodeselector':
    show_nodeselector()
elif sys.argv[1] == 'show_cpus':
    show_cpus()
elif sys.argv[1] == 'show_memory':
    show_memory()
elif sys.argv[1] == 'show_disks':
    show_disks()
elif sys.argv[1] == 'show_probes':
    show_probes()
elif sys.argv[1] == 'show_labels':
    show_labels()
elif sys.argv[1] == 'show_affinity':
    show_affinity()
elif sys.argv[1] == 'show_volumes':
    show_volumes()
elif sys.argv[1] == 'show_upgrade':   
    show_upgrade()
elif sys.argv[1] == 'show_networks':   
    show_networks()
elif sys.argv[1] == 'show_images':  
    show_images()
elif sys.argv[1] == 'show_lifecycle':  
    show_lifecycle()
elif sys.argv[1] == 'show_services': 
    show_services()
elif sys.argv[1] == 'show_others':  
    show_others()
elif sys.argv[1] == 'show_all':
    show_all()
elif sys.argv[1] == "help":
    chartparser_usage()
else:
    chartparser_usage()
