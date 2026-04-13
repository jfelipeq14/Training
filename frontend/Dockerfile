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

EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5173 || exit 1

# Comando para arrancar con pnpm
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0"]