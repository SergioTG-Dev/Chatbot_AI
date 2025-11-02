import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  eslint: {
    // No bloquear el build por errores de ESLint; mantenerlos como warnings
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
