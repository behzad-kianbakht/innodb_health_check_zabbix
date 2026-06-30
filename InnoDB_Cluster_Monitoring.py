#!/usr/bin/python3.12

# Developed by : Behzad Kianbakht (2025/10/05) - Full MYSQLInnodb Cluster Monitoring
# ---------------------------------------------------------------------------------------

import subprocess
import json
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os

# --- Logging setup ---
log_date = datetime.now().strftime("%Y-%m-%d")

LOG_BASE_DIR = "/var/log/zabbix/MysqlInnodb" # Should be Created If not exist
MYSQLSH_LOG_DIR = os.path.join(LOG_BASE_DIR, "mysqlsh") # For Prevent Mysqlsh OS and Zabbix User Log

os.makedirs(LOG_BASE_DIR, exist_ok=True)
os.makedirs(MYSQLSH_LOG_DIR, exist_ok=True)

logger = logging.getLogger("MysqlInnodb")
logger.setLevel(logging.DEBUG)

log_file = f"{LOG_BASE_DIR}/MySQL_InnoDB_log_{log_date}.log"
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# --- Argument validation ---
if len(sys.argv) < 5:
    print("Usage: script.py <value|discovery> <user> <password> [host1,host2,...]")
    sys.exit(1)

SCRIPTTYPE = sys.argv[1] # Script Work in two Mode : value or discovery
USERNAME = sys.argv[2]   # Innodb Cluster Member UserName
PASSWORD = sys.argv[3]   # Innodb Cluster Member Password
HOSTNAME_LIST = sys.argv[4].strip("[]").split(",") # Innodb Cluster Member "LIST" - Code develop that can work Just with one node

logger.info("=============== InnoDB Cluster Check ===============")
logger.info(f"Mode: {SCRIPTTYPE}")
logger.info(f"Node list to check: {HOSTNAME_LIST}")

env = os.environ.copy()
env["MYSQLSH_LOGDIR"] = MYSQLSH_LOG_DIR

# --- Main logic ---
for HOSTNAME in HOSTNAME_LIST:
    HOSTNAME = HOSTNAME.strip()
    if not HOSTNAME:
        continue

    logger.info(f"Checking node: {HOSTNAME}")

    command = [
        "mysqlsh",
        "--js",
        f"{USERNAME}@{HOSTNAME}:3306",
        f"-p{PASSWORD}",
        "--result-format=json",
        "--",
        "cluster",
        "status"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=50,
            cwd=MYSQLSH_LOG_DIR,
            env=env
        )

        if result.returncode != 0:
            logger.error(f"[{HOSTNAME}] mysqlsh failed (return code {result.returncode})")
            logger.error(f"[{HOSTNAME}] STDERR: {result.stderr.strip()}")
            continue

        try:
            data = json.loads(result.stdout)
            cluster_name = data.get("clusterName", "UnknownCluster")
            cluster_status = data.get("defaultReplicaSet", {}).get("status", "Unknown")
            logger.info(f"[{HOSTNAME}] SUCCESS - Cluster '{cluster_name}' is {cluster_status}")
            logger.debug(f"[{HOSTNAME}] Full JSON output: {json.dumps(data, indent=4)}")

            # --- Handle script modes ---
            if SCRIPTTYPE == "value":
                print(json.dumps(data, indent=4))
                break

            elif SCRIPTTYPE == "discovery":
                topology = data.get("defaultReplicaSet", {}).get("topology", {})
                if not topology:
                    logger.warning(f"[{HOSTNAME}] No topology data found.")
                    print(json.dumps([], indent=4))
                    break

                discovery_list = [{'{#MEMBER}': member} for member in topology.keys()]
                print(json.dumps(discovery_list, indent=4))
                break

            else:
                print("Error - Invalid mode (must be 'value' or 'discovery')")
                break

        except json.JSONDecodeError:
            logger.error(f"[{HOSTNAME}] Failed to parse JSON output")
            logger.debug(f"[{HOSTNAME}] Raw STDOUT: {result.stdout.strip()}")
            continue

    except subprocess.TimeoutExpired:
        logger.error(f"[{HOSTNAME}] Command timed out after 15 seconds")
        continue

logger.info("=====================================================")