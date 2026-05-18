export function OriginalViewer({ documentId }: { documentId: string }) {
  return (
    <div className="pane">
      <h3>Original Document</h3>
      {`/api/documents/${documentId}/original`}
    </div>
  );
}
