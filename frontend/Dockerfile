# ── Build stage ──────────────────────────────────────────────
FROM node:20-slim AS builder

WORKDIR /build

COPY package.json .
RUN npm install --omit=dev

# ── Final stage ──────────────────────────────────────────────
FROM node:20-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy only production node_modules from builder
COPY --from=builder /build/node_modules ./node_modules

# Copy app source
COPY app.js .
COPY views/ ./views/

# Switch to non-root user
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })"

CMD ["node", "app.js"]