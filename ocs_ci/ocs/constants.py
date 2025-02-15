"""
Constants module.

This module contains any values that are widely used across the framework,
utilities, or tests that will predominantly remain unchanged.

In the event values here have to be changed it should be under careful review
and with consideration of the entire project.

"""
import os

# Directories
TOP_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
TEMPLATE_DIR = os.path.join(TOP_DIR, "ocs_ci", "templates")
EXTERNAL_DIR = os.path.join(TOP_DIR, "external")
TEMPLATE_DEPLOYMENT_DIR = os.path.join(TEMPLATE_DIR, "ocs-deployment")
TEMPLATE_CSI_DIR = os.path.join(TEMPLATE_DIR, "CSI")
TEMPLATE_CSI_RBD_DIR = os.path.join(TEMPLATE_CSI_DIR, "rbd")
TEMPLATE_CSI_FS_DIR = os.path.join(TEMPLATE_CSI_DIR, "cephfs")
TEMPLATE_PV_PVC_DIR = os.path.join(TEMPLATE_DIR, "pv_pvc")
TEMPLATE_APP_POD_DIR = os.path.join(TEMPLATE_DIR, "app-pods")
TEMPLATE_WORKLOAD_DIR = os.path.join(TEMPLATE_DIR, "workloads")
TEMPLATE_FIO_DIR = os.path.join(TEMPLATE_WORKLOAD_DIR, "fio")
TEMPLATE_SMALLFILE_DIR = os.path.join(TEMPLATE_WORKLOAD_DIR, "smallfile")
TEMPLATE_PGSQL_DIR = os.path.join(TEMPLATE_WORKLOAD_DIR, "pgsql")
TEMPLATE_PGSQL_SERVER_DIR = os.path.join(TEMPLATE_PGSQL_DIR, "server")
TEMPLATE_MCG_DIR = os.path.join(TEMPLATE_DIR, "mcg")
TEMPLATE_OPENSHIFT_INFRA_DIR = os.path.join(
    TEMPLATE_DIR, "openshift-infra/"
)
TEMPLATE_CONFIGURE_PVC_MONITORING_POD = os.path.join(
    TEMPLATE_OPENSHIFT_INFRA_DIR, "monitoring/"
)
TEMPLATE_DEPLOYMENT_LOGGING = os.path.join(
    TEMPLATE_OPENSHIFT_INFRA_DIR, "logging-deployment"
)
TEMPLATE_DEPLOYMENT_EO = os.path.join(
    TEMPLATE_DEPLOYMENT_LOGGING, "elasticsearch_operator"
)
TEMPLATE_DEPLOYMENT_CLO = os.path.join(
    TEMPLATE_DEPLOYMENT_LOGGING, "clusterlogging_operator"
)
DATA_DIR = os.path.join(TOP_DIR, 'data')
ROOK_REPO_DIR = os.path.join(DATA_DIR, 'rook')
ROOK_EXAMPLES_DIR = os.path.join(
    ROOK_REPO_DIR, "cluster", "examples", "kubernetes", "ceph"
)
ROOK_CSI_RBD_DIR = os.path.join(ROOK_EXAMPLES_DIR, "csi", "rbd")
ROOK_CSI_CEPHFS_DIR = os.path.join(ROOK_EXAMPLES_DIR, "csi", "cephfs")


# Statuses
STATUS_PENDING = 'Pending'
STATUS_CONTAINER_CREATING = 'ContainerCreating'
STATUS_AVAILABLE = 'Available'
STATUS_RUNNING = 'Running'
STATUS_TERMINATING = 'Terminating'
STATUS_BOUND = 'Bound'
STATUS_RELEASED = 'Released'
STATUS_COMPLETED = 'Completed'

# Resources / Kinds
CEPHFILESYSTEM = "CephFileSystem"
CEPHBLOCKPOOL = "CephBlockPool"
DEPLOYMENT = "Deployment"
STORAGECLASS = "StorageClass"
PV = "PersistentVolume"
PVC = "PersistentVolumeClaim"
POD = "Pod"
ROUTE = "Route"
NODE = "Node"
DEPLOYMENTCONFIG = "deploymentconfig"
CONFIG = "Config"
MACHINESETS = 'machinesets'
STORAGECLUSTER = 'storagecluster'

