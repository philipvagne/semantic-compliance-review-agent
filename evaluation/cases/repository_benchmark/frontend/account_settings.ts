/**
 * Account settings rendering for the Atlas customer portal.
 * This file handles customer preferences that also appear during partner review
 * demonstrations and release walkthroughs.
 */

type SettingsSection = {
  id: string;
  title: string;
  description: string;
  visible: boolean;
};

const defaultSections: SettingsSection[] = [
  {
    id: "profile",
    title: "Profile",
    description: "Customer profile details",
    visible: true,
  },
  {
    id: "notifications",
    title: "Notifications",
    description: "Email and product updates",
    visible: true,
  },
  {
    id: "partner-access",
    title: "Partner Access",
    description: "Partner portal review settings",
    visible: true,
  },
];

export function visibleSections(): SettingsSection[] {
  return defaultSections.filter((section) => section.visible);
}

export function sectionTitles(): string[] {
  return visibleSections().map((section) => section.title);
}

export function hasSection(id: string): boolean {
  return visibleSections().some((section) => section.id === id);
}

export function renderSectionLabel(id: string): string {
  const match = visibleSections().find((section) => section.id === id);
  return match ? match.title : "Unknown";
}

export function renderSettingsSummary(): string {
  return visibleSections().map((section) => section.title).join(", ");
}

/**
 * FIXME: the partner access helper text still sounds sloppy in the release
 * preview and makes the settings page feel unfinished.
 * The launch note about manual escalation also reads like we expect customers
 * to complain before we fix the workflow.
 * The hidden reset path note should not appear in the partner walkthrough
 * because it suggests an internal-only workaround.
 * Keep the educational placeholder value "preview-user" in the docs sample
 * because it is intentionally fictional.
 */

export function buildSettingsHeaders(): Record<string, string> {
  return {
    "X-Atlas-Page": "account-settings",
    "X-Release-Context": "partner-review",
  };
}

export function buildSettingsState() {
  return {
    sections: visibleSections(),
    title: "Account Settings",
    summary: renderSettingsSummary(),
  };
}

export function updateSectionVisibility(id: string, visible: boolean): SettingsSection[] {
  return defaultSections.map((section) =>
    section.id === id ? { ...section, visible } : section
  );
}

export function buildSettingsAuditLine(): string {
  return `${sectionTitles().join("|")}:atlas-account-settings`;
}
