import json
import logging
import os
import pytest
import threading
import time

from ocs_ci.framework import config
from ocs_ci.ocs import constants, ocp
from ocs_ci.utility.prometheus import PrometheusAPI


logger = logging.getLogger(__name__)


def measure_operation(
    operation,
    result_file,
    minimal_time=None,
    metadata=None,
    measure_after=False
):
    """
    Get dictionary with keys 'start', 'stop', 'metadata' and 'result' that
    contain information about start and stop time of given function and its
    result.

    Args:
        operation (function): Function to be performed
        result_file (str): File name that should contain measurement results
            including logs in json format. If this file exists then it is
            used for test.
        minimal_time (int): Minimal number of seconds to monitor a system.
            If provided then monitoring of system continues even when
            operation is finshed. If not specified then measurement is finished
            when operation is complete
        metadata (dict): This can contain dictionary object with information
            relevant to test (e.g. volume name, operating host, ...)
        measure_after (bool): Determine if time measurement is done before or
            after the operation returns its state. This can be useful e.g.
            for capacity utilization testing where operation fills capacity
            and utilized data are measured after the utilization is completed

    Returns:
        dict: contains information about `start` and `stop` time of given
            function and its `result` and provided `metadata`
            Example:
            {
                'start': 1569827653.1903834,
                'stop': 1569828313.6469617,
                'result': 'rook-ceph-osd-2',
                'metadata': {'status': 'success'},
                'prometheus_alerts': [{'labels': ...}, {...}, ...]
            }
    """
    def prometheus_log(info, alert_list):
        """
        Log all alerts from Prometheus API every 3 seconds.

        Args:
            info (dict): Contains run key attribute that controls thread.
                If `info['run'] == False` then thread will stop
            alert_list (list): List to be populated with alerts
        """
        prometheus = PrometheusAPI()
        logger.info('Logging of all prometheus alerts started')
        while info.get('run'):
            alerts_response = prometheus.get(
                'alerts',
                payload={
                    'silenced': False,
                    'inhibited': False
                }
            )
            msg = f"Request {alerts_response.request.url} failed"
            assert alerts_response.ok, msg
            for alert in alerts_response.json().get('data').get('alerts'):
                if alert not in alert_list:
                    logger.info(f"Adding {alert} to alert list")
                    alert_list.append(alert)
            time.sleep(3)
        logger.info('Logging of all prometheus alerts stopped')

    # check if file with results for this operation already exists
    # if it exists then use it
    if os.path.isfile(result_file) and os.access(result_file, os.R_OK):
        logger.info(
            f"File {result_file} already created."
            f" Trying to use it for tests..."
        )
        with open(result_file) as open_file:
            results = json.load(open_file)
        logger.info(
            f"File {result_file} loaded. Content of file:\n{results}"
        )

    # if there is no file with results from previous run
    # then perform operation measurement
    else:
        logger.info(
            f"File {result_file} not created yet. Starting measurement..."
        )
        if not measure_after:
            start_time = time.time()

        # init logging thread that checks for Prometheus alerts
        # while workload is running
        # based on https://docs.python.org/3/howto/logging-cookbook.html#logging-from-multiple-threads
        info = {'run': True}
        alert_list = []

        logging_thread = threading.Thread(
            target=prometheus_log,
            args=(info, alert_list)
        )
        logging_thread.start()

        result = operation()
        if measure_after:
            start_time = time.time()
        passed_time = time.time() - start_time
        if minimal_time:
            additional_time = minimal_time - passed_time
            if additional_time > 0:
                time.sleep(additional_time)
        stop_time = time.time()
        info['run'] = False
        logging_thread.join()
        results = {
            'start': start_time,
            'stop': stop_time,
            'result': result,
            'metadata': metadata,
            'prometheus_alerts': alert_list
        }
        logger.info(f"Results of measurement: {results}")
        with open(result_file, 'w') as outfile:
            logger.info(f"Dumping results of measurement into {result_file}")
            json.dump(results, outfile)
    return results


