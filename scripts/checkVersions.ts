import fs from "fs";

const manifest = JSON.parse(
    fs.readFileSync("./config/releases/current.json", "utf-8")
);

if (!manifest.rbacPolicyVersion) {
    throw new Error("Missing rbacPolicyVersion");
}

if (!manifest.routerVersion) {
    throw new Error("Missing routerVersion");
}

console.log("✅ Version pinning OK");
