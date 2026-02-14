const sharp = require('sharp');

(async () => {
  await sharp('logo-white.webp').png().toFile('logo-white.png');
  console.log('ok');
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
