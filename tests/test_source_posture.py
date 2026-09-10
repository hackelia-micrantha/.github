from __future__ import annotations

import unittest

from tools import source_posture


class SourcePostureValidationTests(unittest.TestCase):
    def registry(self, *repositories: dict[str, object]) -> dict[str, object]:
        return {
            "schemaVersion": 1,
            "organization": "hackelia-micrantha",
            "repositories": list(repositories),
        }

    def entry(
        self,
        repository: str,
        *,
        visibility: str,
        source_exposure: str | None = None,
        repository_role: str | None = None,
        distribution_mode: str | None = None,
        **extra: object,
    ) -> dict[str, object]:
        item: dict[str, object] = {
            "repository": repository,
            "visibility": visibility,
        }
        if source_exposure is not None:
            item["sourceExposure"] = source_exposure
        if repository_role is not None:
            item["repositoryRole"] = repository_role
        if distribution_mode is not None:
            item["distributionMode"] = distribution_mode
        item.update(extra)
        return item

    def test_unclassified_legacy_entries_are_permitted_during_rollout(self) -> None:
        data = self.registry(
            self.entry("hackelia-micrantha/legacy", visibility="private")
        )

        self.assertEqual(source_posture.validate_registry_posture(data), [])

    def test_invokrum_private_canonical_and_public_binary_distribution_are_valid(self) -> None:
        canonical = self.entry(
            "hackelia-micrantha/invokrum",
            visibility="private",
            source_exposure="private",
            repository_role="canonical",
            distribution_mode="internal",
            implementationAuthority="hackelia-micrantha/invokrum",
            releaseAuthority="hackelia-micrantha/invokrum",
            publicDistributionRepository="hackelia-micrantha/invokrum-community",
        )
        distribution = self.entry(
            "hackelia-micrantha/invokrum-community",
            visibility="public",
            source_exposure="none",
            repository_role="distribution",
            distribution_mode="binary",
            implementationAuthority="hackelia-micrantha/invokrum",
            releaseAuthority="hackelia-micrantha/invokrum",
            canonicalRepository="hackelia-micrantha/invokrum",
        )

        self.assertEqual(
            source_posture.validate_registry_posture(
                self.registry(canonical, distribution)
            ),
            [],
        )

    def test_keylix_private_canonical_and_public_source_projection_are_valid(self) -> None:
        canonical = self.entry(
            "hackelia-micrantha/keylix",
            visibility="private",
            source_exposure="private",
            repository_role="canonical",
            distribution_mode="internal",
            publicDistributionRepository="hackelia-micrantha/keylix-community",
        )
        projection = self.entry(
            "hackelia-micrantha/keylix-community",
            visibility="public",
            source_exposure="public",
            repository_role="projection",
            distribution_mode="source",
            canonicalRepository="hackelia-micrantha/keylix",
            implementationAuthority="hackelia-micrantha/keylix",
            releaseAuthority="hackelia-micrantha/keylix",
        )

        self.assertEqual(
            source_posture.validate_registry_posture(
                self.registry(canonical, projection)
            ),
            [],
        )

    def test_calathea_public_canonical_core_and_private_composition_are_valid(self) -> None:
        public_core = self.entry(
            "hackelia-micrantha/calathea-community",
            visibility="public",
            source_exposure="public",
            repository_role="canonical",
            distribution_mode="source",
            implementationAuthority="hackelia-micrantha/calathea-community",
            releaseAuthority="hackelia-micrantha/calathea-community",
        )
        private_composition = self.entry(
            "hackelia-micrantha/calathea",
            visibility="private",
            source_exposure="private",
            repository_role="internal",
            distribution_mode="internal",
            implementationAuthority="hackelia-micrantha/calathea",
            releaseAuthority="hackelia-micrantha/calathea",
        )

        self.assertEqual(
            source_posture.validate_registry_posture(
                self.registry(public_core, private_composition)
            ),
            [],
        )

    def test_partial_posture_is_rejected(self) -> None:
        data = self.registry(
            self.entry(
                "hackelia-micrantha/example",
                visibility="public",
                source_exposure="public",
            )
        )

        errors = source_posture.validate_registry_posture(data)

        self.assertTrue(any("posture is partial" in error for error in errors))

    def test_source_distribution_requires_public_source_exposure(self) -> None:
        data = self.registry(
            self.entry(
                "hackelia-micrantha/example",
                visibility="public",
                source_exposure="none",
                repository_role="distribution",
                distribution_mode="source",
            )
        )

        errors = source_posture.validate_registry_posture(data)

        self.assertTrue(any("distributes source" in error for error in errors))

    def test_public_repository_cannot_claim_private_source_exposure(self) -> None:
        data = self.registry(
            self.entry(
                "hackelia-micrantha/example",
                visibility="public",
                source_exposure="private",
                repository_role="canonical",
                distribution_mode="binary",
            )
        )

        errors = source_posture.validate_registry_posture(data)

        self.assertTrue(any("is public but declares private source exposure" in error for error in errors))

    def test_repository_references_must_resolve(self) -> None:
        data = self.registry(
            self.entry(
                "hackelia-micrantha/example-community",
                visibility="public",
                source_exposure="none",
                repository_role="distribution",
                distribution_mode="binary",
                canonicalRepository="hackelia-micrantha/missing",
            )
        )

        errors = source_posture.validate_registry_posture(data)

        self.assertTrue(any("references unregistered repository" in error for error in errors))

    def test_public_distribution_reference_must_be_public(self) -> None:
        canonical = self.entry(
            "hackelia-micrantha/example",
            visibility="private",
            source_exposure="private",
            repository_role="canonical",
            distribution_mode="internal",
            publicDistributionRepository="hackelia-micrantha/internal-dist",
        )
        distribution = self.entry(
            "hackelia-micrantha/internal-dist",
            visibility="private",
            source_exposure="private",
            repository_role="distribution",
            distribution_mode="binary",
        )

        errors = source_posture.validate_registry_posture(
            self.registry(canonical, distribution)
        )

        self.assertTrue(any("must reference a public repository" in error for error in errors))

    def test_report_lists_classification_coverage_and_topology_edges(self) -> None:
        canonical = self.entry(
            "hackelia-micrantha/invokrum",
            visibility="private",
            source_exposure="private",
            repository_role="canonical",
            distribution_mode="internal",
            monitor=True,
            publicDistributionRepository="hackelia-micrantha/invokrum-community",
        )
        distribution = self.entry(
            "hackelia-micrantha/invokrum-community",
            visibility="public",
            source_exposure="none",
            repository_role="distribution",
            distribution_mode="binary",
            monitor=True,
            canonicalRepository="hackelia-micrantha/invokrum",
        )

        report = "\n".join(
            source_posture.posture_report_lines(
                self.registry(canonical, distribution)
            )
        )

        self.assertIn("classified: 2/2 repositories", report)
        self.assertIn("canonical/private/internal", report)
        self.assertIn("distribution/none/binary", report)
        self.assertIn(
            "invokrum-community --canonical--> hackelia-micrantha/invokrum",
            report,
        )
        self.assertIn(
            "invokrum --public-distribution--> hackelia-micrantha/invokrum-community",
            report,
        )

    def test_report_surfaces_monitored_unclassified_as_non_failing_migration_warning(self) -> None:
        data = self.registry(
            self.entry(
                "hackelia-micrantha/legacy",
                visibility="private",
                monitor=True,
            )
        )

        report = "\n".join(source_posture.posture_report_lines(data))

        self.assertIn("monitored but unclassified: 1", report)
        self.assertIn("legacy: posture not yet classified", report)
        self.assertEqual(source_posture.validate_registry_posture(data), [])


if __name__ == "__main__":
    unittest.main()
