# chartview
---

This repos is used to parse helm chart for review friendly

# How to use
1. Close this repo
    ```bash
    git clone git@scm.cci.nokia.net:ryliu/chartview.git
    ```

2. Download your helm chart
    ```bash
    cd chartview
    ./chartview.sh
    ```
    NOTE: it is user interactive mode

3. Parse your helm charts
    ```bash
    python ./chartparser.py
    ```
    NOTE: it is user interactive mode and support cmd line mode
    ```bash
    [ryliu@localhost chartview]$ python ./chartparser.py help
        ./chartparser.py is used to explore CNF Helm Charts for feature analysis
        Usage: ./chartparser.py  <cmd>
        cmd: 
                    show_all:	used to show all resources by CNF
        show_kind_apiversion:	used to show all kind and apiversion supported by CNF
         show_kube_resources:	used to show all Resources supported by CNF
        show_securitycontext:	used to show all pod/container securityContext
                    show_pdb:	used to show all pdb info
                   show_role:	used to show all role info
                 show_secret:	used to show all secrets
            show_tolerations:	used to show all telerations
           show_nodeselector:	used to show all nodeSelector
                   show_cpus:	used to show all CPU
                 show_memory:	used to show all MEMORY
                  show_disks:	used to show all disk
                 show_probes:	used to show all probles
                 show_labels:	used to show all labels
               show_affinity:	used to show all affinity
                show_volumes:	used to show all volumes
                show_upgrade:	used to show all upgrade strategy
               show_networks:	used to show all networks
              show_lifecycle:	used to show all containers lifecycle
                 show_images:	used to show all containers image policy
               show_services:	used to show all services
                 show_others:	used to show others info
    ```