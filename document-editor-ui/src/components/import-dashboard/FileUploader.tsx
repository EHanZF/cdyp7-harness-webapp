// FileUploader.tsx
export function FileUploader({
  onFile,
}: {
  onFile: (file: File) => void;
}) {
  return (
    <div>
      <input
        type="file"
        accept=".csv,.json"
        onChange={(e) => e.target.files && onFile(e.target.files[0])}
      />
    </div>
  );
}
