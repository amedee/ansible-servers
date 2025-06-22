import * as core from "@actions/core";
import fetch from "node-fetch";

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
  const diffContent = core.getInput("diff_content");
  const promptMessage = core.getInput("prompt_content");
  const token = process.env.OPENROUTER_API_KEY;

  if (!token) {
    core.setFailed("OPENROUTER_API_KEY is not set");
    return;
  }

  if (!diffContent) {
    core.setFailed("diff_content input is empty");
    return;
  }

  try {
    const body = buildRequestBody(promptMessage, diffContent);
    let message = await fetchCommitMessage(body, token);

    if (!message) {
      core.setFailed("No message generated");
      return;
    }

    const finalMessage = sanitizeMessage(message);
    core.setOutput("message", finalMessage);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
