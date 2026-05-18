// ImportDashboard.tsx
import { useState } from "react";
import { DatasetSelector, DatasetType } from "./DatasetSelector";
import { FileUploader } from "./FileUploader";
import { validateImport } from "../../api/mcpValidation";
import { importToDataverse } from "../../api/dataverse";
import { ValidationSummary } from "./ValidationSummary";

export function ImportDashboard() {
  const [dataset, setDataset] = useState<DatasetType>("MCP_FEATURES");
  const [file, setFile] = useState<File | null>(null);
  const [validation, setValidation] = useState<any>(null);

  async function onValidate() {
    if (!file) return;
    const result = await validateImport(dataset, file);
    setValidation(result);
  }

  async function onImport() {
    if (!file || !validation?.valid) return;
    await importToDataverse(dataset, file);
    alert("Import completed");
  }

  return (
    <>
      <DatasetSelector value={dataset} onChange={setDataset} />
      <FileUploader onFile={setFile} />

      <button onClick={onValidate} disabled={!file}>
        Validate
      </button>

      {validation && <ValidationSummary result={validation} />}

      <button onClick={onImport} disabled={!validation?.valid}>
        Import
      </button>
    </>
  );
}
