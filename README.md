# Nitin Singh Rathore

MS Computer Science · UT Arlington · Graduating December 2026 · [Portfolio](https://nitinsinghrathore.us) · [LinkedIn](https://linkedin.com/in/nitin-singh-rathore) · nxr3560@mavs.uta.edu

---

My thesis research is on fault-tolerant control for autonomous UAV swarms. The core problem: when a standard controller like PID encounters a fault, it keeps pushing harder regardless of whether the error is from wind, a bad sensor, or a broken link. The supervisory layer I built watches the whole swarm, separates real failure conditions from normal tracking error, and changes how drones respond before the situation destabilizes. Validated across 30 randomized seeds with controlled fault injection. GTA at UT Arlington - taught C and C++ programming to undergraduate students.

**Paper under review · IEEE Network Magazine, 2026**

Currently seeking a Fall 2026 internship in autonomy engineering, robotics simulation, or software engineering.

---

## Projects

**[UAV Autonomy Research Suite](https://github.com/Nitin3560/uav-autonomy-research-suite)**
Fault-tolerant UAV swarm simulation and validation framework · MS thesis at UT Arlington

- Failure-aware supervisory control over PID with fault injection across wind, sensor corruption and communication dropout
- CTDE-MAPPO multi-agent RL policies for adaptive relay coordination under degraded comms
- ROS2 telemetry bridge, 30-seed evaluation pipelines, Docker and ROS2 Jazzy for reproducibility

> Kept private during thesis approval and peer review. Now open source.

<br>

**[Traceback AI](https://github.com/Nitin3560/traceback-ai)**
Root cause analysis system for distributed microservice failures · Nexus Hackathon

- FastAPI backend ingesting logs, metrics and deployment events across 10+ microservices
- Graph traversal for failure propagation tracing, Z-score anomaly detection cutting false positives by 30%
- Multi-factor ranking engine surfacing correct root cause in top-3 results 87% of the time

<br>

**[JobPrep AI](https://github.com/Nitin3560/JobPrep-AI-Conversational-RAG-Document-Assistant)**
Conversational RAG assistant generating personalized job application answers from a candidate's resume · runs fully offline via Ollama

- LlamaIndex vector search with sub-2s response times, deployed on GCP serving 12-15 active users
- 45% improvement in indexing efficiency through incremental embedding logic

---

## Stack

**Autonomy and simulation**

![ROS2](https://img.shields.io/badge/ROS2-22314E?style=flat&logo=ros&logoColor=white)
![PyBullet](https://img.shields.io/badge/PyBullet-306998?style=flat&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

**AI and ML**

![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![RLlib](https://img.shields.io/badge/RLlib-028CF0?style=flat&logoColor=white)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-000000?style=flat&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat&logoColor=white)

**Backend and infrastructure**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat&logo=googlecloud&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws&logoColor=white)

