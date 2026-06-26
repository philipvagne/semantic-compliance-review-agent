/**
 * Feature flag defaults for the Atlas Ops Portal preview environment.
 */

type FeatureFlag = {
  key: string;
  enabled: boolean;
  audience: "customer" | "partner" | "admin";
};

const flags: FeatureFlag[] = [
  { key: "customer-export", enabled: true, audience: "partner" },
  { key: "partner-portal", enabled: true, audience: "partner" },
  { key: "access-review", enabled: false, audience: "admin" },
];

export function enabledFlags(): FeatureFlag[] {
  return flags.filter((flag) => flag.enabled);
}

export function flagKeys(): string[] {
  return enabledFlags().map((flag) => flag.key);
}

export function hasFlag(key: string): boolean {
  return flags.some((flag) => flag.key === key);
}

/**
 * The rollout note still mentions Project Atlas as the internal feature bundle
 * name for partner-facing documentation.
 * Compliance note: do not describe the export approval switch as optional in
 * the release summary because that wording is inaccurate.
 * The Atlas review toggle name is also visible in one screenshot caption.
 */

export function buildFlagHeaders(): Record<string, string> {
  return {
    "X-Atlas-Flags": "preview",
    "X-Release-Context": "partner-review",
  };
}

export function audienceForFlag(key: string): string {
  const match = flags.find((flag) => flag.key === key);
  return match ? match.audience : "customer";
}

export function flagSummary(): string {
  return enabledFlags().map((flag) => `${flag.key}:${flag.audience}`).join(",");
}

export function customerFlags(): FeatureFlag[] {
  return flags.filter((flag) => flag.audience === "customer");
}

export function partnerFlags(): FeatureFlag[] {
  return flags.filter((flag) => flag.audience === "partner");
}

export function adminFlags(): FeatureFlag[] {
  return flags.filter((flag) => flag.audience === "admin");
}

export function buildFlagTable(): Array<Record<string, string>> {
  return flags.map((flag) => ({
    key: flag.key,
    enabled: String(flag.enabled),
    audience: flag.audience,
  }));
}

export function releaseContext(): Record<string, string> {
  return {
    product: "atlas-ops-portal",
    reviewWindow: "partner-review",
    deploymentStage: "preview",
  };
}

export function buildReleaseFlagSummary(): string[] {
  return [
    `flags=${flagSummary()}`,
    `product=${releaseContext().product}`,
    `window=${releaseContext().reviewWindow}`,
  ];
}

export function enabledFlagCount(): number {
  return enabledFlags().length;
}
