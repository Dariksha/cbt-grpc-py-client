# cbt-grpc-py-client

## Summary
A simple python client to call ChangedBlockTracking gRPC endpoints.
The gRPC endpoints are hosted in Cerebro uising V4 platform generated protos from ntnx-api-data-protection-grpc repo (TDOD: add link to repo)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
We need to specify PE IP and port for gRPC communication and type of CBT call, i.e either 'vm' or 'volume_group'.

```bash
python cbt_grpc_client.py <PE_IP>:<PORT> 'vm'
```