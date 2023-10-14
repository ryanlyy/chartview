#!/usr/bin/bash

RB_REMOTE_ROOT=https://repo.cci.nokia.net/artifactory/list/udm-generic-candidates/NEAR/AUSF/
OUTPUT_ROOT=/var/www/html/ryliu/udm/chartview/
WORK_ROOT=./chartview/
VALUE_YAML=$WORK_ROOT/values.yaml
CHART_WORK_DIR=$WORK_ROOT/work/
CHART_TEMPLATE_DIR=$CHART_WORK_DIR/templates/
CHART_TEMPLATE_YAML=$CHART_TEMPLATE_DIR/udm-helm-chart.yaml

chartview_log()
{
	echo "$(date)-CHARTVIEW: $1"
}

#Remove temp files
rm -rf $CHART_WORK_DIR
mkdir $CHART_WORK_DIR
mkdir $CHART_TEMPLATE_DIR

#https://repo.cci.nokia.net/artifactory/list/udm-generic-candidates/NEAR/AUSF/23.11/AUSF_UDM_NGCAL2311078/INSTALL_MEDIA/CHARTS/reg-helm-charts-2311.78.0.tgz

list_helm_chart()
{
	CCI_DIR=$1
	curl --silent $CCI_DIR | grep -o 'href=".*">' | sed 's/href="//;s/\">//' |grep reg-helm-charts
}

list_cci_dir()
{
	CCI_DIR=$1
	curl --silent $CCI_DIR | grep -o 'href=".*">' | sed 's/href="//;s/\/">//' | grep -v tar\.gz | grep -v "\.\."
}

down_load_udm_chart_unzip()
{
	CHART_URL=$1
	CHART_NAME=$2
	CHART_DIR_NAME=$CHART_WORK_DIR/$CHART_NAME
	chartview_log "Downloading $CHART_URL in $CHART_WORK_DIR..."
	curl --silent $CHART_URL -o $CHART_DIR_NAME
	cd $CHART_WORK_DIR
	ls $CHART_WORK_DIR
	chartview_log "unzip $CHART_NAME..."
	tar zxf $CHART_NAME
}

helm_template_chart()
{
	cd $CHART_WORK_DIR
	chartview_log "helm template ..."
	helm template -f $VALUE_YAML reg-helm-charts > $CHART_TEMPLATE_YAML 
	helm template -f $VALUE_YAML reg-helm-charts --output-dir $CHART_TEMPLATE_DIR 
	exit	
}

select_udm_version()
{
	VERSION_URL=$RB_REMOTE_ROOT/$1/
	typeset -A UDM_VER_LIST=$(list_cci_dir $VERSION_URL)	
	PS3="Select a AUSF_UDM Version: "
	select UDM_VER in ${UDM_VER_LIST[*]}
	do
		CHART_DIR_URL=$VERSION_URL/$UDM_VER/INSTALL_MEDIA/CHARTS/
		if [[ ${UDM_VER} != "" ]]; then
			CHART_NAME=$(list_helm_chart ${CHART_DIR_URL})
			CHART_URL=$CHART_DIR_URL/$CHART_NAME
			down_load_udm_chart_unzip ${CHART_URL} ${CHART_NAME}
			helm_template_chart 
		else
			break;
		fi
	done
}

#list_cci_dir $RB_REMOTE_ROOT
typeset -A UDM_RELEASE_LIST=$(list_cci_dir $RB_REMOTE_ROOT)
PS3="Select a AUSF_UDM Release: "
select UDM_RELEASE in ${UDM_RELEASE_LIST[*]}
do
	if [[ ${UDM_RELEASE} != "" ]]; then
		select_udm_version ${UDM_RELEASE}
	else
		break;
	fi
done

