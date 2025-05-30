"""
Configuration settings for React Setup CLI
"""

# Default packages for different setups
DEFAULT_PACKAGES = {
    'common': [
        'axios',
        'react-router-dom',
        'styled-components',
        '@mui/material',
        '@emotion/react',
        '@emotion/styled',
        'framer-motion',
        'react-query',
        'zustand',
        'react-hook-form',
        'yup',
    ],
    'dev': [
        'prettier',
        'eslint-config-prettier',
        'eslint-plugin-prettier',
        '@testing-library/react',
        '@testing-library/jest-dom',
        '@testing-library/user-event',
    ],
    'typescript_dev': [
        '@types/react',
        '@types/react-dom',
        '@types/node',
    ]
}

# Default project structure
DEFAULT_STRUCTURE = [
    'src/components/common',
    'src/components/ui',
    'src/pages',
    'src/hooks',
    'src/utils',
    'src/services',
    'src/context',
    'src/assets/images',
    'src/assets/icons',
    'src/styles',
    'public/images',
]

# Framework specific configurations
FRAMEWORK_CONFIG = {
    'cra': {
        'name': 'Create React App',
        'dev_server': 'npm start',
        'port': 3000
    },
    'nextjs': {
        'name': 'Next.js',
        'dev_server': 'npm run dev',
        'port': 3000
    },
    'vite': {
        'name': 'Vite React',
        'dev_server': 'npm run dev',
        'port': 5173
    }
}