# Provisioners
AWS_EFS_PROVISIONER = "openshift.org/aws-efs"
ROLE = 'Role'
ROLEBINDING = "Rolebinding"
SUBSCRIPTION = "Subscription"
NAMESPACES = "Namespaces"
CLUSTER_LOGGING = "ClusterLogging"
OPERATOR_GROUP = "OperatorGroup"
SERVICE_ACCOUNT = "Serviceaccount"
SCC = "SecurityContextConstraints"
PRIVILEGED = "privileged"
CLUSTER_SERVICE_VERSION = 'csv'

# Other
SECRET = "Secret"
NAMESPACE = 'Namespace'
IGNORE_SC_GP2 = "gp2"
IGNORE_SC_FLEX = "rook-ceph-block"
TEST_FILES_BUCKET = "ocsci-test-files"
ROOK_REPOSITORY = "https://github.com/rook/rook.git"
OPENSHIFT_MACHINE_API_NAMESPACE = "openshift-machine-api"
OPENSHIFT_LOGGING_NAMESPACE = "openshift-logging"
OPENSHIFT_OPERATORS_REDHAT_NAMESPACE = "openshift-operators-redhat"
OPENSHIFT_IMAGE_REGISTRY_NAMESPACE = "openshift-image-registry"
OPENSHIFT_INGRESS_NAMESPACE = "openshift-ingress"
MASTER_MACHINE = "master"
WORKER_MACHINE = "worker"
MOUNT_POINT = '/var/lib/www/html'
OCP_QE_MISC_REPO = (
    "http://git.host.prod.eng.bos.redhat.com/git/openshift-misc.git"
)

OCS_WORKLOADS = "https://github.com/red-hat-storage/ocs-workloads"

UPI_INSTALL_SCRIPT = "upi_on_aws-install.sh"

DEFAULT_SECRET = 'rook-ceph-csi'
DEFAULT_BLOCKPOOL = 'rbd'
DEFAULT_SC_CEPHFS = "rook-ceph-cephfs"
DEFAULT_ROUTE_CRT = "router-certs-default"
IMAGE_REGISTRY_RESOURCE_NAME = "cluster"

# encoded value of 'admin'
ADMIN_USER = 'admin'
GB = 1024 ** 3
GB2KB = 1024 ** 2
DEFAULT_DISK_SIZE = 100

# Reclaim Policy
RECLAIM_POLICY_RETAIN = 'Retain'
RECLAIM_POLICY_DELETE = 'Delete'

# Access Mode
ACCESS_MODE_RWO = 'ReadWriteOnce'
ACCESS_MODE_ROX = 'ReadOnlyMany'
ACCESS_MODE_RWX = 'ReadWriteMany'

# Pod label
MON_APP_LABEL = "app=rook-ceph-mon"
MDS_APP_LABEL = "app=rook-ceph-mds"
TOOL_APP_LABEL = "app=rook-ceph-tools"
MGR_APP_LABEL = "app=rook-ceph-mgr"
OSD_APP_LABEL = "app=rook-ceph-osd"
OPERATOR_LABEL = "app=rook-ceph-operator"
CSI_CEPHFSPLUGIN_PROVISIONER_LABEL = "app=csi-cephfsplugin-provisioner"
CSI_RBDPLUGIN_PROVISIONER_LABEL = "app=csi-rbdplugin-provisioner"
CSI_CEPHFSPLUGIN_LABEL = "app=csi-cephfsplugin"
CSI_RBDPLUGIN_LABEL = "app=csi-rbdplugin"
OCS_OPERATOR_LABEL = "name=ocs-operator"
LOCAL_STORAGE_OPERATOR_LABEL = "name=local-storage-operator"
NOOBAA_APP_LABEL = "app=noobaa"
DEFAULT_DEVICESET_PVC_NAME = "example-deviceset"
DEFAULT_MON_PVC_NAME = "rook-ceph-mon"


