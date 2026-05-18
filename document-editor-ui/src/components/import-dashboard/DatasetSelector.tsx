// DatasetSelector.tsx// DatasetSelector.tsx | "MCP_FEATURES"
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
      {[
        ["MCP_FEATURES", "MCP_Features"],
        ["FEATURE_REQUIREMENT_TRACE", "Feature–Requirement Trace"],
        ["FEATURE_REQUIREMENT_VERIFICATION_GRAPH", "Feature–Requirement–Verification Graph"],
      ].map(([id, label]) => (
        <label key={id} style={{ display: "block" }}>
          <input
            type="radio"
            checked={value === id}
            onChange={() => onChange(id as DatasetType)}
          />
          {label}
        </label>
      ))}
    </fieldset>
  );
}
export type DatasetType =
