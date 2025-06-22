import * as core from "@actions/core";
import { spawnSync } from "child_process";
import fetch from "node-fetch";

/**
 * Run a git command synchronously and log output/errors.
 */
function runGitCommand(args, label) {
  const result = spawnSync("git", args, {
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
  });

  if (result.error) {
    console.error("[%s] Error:", label, result.error);
    throw result.error;
  }

  if (result.status !== 0) {
    console.error("[%s] Failed with exit code %d", label, result.status);
    console.error("[%s] stderr: %s", label, result.stderr.trim());
    throw new Error(`${label} failed with code ${result.status}`);
  }

  console.log("[%s] stdout:\n%s", label, result.stdout.trim());
  return result.stdout.trim();
}

/**
 * Get the staged diff for the specified file path (limited to 3000 characters).
 */
function getStagedDiff(diffPath) {
  // Run debug commands first
  runGitCommand(["rev-parse", "--show-toplevel"], "git rev-parse");
  runGitCommand(["status"], "git status");

  // Then get the diff
  const diffArgs = ["diff", "--cached", "--unified=0", "--", diffPath];
  const diffResult = spawnSync("git", diffArgs, {
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
  });

  if (diffResult.error) {
    throw diffResult.error;
  }

  if (diffResult.status !== 0) {
    throw new Error(`git diff failed with code ${diffResult.status}`);
  }

  return diffResult.stdout.slice(0, 3000);
}

/**
 * Generate the prompt message body for OpenRouter API.
 */
function buildRequestBody(promptMessage, diff) {
  return {
    model: "mistralai/devstral-small:free",
    messages: [
      {
        role: "user",
        content: `${promptMessage}\n\n${diff}`,
      },
    ],
    temperature: 0.7,
  };
}

/**
 * Call the OpenRouter API and return the commit message.
 */
async function fetchCommitMessage(body, token) {
  const response = await fetch(
    "https://openrouter.ai/api/v1/chat/completions",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        "HTTP-Referer": `https://github.com/${process.env.GITHUB_REPOSITORY}`,
        "X-Title": "AI Commit Message",
      },
      body: JSON.stringify(body),
    },
  );

  if (!response.ok) {
    throw new Error(`OpenRouter API error: ${response.statusText}`);
  }

  const json = await response.json();
  return json.choices?.[0]?.message?.content || "";
}

/**
 * Clean and truncate the commit message.
 */
function sanitizeMessage(message) {
  const cleaned = message.replace(/`/g, "");
  const lines = cleaned.split("\n");
  if (lines.length > 0) {
    lines[0] = lines[0].slice(0, 72);
  }
  return lines.join("\n");
}

/**
 * Main entrypoint for the action.
 */
async function run() {
  const diffPath = core.getInput("diff-path");
  const promptMessage = core.getInput("prompt-message");
  const token = process.env.OPENROUTER_API_KEY;

  if (!token) {
    core.setFailed("OPENROUTER_API_KEY is not set");
    return;
  }

  try {
    const diff = getStagedDiff(diffPath);
    const body = buildRequestBody(promptMessage, diff);
    let message = await fetchCommitMessage(body, token);

    if (!message) {
      core.warning("No message generated, using fallback.");
      message = "⬆️ Update dependencies";
    }

    const finalMessage = sanitizeMessage(message);
    core.setOutput("message", finalMessage);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
