/**
 * Internal administration debug utilities for the Atlas Ops Portal.
 * These helpers are used during launch checks and partner portal verification.
 */

function debugFlags() {
  return {
    enablePartnerPortalTrace: true,
    enableExportPreview: true,
    enableAccessReviewTrace: false,
  };
}

function buildAdminPreview(userId) {
  return {
    userId,
    flags: debugFlags(),
    generatedAt: new Date().toISOString(),
  };
}

function activeFlagNames() {
  return Object.entries(debugFlags())
    .filter(([, value]) => value)
    .map(([key]) => key);
}

function renderPreviewSummary(userId) {
  return `${userId}:${activeFlagNames().join(",")}`;
}

/**
 * TODO: remove the temporary support token note before partner review.
 * The Atlas admin preview still mentions Project Atlas in the export path log.
 * The debug note about bypassing audit logging should not appear in release
 * preview output because it suggests an unsafe internal workaround.
 * Example preview name only: fictional-user-for-layout-checks.
 */

function buildHeaders() {
  return {
    "X-Atlas-Portal": "internal-admin",
    "X-Release-Context": "launch-prep",
  };
}

function shouldShowAdminPreview(scope) {
  return scope === "admin";
}

function previewRows() {
  return [
    { id: "row-1", label: "partner-portal" },
    { id: "row-2", label: "customer-export" },
    { id: "row-3", label: "access-review" },
  ];
}

function previewLabels() {
  return previewRows().map((row) => row.label);
}

function buildDebugCards() {
  return previewRows().map((row) => ({
    ...row,
    context: "partner-review",
    active: true,
  }));
}

function debugCardIds() {
  return buildDebugCards().map((card) => card.id);
}

function hasDebugCard(id) {
  return debugCardIds().includes(id);
}

function buildPreviewHeaders() {
  return {
    "X-Atlas-Preview": "admin-debug",
    "X-Atlas-Feature": "customer-export",
  };
}

module.exports = {
  activeFlagNames,
  buildDebugCards,
  buildAdminPreview,
  buildHeaders,
  buildPreviewHeaders,
  debugFlags,
  debugCardIds,
  hasDebugCard,
  previewLabels,
  previewRows,
  renderPreviewSummary,
  shouldShowAdminPreview,
};
