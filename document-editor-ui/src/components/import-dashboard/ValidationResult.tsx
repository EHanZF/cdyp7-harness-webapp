import type { ValidationResult } from "../types/ValidationResult";
interface Props {
    result: ValidationResultType;
}

export default function ValidationResult({ result }: Props) {
    const { valid, errors = [], warnings = [] } = result;

    return (
        <div className="validation-container">
            <h3 className={valid ? "valid" : "invalid"}>
                {valid ? "✅ Validation Passed" : "❌ Validation Failed"}
            </h3>

            {errors.length > 0 && (
                <div className="error-section">
                    <strong>Errors:</strong>
                    <ul>
                        {errors.map((err: string, index: number) => (
                            <li key={index}>{err}</li>
                        ))}
                    </ul>
                </div>
            )}

            {warnings.length > 0 && (
                <div className="warning-section">
                    <strong>Warnings:</strong>
                    <ul>
                        {warnings.map((warn: string, index: number) => (
                            <li key={index}>{warn}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}
