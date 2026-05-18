import { mcp } from "../../mcp";

export function AIAssistPanel({
    section,
    onApply,
}: {
    section: any;
    onApply: (text: string) => void;
}) {
    async function runAI() {
        const result = await mcp.callTool<{
            oldText: string;
            newText: string;
        }>("document.rewrite_section", {
            sectionId: section.sectionId,
            text: section.content.text,
            instruction: "Modernize wording without changing meaning",
            constraints: [
                "No new process steps",
                "Preserve technical intent",
                "Return only revised text",
            ],
        });

        onApply(result.newText);
    }

    return <button onClick={runAI}>AI Suggest (MCP)</button>;
}