# YAML paths
TOOL_POD_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_DIR, "toolbox_pod.yaml"
)

CEPHFILESYSTEM_YAML = os.path.join(
    TEMPLATE_CSI_FS_DIR, "CephFileSystem.yaml"
)

CEPHBLOCKPOOL_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_DIR, "cephblockpool.yaml"
)

CSI_RBD_STORAGECLASS_YAML = os.path.join(
    TEMPLATE_CSI_RBD_DIR, "storageclass.yaml"
)

ROOK_CSI_RBD_STORAGECLASS_YAML = os.path.join(
    ROOK_CSI_RBD_DIR, "storageclass.yaml"
)

CSI_CEPHFS_STORAGECLASS_YAML = os.path.join(
    TEMPLATE_CSI_FS_DIR, "storageclass.yaml"
)

ROOK_CSI_CEPHFS_STORAGECLASS_YAML = os.path.join(
    ROOK_CSI_CEPHFS_DIR, "storageclass.yaml"
)

CSI_PVC_YAML = os.path.join(
    TEMPLATE_PV_PVC_DIR, "PersistentVolumeClaim.yaml"
)

MCG_OBC_YAML = os.path.join(
    TEMPLATE_MCG_DIR, "ObjectBucketClaim.yaml"
)

CSI_RBD_POD_YAML = os.path.join(
    TEMPLATE_CSI_RBD_DIR, "pod.yaml"
)

CSI_RBD_RAW_BLOCK_POD_YAML = os.path.join(
    TEMPLATE_APP_POD_DIR, "raw_block_pod.yaml"
)

CSI_CEPHFS_POD_YAML = os.path.join(
    TEMPLATE_CSI_FS_DIR, "pod.yaml"
)
CSI_RBD_SECRET_YAML = os.path.join(
    TEMPLATE_CSI_RBD_DIR, "secret.yaml"
)

CSI_CEPHFS_SECRET_YAML = os.path.join(
    TEMPLATE_CSI_FS_DIR, "secret.yaml"
)

CSI_CEPHFS_PVC_YAML = os.path.join(
    TEMPLATE_CSI_FS_DIR, "pvc.yaml"
)

CSI_RBD_PVC_YAML = os.path.join(
    TEMPLATE_CSI_RBD_DIR, "pvc.yaml"
)
CONFIGURE_PVC_ON_MONITORING_POD = os.path.join(
    TEMPLATE_CONFIGURE_PVC_MONITORING_POD, "configuring_pvc.yaml"
)

PGSQL_SERVICE_YAML = os.path.join(
    TEMPLATE_PGSQL_SERVER_DIR, "Service.yaml"
)

PGSQL_CONFIGMAP_YAML = os.path.join(
    TEMPLATE_PGSQL_SERVER_DIR, "ConfigMap.yaml"
)

PGSQL_STATEFULSET_YAML = os.path.join(
    TEMPLATE_PGSQL_SERVER_DIR, "StatefulSet.yaml"
)

PGSQL_BENCHMARK_YAML = os.path.join(
    TEMPLATE_PGSQL_DIR, "PGSQL_Benchmark.yaml"
)

SMALLFILE_BENCHMARK_YAML = os.path.join(
    TEMPLATE_SMALLFILE_DIR, "SmallFile.yaml"
)

NGINX_POD_YAML = os.path.join(
    TEMPLATE_APP_POD_DIR, "nginx.yaml"
)

AWSCLI_POD_YAML = os.path.join(
    TEMPLATE_APP_POD_DIR, "awscli.yaml"
)

SERVICE_ACCOUNT_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_DIR, "service_account.yaml"
)

FEDORA_DC_YAML = os.path.join(
    TEMPLATE_APP_POD_DIR, "fedora_dc.yaml"
)

# Openshift-logging elasticsearch operator deployment yamls
EO_NAMESPACE_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_EO, "eo-project.yaml"
)

EO_OG_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_EO, "eo-og.yaml"
)
EO_RBAC_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_EO, "eo-rbac.yaml"
)
EO_SUB_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_EO, "eo-sub.yaml"
)

DEVICESET_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_DIR, "deviceset.yaml"
)

