# Nitin Singh Rathore

**MS Computer Science · UT Arlington · Graduating December 2026**

My thesis research is on fault-tolerant control for autonomous UAV swarms. The core problem: when a standard controller like PID encounters a fault, it keeps pushing harder regardless of whether the error is from wind, a bad sensor, or a broken link. The supervisory layer I built watches the whole swarm, separates real failure conditions from normal tracking error, and changes how drones respond before the situation destabilizes. Validated across 30 randomized seeds with controlled fault injection. Paper under review at IEEE Network Magazine, 2026.

Currently seeking a **Fall 2026 internship** in autonomy engineering, robotics simulation, or software engineering.

---

## Projects

**[UAV Autonomy Research Suite](https://github.com/Nitin3560/uav-autonomy-research-suite)**
Fault-tolerant UAV swarm simulation and validation framework - thesis project at UT Arlington.
- Failure-aware supervisory control over PID with fault injection across wind, sensor corruption and communication dropout
- CTDE-MAPPO multi-agent RL policies for adaptive relay coordination under degraded comms
- ROS2 telemetry bridge, 30-seed evaluation pipelines, Docker for reproducibility

> Kept private during thesis approval and peer review. Now open source.

**[Traceback AI](https://github.com/Nitin3560/traceback-ai)**
Root cause analysis system for distributed microservice failures - showcased at Nexus Hackathon.
- FastAPI backend ingesting logs, metrics and deployment events across 10+ microservices
- Graph traversal for failure propagation tracing, Z-score anomaly detection cutting false positives by 30%
- Multi-factor ranking engine surfacing correct root cause in top-3 results 87% of the time

**[JobPrep AI](https://github.com/Nitin3560/JobPrep-AI-Conversational-RAG-Document-Assistant)**
Conversational RAG assistant that generates personalized job application answers from a candidate's resume - runs fully offline via Ollama.
- LlamaIndex vector search with sub 2 second response times, deployed on GCP serving 12-15 active users
- 45% improvement in indexing efficiency through incremental embedding logic

---

## Stack

| Domain | Tools |
|---|---|
| Simulation | PyBullet · Gym-PyBullet-Drones · Gymnasium |
| Autonomy and control | ROS2 · CTDE-MAPPO · RLlib · PettingZoo |
| Backend and systems | FastAPI · PostgreSQL · Docker |
| AI and ML | LLMs · RAG · Anomaly detection |
| Languages | Python · C++ |
| Infrastructure | GCP · AWS |

---

## Links

[Portfolio](https://nitinsinghrathore.us) · [LinkedIn](https://linkedin.com/in/nitin-singh-rathore) · [UAV Research](https://github.com/Nitin3560/uav-autonomy-research-suite) · nxr3560@mavs.uta.edu