@pytest.fixture
def measurement_dir(tmp_path):
    """
    Returns directory path where should be stored all results related
    to measurement. If 'measurement_dir' is provided by config then use it,
    otherwise new directory is generated.

    Returns:
        str: Path to measurement directory
    """
    if config.ENV_DATA.get('measurement_dir'):
        measurement_dir = config.ENV_DATA.get('measurement_dir')
        logger.info(
            f"Using measurement dir from configuration: {measurement_dir}"
        )
    else:
        measurement_dir = os.path.join(
            os.path.dirname(tmp_path),
            'measurement_results'
        )
    if not os.path.exists(measurement_dir):
        logger.info(
            f"Measurement dir {measurement_dir} doesn't exist. Creating it."
        )
        os.mkdir(measurement_dir)
    return measurement_dir


@pytest.fixture
def measure_stop_ceph_mgr(measurement_dir):
    """
    Downscales Ceph Manager deployment, measures the time when it was
    downscaled and monitors alerts that were triggered during this event.

    Returns:
        dict: Contains information about `start` and `stop` time for stopping
            Ceph Manager pod
    """
    oc = ocp.OCP(
        kind=constants.DEPLOYMENT,
        namespace=config.ENV_DATA['cluster_namespace']
    )
    mgr_deployments = oc.get(selector=constants.MGR_APP_LABEL)['items']
    mgr = mgr_deployments[0]['metadata']['name']

    def stop_mgr():
        """
        Downscale Ceph Manager deployment for 6 minutes. First 5 minutes
        the alert should be in 'Pending'.
        After 5 minutes it should be 'Firing'.
        This configuration of monitoring can be observed in ceph-mixins which
        are used in the project:
            https://github.com/ceph/ceph-mixins/blob/d22afe8c0da34490cb77e52a202eefcf4f62a869/config.libsonnet#L25

        Returns:
            str: Name of downscaled deployment
        """
        # run_time of operation
        run_time = 60 * 6
        nonlocal oc
        nonlocal mgr
        logger.info(f"Downscaling deployment {mgr} to 0")
        oc.exec_oc_cmd(f"scale --replicas=0 deployment/{mgr}")
        logger.info(f"Waiting for {run_time} seconds")
        time.sleep(run_time)
        return oc.get(mgr)

    test_file = os.path.join(measurement_dir, 'measure_stop_ceph_mgr.json')
    measured_op = measure_operation(stop_mgr, test_file)
    logger.info(f"Upscaling deployment {mgr} back to 1")
    oc.exec_oc_cmd(f"scale --replicas=1 deployment/{mgr}")
    return measured_op


