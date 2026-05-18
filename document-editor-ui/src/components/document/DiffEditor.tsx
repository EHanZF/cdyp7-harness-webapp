import { useEffect, useState } from "react";
import { getStructuredDocument } from "../../api/documents";
import { SectionEditor } from "./SectionEditor";

export function DiffEditor({ documentId }: { documentId: string }) {
  const [doc, setDoc] = useState<any>(null);

  useEffect(() => {
    getStructuredDocument(documentId).then(setDoc);
  }, [documentId]);

  if (!doc) return <div className="pane">Loading…</div>;

  return (
    <div className="pane">
      <h3>Editable / Diff View</h3>
      {doc.structure.sections.map((s: any) => (
        <SectionEditor key={s.sectionId} section={s} />
      ))}
    </div>
  );
}
