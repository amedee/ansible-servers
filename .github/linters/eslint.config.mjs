export default [
  {
    ignores: ["**/dist/**", "**/node_modules/**"],

    languageOptions: {
      parserOptions: {
        ecmaVersion: 2022,
        sourceType: "module",
      },
      globals: {
        global: "readonly",
        process: "readonly",
        console: "readonly",
        Atomics: "readonly",
        SharedArrayBuffer: "readonly",
      },
    },

    rules: {
      // ESLint recommended rules (subset)
      "for-direction": "error",
      "no-await-in-loop": "error",
      "no-compare-neg-zero": "error",
      "no-cond-assign": ["error", "always"],
      "no-constant-condition": ["error", { checkLoops: false }],
      "no-control-regex": "error",
      "no-debugger": "error",
      "no-dupe-args": "error",
      "no-dupe-keys": "error",
      "no-duplicate-case": "error",
      "no-empty": ["error", { allowEmptyCatch: true }],
      "no-empty-character-class": "error",
      "no-ex-assign": "error",
      "no-extra-boolean-cast": "error",
      "no-extra-parens": ["error", "functions"],
      "no-extra-semi": "error",
      "no-func-assign": "error",
      "no-inner-declarations": ["error", "functions"],
      "no-invalid-regexp": "error",
      "no-irregular-whitespace": "error",
      "no-misleading-character-class": "error",
      "no-obj-calls": "error",
      "no-prototype-builtins": "error",
      "no-regex-spaces": "error",
      "no-sparse-arrays": "error",
      "no-template-curly-in-string": "error",
      "no-unexpected-multiline": "error",
      "no-unreachable": "error",
      "no-unsafe-finally": "error",
      "no-unsafe-negation": ["error", { enforceForOrderingRelations: true }],
      "use-isnan": "error",
      "valid-typeof": ["error", { requireStringLiterals: true }],

      // Your overrides
      "no-undef": "error",
      "no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
      "no-prototype-builtins": "off",
      "no-var": "error",
      "prefer-const": "warn",
      "require-yield": "off",
    },
  },
];
