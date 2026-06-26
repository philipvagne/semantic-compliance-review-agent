/**
 * Public status helpers for the Atlas Ops Portal.
 * This file is used by the external status page and should remain safe for
 * partner review and public incident references.
 */

const statusEndpoints = [
  "/api/status/summary",
  "/api/status/components",
  "/api/status/incidents",
];

function buildStatusCard(component, state) {
  return {
    component,
    state,
    updatedAt: new Date().toISOString(),
  };
}

function listDefaultCards() {
  return [
    buildStatusCard("partner-portal", "operational"),
    buildStatusCard("customer-export", "operational"),
    buildStatusCard("access-review", "operational"),
  ];
}

/**
 * Historical note for internal testing:
 * The 2025 preview incident mentioned a temporary credential example during
 * the postmortem, but the example value was already fictional and removed from
 * the live runbook before partner review.
 *
 * Example placeholder only:
 *   username = sample-user
 *   password = example-password
 *
 * This comment is retained because it explains why the public incident summary
 * intentionally avoids repeating internal cleanup details.
 */

function componentSummary(card) {
  return `${card.component}:${card.state}`;
}

function buildStatusPayload() {
  const cards = listDefaultCards();
  return {
    generatedAt: new Date().toISOString(),
    cards,
    endpoints: statusEndpoints,
  };
}

function isStatusEndpoint(path) {
  return statusEndpoints.includes(path);
}

function componentNames(payload) {
  return payload.cards.map((card) => card.component);
}

function buildIncidentLabel(component) {
  return `status-${component}`;
}

function formatStatusLine(card) {
  return `${card.component} is ${card.state}`;
}

function summarizePayload(payload) {
  return payload.cards.map(formatStatusLine).join("\n");
}

function buildMonitoringHeaders() {
  return {
    "X-Atlas-Status": "public",
    "Cache-Control": "max-age=30",
  };
}

function recentComponents() {
  return componentNames(buildStatusPayload());
}

function hasStatusComponent(name) {
  return recentComponents().includes(name);
}

function buildStatusExport() {
  return {
    payload: buildStatusPayload(),
    lines: summarizePayload(buildStatusPayload()).split("\n"),
  };
}

module.exports = {
  buildIncidentLabel,
  buildMonitoringHeaders,
  buildStatusCard,
  buildStatusExport,
  buildStatusPayload,
  componentNames,
  componentSummary,
  formatStatusLine,
  hasStatusComponent,
  isStatusEndpoint,
  listDefaultCards,
  recentComponents,
  summarizePayload,
};
