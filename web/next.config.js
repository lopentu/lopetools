const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  reactStrictMode: true, // https://react.dev/learn/keeping-components-pure
  eslint: {
    ignoreDuringBuilds: true,
  },
  basePath: '/lopeGPT'
});
