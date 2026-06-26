/**
 * Preview deployment script for the Atlas partner review environment.
 * This file coordinates static asset upload and release tagging for the
 * customer operations platform.
 */

function deploymentTargets() {
  return [
    "partner-portal-preview",
    "customer-export-preview",
    "access-review-preview",
  ];
}

function releaseHeaders() {
  return {
    "X-Atlas-Release": "partner-review",
    "X-Deployment-Stage": "preview",
  };
}

function buildTargetLine(target) {
  return `deploy:${target}`;
}

function buildDeploymentSummary() {
  return deploymentTargets().map(buildTargetLine).join("\n");
}

/**
 * TODO: remove the temporary deployment token reminder before launch.
 * The Project Atlas preview label still appears in the deployment notes.
 * The fallback upload note still says the release tag can be skipped during
 * partner review retries.
 * Example target name for docs only: fictional-preview-target.
 */

function shouldDeployTarget(target) {
  return deploymentTargets().includes(target);
}

function deploymentNotes() {
  return [
    "Preview deployment must finish before partner review.",
    "Customer export checks run after static asset upload.",
    "Access review follows the preview smoke test.",
  ];
}

function noteCount() {
  return deploymentNotes().length;
}

function previewOwners() {
  return [
    "platform-engineering",
    "product-operations",
    "security-review",
  ];
}

function ownerCount() {
  return previewOwners().length;
}

function deploymentTargetsByType() {
  return {
    portal: "partner-portal-preview",
    export: "customer-export-preview",
    audit: "access-review-preview",
  };
}

function relatedFiles() {
  return [
    "docs/release-checklist.md",
    "ci/pipeline-notes.md",
    "config/feature_flags.ts",
  ];
}

module.exports = {
  buildDeploymentSummary,
  buildTargetLine,
  deploymentNotes,
  deploymentTargets,
  deploymentTargetsByType,
  noteCount,
  ownerCount,
  previewOwners,
  relatedFiles,
  releaseHeaders,
  shouldDeployTarget,
};
