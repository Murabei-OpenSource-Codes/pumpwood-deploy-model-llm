"""Kubernetes deployment manifests for the Pumpwood Model LLM microservice.

This module builds Secret, Deployment, and Service YAML files for
``pumpwood-llm-model-app`` and three dataloader workers (embedding,
extraction, segmentation). Manifests are registered with
``DeployPumpWood.add_microservice`` from ``pumpwood-deploy``.

Storage bucket and type are read from the cluster ``storage`` ConfigMap
deployed by ``StandardMicroservices``.
"""
import base64
from importlib import resources
from pumpwood_deploy.abc import BasePumpwoodDeployMicroservice
from pumpwood_deploy.type import (
    PumpwoodDeploy, PumpwoodDeploySecret, PumpwoodDeployDeployment)


secrets = resources.files('pumpwood_deploy_model_llm')\
    .joinpath('resources/secrets.yml')\
    .read_text(encoding='utf-8')
deploy_app = resources.files('pumpwood_deploy_model_llm')\
    .joinpath('resources/deploy__app.yml')\
    .read_text(encoding='utf-8')
deploy_embedding_worker = resources.files('pumpwood_deploy_model_llm')\
    .joinpath('resources/deploy__embedding__worker.yml')\
    .read_text(encoding='utf-8')
deploy_extraction_worker = resources.files('pumpwood_deploy_model_llm')\
    .joinpath('resources/deploy__extraction__worker.yml')\
    .read_text(encoding='utf-8')
deploy_segmentation_worker = resources.files('pumpwood_deploy_model_llm')\
    .joinpath('resources/deploy__segmentation__worker.yml')\
    .read_text(encoding='utf-8')