# Openshift-logging clusterlogging operator deployment yamls
CL_NAMESPACE_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_CLO, "cl-namespace.yaml"
)
CL_OG_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_CLO, "cl-og.yaml"
)
CL_SUB_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_CLO, "cl-sub.yaml"
)
CL_INSTANCE_YAML = os.path.join(
    TEMPLATE_DEPLOYMENT_CLO, "instance.yaml"
)

# Workload-io yamls
FIO_IO_PARAMS_YAML = os.path.join(
    TEMPLATE_FIO_DIR, "workload_io.yaml"
)
FIO_IO_RW_PARAMS_YAML = os.path.join(
    TEMPLATE_FIO_DIR, "workload_io_rw.yaml"
)

# Openshift infra yamls:
RSYNC_POD_YAML = os.path.join(
    TEMPLATE_OPENSHIFT_INFRA_DIR, "rsync-pod.yaml"
)

# constants
RBD_INTERFACE = 'rbd'
CEPHFS_INTERFACE = 'cephfs'
RAW_BLOCK_DEVICE = '/dev/block'

# EC2 instance statuses
INSTANCE_PENDING = 0
INSTANCE_STOPPING = 64
INSTANCE_STOPPED = 80
INSTANCE_RUNNING = 16
INSTANCE_SHUTTING_DOWN = 32
INSTANCE_TERMINATED = 48

# Node statuses
NODE_READY = 'Ready'
NODE_NOT_READY = 'NotReady'
NODE_READY_SCHEDULING_DISABLED = 'Ready,SchedulingDisabled'

# Alert labels
ALERT_CLUSTERWARNINGSTATE = 'CephClusterWarningState'
ALERT_DATARECOVERYTAKINGTOOLONG = 'CephDataRecoveryTakingTooLong'
ALERT_MGRISABSENT = 'CephMgrIsAbsent'
ALERT_MONQUORUMATRISK = 'CephMonQuorumAtRisk'
ALERT_OSDDISKNOTRESPONDING = 'CephOSDDiskNotResponding'

# OCS Deployment related constants
OPERATOR_NODE_LABEL = "cluster.ocs.openshift.io/openshift-storage=''"
OPERATOR_NODE_TAINT = "node.ocs.openshift.io/storage=true:NoSchedule"
OPERATOR_CATALOG_SOURCE_NAME = "ocs-catalogsource"
OPERATOR_CS_QUAY_API_QUERY = (
    'https://quay.io/api/v1/repository/rhceph-dev/ocs-registry/'
    'tag/?onlyActiveTags=true&limit=2'
)

# Platforms
AWS_PLATFORM = 'aws'
VSPHERE_PLATFORM = 'vsphere'

# Default SC based on platforms
DEFAULT_SC_AWS = "gp2"
DEFAULT_SC_VSPHERE = "thin"

# ignition files
BOOTSTRAP_IGN = "bootstrap.ign"
MASTER_IGN = "master.ign"
WORKER_IGN = "worker.ign"

# vSphere related constants
VSPHERE_INSTALLER_REPO = "https://github.com/openshift/installer.git"
VSPHERE_DIR = os.path.join(EXTERNAL_DIR, "installer/upi/vsphere/")
INSTALLER_IGNITION = os.path.join(VSPHERE_DIR, "machine/ignition.tf")
INSTALLER_ROUTE53 = os.path.join(VSPHERE_DIR, "route53/main.tf")
INSTALLER_MACHINE_CONF = os.path.join(VSPHERE_DIR, "machine/main.tf")
VSPHERE_CONFIG_PATH = os.path.join(TOP_DIR, "conf/ocsci/vsphere_upi_vars.yaml")
VSPHERE_MAIN = os.path.join(VSPHERE_DIR, "main.tf")
TERRAFORM_DATA_DIR = "terraform_data"
TERRAFORM_VARS = "terraform.tfvars"
VM_DISK_TYPE = "thin"
VM_DISK_MODE = "persistent"
INSTALLER_DEFAULT_DNS = "1.1.1.1"

# Config related constants
config_keys_patterns_to_censor = ['passw', 'token', 'secret']
