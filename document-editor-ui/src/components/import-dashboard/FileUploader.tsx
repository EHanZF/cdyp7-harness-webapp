import { useState } from "react";
import { validateImport } from "../../api/mcpValidation";

import type { DatasetType } from "./DatasetSelector";
import type { ValidationResult } from "../types/ValidationResult";

interface Props {
  dataset: DatasetType;
  onResult: (result: ValidationResult) => void;
}

export default function FileUploader({ dataset, onResult }: Props) {
  const [status, setStatus] = useState<string>("Ready");

  async function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    setStatus("Validating...");

    try {
      const result = await validateImport(dataset, file);
      onResult(result);

      setStatus(result.valid ? "✅ Validation passed" : "❌ Validation failed");
    } catch (err) {
      console.error(err);
      setStatus("❌ Error during validation");
    }
  }

  return (
    <div>
      <label htmlFor="file-upload">Upload CSV or JSON file</label>
      <input id="file-upload" type="file" onChange={handleFileChange} />
      <div>{status}</div>
    </div>
  );
}
