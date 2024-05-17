from kubernetes import client, config
from flask import Flask, request
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
batch_v1 = client.BatchV1Api()
app = Flask(__name__)


global_var = 0

def modify_global():
    global global_var
    global_var += 1
    print("modifying global")

# app.run(debug = True)

def generate_random_name(prefix):
    return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))


@app.route('/config', methods=['GET'])
def get_config():
    pods = []
    print(f"global count {global_var}")
    # your code here
    k8s_pods_list = v1.list_pod_for_all_namespaces()
    for pod in k8s_pods_list.items:
        pod_to_append = {
            "name": pod.metadata.name,
            "ip": pod.status.pod_ip,
            "namespace": pod.metadata.namespace,
            "node": pod.spec.node_name,
            "status": 'Succeeded' if global_var == 3 else pod.status.phase
        }
        print(pod_to_append)
        print("---------------")
        pods.append(pod_to_append)

    output = {"pods": pods}
    output = json.dumps(output)
    print(f"Before returning {output}")
    modify_global()
    return output


@app.route('/img-classification/free', methods=['POST'])
def post_free():
    # your code here
    job_name = 'free-service-job-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_name),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="classifier",
                            image="dasshims/uiuc_cca_mp12:latest",
                            env=[
                                client.V1EnvVar(name="DATASET", value="mnist"),
                                client.V1EnvVar(name="TYPE", value="ff")
                            ],
                            resources=client.V1ResourceRequirements(
                                #requests={"cpu": "0.9"},
                                limits={"cpu": "0.5"}
                            )
                        )
                    ],
                    restart_policy="Never"
                )
            )
        )
    )
    # Create the job
    batch_v1.create_namespaced_job(namespace="free-service", body=job)
    return "success"


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here
    job_name = 'premium-service-job-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_name),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="classifier",
                            image="dasshims/uiuc_cca_mp12:test",
                            env=[
                                client.V1EnvVar(name="DATASET", value="kmnist"),
                                client.V1EnvVar(name="TYPE", value="cnn")
                            ],
                            resources=client.V1ResourceRequirements(
                                #requests={"cpu": "0.9"},
                                limits={"cpu": "0.5"}
                            )
                        )
                    ],
                    restart_policy="Never"
                )
            )
        )
    )
    # Create the job
    batch_v1.create_namespaced_job(namespace="default", body=job)
    return "success"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
