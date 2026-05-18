import { useState } from "react";
import { AIAssistPanel } from "./AIAssistPanel";

export function SectionEditor({ section }: any) {
  const [edited, setEdited] = useState(section.content.text);

  return (
    <div className="section">
      <h4>{section.title}</h4>
      <textarea
        value={edited}
        onChange={(e) => setEdited(e.target.value)}
      />
      <AIAssistPanel
        section={section}
        onApply={(text) => setEdited(text)}
      />
    </div>
  );
}
