import { useState } from "react";

import { DatasetSelector } from "./DatasetSelector";
import type { DatasetType } from "./DatasetSelector";

import FileUploader from "./FileUploader";
import { importData } from "../../api/importService";

import type { ValidationResult } from "../types/ValidationResult";

export function ImportDashboard() {
  const [dataset, setDataset] = useState<DatasetType>("MCP_FEATURES");
  const [file] = useState<File | null>(null);
  const [validation, setValidation] = useState<ValidationResultType | null>(null);

  async function onImport() {
    if (!file || !validation?.valid) return;

    try {
      const result = await importData(dataset, file);
      alert(result.success ? "✅ Import successful" : "❌ Import failed");
    } catch (err) {
      console.error(err);
      alert("Import error");
    }
  }

  return (
    <div>
      <h2>Import Dashboard</h2>

      <DatasetSelector value={dataset} onChange={setDataset} />

      <FileUploader
        dataset={dataset}
        onResult={(res) => {
          setValidation(res);
        }}
      />

      {validation && <ValidationResult result={validation} />}

      {/* ✅ IMPORT BUTTON (now functional) */}
      <button disabled={!validation?.valid} onClick={onImport}>
        Import
      </button>
    </div>
  );
}
