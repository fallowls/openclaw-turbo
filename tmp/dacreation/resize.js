const sharp = require('sharp');

(async () => {
  await sharp('logo-white.webp')
    .resize({ width: 180 })
    .png({ compressionLevel: 9, palette: true })
    .toFile('logo-white-180.png');
  console.log('ok');
})().catch((e) => { console.error(e); process.exit(1); });