class PumpWoodModelLLMMicroservice(BasePumpwoodDeployMicroservice):
    """Deploy Kubernetes manifests for the Pumpwood Model LLM microservice.

    Model LLM serves HTTP APIs for large-language-model workflows in
    Pumpwood. Three workers consume RabbitMQ messages for embedding,
    extraction, and segmentation tasks.

    The deploy class renders five manifests: model-llm secrets, the
    application (``pumpwood-llm-model-app``), and workers for embedding,
    extraction, and segmentation.

    Example:
        ```python
        import os
        from pumpwood_deploy.deploy import DeployPumpWood
        from pumpwood_deploy_model_llm import PumpWoodModelLLMMicroservice

        deploy.add_microservice(
            PumpWoodModelLLMMicroservice(
                app_version=os.getenv("PUMPWOOD_MODEL_LLM_APP"),
                worker_embedding_version=os.getenv(
                    "PUMPWOOD_MODEL_LLM_EMBEDDING"),
                worker_extraction_version=os.getenv(
                    "PUMPWOOD_MODEL_LLM_EXTRACTION"),
                worker_segmentation_version=os.getenv(
                    "PUMPWOOD_MODEL_LLM_SEGMENTATION"),
                db_host="pgbouncer-pumpwood-model-llm",
                db_database="pumpwood_model_llm",
                db_password=secrets["postgres_password"],
                microservice_password=secrets["microservice--model-llm"],
            ))
        ```
    """

    def __init__(self,
                 app_version: str,
                 worker_embedding_version: str,
                 worker_extraction_version: str,
                 worker_segmentation_version: str,
                 microservice_password: str = "microservice--model-llm",
                 db_username: str = "pumpwood",
                 db_password: str = "pumpwood",
                 db_host: str = "pgbouncer-pumpwood-model-llm",
                 db_port: str = "5432",
                 db_database: str = "pumpwood",
                 repository: str = "gcr.io/repositorio-geral-170012",
                 app_debug: str = "FALSE",
                 app_replicas: int = 1,
                 app_timeout: int = 300,
                 app_workers: int = 10,
                 app_limits_memory: str = "60Gi",
                 app_limits_cpu: str = "12000m",
                 app_requests_memory: str = "20Mi",
                 app_requests_cpu: str = "1m",
                 worker_embedding_debug: str = "FALSE",
                 worker_embedding_replicas: int = 1,
                 worker_embedding_n_parallel: int = 4,
                 worker_embedding_chunk_size: int = 1000,
                 worker_embedding_query_limit: int = 1000000,
                 worker_embedding_limits_memory: str = "60Gi",
                 worker_embedding_limits_cpu: str = "12000m",
                 worker_embedding_requests_memory: str = "20Mi",
                 worker_embedding_requests_cpu: str = "1m",
                 worker_extraction_debug: str = "FALSE",
                 worker_extraction_replicas: int = 1,
                 worker_extraction_n_parallel: int = 4,
                 worker_extraction_chunk_size: int = 1000,
                 worker_extraction_query_limit: int = 1000000,
                 worker_extraction_limits_memory: str = "60Gi",
                 worker_extraction_limits_cpu: str = "12000m",
                 worker_extraction_requests_memory: str = "20Mi",
                 worker_extraction_requests_cpu: str = "1m",
                 worker_segmentation_debug: str = "FALSE",
                 worker_segmentation_replicas: int = 1,
                 worker_segmentation_n_parallel: int = 4,
                 worker_segmentation_chunk_size: int = 1000,
                 worker_segmentation_query_limit: int = 1000000,
                 worker_segmentation_limits_memory: str = "60Gi",
                 worker_segmentation_limits_cpu: str = "12000m",
                 worker_segmentation_requests_memory: str = "20Mi",
                 worker_segmentation_requests_cpu: str = "1m"):
        """Initialize Model LLM deployment configuration.

        Args:
            app_version (str):
                Container image tag for ``pumpwood-llm-model-app``.
            worker_embedding_version (str):
                Image tag for ``pumpwood-llm-model-embedding-worker``.
            worker_extraction_version (str):
                Image tag for ``pumpwood-llm-model-extraction-worker``.
            worker_segmentation_version (str):
                Image tag for ``pumpwood-llm-model-segmentation-worker``.
            microservice_password (str):
                Password for the ``microservice--model-llm`` service user.
                Defaults to ``microservice--model-llm``.
            db_username (str):
                Postgres connection username. Defaults to ``pumpwood``.
            db_password (str):
                Postgres connection password. Defaults to ``pumpwood``.
            db_host (str):
                Postgres hostname, usually a PgBouncer service. Defaults
                to ``pgbouncer-pumpwood-model-llm``.
            db_port (str):
                Postgres port. Defaults to ``5432``.
            db_database (str):
                Postgres database name. Defaults to ``pumpwood``.
            repository (str):
                Docker registry for app and worker images. Defaults to
                ``gcr.io/repositorio-geral-170012``.
            app_debug (str):
                Debug flag for the application. Accepts ``TRUE`` or
                ``FALSE``. Defaults to ``FALSE``.
            app_replicas (int):
                Number of app pod replicas. Defaults to ``1``.
            app_timeout (int):
                Request timeout in seconds for the app. Defaults to
                ``300``.
            app_workers (int):
                Number of Granian workers for the app. Defaults to
                ``10``.
            app_limits_memory (str):
                Memory limit for app pods. Defaults to ``60Gi``.
            app_limits_cpu (str):
                CPU limit for app pods. Defaults to ``12000m``.
            app_requests_memory (str):
                Memory request for app pods. Defaults to ``20Mi``.
            app_requests_cpu (str):
                CPU request for app pods. Defaults to ``1m``.
            worker_embedding_debug (str):
                Debug flag for the embedding worker. Defaults to
                ``FALSE``.
            worker_embedding_replicas (int):
                Embedding worker pod count. Defaults to ``1``.
            worker_embedding_n_parallel (int):
                Parallel requests for embedding worker. Defaults to
                ``4``.
            worker_embedding_chunk_size (int):
                Rows per parallel batch for embedding. Defaults to
                ``1000``.
            worker_embedding_query_limit (int):
                Max rows per cycle for embedding. Defaults to
                ``1000000``.
            worker_embedding_limits_memory (str):
                Memory limit for embedding worker. Defaults to ``60Gi``.
            worker_embedding_limits_cpu (str):
                CPU limit for embedding worker. Defaults to ``12000m``.
            worker_embedding_requests_memory (str):
                Memory request for embedding worker. Defaults to
                ``20Mi``.
            worker_embedding_requests_cpu (str):
                CPU request for embedding worker. Defaults to ``1m``.
            worker_extraction_debug (str):
                Debug flag for the extraction worker. Defaults to
                ``FALSE``.
            worker_extraction_replicas (int):
                Extraction worker pod count. Defaults to ``1``.
            worker_extraction_n_parallel (int):
                Parallel requests for extraction worker. Defaults to
                ``4``.
            worker_extraction_chunk_size (int):
                Rows per parallel batch for extraction. Defaults to
                ``1000``.
            worker_extraction_query_limit (int):
                Max rows per cycle for extraction. Defaults to
                ``1000000``.
            worker_extraction_limits_memory (str):
                Memory limit for extraction worker. Defaults to ``60Gi``.
            worker_extraction_limits_cpu (str):
                CPU limit for extraction worker. Defaults to ``12000m``.
            worker_extraction_requests_memory (str):
                Memory request for extraction worker. Defaults to
                ``20Mi``.
            worker_extraction_requests_cpu (str):
                CPU request for extraction worker. Defaults to ``1m``.
            worker_segmentation_debug (str):
                Debug flag for the segmentation worker. Defaults to
                ``FALSE``.
            worker_segmentation_replicas (int):
                Segmentation worker pod count. Defaults to ``1``.
            worker_segmentation_n_parallel (int):
                Parallel requests for segmentation worker. Defaults to
                ``4``.
            worker_segmentation_chunk_size (int):
                Rows per parallel batch for segmentation. Defaults to
                ``1000``.
            worker_segmentation_query_limit (int):
                Max rows per cycle for segmentation. Defaults to
                ``1000000``.
            worker_segmentation_limits_memory (str):
                Memory limit for segmentation worker. Defaults to
                ``60Gi``.
            worker_segmentation_limits_cpu (str):
                CPU limit for segmentation worker. Defaults to
                ``12000m``.
            worker_segmentation_requests_memory (str):
                Memory request for segmentation worker. Defaults to
                ``20Mi``.
            worker_segmentation_requests_cpu (str):
                CPU request for segmentation worker. Defaults to
                ``1m``.
        """
        self.repository = repository.rstrip("/")

        self._microservice_password = base64.b64encode(
            microservice_password.encode()).decode()
        self._db_password = base64.b64encode(db_password.encode()).decode()
        self.db_username = db_username
        self.db_host = db_host
        self.db_port = db_port
        self.db_database = db_database

        self.app_version = app_version
        self.app_debug = app_debug
        self.app_replicas = app_replicas
        self.app_timeout = app_timeout
        self.app_workers = app_workers
        self.app_limits_memory = app_limits_memory
        self.app_limits_cpu = app_limits_cpu
        self.app_requests_memory = app_requests_memory
        self.app_requests_cpu = app_requests_cpu

        self.worker_embedding_version = worker_embedding_version
        self.worker_embedding_debug = worker_embedding_debug
        self.worker_embedding_replicas = worker_embedding_replicas
        self.worker_embedding_n_parallel = worker_embedding_n_parallel
        self.worker_embedding_chunk_size = worker_embedding_chunk_size
        self.worker_embedding_query_limit = worker_embedding_query_limit
        self.worker_embedding_limits_memory = worker_embedding_limits_memory
        self.worker_embedding_limits_cpu = worker_embedding_limits_cpu
        self.worker_embedding_requests_memory = \
            worker_embedding_requests_memory
        self.worker_embedding_requests_cpu = worker_embedding_requests_cpu

        self.worker_extraction_version = worker_extraction_version
        self.worker_extraction_debug = worker_extraction_debug
        self.worker_extraction_replicas = worker_extraction_replicas
        self.worker_extraction_n_parallel = worker_extraction_n_parallel
        self.worker_extraction_chunk_size = worker_extraction_chunk_size
        self.worker_extraction_query_limit = worker_extraction_query_limit
        self.worker_extraction_limits_memory = worker_extraction_limits_memory
        self.worker_extraction_limits_cpu = worker_extraction_limits_cpu
        self.worker_extraction_requests_memory = \
            worker_extraction_requests_memory
        self.worker_extraction_requests_cpu = worker_extraction_requests_cpu

        self.worker_segmentation_version = worker_segmentation_version
        self.worker_segmentation_debug = worker_segmentation_debug
        self.worker_segmentation_replicas = worker_segmentation_replicas
        self.worker_segmentation_n_parallel = worker_segmentation_n_parallel
        self.worker_segmentation_chunk_size = worker_segmentation_chunk_size
        self.worker_segmentation_query_limit = \
            worker_segmentation_query_limit
        self.worker_segmentation_limits_memory = \
            worker_segmentation_limits_memory
        self.worker_segmentation_limits_cpu = worker_segmentation_limits_cpu
        self.worker_segmentation_requests_memory = \
            worker_segmentation_requests_memory
        self.worker_segmentation_requests_cpu = \
            worker_segmentation_requests_cpu

    def create_deployment_file(self) -> list[PumpwoodDeploy]:
        """Build Kubernetes manifests for Model LLM.

        Returns:
            list[PumpwoodDeploy]:
                Secret ``pumpwood_model_llm__secrets``, application deploy
                ``pumpwood_model_llm__deploy``, and worker deploys
                ``pumpwood_llm_model_embedding_worker``,
                ``pumpwood_llm_model_extraction_worker``, and
                ``pumpwood_llm_model_segmentation_worker``.
        """
        secrets_text_formated = secrets.format(
            db_password=self._db_password,
            microservice_password=self._microservice_password)

        app_deployment_frmtd = deploy_app.format(
            repository=self.repository,
            version=self.app_version,
            replicas=self.app_replicas,
            requests_memory=self.app_requests_memory,
            requests_cpu=self.app_requests_cpu,
            limits_cpu=self.app_limits_cpu,
            limits_memory=self.app_limits_memory,
            workers_timeout=self.app_timeout,
            n_workers=self.app_workers,
            debug=self.app_debug,
            db_username=self.db_username,
            db_host=self.db_host,
            db_port=self.db_port,
            db_database=self.db_database)

        deploy_embedding_worker_frmted = deploy_embedding_worker.format(
            repository=self.repository,
            version=self.worker_embedding_version,
            db_username=self.db_username,
            db_host=self.db_host,
            db_port=self.db_port,
            db_database=self.db_database,
            n_parallel=self.worker_embedding_n_parallel,
            chunk_size=self.worker_embedding_chunk_size,
            query_limit=self.worker_embedding_query_limit,
            replicas=self.worker_embedding_replicas,
            requests_memory=self.worker_embedding_requests_memory,
            requests_cpu=self.worker_embedding_requests_cpu,
            limits_cpu=self.worker_embedding_limits_cpu,
            limits_memory=self.worker_embedding_limits_memory,
            debug=self.worker_embedding_debug)

        deploy_extraction_worker_frmted = deploy_extraction_worker.format(
            repository=self.repository,
            version=self.worker_extraction_version,
            db_username=self.db_username,
            db_host=self.db_host,
            db_port=self.db_port,
            db_database=self.db_database,
            n_parallel=self.worker_extraction_n_parallel,
            chunk_size=self.worker_extraction_chunk_size,
            query_limit=self.worker_extraction_query_limit,
            replicas=self.worker_extraction_replicas,
            requests_memory=self.worker_extraction_requests_memory,
            requests_cpu=self.worker_extraction_requests_cpu,
            limits_cpu=self.worker_extraction_limits_cpu,
            limits_memory=self.worker_extraction_limits_memory,
            debug=self.worker_extraction_debug)

        deploy_segmentation_worker_frmted = \
            deploy_segmentation_worker.format(
                repository=self.repository,
                version=self.worker_segmentation_version,
                db_username=self.db_username,
                db_host=self.db_host,
                db_port=self.db_port,
                db_database=self.db_database,
                n_parallel=self.worker_segmentation_n_parallel,
                chunk_size=self.worker_segmentation_chunk_size,
                query_limit=self.worker_segmentation_query_limit,
                replicas=self.worker_segmentation_replicas,
                requests_memory=self.worker_segmentation_requests_memory,
                requests_cpu=self.worker_segmentation_requests_cpu,
                limits_cpu=self.worker_segmentation_limits_cpu,
                limits_memory=self.worker_segmentation_limits_memory,
                debug=self.worker_segmentation_debug)

        return [
            PumpwoodDeploySecret(
                name='pumpwood_model_llm__secrets',
                content=secrets_text_formated),
            PumpwoodDeployDeployment(
                name='pumpwood_model_llm__deploy',
                content=app_deployment_frmtd),
            PumpwoodDeployDeployment(
                name='pumpwood_llm_model_embedding_worker',
                content=deploy_embedding_worker_frmted),
            PumpwoodDeployDeployment(
                name='pumpwood_llm_model_extraction_worker',
                content=deploy_extraction_worker_frmted),
            PumpwoodDeployDeployment(
                name='pumpwood_llm_model_segmentation_worker',
                content=deploy_segmentation_worker_frmted),
        ]
