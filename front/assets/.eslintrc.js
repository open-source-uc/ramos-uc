module.exports = {
    extends: "eslint:recommended",
    env: {
        browser: true,
        es2021: true,
    },
    ignorePatterns: [
        "dist",
        "node_modules",
    ],
    parserOptions: {
        ecmaVersion: 12,
        sourceType: "module",
    },
    rules: {
        // https://eslint.org/docs/rules
        "comma-dangle": [1, "always-multiline"],
        "comma-spacing": 1,
        "eol-last": 1,
        "indent": [2, 4],
        "linebreak-style": [2, "unix"],
        "max-len": [1, { code: 120, ignoreStrings: true, ignoreTemplateLiterals: true }],
        "no-trailing-spaces": 1,
        "object-curly-spacing": [1, "always"],
        "prefer-template": 1,
        "quote-props": [1, "consistent-as-needed"],
        "quotes": [1, "double"],
        "semi": [1, "never"],
        "space-infix-ops": 1,
        "template-curly-spacing": 1,
    },
    globals: {
        __dirname: "readonly",
        $: "readonly",
        google: "readonly",
        gtag: "readonly",
        module: "readonly",
        require: "readonly",
        wp: "readonly",
    },
}
