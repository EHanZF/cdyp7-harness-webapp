import { useEffect, useState } from "react";

type Usage = {
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  budgetLimit?: number;
};

export function ExecutionStatusPanel({
  executionId,
}: {
  executionId: string;
}) {
  const [usage, setUsage] = useState<Usage | null>(null);
  const [status, setStatus] = useState<string>("connecting");

  useEffect(() => {
    const ws = new WebSocket(
      `${location.origin.replace("http", "ws")}/api/execution/stream`
    );

    ws.onopen = () => {
      ws.send(JSON.stringify({ executionId }));
      setStatus("running");
    };

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);

      switch (msg.type) {
        case "usage.update":
          setUsage(msg);
          break;

        case "execution.completed":
          setStatus("completed");
          ws.close();
          break;

        case "execution.failed":
          setStatus("failed");
          ws.close();
          break;
      }
    };

    return () => ws.close();
  }, [executionId]);

  return (
    <div className="execution-panel">
      <h4>AI Execution</h4>
      <div>Status: {status}</div>

      {usage ? (
        <>
          <div>Prompt tokens: {usage.promptTokens}</div>
          <div>Completion tokens: {usage.completionTokens}</div>
          <div>Total tokens: {usage.totalTokens}</div>
          {usage.budgetLimit && (
            <div>
              Budget remaining: {usage.budgetLimit - usage.totalTokens}
            </div>
          )}
        </>
      ) : (
        <div>Token usage: collecting…</div>
      )}
    </div>
  );
}
