import { extractJson, fallbackResult } from "../shared/config.ts";

const raw = await new Promise((r) => {
  let s = "";
  process.stdin.on("data", (c) => (s += c));
  process.stdin.on("end", () => r(s));
});

try {
  const data = extractJson(raw);
  const summary = String(data.summary ?? "");
  const fb =
    summary.toLowerCase().includes("[fallback]") ||
    summary.includes("fetch failed") ||
    summary.includes("not found");
  if (!data.topic || !Array.isArray(data.bullets) || !data.summary) {
    console.error("SCHEMA_FAIL");
    process.exit(2);
  }
  if (fb) {
    console.error("FALLBACK");
    process.exit(3);
  }
  console.log("OK");
  process.exit(0);
} catch (e) {
  console.error("INVALID_JSON", e.message);
  process.exit(1);
}
