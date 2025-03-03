const puppeteer = require('puppeteer'),
      fs = require('fs').promises,
      axios = require('axios');

(async () => {
    // Avvia un'istanza di Puppeteer
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    console.log("go to site");
    // Naviga alla pagina Facebook
    await page.goto('https://www.facebook.com/PastaPasticciRistorante/?locale=it_IT'); 

    console.log("wait image");

    await page.waitForSelector('img');

    const images_url = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('img')).map(img => img.src).filter(src => src.startsWith('http'));
    });

    await Promise.all(
        images_url.map((url, index) => downloadImage(url, `images/${index}.png`))
    );

    console.log("Download completato!");

    await browser.close();
})();


async function downloadImage(url, filePath) {
    try {
        const res = await axios({ url, responseType: 'arraybuffer' }); 

        if (parseInt(res.headers['content-length']) > 10000) { 
            await fs.writeFile(filePath, res.data);
        } 
    } catch (error) {
        console.error(`Errore durante il download di ${url}:`, error.message);
    }
}
