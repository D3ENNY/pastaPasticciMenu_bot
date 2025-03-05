const { log, error } = require('console');

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

    images_url.length > 28 ? await sendImage(images_url[28], `images/menu.png`) : console.error("menù non trovato")

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

async function getBase64(image, contentType) {
    try{
        const base64Image =  Buffer.from(image).toString('base64')
        return `data:${contentType};base64,${base64Image}`
    } catch (error) {
        console.error("errore nella conversione a base64", error.message)
    }

}

async function sendImage(url, filePath) {
    try {
        const res = await axios({url, responseType: 'arraybuffer' })

        if(parseInt(res.headers['content-lenght']) < 10_000) {
            return
        }

        const imageBase64 = await getBase64(res.data, res.headers['content-type'])

        axios.post('http://127.0.0.1:5000/api/upload_menu', {
            menu_base64: imageBase64
        }).then((res) => {
            console.log(res);
        }).catch((err)=>{
            console.error(err)
        })

    } catch (error) {
        console.error(`Errore nell'eseguire la richiesta POST`, error.message)
    }
}