from __future__ import annotations

import copy
import unittest

from tools import release_readiness


class ReleaseReadinessTests(unittest.TestCase):
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
        source_exposure: str,
        repository_role: str,
        distribution_mode: str,
        **extra: object,
    ) -> dict[str, object]:
        item: dict[str, object] = {
            "repository": repository,
            "visibility": visibility,
            "sourceExposure": source_exposure,
            "repositoryRole": repository_role,
            "distributionMode": distribution_mode,
        }
        item.update(extra)
        return item

    def invokrum_registry(self) -> dict[str, object]:
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
        return self.registry(canonical, distribution)

    def binary_evidence(self) -> dict[str, object]:
        return {
            "schemaVersion": 1,
            "repository": "hackelia-micrantha/invokrum-community",
            "release": {
                "releaseAuthority": "hackelia-micrantha/invokrum",
                "canonicalIdentity": "0.3.0",
                "identityClaims": {
                    "executable": "0.3.0",
                    "archive": "0.3.0",
                    "package": "0.3.0",
                    "manPage": "0.3.0",
                    "provenance": "0.3.0",
                },
            },
            "acquisition": {
                "mode": "binary",
                "sourceBuild": False,
                "immutable": True,
                "requiresPrivateCredentials": False,
                "cryptographicPins": ["sha256:" + "a" * 64],
            },
            "artifacts": [
                {"path": "bin/invokrum", "kind": "executable", "executable": True},
                {
                    "path": "share/man/man1/invokrum.1",
                    "kind": "man",
                    "executable": False,
                },
            ],
            "cli": {
                "executablePath": "bin/invokrum",
                "manPagePath": "share/man/man1/invokrum.1",
                "smokePassed": True,
                "operatorDocsPresent": True,
            },
            "inspection": {
                "privateImplementationSourcePresent": False,
                "credentialsPresent": False,
                "signingKeysPresent": False,
                "privateSecurityCorpusPresent": False,
                "developmentOnlyMaterialPresent": False,
            },
            "cleanConsumer": {
                "tested": True,
                "cacheMiss": True,
                "privateCredentialsAvailable": False,
                "passed": True,
            },
        }

    def source_evidence(self, repository: str, release_authority: str) -> dict[str, object]:
        return {
            "schemaVersion": 1,
            "repository": repository,
            "release": {
                "releaseAuthority": release_authority,
                "canonicalIdentity": "0.2.0",
                "identityClaims": {"package": "0.2.0"},
            },
            "acquisition": {
                "mode": "source",
                "sourceBuild": True,
                "immutable": True,
                "requiresPrivateCredentials": False,
            },
            "inspection": {
                "privateImplementationSourcePresent": False,
                "credentialsPresent": False,
                "signingKeysPresent": False,
                "privateSecurityCorpusPresent": False,
                "developmentOnlyMaterialPresent": False,
            },
            "cleanConsumer": {
                "tested": True,
                "cacheMiss": True,
                "privateCredentialsAvailable": False,
                "passed": True,
            },
        }

    def test_invokrum_public_binary_release_is_valid(self) -> None:
        self.assertEqual(
            release_readiness.validate_release_evidence(
                self.invokrum_registry(), self.binary_evidence()
            ),
            [],
        )

    def test_binary_distribution_cannot_compile_private_implementation_source(self) -> None:
        evidence = self.binary_evidence()
        evidence["acquisition"]["sourceBuild"] = True

        errors = release_readiness.validate_release_evidence(
            self.invokrum_registry(), evidence
        )

        self.assertTrue(any("[binary.no-source-build]" in error for error in errors))

    def test_public_binary_distribution_requires_cryptographic_pin(self) -> None:
        evidence = self.binary_evidence()
        evidence["acquisition"]["cryptographicPins"] = []

        errors = release_readiness.validate_release_evidence(
            self.invokrum_registry(), evidence
        )

        self.assertTrue(any("[binary.pin]" in error for error in errors))

    def test_public_distribution_cannot_require_private_source_credentials(self) -> None:
        evidence = self.binary_evidence()
        evidence["acquisition"]["requiresPrivateCredentials"] = True
        evidence["cleanConsumer"]["privateCredentialsAvailable"] = True

        errors = release_readiness.validate_release_evidence(
            self.invokrum_registry(), evidence
        )

        self.assertTrue(any("[acquisition.credentials]" in error for error in errors))
        self.assertTrue(any("[consumer.clean]" in error for error in errors))

    def test_binary_distribution_rejects_private_source_in_generated_artifact(self) -> None:
        evidence = self.binary_evidence()
        evidence["inspection"]["privateImplementationSourcePresent"] = True

        errors = release_readiness.validate_release_evidence(
            self.invokrum_registry(), evidence
        )

        self.assertTrue(any("[binary.private-source]" in error for error in errors))

    def test_generated_artifact_rejects_secret_or_private_security_material(self) -> None:
        evidence = self.binary_evidence()
        evidence["inspection"]["credentialsPresent"] = True
        evidence["inspection"]["privateSecurityCorpusPresent"] = True

        errors = release_readiness.validate_release_evidence(
            self.invokrum_registry(), evidence
        )

        self.assertTrue(any("[artifact.credentials]" in error for error in errors))
        self.assertTrue(
            any("[artifact.private-security-corpus]" in error for error in errors)
        )

    def test_cli_release_requires_executable_man_page_smoke_and_docs(self) -> None:
        evidence = self.binary_evidence()
        evidence["artifacts"] = [
            {"path": "bin/invokrum", "kind": "executable", "executable": False}
        ]
        evidence["cli"]["smokePassed"] = False
        evidence["cli"]["operatorDocsPresent"] = False

        errors = release_readiness.validate_release_evidence(
            self.invokrum_registry(), evidence
        )

        self.assertTrue(any("[cli.executable]" in error for error in errors))
        self.assertTrue(any("[cli.man]" in error for error in errors))
        self.assertTrue(any("[cli.smoke]" in error for error in errors))
        self.assertTrue(any("[cli.docs]" in error for error in errors))

    def test_release_identity_drift_fails_readiness(self) -> None:
        evidence = self.binary_evidence()
        evidence["release"]["identityClaims"]["manPage"] = "0.2.0"

        errors = release_readiness.validate_release_evidence(
            self.invokrum_registry(), evidence
        )

        self.assertTrue(any("identity claim 'manPage'" in error for error in errors))

    def test_repora_public_source_build_is_valid(self) -> None:
        repository = self.entry(
            "hackelia-micrantha/repora",
            visibility="public",
            source_exposure="public",
            repository_role="canonical",
            distribution_mode="source",
            implementationAuthority="hackelia-micrantha/repora",
            releaseAuthority="hackelia-micrantha/repora",
        )

        self.assertEqual(
            release_readiness.validate_release_evidence(
                self.registry(repository),
                self.source_evidence(
                    "hackelia-micrantha/repora", "hackelia-micrantha/repora"
                ),
            ),
            [],
        )

    def test_keylix_public_source_projection_keeps_private_canonical_authority(self) -> None:
        canonical = self.entry(
            "hackelia-micrantha/keylix",
            visibility="private",
            source_exposure="private",
            repository_role="canonical",
            distribution_mode="internal",
            implementationAuthority="hackelia-micrantha/keylix",
            releaseAuthority="hackelia-micrantha/keylix",
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
            release_readiness.validate_release_evidence(
                self.registry(canonical, projection),
                self.source_evidence(
                    "hackelia-micrantha/keylix-community",
                    "hackelia-micrantha/keylix",
                ),
            ),
            [],
        )

    def test_calathea_public_canonical_source_release_is_valid(self) -> None:
        public_core = self.entry(
            "hackelia-micrantha/calathea-community",
            visibility="public",
            source_exposure="public",
            repository_role="canonical",
            distribution_mode="source",
            implementationAuthority="hackelia-micrantha/calathea-community",
            releaseAuthority="hackelia-micrantha/calathea-community",
        )

        self.assertEqual(
            release_readiness.validate_release_evidence(
                self.registry(public_core),
                self.source_evidence(
                    "hackelia-micrantha/calathea-community",
                    "hackelia-micrantha/calathea-community",
                ),
            ),
            [],
        )

    def test_release_authority_must_match_registry(self) -> None:
        evidence = self.binary_evidence()
        evidence["release"]["releaseAuthority"] = "hackelia-micrantha/invokrum-community"

        errors = release_readiness.validate_release_evidence(
            self.invokrum_registry(), evidence
        )

        self.assertTrue(any("[release.authority]" in error for error in errors))

    def test_evidence_for_unclassified_repository_fails_closed(self) -> None:
        registry = {
            "schemaVersion": 1,
            "organization": "hackelia-micrantha",
            "repositories": [
                {
                    "repository": "hackelia-micrantha/legacy",
                    "visibility": "public",
                }
            ],
        }
        evidence = copy.deepcopy(self.binary_evidence())
        evidence["repository"] = "hackelia-micrantha/legacy"

        errors = release_readiness.validate_release_evidence(registry, evidence)

        self.assertEqual(
            errors,
            [
                "[registry.unclassified] repository posture is not classified: hackelia-micrantha/legacy"
            ],
        )


if __name__ == "__main__":
    unittest.main()
