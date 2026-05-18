import { useState } from "react";
import { UploadPage } from "./UploadPage";
import { DocumentWorkspace } from "./DocumentWorkspace";

export default function App() {
  const [documentId, setDocumentId] = useState<string | null>(null);

  if (!documentId) {
    return <UploadPage onUploaded={setDocumentId} />;
  }

  return <DocumentWorkspace documentId={documentId} />;
}
