import { ApiReference } from '@scalar/nextjs-api-reference'

const config = {
  spec: {
    url: '/api/openapi',
  },
  theme: 'purple', // Opciones: 'default', 'alternate', 'moon', 'purple', 'solarized'
  darkMode: true,
  layout: 'modern', // Opciones: 'modern', 'classic'
}

export const GET = ApiReference(config)