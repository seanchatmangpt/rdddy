/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
    return [
      {
        source: '/receive_transcript', // Prefix for your API calls
        destination: 'http://localhost:8000/receive_transcript', // Your FastAPI backend
      },
    ];
  },
};

export default nextConfig;
