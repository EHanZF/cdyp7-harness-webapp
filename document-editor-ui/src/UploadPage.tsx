export function UploadPage({
  onUploaded,
}: {
  onUploaded: (id: string) => void;
}) {
  return (
    <div>
      <h1>Upload Page</h1>
      <button onClick={() => onUploaded("test-doc-id")}>
        Continue
      </button>
    </div>
  );
}
