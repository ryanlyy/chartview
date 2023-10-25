#!/usr/bin/bash

HELM_CHARTS_URL_ROOT=https://artifactory-blr1.int.net.nokia.com/artifactory/ims_pltf_local/

PUBLISH_ROOT_DIR=/var/www/html/ryliu/udm/chartview/

WORK_ROOT_DIR=$(pwd)
VALUE_YAML=$WORK_ROOT_DIR/values.yaml

CHART_WORK_DIR=$WORK_ROOT_DIR/work/
CHART_DOWNLOAD_DIR=$CHART_WORK_DIR/download/
CHART_FINAL_DIR=""
CHART_TEMPLATE_DIR=$CHART_WORK_DIR/templates/

CHART_TEMPLATE_YAML=udm-helm-chart.yaml

CHART_DOWNLOAD_REL_VERSION=""
CHART_DOWNLOAD_BLD_VERSION=""

chartview_log()
{
	echo "$(date)-CHARTVIEW: $1"
}

#Remove temp files
if [[ ! -d $CHART_WORK_DIR ]]; then
	mkdir $CHART_WORK_DIR24

fi
if [[ ! -d $CHART_DOWNLOAD_DIR ]]; then
	mkdir $CHART_DOWNLOAD_DIR
fi
if [[ ! -d $CHART_TEMPLATE_DIR ]]; then 
	mkdir $CHART_TEMPLATE_DIR
fi

#https://artifactory-blr1.int.net.nokia.com/artifactory/ims_pltf_local/23.11/5G_IMAGES/AUSF_UDM_NGCAL2311095.tar.gz

list_helm_chart()
{
	CCI_DIR=$1
	curl --silent $CCI_DIR | grep -o 'href=".*">' | sed 's/href="//;s/\">//' |grep ".tar.gz$" | cut -d"." -f1
}

list_cci_dir()
{
	CCI_DIR=$1
	curl --silent $CCI_DIR | grep -o 'href=".*">' | sed 's/href="//;s/\">//' | grep "^[1-9][0-9].*"
}

down_load_udm_chart_unzip()
{
	CHART_URL=$1
	CHART_NAME=$(basename $CHART_URL)
	CHART_DIR_NAME=$CHART_DOWNLOAD_DIR/$CHART_NAME
	if [[ ! -f $CHART_DIR_NAME ]]; then
		chartview_log "Downloading $CHART_URL in $CHART_DOWNLOAD_DIR ..."
		curl --silent $CHART_URL -o $CHART_DIR_NAME
	fi
	chartview_log "$CHART_NAME is downloaded in $CHART_DOWNLOAD_DIR"

	cd $CHART_DOWNLOAD_DIR
	rm -rf $CHART_DOWNLOAD_BLD_VERSION
	chartview_log "unzip $CHART_NAME..."
	tar zxf $CHART_NAME

	cd $CHART_DOWNLOAD_BLD_VERSION/Helm_charts/
	HELM_CHART_DIR1=$(echo $CHART_NAME|cut -d"_" -f3 | cut -d "." -f1)
	mkdir $HELM_CHART_DIR1
	cd $HELM_CHART_DIR1
	HELM_CHART_TGZ1="udm-ausf-helm-charts-$(echo $CHART_NAME|cut -d"_" -f3-)"
	tar zxf ../$HELM_CHART_TGZ1

	HELM_CHART_TGZ2=$(ls reg-helm-charts*tgz)
	tar zxf $HELM_CHART_TGZ2

	CHART_FINAL_DIR=$PWD

	chartview_log "RELEASE $CHART_DOWNLOAD_REL_VERSION BLD $CHART_DOWNLOAD_BLD_VERSION is downloaded in $CHART_DOWNLOAD_DIR and unziped in $CHART_FINAL_DIR"
	ls -l $CHART_FINAL_DIR
}

helm_template_chart()
{
	CHART_TEMPLATE_GENERATED_FILE=$CHART_TEMPLATE_DIR/$CHART_DOWNLOAD_REL_VERSION/$CHART_DOWNLOAD_BLD_VERSION
	rm -rf $CHART_TEMPLATE_GENERATED_FILE
	mkdir -p $CHART_TEMPLATE_GENERATED_FILE
	cd $CHART_FINAL_DIR
	chartview_log "helm template ..."
	helm template -f $VALUE_YAML reg-helm-charts > $CHART_TEMPLATE_GENERATED_FILE/$CHART_TEMPLATE_YAML 
	#helm template -f $VALUE_YAML reg-helm-charts --output-dir $CHART_TEMPLATE_DIR 
	exit	
}

select_udm_version()
{
	VERSION_URL=$HELM_CHARTS_URL_ROOT/$1/5G_IMAGES/
	typeset -A UDM_VER_LIST=$(list_helm_chart $VERSION_URL)	
	PS3="Select a AUSF_UDM BUILD APS: "
	select UDM_VER in ${UDM_VER_LIST[*]}
	do
		if [[ ${UDM_VER} != "" ]]; then
			CHART_DOWNLOAD_BLD_VERSION=$UDM_VER
			CHART_DIR_URL=$VERSION_URL/$UDM_VER.tar.gz
			#echo $CHART_DIR_URL
			down_load_udm_chart_unzip ${CHART_DIR_URL}
			helm_template_chart 
		else
			break;
		fi
	done
}

#list_cci_dir $RB_REMOTE_ROOT
typeset -A UDM_RELEASE_LIST=$(list_cci_dir $HELM_CHARTS_URL_ROOT)
PS3="Select a AUSF_UDM Release: "
select UDM_RELEASE in ${UDM_RELEASE_LIST[*]}
do
	if [[ ${UDM_RELEASE} != "" ]]; then
		CHART_DOWNLOAD_REL_VERSION=${UDM_RELEASE}
		select_udm_version ${UDM_RELEASE}
	else
		break;
	fi
done