@pytest.fixture
def measure_stop_ceph_mon(measurement_dir):
    """
    Downscales Ceph Monitor deployment, measures the time when it was
    downscaled and monitors alerts that were triggered during this event.

    Returns:
        dict: Contains information about `start` and `stop` time for stopping
            Ceph Monitor pod
    """
    oc = ocp.OCP(
        kind=constants.DEPLOYMENT,
        namespace=config.ENV_DATA['cluster_namespace']
    )
    mon_deployments = oc.get(selector=constants.MON_APP_LABEL)['items']
    mons = [
        deployment['metadata']['name']
        for deployment in mon_deployments
    ]

    # get monitor deployments to stop, leave even number of monitors
    split_index = len(mons) // 2 if len(mons) > 3 else 2
    mons_to_stop = mons[split_index:]
    logger.info(f"Monitors to stop: {mons_to_stop}")
    logger.info(f"Monitors left to run: {mons[:split_index]}")

    def stop_mon():
        """
        Downscale Ceph Monitor deployments for 12 minutes. First 15 minutes
        the alert CephMonQuorumAtRisk should be in 'Pending'. After 15 minutes
        the alert turns into 'Firing' state.
        This configuration of monitoring can be observed in ceph-mixins which
        are used in the project:
            https://github.com/ceph/ceph-mixins/blob/d22afe8c0da34490cb77e52a202eefcf4f62a869/config.libsonnet#L16
        `Firing` state shouldn't actually happen because monitor should be
        automatically redeployed shortly after 10 minutes.

        Returns:
            str: Names of downscaled deployments
        """
        # run_time of operation
        run_time = 60 * 12
        nonlocal oc
        nonlocal mons_to_stop
        for mon in mons_to_stop:
            logger.info(f"Downscaling deployment {mon} to 0")
            oc.exec_oc_cmd(f"scale --replicas=0 deployment/{mon}")
        logger.info(f"Waiting for {run_time} seconds")
        time.sleep(run_time)
        return mons_to_stop

    test_file = os.path.join(measurement_dir, 'measure_stop_ceph_mon.json')
    measured_op = measure_operation(stop_mon, test_file)

    # get new list of monitors to make sure that new monitors were deployed
    mon_deployments = oc.get(selector=constants.MON_APP_LABEL)['items']
    mons = [
        deployment['metadata']['name']
        for deployment in mon_deployments
    ]

    # check that downscaled monitors are removed as OCS should redeploy them
    check_old_mons_deleted = all(mon not in mons for mon in mons_to_stop)
    if not check_old_mons_deleted:
        for mon in mons_to_stop:
            logger.info(f"Upscaling deployment {mon} back to 1")
            oc.exec_oc_cmd(f"scale --replicas=1 deployment/{mon}")
        msg = f"Downscaled monitors {mons_to_stop} were not replaced"
        assert check_old_mons_deleted, msg

    return measured_op


@pytest.fixture
def measure_stop_ceph_osd(measurement_dir):
    """
    Downscales Ceph osd deployment, measures the time when it was
    downscaled and alerts that were triggered during this event.

    Returns:
        dict: Contains information about `start` and `stop` time for stopping
            Ceph osd pod
    """
    oc = ocp.OCP(
        kind=constants.DEPLOYMENT,
        namespace=config.ENV_DATA.get('cluster_namespace')
    )
    osd_deployments = oc.get(selector=constants.OSD_APP_LABEL).get('items')
    osds = [
        deployment.get('metadata').get('name')
        for deployment in osd_deployments
    ]

    # get osd deployments to stop, leave even number of osd
    osd_to_stop = osds[-1]
    logger.info(f"osd disks to stop: {osd_to_stop}")
    logger.info(f"osd disks left to run: {osds[:-1]}")

    def stop_osd():
        """
        Downscale Ceph osd deployments for 11 minutes. First 1 minutes
        the alert CephOSDDiskNotResponding should be in 'Pending'.
        After 1 minute the alert turns into 'Firing' state.
        This configuration of osd can be observed in ceph-mixins which
        is used in the project:
            https://github.com/ceph/ceph-mixins/blob/d22afe8c0da34490cb77e52a202eefcf4f62a869/config.libsonnet#L21
        There should be also CephClusterWarningState alert that takes 10
        minutest to be firing.

        Returns:
            str: Names of downscaled deployments
        """
        # run_time of operation
        run_time = 60 * 11
        nonlocal oc
        nonlocal osd_to_stop
        logger.info(f"Downscaling deployment {osd_to_stop} to 0")
        oc.exec_oc_cmd(f"scale --replicas=0 deployment/{osd_to_stop}")
        logger.info(f"Waiting for {run_time} seconds")
        time.sleep(run_time)
        return osd_to_stop

    test_file = os.path.join(measurement_dir, 'measure_stop_ceph_osd.json')
    measured_op = measure_operation(stop_osd, test_file)
    logger.info(f"Upscaling deployment {osd_to_stop} back to 1")
    oc.exec_oc_cmd(f"scale --replicas=1 deployment/{osd_to_stop}")

    return measured_op
