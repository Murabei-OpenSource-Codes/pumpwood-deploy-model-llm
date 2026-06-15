"""Kubernetes deployment package for the Pumpwood Model LLM microservice.

Use ``PumpWoodModelLLMMicroservice`` with ``DeployPumpWood`` from
``pumpwood-deploy`` to generate and apply model-llm manifests.

Example:
    ```python
    from pumpwood_deploy_model_llm import PumpWoodModelLLMMicroservice

    model_llm = PumpWoodModelLLMMicroservice(
        app_version="1.0",
        worker_embedding_version="1.0",
        worker_extraction_version="1.0",
        worker_segmentation_version="1.0",
    )
    deploy.add_microservice(model_llm)
    ```

Cluster prerequisites include ``StandardMicroservices`` (storage
ConfigMap, general secrets, RabbitMQ), ``PumpWoodAuthMicroservice`` for
authorization, and Postgres via ``PGBouncerDatabase``.
"""
from .deploy import PumpWoodModelLLMMicroservice

__all__ = [
    PumpWoodModelLLMMicroservice
]
