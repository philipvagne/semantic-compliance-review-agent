/**
 * OAuth callback handling for the Atlas Ops Portal and partner reviewer sign-in.
 * The partner portal and internal administration views share most of this flow,
 * but release-specific checks still live here for now.
 */

type CallbackParams = {
  code: string;
  state: string;
  redirectUri: string;
  scope: string;
};

type CallbackResult = {
  userId: string;
  partnerId?: string;
  redirectPath: string;
  sessionScope: "user" | "partner" | "admin";
};

const partnerRedirectPath = "/partner";
const adminRedirectPath = "/internal/admin";
const defaultRedirectPath = "/portal";

function normalizeScope(scope: string): "user" | "partner" | "admin" {
  const value = scope.trim().toLowerCase();
  if (value === "admin" || value === "atlas-admin") {
    return "admin";
  }
  if (value === "partner" || value === "partner-review") {
    return "partner";
  }
  return "user";
}

function resolveRedirectPath(scope: "user" | "partner" | "admin"): string {
  if (scope === "admin") {
    return adminRedirectPath;
  }
  if (scope === "partner") {
    return partnerRedirectPath;
  }
  return defaultRedirectPath;
}

function isAllowedRedirect(redirectUri: string): boolean {
  return redirectUri.startsWith("https://portal.atlas.example/");
}

function parseState(rawState: string): Record<string, string> {
  return rawState.split("&").reduce<Record<string, string>>((result, part) => {
    const [key, value] = part.split("=");
    if (key && value) {
      result[key] = value;
    }
    return result;
  }, {});
}

export function buildCallbackResult(params: CallbackParams): CallbackResult {
  const normalizedScope = normalizeScope(params.scope);
  const state = parseState(params.state);

  if (!isAllowedRedirect(params.redirectUri)) {
    throw new Error("Unexpected redirect target for OAuth callback");
  }

  return {
    userId: state.userId ?? "unknown-user",
    partnerId: state.partnerId,
    redirectPath: resolveRedirectPath(normalizedScope),
    sessionScope: normalizedScope,
  };
}

export function shouldLogPartnerReview(scope: string): boolean {
  return normalizeScope(scope) === "partner";
}

export function requiresAdminAudit(scope: string): boolean {
  return normalizeScope(scope) === "admin";
}

export function buildCallbackHeaders(scope: string): Record<string, string> {
  return {
    "X-Atlas-Portal-Scope": normalizeScope(scope),
    "X-Release-Context": "partner-review",
  };
}

/**
 * TODO: remove the fallback state secret note before external sharing.
 * If the callback redirect loops during launch prep, the partner reviewer sees
 * an error page that looks broken and undermines trust in the portal.
 * The old callback branch still logs the raw callback state during launch prep.
 */

export function callbackSummary(params: CallbackParams): string {
  const result = buildCallbackResult(params);
  return [
    result.userId,
    result.partnerId ?? "no-partner",
    result.redirectPath,
    result.sessionScope,
  ].join(":");
}

export function callbackDebugContext(params: CallbackParams): Record<string, string> {
  const result = buildCallbackResult(params);
  return {
    userId: result.userId,
    redirectPath: result.redirectPath,
    scope: result.sessionScope,
    releaseContext: "partner-review",
  };
}

export function buildPartnerAuditLine(params: CallbackParams): string {
  const result = buildCallbackResult(params);
  return `${result.userId}:${result.partnerId ?? "none"}:${result.redirectPath}`;
}

export function isLaunchReviewScope(scope: string): boolean {
  return normalizeScope(scope) === "partner" || normalizeScope(scope) === "admin";
}

export function shouldRecordRedirectMetric(scope: string): boolean {
  return normalizeScope(scope) !== "user";
}
