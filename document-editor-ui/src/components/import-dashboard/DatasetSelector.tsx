export type DatasetType =
  | "MCP_FEATURES"
  | "FEATURE_REQUIREMENT_TRACE"
  | "FEATURE_REQUIREMENT_VERIFICATION_GRAPH";

export function DatasetSelector({
  value,
  onChange,
}: {
  value: DatasetType;
  onChange: (v: DatasetType) => void;
}) {
  return (
    <fieldset>
      <legend>Dataset Type</legend>

      <label>
        <input
          type="radio"
          checked={value === "MCP_FEATURES"}
          onChange={() => onChange("MCP_FEATURES")}
        />
        MCP_Features
      </label>

      <label>
        <input
          type="radio"
          checked={value === "FEATURE_REQUIREMENT_TRACE"}
          onChange={() => onChange("FEATURE_REQUIREMENT_TRACE")}
        />
        Feature–Requirement Trace
      </label>

      <label>
        <input
          type="radio"
          checked={value === "FEATURE_REQUIREMENT_VERIFICATION_GRAPH"}
          onChange={() =>
            onChange("FEATURE_REQUIREMENT_VERIFICATION_GRAPH")
          }
        />
        Feature–Requirement–Verification Graph
      </label>
    </fieldset>
  );
}
