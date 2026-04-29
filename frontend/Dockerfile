FROM node:20-alpine

# Instalamos pnpm globalmente dentro del contenedor
RUN npm install -g pnpm

WORKDIR /usr/src/app

# Copiamos solo los archivos de dependencias de pnpm
COPY package.json pnpm-lock.yaml ./

# Instalamos las dependencias usando pnpm
RUN pnpm install --frozen-lockfile

# Copiamos el resto del código
COPY . .

# Ejecutamos prettier para formatear el código
RUN pnpm run format || true

# Ejecutamos eslint para corregir automáticamente problemas de linting
RUN pnpm run lint:fix || true

# Ejecutamos verificación de tipos TypeScript
RUN pnpm run type-check || true

# Ejecutamos el script combinado de formateo y linting
RUN pnpm run format:lint || true

EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5173 || exit 1

# Comando para arrancar con pnpm
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0"]