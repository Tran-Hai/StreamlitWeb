const puppeteer = require('puppeteer');

async function crawlData(startDate, endDate) {
    const browser = await puppeteer.launch(
        {
            headless: true,
            //executablePath: './Chrome/Application/chrome.exe',
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
            executablePath: '/usr/bin/chromium'
        }
    );
    
    const page = await browser.newPage();

    //await page.goto("http://10.122.72.1/user/index/loginform?qsemail=0")
    await page.goto('http://10.122.72.1/static/m647');
    // Login
    await page.type('#epUserID', 's00024');
    await page.type('#epPassWord', '1234qwer!');
    const loginButton = await page.$('#login_form > div > button');
    if (loginButton) {
        await loginButton.click();
    } else {
        throw new Error('Login button not found');
    }

    


    // Setting time range
    await page.waitForSelector("#start");
    await page.evaluate((startDate) =>{
        document.querySelector("#start").value = startDate;
    }, startDate);

    await page.waitForSelector("#end");
    await page.evaluate((endDate) => {
        document.querySelector("#end").value = endDate;
    }, endDate);

    //  Click on status of report
    await page.waitForSelector('input#Status_3', {visible:true});
    await page.$eval('input#Status_3', el => el.click());

    await page.waitForSelector('input#Status_4', {visible:true});
    await page.$eval('input#Status_4', el => el.click());

    await page.waitForSelector('input#Type_8', {visible:true});
    await page.$eval('input#Type_8', el => el.click());


    // Click on view data button
    await page.waitForSelector("#pt-showreport", {visible:true});
    // await page.click("#pt-showreport");
    const view_data = await page.$('#pt-showreport');
    if (view_data) {
        await view_data.evaluate(el => el.click());
    } else {
        throw new Error('View data button not found');
    }

    // Start store data
    let data
    try {
        await page.waitForSelector("#print-area > div > table > tbody", {visible:true});
        data = await page.evaluate(() => {
            const rows = Array.from(document.querySelectorAll("#print-area > div > table > tbody > tr"));
            return rows.map(row => {
                const columns = Array.from(row.querySelectorAll('td'));
                if (columns.length === 5) return null;
                return columns.slice(0, 15).map(col => col.innerText);
            }).filter(row => row !== null);
        });
        //console.log(data);
    } catch (error) {
        console.error('Failed to find the data:', error);
    }

    await browser.close();

    return data;
}

module.exports = { crawlData };