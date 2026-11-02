import { defineConfig } from 'i18next-cli'

export default defineConfig({
  locales: ['ja', 'en'],
  extract: {
    input: ['src/**/*.{ts,tsx}'],
    output: 'src/locales/{{language}}/{{namespace}}.json',
    defaultNS: 'translation',
    sort: false,
    indentation: 2,
    defaultValue: (key) => key,
  },
})
