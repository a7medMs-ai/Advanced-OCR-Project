import execjs
import requests

def tesseract_ocr(image_path):
    # Use Tesseract.js via JavaScript runtime
    ctx = execjs.compile("""
    const { createWorker } = require('tesseract.js');
    async function recognize(image) {
        const worker = await createWorker();
        await worker.loadLanguage('eng+ara');
        await worker.initialize('eng+ara');
        const { data } = await worker.recognize(image);
        await worker.terminate();
        return data.text;
    }
    """)
    return ctx.call("recognize", image_path)
