// eslint.config.js
import globals from "globals";
import js from "@eslint/js";
import prettier from "eslint-config-prettier";

export default [
	{
		ignores: ["**/dist/**", "**/node_modules/**"],
	},
	{
		files: [
			".github/linters/eslint.config.js",
			".github/actions/ai-commit-message/index.js",
		],
		...js.configs.recommended,
		...prettier,
		languageOptions: {
			ecmaVersion: 2022,
			sourceType: "module",
			globals: {
				...globals.node,
				...globals.es2022,
			},
		},
		rules: {
			// === StandardJS core rules ===
			"no-var": "error",
			"prefer-const": "error",
			"no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
			"no-undef": "error",
			eqeqeq: ["error", "always"],
			curly: ["error", "multi-line"],
			"brace-style": ["error", "1tbs", { allowSingleLine: true }],
			"comma-dangle": ["error", "always-multiline"],
			indent: ["error", 2, { SwitchCase: 1 }],
			semi: ["error", "always"],
			"space-before-function-paren": ["error", "never"],
			"keyword-spacing": ["error", { before: true, after: true }],
			"object-curly-spacing": ["error", "always"],
			"array-bracket-spacing": ["error", "never"],
			"space-in-parens": ["error", "never"],
			"no-multiple-empty-lines": ["error", { max: 1, maxEOF: 0 }],
			quotes: ["error", "double", { avoidEscape: true }],
			"arrow-spacing": ["error", { before: true, after: true }],
			"no-prototype-builtins": "off",
			"require-yield": "off",
		},
	},
];
