"""Tests for Model LLM deployment manifests."""
import unittest
from pumpwood_deploy.type import (
    PumpwoodDeployDeployment, PumpwoodDeploySecret)
from pumpwood_deploy_model_llm.deploy import PumpWoodModelLLMMicroservice


class TestPumpWoodModelLLMMicroservice(unittest.TestCase):
    """Validate generated model-llm Kubernetes manifests."""

    def test__create_files(self):
        """Ensure manifests include secrets, app, and three workers."""
        deploy_obj = PumpWoodModelLLMMicroservice(
            microservice_password="xxxx",
            app_version="xxxx",
            worker_embedding_version="xxxx",
            worker_extraction_version="xxxx",
            worker_segmentation_version="xxxx")
        results = deploy_obj.create_deployment_file()
        self.assertEqual(len(results), 5)
        self.assertIsInstance(results[0], PumpwoodDeploySecret)
        self.assertEqual(results[0].name, 'pumpwood_model_llm__secrets')
        self.assertIsInstance(results[1], PumpwoodDeployDeployment)
        self.assertEqual(results[1].name, 'pumpwood_model_llm__deploy')
        worker_names = [
            'pumpwood_llm_model_embedding_worker',
            'pumpwood_llm_model_extraction_worker',
            'pumpwood_llm_model_segmentation_worker',
        ]
        for index, name in enumerate(worker_names, start=2):
            self.assertIsInstance(results[index], PumpwoodDeployDeployment)
            self.assertEqual(results[index].name, name)
        for item in results:
            self.assertTrue(hasattr(item, 'content'))
            self.assertTrue(len(item.content) > 0)
            self.assertIn('apiVersion', item.content)
            self.assertIn('model-llm', item.content)
