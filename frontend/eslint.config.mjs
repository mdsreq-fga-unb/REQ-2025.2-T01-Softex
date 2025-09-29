import js from "@eslint/js";
import globals from "globals";
import tsplugin from "@typescript-eslint/eslint-plugin";
import tsparser from "@typescript-eslint/parser";
import vuePlugin from "eslint-plugin-vue";
import { defineConfig } from "eslint";

export default defineConfig({
  overrides: [
    {
      files: ["**/*.{js,mjs,cjs,ts,mts,cts,vue}"],
      plugins: { js },
      extends: ["plugin:js/recommended"],
      languageOptions: { globals: globals.browser },
    },
    {
      files: ["**/*.ts"],
      parser: tsparser,
      plugins: { "@typescript-eslint": tsplugin },
      extends: ["plugin:@typescript-eslint/recommended"],
    },
    {
      files: ["**/*.vue"],
      plugins: { vue: vuePlugin },
      extends: ["plugin:vue/vue3-essential"],
      parser: "vue-eslint-parser",
      parserOptions: { parser: tsparser },
    },
  ],
});
