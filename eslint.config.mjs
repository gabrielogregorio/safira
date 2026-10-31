import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import js from '@eslint/js';
import prettier from 'eslint-config-prettier';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import sonarjs from 'eslint-plugin-sonarjs';
import globals from 'globals';
import tseslint from 'typescript-eslint';

const rootDirectory = dirname(fileURLToPath(import.meta.url));

export default tseslint.config(
  { ignores: ['build', 'coverage', 'node_modules', 'playwright-report', 'test-results', 'trash', '*.mjs'] },
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  sonarjs.configs.recommended,
  {
    files: ['**/*.{ts,tsx,mts}'],
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
      parserOptions: { project: './tsconfig.json', tsconfigRootDir: rootDirectory },
    },
    plugins: { react, 'react-hooks': reactHooks, 'jsx-a11y': jsxA11y },
    settings: { react: { version: 'detect' } },
    rules: {
      ...jsxA11y.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,
      'react/button-has-type': 'error',
      'curly': ['error', 'all'],
      'no-plusplus': 'error',
      'no-nested-ternary': 'error',
      'padding-line-between-statements': ['error', { blankLine: 'always', prev: '*', next: 'return' }],
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-non-null-assertion': 'error',
      '@typescript-eslint/no-floating-promises': 'error',
      'sonarjs/pseudo-random': 'off',
      'sonarjs/function-return-type': 'off',
      'sonarjs/different-types-comparison': 'off',
      'jsx-a11y/no-noninteractive-tabindex': ['error', { tags: [], roles: ['log', 'region', 'separator'] }],
      'sonarjs/cognitive-complexity': ['error', 25],
    },
  },
  {
    files: ['**/*.test.ts', '**/*.test.tsx', 'e2e/**/*.ts'],
    rules: {
      'sonarjs/no-duplicate-string': 'off',
      'sonarjs/no-nested-functions': 'off',
      '@typescript-eslint/unbound-method': 'off',
    },
  },
  prettier,
);
