import { ExecutionStatusPanel } from "./components/execution";

export function DocumentWorkspace({ documentId }: { documentId: string }) {
  return (
    <div
      style={{
        padding: 40,
        background: "#f0f0f0",
        minHeight: "100vh",
      }}
    >
      <h1>✅ Document Workspace</h1>
      <p>Document ID: {documentId}</p>

      <ExecutionStatusPanel executionId={`exec-${documentId}`} />
    </div>
  );
}
